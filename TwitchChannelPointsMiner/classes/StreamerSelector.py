import abc
import time

from TwitchChannelPointsMiner.classes.Settings import Priority
from TwitchChannelPointsMiner.classes.entities.Streamer import Streamer


class StreamerSelector(abc.ABC):
    """Class for selecting streamers from a list."""

    @abc.abstractmethod
    def select(self, streamers: list[Streamer]) -> list[int]:
        """
        Selects streamers from the list.
        :param streamers: The streamers to consider.
        :return: The selected streamers.
        """
        pass


class PrioritySelector(StreamerSelector):
    def __init__(self, priorities: list[Priority]):
        self.priorities = priorities

    def select(self, streamers: list[Streamer]) -> list[int]:
        """
        Selects streamers from the list based on the priorities.
        :param streamers: The streamers to consider.
        :return: The selected streamers.
        """
        streamers_index = [
            i
            for i in range(0, len(streamers))
            if streamers[i].is_online is True
            and (
                streamers[i].online_at == 0
                or (time.time() - streamers[i].online_at) > 30
            )
        ]

        """
        Twitch has a limit - you can't watch more than 2 channels at one time.
        We'll take the first two streamers from the final list as they have the highest priority.
        """
        max_watch_amount = 2
        streamers_watching: set[int] = set()

        def remaining_watch_amount():
            return max_watch_amount - len(streamers_watching)

        def add_to_watching(*streamer_indices: int):
            """
            Adds 1 or more streamer indices to the watch set and returns whether the set has more room.
            :param streamer_indices: The indices to add.
            :return: True if the set has room, False if it's full.
            """
            for streamer_index in streamer_indices:
                if remaining_watch_amount() > 0:
                    streamers_watching.add(streamer_index)
                else:
                    return False
            return remaining_watch_amount() > 0

        for priority in self.priorities:
            if remaining_watch_amount() <= 0:
                break

            if priority == Priority.ORDER:
                # Get the first 2 items, they are already in order
                if not add_to_watching(*streamers_index):
                    break

            elif priority in [Priority.POINTS_ASCENDING, Priority.POINTS_DESCENDING]:
                items = [
                    {"points": streamers[index].channel_points, "index": index}
                    for index in streamers_index
                ]
                items = sorted(
                    items,
                    key=lambda x: x["points"],
                    reverse=(True if priority == Priority.POINTS_DESCENDING else False),
                )
                if not add_to_watching(*[item["index"] for item in items]):
                    break

            elif priority == Priority.STREAK:
                """
                Check if we need need to change priority based on watch streak
                Viewers receive points for returning for x consecutive streams.
                Each stream must be at least 10 minutes long and it must have been at least 30 minutes since the last stream ended.
                Watch at least 6m for get the +10
                """
                for index in streamers_index:
                    if (
                        streamers[index].settings.watch_streak is True
                        and streamers[index].stream.watch_streak_missing is True
                        and (
                            streamers[index].offline_at == 0
                            or ((time.time() - streamers[index].offline_at) // 60) > 30
                        )
                        # fix #425
                        and streamers[index].stream.minute_watched < 7
                    ):
                        if not add_to_watching(index):
                            break

            elif priority == Priority.DROPS:
                for index in streamers_index:
                    if streamers[index].any_campaign_has_claimable_drop() is True:
                        if not add_to_watching(index):
                            break

            elif priority == Priority.SUBSCRIBED:
                streamers_with_multiplier = [
                    index
                    for index in streamers_index
                    if streamers[index].viewer_has_points_multiplier()
                ]
                streamers_with_multiplier = sorted(
                    streamers_with_multiplier,
                    key=lambda x: streamers[x].total_points_multiplier(),
                    reverse=True,
                )
                if not add_to_watching(*streamers_with_multiplier):
                    break

        return list(streamers_watching)[:max_watch_amount]
