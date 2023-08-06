class StratumBaseException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class VersionError(StratumBaseException):
    def __init__(self, message):
        super(VersionError, self).__init__(message)


class SettingsError(StratumBaseException):
    def __init__(self, message):
        super(SettingsError, self).__init__(message)


class ServiceNotFound(StratumBaseException):
    def __init__(self, message):
        super(ServiceNotFound, self).__init__(message)


class MethodNotFound(StratumBaseException):
    def __init__(self, message):
        super(MethodNotFound, self).__init__(message)


class MissingServiceType(StratumBaseException):
    def __init__(self, message):
        super(MissingServiceType, self).__init__(message)


class MissingServiceVendor(StratumBaseException):
    def __init__(self, message):
        super(MissingServiceVendor, self).__init__(message)


class MissingServiceIsDefault(StratumBaseException):
    def __init__(self, message):
        super(MissingServiceIsDefault, self).__init__(message)


class DefaultServiceAlreadyExist(StratumBaseException):
    def __init__(self, message):
        super(DefaultServiceAlreadyExist, self).__init__(message)


class SignatureVerificationFailed(StratumBaseException):
    def __init__(self, message):
        super(SignatureVerificationFailed, self).__init__(message)


class UnknownSignatureAlgorithm(StratumBaseException):
    def __init__(self, message):
        super(UnknownSignatureAlgorithm, self).__init__(message)


class UnknownSignatureId(StratumBaseException):
    def __init__(self, message):
        super(UnknownSignatureId, self).__init__(message)


class ServiceException(StratumBaseException):
    def __init__(self, message):
        super(ServiceException, self).__init__(message)


class ProtocolException(StratumBaseException):
    def __init__(self, message):
        super(ProtocolException, self).__init__(message)


class RemoteServiceException(ServiceException):
    def __init__(self, message):
        super(RemoteServiceException, self).__init__(message)


class PubsubException(ServiceException):
    def __init__(self, message):
        super(PubsubException, self).__init__(message)


class AlreadySubscribed(ServiceException):
    def __init__(self, message):
        super(AlreadySubscribed, self).__init__(message)
