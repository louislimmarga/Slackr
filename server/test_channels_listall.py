import pytest
from changes.data_backend import reset_data
from changes.auth_backend import auth_register
from changes.channel_backend import channels_create, channels_listall
from clearDatabase import clear

def test_private_channel():
    reset_data()
    login_info = auth_register("1196746264@qq.com", "UNSW123456", "Jason", "Jin")
    login_info_2 = auth_register("yyy000000@qq.com", "UNSW123456", "Jason", "Jin")
    channels_create(login_info["token"],"UNSW Slackers", 'false')
    assert channels_listall(login_info_2["token"]) == {"channels": []}
    channels_create(login_info["token"], "UNSW Slackers 2", 'true')
    curr_channels = channels_listall(login_info_2["token"])
    assert curr_channels['channels'][0]['name'] == "UNSW Slackers 2"
    clear()
    

