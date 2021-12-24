import pytest
from changes.data_backend import reset_data
from changes.auth_backend import auth_register
from changes.channel_backend import channels_create, channel_invite, channels_list
from clearDatabase import clear

def test_channels_list ():
    reset_data()
    register_info = auth_register("feddrick100@yahoo.com","123456","Feddrick","Aquino")

    token = register_info["token"]

    channel_id1 = channels_create(token, "test1", 'true')    #assuming true = public

    curr_channels = channels_list(token)
    assert curr_channels["channels"][0]["name"] == "test1"
    assert curr_channels["channels"][0]["channel_id"] == channel_id1["channel_id"]

    channel_id2 = channels_create(token, "test2", 'true')    #assuming true = public
    channel_id3 = channels_create(token, "test3", 'true')    #assuming true = public

    curr_channels = channels_list(token)
    assert curr_channels["channels"][0]["name"] == "test1"
    assert curr_channels["channels"][0]["channel_id"] == channel_id1["channel_id"]
    assert curr_channels["channels"][1]["name"] == "test2"
    assert curr_channels["channels"][1]["channel_id"] == channel_id2["channel_id"]
    assert curr_channels["channels"][2]["name"] == "test3"
    assert curr_channels["channels"][2]["channel_id"] == channel_id3["channel_id"]
    clear()
    
