import pytest

from TwitchChannelPointsMiner.utils.LimitedSet import LimitedSet


class TestLimitedSet:
    add_single_data = [
        [0, "a", False, 0, False],
        [1, "b", False, 0, True],
        [2, "c", True, 1, True],
        [3, "d", True, 2, True],
        [4, "e", True, 3, True],
    ]

    add_multiple_data = [
        [0, [], False, 0, []],
        [0, ["a"], False, 0, [False]],
        [0, ["a", "b"], False, 0, [False, False]],
        [1, [], True, 1, []],
        [1, ["a"], False, 0, [True]],
        [1, ["a", "b"], False, 0, [True, False]],
        [2, [], True, 2, []],
        [2, ["a"], True, 1, [True]],
        [2, ["a", "b"], False, 0, [True, True]],
        [2, ["a", "b", "c"], False, 0, [True, True, False]],
    ]

    add_single_with_partially_full_data = [
        [1, ["a"], "b", False, 0, False],
        [2, ["a"], "b", False, 0, True],
        [2, ["a", "b"], "c", False, 0, False],
        [3, ["a"], "b", True, 1, True],
        [3, ["a", "b"], "c", False, 0, True],
        [3, ["a", "b", "c"], "d", False, 0, False],
    ]

    add_multiple_with_partially_full_data = [
        [1, ["a"], ["b", "c"], False, 0, [False, False]],
        [2, ["a"], ["b", "c"], False, 0, [True, False]],
        [2, ["a", "b"], ["c", "d"], False, 0, [False, False]],
        [3, ["a"], ["b", "c"], False, 0, [True, True]],
        [3, ["a", "b"], ["c", "d"], False, 0, [True, False]],
        [3, ["a", "b", "c"], ["d", "e"], False, 0, [False, False]],
        [4, ["a"], ["b", "c"], True, 1, [True, True]],
        [4, ["a", "b"], ["c", "d"], False, 0, [True, True]],
        [4, ["a", "b", "c"], ["d", "e"], False, 0, [True, False]],
        [4, ["a", "b", "c", "d"], ["e", "f"], False, 0, [False, False]],
    ]

    add_single_existing_data = [
        [1, ["a"], "a", False, 0],
        [2, ["a"], "a", True, 1],
        [2, ["a", "b"], "a", False, 0],
        [2, ["a", "b"], "b", False, 0],
        [3, ["a"], "a", True, 2],
        [3, ["a", "b"], "a", True, 1],
        [3, ["a", "b"], "b", True, 1],
        [3, ["a", "b", "c"], "a", False, 0],
        [3, ["a", "b", "c"], "b", False, 0],
        [3, ["a", "b", "c"], "c", False, 0],
    ]

    add_multiple_existing_data = [
        [1, ["a"], ["a", "b"], False, 0, [True, False]],
        [1, ["a"], ["a", "b", "c"], False, 0, [True, False, False]],
        [1, ["b"], ["a", "b", "c"], False, 0, [False, True, False]],
        [1, ["c"], ["a", "b", "c"], False, 0, [False, False, True]],
        [2, ["a"], ["a", "b"], False, 0, [True, True]],
        [2, ["b"], ["a", "b"], False, 0, [True, True]],
        [2, ["a", "b"], ["a", "b"], False, 0, [True, True]],
        [2, ["a", "b"], ["a", "b", "c"], False, 0, [True, True, False]],
        [2, ["a", "c"], ["a", "b", "c"], False, 0, [True, False, True]],
        [2, ["b", "c"], ["a", "b", "c"], False, 0, [False, True, True]],
    ]

    @pytest.mark.parametrize(
        "max_size,item,expected_room,expected_remaining,expect_in", add_single_data
    )
    def test_add_single(
        self,
        max_size: int,
        item: str,
        expected_room: bool,
        expected_remaining: int,
        expect_in: bool,
    ):
        limited_set = LimitedSet(max_size)
        room = limited_set.add(item)
        remaining = limited_set.remaining()
        in_set = item in limited_set
        assert room == expected_room
        assert remaining == expected_remaining
        assert in_set == expect_in

    @pytest.mark.parametrize(
        "max_size,items,expected_room,expected_remaining,expect_in", add_multiple_data
    )
    def test_add_multiple(
        self,
        max_size: int,
        items: list[str],
        expected_room: bool,
        expected_remaining: int,
        expect_in: list[bool],
    ):
        limited_set = LimitedSet(max_size)
        room = limited_set.add(*items)
        remaining = limited_set.remaining()
        in_set = [item in limited_set for item in items]
        assert room == expected_room
        assert remaining == expected_remaining
        assert in_set == expect_in

    @pytest.mark.parametrize(
        "max_size,initial_items,item,expected_room,expected_remaining,expect_in",
        add_single_with_partially_full_data,
    )
    def test_add_single_with_partially_full(
        self,
        max_size: int,
        initial_items: list[str],
        item: str,
        expected_room: bool,
        expected_remaining: int,
        expect_in: bool,
    ):
        limited_set = LimitedSet[str](max_size)
        limited_set.add(*initial_items)
        room = limited_set.add(item)
        remaining = limited_set.remaining()
        in_set = item in limited_set
        assert room == expected_room
        assert remaining == expected_remaining
        assert in_set == expect_in

    @pytest.mark.parametrize(
        "max_size,initial_items,items,expected_room,expected_remaining,expect_in",
        add_multiple_with_partially_full_data,
    )
    def test_add_multiple_with_partially_full(
        self,
        max_size: int,
        initial_items: list[str],
        items: list[str],
        expected_room: bool,
        expected_remaining: int,
        expect_in: list[bool],
    ):
        limited_set = LimitedSet(max_size)
        limited_set.add(*initial_items)
        room = limited_set.add(*items)
        remaining = limited_set.remaining()
        in_set = [item in limited_set for item in items]
        assert room == expected_room
        assert remaining == expected_remaining
        assert in_set == expect_in

    @pytest.mark.parametrize(
        "max_size,initial_items,item,expected_room,expected_remaining",
        add_single_existing_data,
    )
    def test_add_single_existing(
        self,
        max_size: int,
        initial_items: list[str],
        item: str,
        expected_room: bool,
        expected_remaining: int,
    ):
        limited_set = LimitedSet[str](max_size)
        limited_set.add(*initial_items)
        room = limited_set.add(item)
        remaining = limited_set.remaining()
        in_set = item in limited_set
        assert room == expected_room
        assert remaining == expected_remaining
        assert in_set == True

    @pytest.mark.parametrize(
        "max_size,initial_items,items,expected_room,expected_remaining,expect_in",
        add_multiple_existing_data,
    )
    def test_add_multiple_existing(
        self,
        max_size: int,
        initial_items: list[str],
        items: list[str],
        expected_room: bool,
        expected_remaining: int,
        expect_in: list[bool]
    ):
        limited_set = LimitedSet(max_size)
        limited_set.add(*initial_items)
        room = limited_set.add(*items)
        remaining = limited_set.remaining()
        in_set = [item in limited_set for item in items]
        assert room == expected_room
        assert remaining == expected_remaining
        assert in_set == expect_in
