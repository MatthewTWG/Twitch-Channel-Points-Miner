import abc
import logging
import time
from typing import Protocol

from TwitchChannelPointsMiner.classes.Settings import Priority
from TwitchChannelPointsMiner.classes.entities.Streamer import Streamer
from TwitchChannelPointsMiner.utils.LimitedSet import LimitedSet

logger = logging.getLogger(__name__)


class StreamerSelector(abc.ABC):
    """Class for selecting streamers from a list."""

    @abc.abstractmethod
    def select(self, streamers: list[Streamer], max_amount: int) -> list[str]:
        """
        Selects streamers from the list.
        :param streamers: The streamers to consider.
        :param max_amount: The maximum amount of streamers to select.
        :return: The selected streamers.
        """
        pass


def priority_order(streamers: list[Streamer], max_amount: int) -> list[str]:
    return [streamer.channel_id for streamer in streamers[:max_amount]]


def priority_points(
    streamers: list[Streamer], max_amount: int, descending: bool
) -> list[str]:
    items = [
        {"points": streamer.channel_points, "id": streamer.channel_id}
        for streamer in streamers
    ]
    items = sorted(
        items,
        key=lambda x: x["points"],
        reverse=descending,
    )
    return [item["id"] for item in items][:max_amount]


def priority_points_ascending(streamers: list[Streamer], max_amount: int) -> list[str]:
    return priority_points(streamers, max_amount, False)


def priority_points_descending(streamers: list[Streamer], max_amount: int) -> list[str]:
    return priority_points(streamers, max_amount, True)


def priority_streak(streamers: list[Streamer], max_amount: int) -> list[str]:
    result = []
    for streamer in streamers:
        if len(result) >= max_amount:
            break
        if (
            streamer.settings.watch_streak is True
            and streamer.stream.watch_streak_missing is True
            and (
                streamer.offline_at == 0
                or ((time.time() - streamer.offline_at) // 60) > 30
            )
        ):
            result.append(streamer.channel_id)
    return result


def priority_drops(streamers: list[Streamer], max_amount: int) -> list[str]:
    # max_amount can be ignored due to 1 drop limit
    for streamer in streamers:
        if streamer.any_campaign_has_claimable_drop() is True:
            return [streamer.channel_id]
    return []


def priority_subscribed(streamers: list[Streamer], max_amount: int) -> list[str]:
    streamers_with_multiplier = [
        streamer for streamer in streamers if streamer.viewer_has_points_multiplier()
    ]
    streamers_with_multiplier = sorted(
        streamers_with_multiplier,
        key=lambda x: x.total_points_multiplier(),
        reverse=True,
    )
    return [streamer.channel_id for streamer in streamers_with_multiplier[:max_amount]]


class PriorityFunction(Protocol):
    def __call__(self, streamers: list[Streamer], max_amount: int) -> list[str]: ...


priority_functions: dict[Priority, PriorityFunction] = {
    Priority.ORDER: priority_order,
    Priority.POINTS_ASCENDING: priority_points_ascending,
    Priority.POINTS_DESCENDING: priority_points_descending,
    Priority.STREAK: priority_streak,
    Priority.DROPS: priority_drops,
    Priority.SUBSCRIBED: priority_subscribed,
}


class PrioritySelector(StreamerSelector):
    """StreamerSelector that considers a given list of Priorities."""

    def __init__(
        self,
        priorities: list[Priority],
        priority_function_overrides: dict[Priority, PriorityFunction] | None = None,
    ):
        self.priorities = priorities
        if priority_function_overrides is not None:
            self.priority_functions = {
                priority: priority_function_overrides.get(
                    priority, priority_functions[priority]
                )
                for priority in priority_functions.keys()
            }
        else:
            self.priority_functions = priority_functions

    def select(self, streamers: list[Streamer], max_amount: int) -> list[str]:
        selected = LimitedSet[str](max_amount)
        unselected = {streamer.channel_id: streamer for streamer in streamers}
        for priority in self.priorities:
            if selected.remaining() <= 0 or len(unselected) <= 0:
                break

            if priority in self.priority_functions:
                to_add = self.priority_functions[priority](
                    list(unselected.values()), selected.remaining()
                )
                if not selected.add(*to_add):
                    break
                else:
                    for streamer in selected:
                        unselected.pop(streamer, None)
            else:
                logger.warning(f"Unknown priority {priority}")

        return list(selected)[:max_amount]


class PriorityGroupSelector(StreamerSelector):
    """Selects streamers based on the given PriorityGroup."""

    def __init__(self, streamers: list[str] | None, selector: PrioritySelector) -> None:
        self.streamers = streamers
        self.selector = selector

    def select(self, streamers: list[Streamer], max_amount: int) -> list[str]:
        streamers_by_ids = {streamer.channel_id: streamer for streamer in streamers}
        if self.streamers is None or len(self.streamers) == 0:
            sub_streamers = streamers
        else:
            group_streamers = self.streamers
            sub_streamers = [
                streamers_by_ids[streamer_id]
                for streamer_id in group_streamers
                if streamer_id in streamers_by_ids
            ]
        selection = self.selector.select(sub_streamers, max_amount)
        return selection[:max_amount]


class NestedSelector(StreamerSelector):
    """Selects streamers using the given selectors in order."""

    def __init__(self, selectors: list[StreamerSelector]) -> None:
        self.selectors = selectors

    def select(self, streamers: list[Streamer], max_amount: int) -> list[str]:
        selected = LimitedSet(max_amount)
        unselected = {streamer.channel_id: streamer for streamer in streamers}
        for selector in self.selectors:
            selection = selector.select(list(unselected.values()), selected.remaining())
            if not selected.add(*selection):
                break
            else:
                for streamer in selected:
                    unselected.pop(streamer, None)
        return list(selected)[:max_amount]


# Custom priority functions


def priority_streak_by_earliest_stream_created_at(
    streamers: list[Streamer], max_amount: int
) -> list[str]:
    """
    Prioritises only streamers that have streaks, ordered by ascending stream.created_at to prioritise streams that came
    online first.
    :param streamers: The streamers to consider.
    :param max_amount: The maximum amount of streamers to select.
    :return: The selected streamer ids.
    """
    streamers.sort(
        key=lambda streamer: (
            streamer.stream.created_at.timestamp()
            if streamer.stream.created_at is not None
            else 0
        ),
        reverse=False,
    )
    return priority_streak(streamers, max_amount)
