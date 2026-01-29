class LimitedSet[Value]:
    """A set that will only allow up to a given amount of items."""

    def __init__(self, max_size: int) -> None:
        self.max_size = max_size
        self._values = set[Value]()

    def full(self):
        return self.remaining() <= 0

    def remaining(self) -> int:
        return self.max_size - len(self._values)

    def add(self, *values: Value):
        """
        Attempts to add 1 or more value to the set and returns whether the set has more room.
        :param values: The values to add.
        :return: True if the set has room, False if it's full.
        """
        for value in values:
            if not self.full():
                self._values.add(value)
            else:
                return False
        return not self.full()

    def __iter__(self):
        return iter(self._values)
