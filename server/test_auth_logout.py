import pytest
from changes.data_backend import reset_data
from changes.auth_backend import auth_register, auth_logout
from changes.channel_backend import channels_list, channels_listall
from clearDatabase import clear

def test_auth_logout_working():
    reset_data()
    register_info = auth_register("feddrickaquino@gmail.com","123456","Feddrick","Aquino")
    auth_logout(register_info["token"])
    #i assume that in the future, i will implement the function to raise an exception when passed in invalid token
    with pytest.raises(Exception):
        channels_list(register_info["token"])
    with pytest.raises(Exception):
        channels_listall(register_info["token"])
    clear()

def test_wrong_token():
    reset_data()
    auth_register("feddrick38@yahoo.com","123456","Feddrick","Aquino")
    with pytest.raises(Exception):
        auth_logout('hahaha')
    status = auth_logout("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImZlZGRyaWNrMzhAeWFob28uY29tIiwidGltZXN0YW1wIjoxNTczNzg5MzYzLjU5NTkwMjJ9.FTIbiMGj7-wnp0iUs0AO-ac2edCLwOs2y0lKEGX-g94")
    assert status['is_success'] == False
