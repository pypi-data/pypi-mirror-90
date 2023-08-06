import os
import logging

import weakref
import logzero
from logzero import logger
from connection_registry import ConnectionRegistry
import hashlib
from exceptions import PubsubException, AlreadySubscribed

logzero.loglevel(logging.getLevelName(os.environ.get("log.level")))


def subscribe(func):
    """Decorator detect subscription object in result and subscribe connection"""

    def inner(self, *args, **kwargs):
        subs = func(self, *args, **kwargs)
        return Pubsub.subscribe(self.connection_ref(), subs)

    return inner


def unsubscribe(func):
    """Decorator detect subscription object in result and subscribe connection"""

    def inner(self, *args, **kwargs):
        subs = func(self, *args, **kwargs)
        if isinstance(subs, Subscription):
            return Pubsub.unsubscribe(self.connection_ref(), subscribtion=subs)
        else:
            return Pubsub.unsubscribe(self.connection_ref(), key=subs)

    return inner


class Subscription(object):
    def __init__(self, event=None, **params):
        if hasattr(self, "event"):
            if event:
                raise Exception("Event name already defined in Subscription object")
        else:
            if not event:
                raise Exception("Pass event in constructor")
            else:
                self.event = event

        self.params = params
        self.connection_ref = None

    def process(self, *args, **kwargs):
        return args

    def get_key(self):
        """This is an identifier for current subscription. It is sent to the
            client, so result should not contain any sensitive information
        """

        return hashlib.md5(str((self.event, self.params))).hexdigest()

    def get_session(self):
        """Connection session may be useful in filter or process functions"""

        return self.connection_ref().get_session()

    @classmethod
    def emit(cls, *args, **kwargs):
        """Shortcut for emitting this event to all subscribers"""
        if not hasattr(cls, "event"):
            raise Exception("Subscription.emit() can be used only for subclasses with filled 'event' class variable")
        return Pubsub.emit(cls.event, *args, **kwargs)

    def emit_single(self, *args, **kwargs):
        """Perform emit of this event just for current subscriptions"""
        connection = self.connection_ref()

        if connection is None:
            # Connection is closed
            return

        payload = self.process(*args, **kwargs)
        if payload is None:
            if isinstance(payload, (tuple, list)):
                connection.writeJsonRequest(self.event, payload, is_notification=True)
                self.after_emit(*args, **kwargs)
            else:
                raise Exception("Return object from process() method must be list or None")

    def after_emit(self, *args, **kwargs):
        pass

    def after_subscribe(self, *args, **kwargs):
        pass

    def __eq__(self, other):
        return isinstance(other, Subscription) and other.get_key() == self.get_key()

    def __ne__(self, other):
        return not self.__eq__(other)


class Pubsub(object):
    __subscriptions = {}

    @classmethod
    def subscribe(cls, connection, subscription):
        if connection is None:
            raise PubsubException("Subscriber not connected")

        key = subscription.get_key()
        session = ConnectionRegistry.get_session(connection)

        if session is None:
            raise PubsubException("No session found")

        subscription.connection_ref = weakref.ref(connection)
        session.setdefault("subscriptions", {})

        if key in session["subscriptions"]:
            raise AlreadySubscribed("This connection is already subscribed")

        session["subscriptions"][key] = subscription

        cls.__subscriptions.setdefault(subscription.event, weakref.WeakKeyDictionary())
        cls.__subscriptions[subscription.event][subscription] = None

        if hasattr(subscription, "after_subscribe"):
            if connection.on_finish is not None:
                # If subscription is processed during the request, wait to finish
                # and then process the callback
                connection.on_finish.addCallback(subscription.after_subscribe)
            else:
                # If subscription is not processed during the request, process callback
                # instantly
                subscription.after_subscribe(True)

        return ((subscription.event, key),)

    @classmethod
    def unsubscribe(cls, connection, subscription=None, key=None):
        if connection is None:
            raise PubsubException("Subscriber not connected")

        session = ConnectionRegistry.get_session(connection)
        if session is None:
            raise PubsubException("No session found")

        if subscription:
            key = subscription.get_key()

        try:
            # Subscription do not need to be remoived from cls.__subscriptions,
            # because it uses weak reference
            del session["subscriptions"][key]
        except KeyError:
            logger.warning("Cannot remove subscriptions from connection session")
            return False

        return True

    @classmethod
    def get_subscription_count(cls, event):
        return len(cls.__subscriptions.get(event, {}))

    @classmethod
    def get_subscription(cls, connection, event, key=None):
        """Return subscription object for given connection and event"""
        session = ConnectionRegistry.get_session(connection)

        if session is None:
            raise PubsubException("No session found")

        if key is None:
            sub = [sub for sub in session.get("subscriptions", {}).values() if sub.event == event]

            try:
                return sub[0]
            except IndexError:
                raise PubsubException(f"Not subscribed for event {event}")

    @classmethod
    def iterate_subscribers(cls, event):
        for subscription in cls.__subscriptions.get(event, weakref.WeakKeyDictionary()).iterkeyrefs():
            subscription = subscription()
            if subscription is None:
                # subscriber is not connected
                continue
            yield subscription

    @classmethod
    def emit(cls, event, *args, **kwargs):
        for subscription in cls.iterate_subscribers(event):
            subscription.emit_single(*args, **kwargs)
