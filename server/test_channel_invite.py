import pytest
from changes.data_backend import reset_data
from changes.auth_backend import auth_register, auth_login
from changes.channel_backend import channels_create, channel_invite
from clearDatabase import clear

#Someone has to be in the channel in order to invite other friends
def test_not_in_channel():
    reset_data()
    register_info = auth_register("1196746264@qq.com", "123456", "Jason", "Jin")
    login_info = auth_login("1196746264@qq.com", "123456")
    register_info2 = auth_register("dedy@qq.com", "123456", "Dedy", "Hariady")
    login_info_2 = auth_login('dedy@qq.com', "123456")
    channel_info = channels_create(login_info_2['token'],"higuys", "true")
    with pytest.raises(Exception):
        channel_invite(login_info["token"], channel_info['channel_id'], login_info2["u_id"])
    clear()
    
#assuming that the user with 4396 does not exist
def test_invalid_user():
    reset_data()
    auth_register("1196746264@qq.com", "123456", "Jason", "Jin")
    login_info = auth_login("1196746264@qq.com", "123456") 
    channel_info = channels_create(login_info["token"],"UNSW bad student",'true')
    with pytest.raises(Exception):
        channel_invite(login_info["token"], channel_info["channel_id"], 4396)
    clear()

def test_already_in():
    reset_data()
    auth_register("1196746264@qq.com", "123456", "Jason", "Jin")
    login_info = auth_login("1196746264@qq.com", "123456")
    auth_register("64@qq.com", "123456", "Jason", "Jin")
    login_info_2 = auth_login("64@qq.com", "123456")
    channel_info = channels_create(login_info["token"],"UNSW bad student",'true')
    channel_invite(login_info['token'], channel_info['channel_id'], login_info_2['u_id'])
    with pytest.raises(Exception):
        channel_invite(login_info['token'], channel_info['channel_id'], login_info_2['u_id'])
    clear()

def test_non_member_invite_user_to_channel():
    reset_data()
    login_info = auth_register("1196746264@qq.com", "123456", "Jason", "Jin")
    login_info_2 = auth_register("64@qq.com", "123456", "Jason", "Jin")
    login_info_3 = auth_register("fedd@yahoo.com", "feddrickPassword", "Feddrick", "Aquino")
    channel_info = channels_create(login_info["token"],"UNSW bad student",'true')
    with pytest.raises(Exception):
        channel_invite(login_info_2['token'], channel_info['channel_id'], login_info_3['u_id'])
    clear()
        
            


    
