from TwitchChannelPointsMiner.classes.gql.data.Parser import Parser


class TestParseDropCampaignDetailsResponse:
    response = {
        "data": {
            "user": {
                "id": "123456",
                "dropCampaign": {
                    "id": "bea2eb2b-b3f3-4c12-90e9-d6c7afb50bc5",
                    "name": "CDL Major 4",
                    "status": "ACTIVE",
                    "game": {
                        "id": "2012789438",
                        "slug": "call-of-duty-black-ops-7",
                        "displayName": "Call of Duty: Black Ops 7",
                    },
                    "allow": {
                        "channels": [{"id": "41744414"}],
                        "isEnabled": True,
                    },
                    "startAt": "2026-06-05T12:00:00Z",
                    "endAt": "2026-06-06T06:29:59.999Z",
                    "timeBasedDrops": [
                        {
                            "id": "cee6bcc3-5564-11f1-9875-0a58a9feac02",
                            "name": "60 Min Drop",
                            "startAt": "2026-06-05T12:00:00Z",
                            "endAt": "2026-06-06T06:29:59.999Z",
                            "benefitEdges": [
                                {"benefit": {"name": "1 Hour XP Token"}}
                            ],
                            "requiredMinutesWatched": 60,
                            "requiredSubs": 0,
                        }
                    ],
                },
            }
        },
        "extensions": {"operationName": "DropCampaignDetails"},
    }

    def test_parses_campaign_from_user_drop_campaign(self):
        result = Parser().parse_drop_campaign_details_response(self.response)

        campaign = result.campaign
        assert campaign.id == "bea2eb2b-b3f3-4c12-90e9-d6c7afb50bc5"
        assert campaign.name == "CDL Major 4"
        assert campaign.status == "ACTIVE"
        assert campaign.game.slug == "call-of-duty-black-ops-7"
        assert campaign.allow_channel_ids == ["41744414"]
        assert len(campaign.time_based_drops) == 1
        assert campaign.time_based_drops[0].required_minutes_watched == 60
