from twisted.internet import defer
import logzero
from logzero import logger
import os
import logging

from services import wrap_result_object
from exceptions import MethodNotFound

logzero.loglevel(logging.getLevelName(os.environ.get("log.level")))


class GenericEventHandler(object):
    def _handle_event(self, msg_method, msg_params, connection_ref):
        return defer.maybeDeferred(wrap_result_object, self.handle_event(msg_method, msg_params, connection_ref))

    def handle_event(self, msg_method, msg_params, connection_ref):
        logger.error(f"Other side called method {msg_method} with params {msg_params}")
        raise MethodNotFound(f"Method {msg_method} not implemented")
