import pytest
from changes.data_backend import reset_data
from changes.auth_backend import auth_register, auth_login
from changes.channel_backend import channels_create, channel_details
from clearDatabase import clear

#assuming that there is no channel_id "000000"
def test_non_existent_channel_id():
    reset_data()
    auth_register("1196746264@qq.com", "123456", "Jason", "Jin")
    login_info = auth_login("1196746264@qq.com", "123456")
    with pytest.raises(Exception):
        channel_details(login_info["tokens"], 000000)
    clear()
    
#assume that the two users are not in the same channel
def test_non_existent_member():
    reset_data()
    auth_register("1196746264@qq.com", "123456", "Jason", "Jin")
    auth_register("1196746260@qq.com", "123465", "Jason", "Jin")   
    login_info = auth_login("1196746264@qq.com", "123456")
    login_info_2 = auth_login("1196746260@qq.com", "123465")
    channel_info = channels_create(login_info["token"],"UNSW bad student",'true')
    with pytest.raises(Exception):
        channel_details(login_info_2["token"], channel_info['channel_id'])
    clear()

def test_function_run():
    reset_data()
    auth_register("119674626@qq.com", "123456", "Jason", "Jin")
    login_info = auth_login("119674626@qq.com", "123456")
    channel_info = channels_create(login_info['token'], "UNSW bad student", "true")
    channel_details(login_info['token'], channel_info['channel_id'])


