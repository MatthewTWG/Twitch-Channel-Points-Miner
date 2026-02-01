from typing import Any


class ChatRoomBanStatusResponse:
    def __init__(self, status: Any | None):
        self.status = status
        """Not None if the user is banned."""

    def __repr__(self):
        return f"ChatRoomBanStatusResponse({self.__dict__})"
