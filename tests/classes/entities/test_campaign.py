from datetime import datetime, timedelta, timezone

from TwitchChannelPointsMiner.classes.entities.Campaign import Campaign
from TwitchChannelPointsMiner.classes.gql.data.response.Drops import (
    DropCampaignDetails,
    GameDetails,
)


def make_details(start_at: datetime, end_at: datetime) -> DropCampaignDetails:
    return DropCampaignDetails(
        _id="bea2eb2b-b3f3-4c12-90e9-d6c7afb50bc5",
        name="Test Campaign",
        status="ACTIVE",
        game=GameDetails("1", "test-game", "Test Game"),
        allow_channel_ids=None,
        start_at=start_at,
        end_at=end_at,
        time_based_drops=[],
    )


class TestCampaign:
    # The GQL parser produces timezone-aware datetimes ("Z" suffix), so the
    # dt_match comparison must not break against the local naive clock.
    def test_dt_match_true_for_running_campaign(self):
        now = datetime.now(timezone.utc)
        campaign = Campaign(
            make_details(now - timedelta(hours=1), now + timedelta(hours=1))
        )
        assert campaign.dt_match is True

    def test_dt_match_false_for_ended_campaign(self):
        now = datetime.now(timezone.utc)
        campaign = Campaign(
            make_details(now - timedelta(hours=2), now - timedelta(hours=1))
        )
        assert campaign.dt_match is False
