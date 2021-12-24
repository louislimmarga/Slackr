import pytest
from changes.data_backend import reset_data
from changes.auth_backend import auth_register, auth_login
from changes.channel_backend import channels_create, channel_join
from clearDatabase import clear

#assuming that the channel with id 123456 does not exit since that it is not 
#created yet

def test_none_existing_channel():
    reset_data()
    login_info = auth_register("1196746264@qq.com", "UNSW666", "Jason", "Jin")
    login_info_2 = auth_register("119600000@qq.com", "UNSW666", "Jason", "Jin")
    with pytest.raises(Exception):
        channel_join(login_info["token"], 123456)
    clear()
    
def test_private_channel():
    reset_data()
    login_info = auth_register("1196746264@qq.com", "UNSW666", "Jason", "Jin")
    login_info_2 = auth_register("119600000@qq.com", "UNSW666", "Jason", "Jin")
    ID = channels_create(login_info["token"], "UNSW's bad kids", 'false')
    with pytest.raises(Exception):
        channel_join(login_info_2["token"], ID["channel_id"])
    clear()

def test_joining_joined_channel():
    reset_data()
    login_info = auth_register("feddrick38@yahoo.com", "UNSW666", "Feddrick", "Aquino")
    login_info_2 = auth_register("Jim@yahoo.com", "UNSW666", "Jim", "Jam")
    channel_id = channels_create(login_info["token"], "Fedd channel", 'true')
    channel_join(login_info_2["token"], channel_id["channel_id"])
    with pytest.raises(Exception):
        #second user joining an already joined channel
        channel_join(login_info_2["token"], channel_id["channel_id"])
    clear()
