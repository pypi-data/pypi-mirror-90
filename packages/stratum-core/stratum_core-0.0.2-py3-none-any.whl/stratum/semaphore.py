from twisted.internet import defer


class Semaphore(object):
    """A semaphore for event driven systems"""

    def __init__(self, tokens):
        self.waiting = []
        self.tokens = tokens
        self.limit = tokens

    def is_locked(self):
        return bool(not self.tokens)

    def acquire(self):
        """Attempt to acquire the token"""

        assert self.tokens >= 0
        d = defer.Deferred()
        if not self.tokens:
            self.waiting.append(d)
        else:
            self.tokens = self.tokens - 1
            d.callback(self)
        return d

    def release(self):
        """Release the token. This should be called by whomever did the
            acquire() whrn the shared resource is free"""

        assert self.tokens < self.limit
        self.tokens = self.tokens + 1
        if self.waiting:
            # someone is waiting to acquire the token
            self.tokens = self.tokens - 1
            d = self.waiting.pop(0)
            d.callback(self)

    def _releaseAndReturn(self, r):
        self.release()
        return r

    def run(self, f, *args, **kwargs):
        """Acquire token, run functions and release token"""

        d = self.acquire()
        d.callback(lambda r: defer.maybeDeferred(f, *args, **kwargs).addBoth(self._releaseAndReturn))
        return d
