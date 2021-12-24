import pytest
from changes.data_backend import reset_data
from changes.auth_backend import auth_register, auth_login
from changes.channel_backend import channels_create, channel_invite, channel_leave
from clearDatabase import clear

#assuming that there is no channel_id with the number 123456
def test_non_existing_channel():
    reset_data()
    auth_register("1196746264@qq.com", "UNSWgoodgoodgood", "Jason", "Jin")
    login_info = auth_login("1196746264@qq.com", "UNSWgoodgoodgood")
    with pytest.raises(Exception):
        channel_leave(login_info["token"], 123456)
    clear()

def test_function_working():
    reset_data()
    auth_register("1196746264@qq.com", "UNSWbadbadbad", "Jsaon", "KKK")
    login_info = auth_login("1196746264@qq.com", "UNSWbadbadbad")
    login_info2 = auth_register("Feddrick@yahoo.com", "feddrickPassword", "Feddrick", "Aquino")
    channel_info = channels_create(login_info['token'], "higuys", "true")
    channel_invite(login_info['token'], channel_info['channel_id'], login_info2['u_id'])
    channel_leave(login_info['token'], channel_info['channel_id'])
    channel_leave(login_info2['token'], channel_info['channel_id'])
    with pytest.raises(Exception):
        channel_leave(login_info['token'], channel_info['channel_id'])
