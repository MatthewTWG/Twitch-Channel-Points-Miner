from datetime import datetime


class Stream:
    def __init__(self, _id: str, created_at: datetime):
        self.id = _id
        """ Id of the stream """
        self.created_at = created_at
        """The time the stream was created."""

    def __repr__(self):
        return f"Stream({self.__dict__})"


class User:
    def __init__(self, _id: str, stream: Stream | None):
        self.id = _id
        """ Id of the streamer """
        self.stream = stream

    def __repr__(self):
        return f"User({self.__dict__})"


class WithIsStreamLiveQueryResponse:
    def __init__(self, user: User):
        self.user = user

    def __repr__(self):
        return f"WithIsStreamLiveQueryResponse({self.__dict__})"
