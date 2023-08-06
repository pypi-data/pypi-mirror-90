from grpc import StatusCode
from grpc._channel import _InactiveRpcError


class SeismicServiceError(Exception):
    def __init__(self, status=None, message=None, hint=None, source=None):
        super().__init__()

        self.status = status
        self.message = message
        self.hint = hint
        self.source = source

    def __repr__(self):
        e = "status: {}\nmessage: {}".format(self.status, self.message)
        if self.hint is not None:
            e += "\nhint: {}".format(self.hint)
        return e

    def __str__(self):
        return self.__repr__()


def _from_grpc_error(e: _InactiveRpcError):
    se = SeismicServiceError()
    se.status = e.code()
    se.message = e.details()
    se.source = e
    if e.code() == StatusCode.UNAVAILABLE:
        se.hint = "This is a transient error, please try again"
    return se
