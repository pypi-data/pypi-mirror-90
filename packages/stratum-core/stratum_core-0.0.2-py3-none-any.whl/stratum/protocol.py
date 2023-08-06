import os
import logging
import json
import socket
import logzero
from logzero import logger
from twisted.internet.protocol import connectionDone
from twisted.protocols.basic import LineOnlyReceiver
from twisted.internet import defer, error
from twisted.python.failure import Failure

import stats
import signature
import connection_registry
from exceptions import MethodNotFound, ServiceException, ProtocolException, RemoteServiceException

logzero.loglevel(logging.getLevelName(os.environ.get("log.level")))


class RequestCounter(object):
    def __init__(self):
        self.on_finish = defer.Deferred()
        self.counter = 0

    def set_count(self, count):
        self.counter = count

    def decrease(self):
        self.counter -= 1
        if self.counter <= 0:
            self.finish()

    def finish(self):
        if not self.on_finish.called:
            self.on_finish.callback(True)


class Protocol(LineOnlyReceiver):
    delimiter = "\n"

    def _get_id(self):
        self.request_id += 1
        return self.request_id

    def _get_ip(self):
        # Get global unique ID of connection
        return f"{self.proxied_ip or self.transport.getPeer().host}:{id(self)}"

    def get_session(self):
        return self.session

    def connectionMade(self):
        try:
            self.transport.setTcpNoDelay(True)
            self.transport.setTcpKeepAlive(True)
            # Seconds before sending keep alive probes
            self.transport.socket.setsockopt(socket.SOL_TCP, socket.TCP_KEEPIDLE, 120)
            # Interval in seconds between keep alive probes
            self.transport.socket.setsockopt(socket.SOL_TCP, socket.TCP_KEEPINTVL, 1)
            # Failed keepalive probes before declaring other end
            self.transport.socket.setsockopt(socket.SOL_TCP, socket.TCP_KEEPCNT, 5)
        except:
            # Supported only by the socket transport
            # but there is really no better place in code to trigger this
            pass

        # Read settings.tcp["PROXY_PROTOCOL"]
        self.expect_tcp_proxy_protocol_header = self.factory.__dict__.get("tcp_proxy_protocol_enable", False)
        self.proxied_ip = None  # IP obtained from TCP proxy protocol

        self.request_id = 0
        self.lookup_table = {}
        self.event_handler = self.factory.event_handler()
        self.on_disconnect = defer.Deferred()
        # Will point to defer which is called once all client requests are processed
        self.on_finish = None

        # Initiate connection session
        self.session = {}

        stats.PeerStats.client_connected()
        logger.debug(f"Connected {self.transport.getPeer().host}")
        connection_registry.ConnectionRegistry.add_connection(self)

    def transport_write(self, data):
        """Overwrite this if transport needs some extra care about data written
            to the socket, like adding message message format in websocket
        """
        try:
            self.transport.write(data)
        except AttributeError:
            # Transport is disconnected
            pass

    def connectionLost(self, reason=connectionDone):
        if self.on_disconnect != None and not self.on_disconnect.called:
            self.on_disconnect.callback(self)
            self.on_disconnect = None

        stats.PeerStats.client_disconnected()
        connection_registry.ConnectionRegistry.remove_connection(self)
        self.transport = None

    def writeJsonRequest(self, method, params, is_notification=False):
        request_id = None if is_notification else self._get_id()
        serialized = json.dumps({"id": request_id, "method": method, "params": params})

        if self.factory.debug:
            logger.debug(f"< {serialized}")

        self.transport_write(f"{serialized}\n")
        return request_id

    def writeJsonResponse(self, data, message_id, use_signature=False, sign_method="", sign_params=[]):
        if use_signature:
            serialized = signature.jsonrpc_dumps_sign(self.factory.signing_key, self.factory.signing_id, False,
                                                      message_id, sign_method, sign_params, data, None)
        else:
            serialized = json.dumps({"id": message_id, "result": data, "error": None})

        if self.factory.debug:
            logger.debug(f"< {serialized}")

        self.transport_write(f"{serialized}\n")

    def writeJsonError(self, code, message, traceback, message_id, use_signature=False, sign_method="",
                       sign_params=[]):
        if use_signature:
            serialized = signature.jsonrpc_dumps_sign(self.factory.signing_key, self.factory.signing_id, False,
                                                      message_id, sign_method, sign_params, None,
                                                      (code, message, traceback))
        else:
            serialized = json.dumps({"id": message_id, "result": None, "error": (code, message, traceback)})

        self.transport_write(f"{serialized}\n")

    def writeGeneralError(self, message, code=-1):
        logger.error(message)
        return self.writeJsonError(code, message, None, None)

    def process_response(self, data, message_id, sign_method, sign_params, request_counter):
        self.writeJsonResponse(data.result, message_id, data.sign, sign_method, sign_params)
        request_counter.decrease()

    def process_failure(self, failure, message_id, sign_method, sign_params, request_counter):
        if not isinstance(failure.value, ServiceException):
            # All handled exceptions should inherit from ServiceException class
            # Throwing other exception class means that it is unhandled error
            # and we should log it
            logger.critical(failure)

        sign = False
        code = getattr(failure.value, "code", -1)

        if message_id is not None:
            # Other party does not care of error state for notifications
            if os.environ.get("debug"):
                tb = failure.getBriefTraceback()
            else:
                tb = None
            self.writeJsonError(code, failure.getErrorMessage(), tb, message_id, sign, sign_method, sign_params)

        request_counter.decrease()

    def dataReceived(self, data, request_counter=None):
        """Original code fromm twisted, hacked for request_counter proxying"""

        if request_counter is None:
            request_counter = RequestCounter()

        lines = (self._buffer + data).split(self.delimiter)
        self._buffer = lines.pop(-1)
        request_counter.set_count(len(lines))
        self.on_finish = request_counter.on_finish

        for line in lines:
            if self.transport.disconnecting:
                request_counter.finish()
                return
            if len(line) > self.MAX_LENGTH:
                request_counter.finish()
                return self.lineLengthExceeded(line)
            else:
                try:
                    self.lineReceived(line, request_counter)
                except Exception as exc:
                    request_counter.finish()
                    logger.warning(f"Failed message: {str(exc)} from {self._get_ip()}")
                    return error.ConnectionLost("Processing of message failed")
        if len(self._buffer) > self.MAX_LENGTH:
            request_counter.finish()
            return self.lineLengthExceeded(self._buffer)

    def lineReceived(self, line, request_counter):
        if self.expect_tcp_proxy_protocol_header:
            # This flag may be set only for TCP transport and when PROXY_PROTOCOL is
            # enabled in server config. Then we expect the first line of the stream
            # may contain proxy metadata

            # We do not expect this header during this session anymore
            self.expect_tcp_proxy_protocol_header = False

            if line.startswith("PROXY"):
                self.proxied_ip = line.split()[2]

                request_counter.decrease()
                return
        try:
            message = json.loads(line)
        except:
            request_counter.finish()
            raise ProtocolException(f"Cannot decode message {line.strip()}")

        if self.factory.debug:
            logger.debug(f"> {message}")

        message_id = message.get("id", 0)
        message_method = message.get("method")
        message_params = message.get("params")
        message_result = message.get("result")
        message_error = message.get("error")

        if message_method:
            # It is a RPC call or notification
            try:
                result = self.event_handler._handle_event(message_method, message_params, connection_ref=self)
                if result is None and message_id is not None:
                    # event handler must return Deferred or raise exception for rpc request
                    raise MethodNotFound(f"Event handler cannot process method {message_method}")
            except:
                failure = Failure()
                self.process_failure(failure, message_id, message_params, request_counter)
            else:
                if message_id is None:
                    # It is a notification, do not expect a response
                    request_counter.decrease()
                else:
                    # It is a RPC call
                    result.addCallback(self.process_response, message_id, message_method, message_params,
                                       request_counter)
                    result.addErrback(self.process_failure, message_id, message_method, message_params,
                                      request_counter)
        elif message_id:
            # It is a RPC response
            # Perform lookup to the table of waiting requests
            request_counter.decrease()

            try:
                meta = self.lookup_table[message_id]
                del self.lookup_table[message_id]
            except KeyError:
                # When deferred object for given message ID is not found, it is an error
                raise ProtocolException(f"Lookup for deferred object for message ID {message_id} failed")

            # If there is an error, habdle is as errback
            # If both result and error are null, handle it as a success with blank result
            if message_error is not None:
                meta["defer"].errback(RemoteServiceException(message_error[0], message_error[1], message_error[2]))
            else:
                meta["defer"].callback(message_result)

    def rpc(self, method, params, is_notification=False):
        """This method performs remote RPC call. If method should expect an response, it store
            request ID to lookup table and wait for corresponding response message
        """
        request_id = self.writeJsonRequest(method, params, is_notification)

        if is_notification:
            return

        d = defer.Deferred()
        self.lookup_table[request_id] = {"defer": d, "method": method, "params": params}

        return d


class ClientProtocol(Protocol):
    def connectionMade(self):
        Protocol.connectionMade(self)
        self.factory.client = self

        if self.factory.timeout_handler:
            self.factory.timeout_handler.cancel()
            self.factory.timeout_handler = None

        if isinstance(getattr(self.factory, "after_connect", None), list):
            logger.debug(f"Resuming connection: {self.factory.after_connect}")
            for cmd in self.factory.after_connect:
                self.rpc(cmd[0], cmd[1])

        if not self.factory.on_connect.called:
            d = self.factory.on_connect
            self.factory.on_connect = defer.Deferred()
            d.callback(self.factory)

    def connectionLost(self, reason=connectionDone):
        self.factory.client = None

        if self.factory.timeout_handler:
            self.factory.timeout_handler.cancel()
            self.factory.timeout_handler = None

        if not self.factory.on_disconnect.called:
            d = self.factory.on_disconnect
            self.factory.on_disconnect = defer.Deferred()
            d.callback(self.factory)

        Protocol.connectionLost(self, reason)
