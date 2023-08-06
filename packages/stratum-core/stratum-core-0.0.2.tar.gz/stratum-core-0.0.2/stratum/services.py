import os
import logging
from twisted.internet import defer, threads
import weakref
import re as regex
import logzero
from logzero import logger
from exceptions import ServiceNotFound, MethodNotFound, MissingServiceType, MissingServiceVendor, \
    MissingServiceIsDefault, DefaultServiceAlreadyExist

logzero.loglevel(logging.getLevelName(os.environ.get("log.level")))

VENDOR_RE = regex.compile(r"\[(.*)\\]")


class ResultObject(object):
    def __init__(self, result=None, sign=False, sign_algo=None, sign_id=None):
        self.result = result
        self.sign = sign
        self.sign_algo = sign_algo
        self.sign_id = sign_id


def wrap_result_object(obj):
    def _wrap(o):
        if isinstance(o, ResultObject):
            return o
        return ResultObject(result=o)

    return _wrap(obj)


class ServiceFactory(object):
    registry = {}  # Mapping service_type -> vendor -> cls

    @classmethod
    def _split_method(cls, rpc_method):
        """Parses 'some.service[vendor].rpc_method' and returns 3-tuple with
            (service_type, vendor, rpc_method)
        """
        service_type, method_name = rpc_method.rsplit(".", 1)
        vendor = None

        if "[" in service_type:
            # Use regex only when brackets are found
            try:
                vendor = VENDOR_RE.search(service_type).group(1)
                service_type = service_type.replace(f"[{vendor}]", "")
            except regex.error:
                raise ServiceNotFound(f"Invalid syntax in service name {service_type}")

        return service_type, vendor, method_name

    @classmethod
    def call(cls, rpc_method, params, connection_ref=None):
        try:
            service_type, vendor, function_name = cls._split_method(rpc_method=rpc_method)
        except ValueError:
            raise MethodNotFound(
                "Method name parsing failed. You must use format <service_name>.<method_name>, eg 'mining.authorize'")

        try:
            if function_name.startswith("_"):
                raise

            _inst = cls.lookup(service_type, vendor)()
            _inst.connection_ref = weakref.ref(connection_ref)
            func = _inst.__getattribute__(function_name)
            if not callable(func):
                raise
        except:
            raise MethodNotFound(f"Method {function_name} not found for service {service_type}")

        def _run(func, *params):
            return wrap_result_object(func(*params))

        # Returns defer which will lead to ResultObject
        return defer.maybeDeferred(_run, func, *params)

    @classmethod
    def lookup(cls, service_type, vendor=None):
        # lookup for service type provided by specific vendor
        if vendor:
            try:
                return cls.registry[service_type][vendor]
            except KeyError:
                raise ServiceNotFound("Class for given service type and vendor not registered")

        # Lookup for any vendor, prefer default one
        try:
            vendors = cls.registry[service_type]
        except KeyError:
            raise ServiceNotFound("Class for given service type not registered")

        last_found = None
        for _, _cls in vendor.items():
            last_found = _cls
            if last_found.is_default:
                return last_found

        if not last_found:
            raise ServiceNotFound("Class for given service type not registered")

        return last_found

    @classmethod
    def register_service(cls, _cls, meta):
        # Register service class to SeerviceFactory
        service_type = meta.get("service_type")
        service_vendor = meta.get("service_vendor")
        is_default = meta.get("is_default")

        if str(_cls.__name__) in ("GenericService",):
            return

        if not service_type:
            raise MissingServiceType(f"Service class {_cls} is missing 'service_type' property")

        if not service_vendor:
            raise MissingServiceVendor(f"Service class {_cls} is missing 'service_vendor' property")

        if is_default is None:
            raise MissingServiceIsDefault(f"Service class {_cls} is missing 'is_default' property")

        if is_default:
            # Check if there is any other default service
            try:
                current = cls.lookup(service_type)
                if current.is_default:
                    raise DefaultServiceAlreadyExist(f"Default service already exists for type {service_type}")
            except ServiceNotFound:
                pass

        setup_func = meta.get("_setup", None)
        if setup_func is not None:
            _cls()._setup()

        ServiceFactory.registry.setdefault(service_type, {})
        ServiceFactory.registry[service_type][service_vendor] = _cls

        logger.info(f"Registered {_cls} for service {service_type}, vendor {service_vendor} (default: {is_default})")


def signature(func):
    """Decorate RPC method result with server's signature. This decorator can be chained
        with Deferred or inlineCallbacks, thanks to _sign_generator() hack
    """

    def _sign_generator(iterator):
        """Iterate through generator object, detects BaseException and inject
            signature into execution's value (=result of inner method)
        """
        for i in iterator:
            try:
                iterator.send((yield i))
            except BaseException as exc:
                exc.value = wrap_result_object(exc.value)
                exc.value.sign = True
                raise

    def _sign_deferred(res):
        obj = wrap_result_object(res)
        obj.sign = True
        return obj

    def _sign_failure(fail):
        fail.value = wrap_result_object(fail.value)
        fail.value.sign = True
        return fail

    def inner(*args, **kwargs):
        ret = defer.maybeDeferred(func, *args, **kwargs)
        ret.addCallback(_sign_deferred)
        ret.addErrback(_sign_failure)
        return ret

    return inner


def synchronous(func):
    """Run given method synchronously in separate thread and return the result"""

    def inner(*args, **kwargs):
        return threads.deferToThread(func, *args, **kwargs)

    return inner


class ServiceMetaclass(type):
    def __init__(cls, name, bases, _dict):
        super(ServiceMetaclass, cls).__init__(name, bases, _dict)
        ServiceFactory.register_service(cls, _dict)


class GenericService(object):
    __metaclass__ = ServiceMetaclass
    service_type = None
    service_vendor = None
    is_default = None

    # Keep weak reference to connection which asked for current RPC call. Useful
    # for pubsub mechanism, but use it with care. It does not need to point to
    # actual and valid data, so you have to check if connection still exists
    # every time
    connection_ref = None


class ServiceDiscovery(GenericService):
    service_type = "discovery"
    service_vendor = "Stratum"
    is_default = True

    def list_services(self):
        return ServiceFactory.registry.keys()

    def list_vendors(self, service_type):
        return ServiceFactory.registry[service_type].keys()

    def list_methods(self, service_name):
        # Accepts vendors as well in square brackets: name[name.com]

        # Parse service type and vendor
        service_type, vendor, _ = ServiceFactory._split_method(f"{service_name}.foo")
        service = ServiceFactory.lookup(service_type, vendor)
        out = []

        for name, obj in service.__dict__.items():
            if name.startswith("_"):
                continue

            if not callable(obj):
                continue

            out.append(name)
        return out

    def list_params(self, method):
        service_type, vendor, rpc_method = ServiceFactory._split_method(method)
        service = ServiceFactory.lookup(service_type, vendor)

        # Load params and helper text from method attributes
        func = service.__dict__[rpc_method]
        params = getattr(func, "params", None)
        help_text = getattr(func, "help_text", None)

        return help_text, params

    list_params.help_text = "Accepts name of methods and returns it's description and available parameters"
    list_params.params = [("method", "string", "Method to lookup for description and parameters")]
