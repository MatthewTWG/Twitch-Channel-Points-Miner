import pytest

from TwitchChannelPointsMiner.classes.entities.Streamer import Streamer


class TestStreamer:
    update_history_data = [
        [[], {}, 0, True],
        [[["WATCH", 10, 1]], {"WATCH": {"amount": 10, "counter": 1}}, 1, True],
        [
            [["WATCH_STREAK", 300, 1]],
            {"WATCH_STREAK": {"amount": 300, "counter": 1}},
            0,
            False,
        ],
        [
            [["WATCH_STREAK", 300, 1], ["WATCH", 10, 1]],
            {
                "WATCH_STREAK": {"amount": 300, "counter": 1},
                "WATCH": {"amount": 10, "counter": 1},
            },
            1,
            False,
        ],
        [
            [["WATCH", 10, 1], ["WATCH", 10, 1]],
            {
                "WATCH": {"amount": 20, "counter": 2},
            },
            2,
            False,
        ],
        [
            [["WATCH", 10, 1], ["WATCH", 10, 1], ["WATCH_STREAK", 300, 1]],
            {
                "WATCH_STREAK": {"amount": 300, "counter": 1},
                "WATCH": {"amount": 20, "counter": 2},
            },
            2,
            False,
        ],
        [
            [
                ["WATCH", 10, 1],
                ["WATCH", 10, 1],
                ["WATCH_STREAK", 300, 1],
                ["WATCH", 10, 1],
                ["WATCH", 12, 1],
                ["WATCH", 12, 1],
            ],
            {
                "WATCH_STREAK": {"amount": 300, "counter": 1},
                "WATCH": {"amount": 54, "counter": 5},
            },
            5,
            False,
        ],
    ]

    @pytest.mark.parametrize(
        "updates,expected_counts,expected_stream_watch_count,expected_watch_streak_missing",
        update_history_data,
    )
    def test_update_history(
        self,
        updates: list,
        expected_counts: dict,
        expected_stream_watch_count: int,
        expected_watch_streak_missing: bool,
    ):
        streamer = Streamer("test_username")

        for update in updates:
            streamer.update_history(update[0], update[1], update[2])

        assert len(streamer.history) == len(expected_counts)
        for reason in expected_counts.keys():
            assert streamer.history[reason] == expected_counts[reason]

        assert streamer.stream.watch_count == expected_stream_watch_count
        assert streamer.stream.watch_streak_missing == expected_watch_streak_missing
