# -*- coding: utf-8 -*-

from TwitchChannelPointsMiner import TwitchChannelPointsMiner

twitch_miner = TwitchChannelPointsMiner(
    username="your-twitch-username",
    password="write-your-secure-psw",
)

twitch_miner.mine(
    streamers=[],
    followers=True,
)
