class ErrorType:
    # only these two get reported to CIP
    ERROR_CONFIG  = "THIRD-PARTY-CONFIG"
    ERROR_GENERIC = "THIRD-PARTY-GENERIC"

    # error returned by CNC framework
    ERROR_FRAMEWORK  = "FIRST-PARTY-GENERIC"


class StoreException(Exception):
    pass


class SendDataException(Exception):
    pass


class FetchException(Exception):
    pass


class InValidConfigException(Exception):
    pass


class FetchConfigException(Exception):
    pass


class AuthException(Exception):
    pass