import pytest
from changes.data_backend import reset_data
from changes.auth_backend import auth_register, auth_login
from changes.channel_backend import channels_create
from clearDatabase import clear

#assuming that channels_create can have only either True or False for 
#one of the parameter
def test_invalid_channel_name():
    reset_data()
    auth_register("1196746264@qq.com", "UNSW123456", "Jason", "Jin")
    login_info = auth_login("1196746264@qq.com", "UNSW123456")
    with pytest.raises(Exception):
        channels_create(login_info["token"],"qwertyuiopasdfghjklzxcq", 'true')
    with pytest.raises(Exception):
        channels_create(login_info["token"],"qwertyuiopasdfghjklzxcq", 'false')
        
    ID = channels_create(login_info["token"],"Jason public", 'true')
    ID = channels_create(login_info["token"],"Jason private", 'false')
    clear()

