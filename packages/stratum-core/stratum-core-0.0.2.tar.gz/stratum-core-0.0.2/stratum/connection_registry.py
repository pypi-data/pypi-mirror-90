import weakref
import logzero
from logzero import logger
from twisted.internet import reactor
from services import GenericService
import os
import logging

logzero.loglevel(logging.getLevelName(os.environ.get("log.level")))


class ConnectionRegistry(object):
    __connections = weakref.WeakKeyDictionary()

    @classmethod
    def add_connection(cls, connection):
        cls.__connections[connection] = True

    @classmethod
    def remove_connection(cls, connection):
        try:
            del cls.__connections[connection]
        except:
            logger.warning("Cannot remove connection from ConnectionRegistry")

    @classmethod
    def get_session(cls, connection):
        if isinstance(connection, weakref.ref):
            connection = connection()

        if isinstance(connection, GenericService):
            connection = connection.connection_ref()

        if connection is None:
            return None

        return connection.get_session()

    @classmethod
    def iterate(cls):
        return cls.__connections.iterkeyrefs()


def dump_connections():
    for x in ConnectionRegistry.iterate():
        c = x()
        c.transport.write("cus")
        logger.info("!!!", c)
    reactor.callLater(5, dump_connections)
