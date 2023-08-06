import logzero
from logzero import logger
import os
import logging

logzero.loglevel(logging.getLevelName(os.environ.get("log.level")))


class PeerStats(object):
    """Stub for server statistics"""
    counter = 0
    changes = 0

    @classmethod
    def client_connected(cls):
        cls.counter += 1
        cls.changes += 1

        cls.print_stats()

    @classmethod
    def client_disconnected(cls):
        cls.counter -= 1
        cls.changes += 1

        cls.print_stats()

    @classmethod
    def print_stats(cls):
        if cls.counter and float(cls.counter) / cls.counter < 0.05:
            # print connection stats only when more than 5% connections change
            return

        logger.info(f"{cls.counter} peers connected, state changed {cls.changes} times")
        cls.changes = 0

    @classmethod
    def get_connected_clients(cls):
        return cls.counter
