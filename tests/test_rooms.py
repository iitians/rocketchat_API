import pytest

from rocketchat_API.APIExceptions.RocketExceptions import RocketMissingParamException


def test_rooms_upload(logged_rocket):
    # ToDo: Find a better way to test that this endpoint actually works fine (when using json and not data fails
    # silently)
    rooms_upload = logged_rocket.rooms_upload(
        "GENERAL", file="tests/assets/avatar.png", description="hey there"
    ).json()
    assert rooms_upload.get("success")


def test_rooms_get(logged_rocket):
    rooms_get = logged_rocket.rooms_get().json()
    assert rooms_get.get("success")


def test_rooms_clean_history(logged_rocket):
    rooms_clean_history = logged_rocket.rooms_clean_history(
        room_id="GENERAL",
        latest="2016-09-30T13:42:25.304Z",
        oldest="2016-05-30T13:42:25.304Z",
    ).json()
    assert rooms_clean_history.get("success")


def test_rooms_favorite(logged_rocket):
    rooms_favorite = logged_rocket.rooms_favorite(
        room_id="GENERAL", favorite=True
    ).json()
    assert rooms_favorite.get("success")

    rooms_favorite = logged_rocket.rooms_favorite(
        room_name="general", favorite=True
    ).json()
    assert rooms_favorite.get("success")

    rooms_favorite = logged_rocket.rooms_favorite(
        room_id="unexisting_channel", favorite=True
    ).json()
    assert not rooms_favorite.get("success")

    with pytest.raises(RocketMissingParamException):
        logged_rocket.rooms_favorite()


def test_rooms_info(logged_rocket):
    rooms_infoby_name = logged_rocket.rooms_info(room_name="general").json()
    assert rooms_infoby_name.get("success")
    assert rooms_infoby_name.get("room").get("_id") == "GENERAL"
    rooms_info_by_id = logged_rocket.rooms_info(room_id="GENERAL").json()
    assert rooms_info_by_id.get("success")
    assert rooms_info_by_id.get("room").get("_id") == "GENERAL"
    with pytest.raises(RocketMissingParamException):
        logged_rocket.rooms_info()


def test_rooms_admin_rooms(logged_rocket):
    rooms_simple = logged_rocket.rooms_admin_rooms().json()
    assert rooms_simple.get("success")

    # Using a room type filter does not seem to work
    offset = actual_count = 0
    res = {}
    while res.get("total") is None or res.get("total") > offset:
        res = logged_rocket.rooms_admin_rooms(
            **{
                "types": [
                    "c",
                ],
                "offset": offset,
            }
        ).json()
        assert res.get("success")
        offset += res.get("count")
        actual_count += len(list(filter(lambda x: "c" in x["t"], res.get("rooms"))))
    assert res.get("total") == actual_count

    rooms_with_filter = logged_rocket.rooms_admin_rooms(**{"filter": "general"}).json()
    assert rooms_with_filter.get("success")
    assert rooms_with_filter.get("rooms")[0].get("_id") == "GENERAL"
