import pytest
from changes.data_backend import reset_data
from changes.auth_backend import auth_register
from changes.user_backend import user_profile, user_profile_sethandle
from clearDatabase import clear

def test_user_profile ():
    reset_data()
    register_info1 = auth_register("dimitri@yahoo.com", "1234562", "Dimitry", "Quino")
    register_info = auth_register("feddrick100@yahoo.com", "123456", "Feddrick", "Aquino")
    register_info2 = auth_register("tim@yahoo.com", "1234562", "Tim", "Tam")
    token = register_info["token"]
    user_id = register_info["u_id"]
    
    profile = user_profile (token, user_id)

    assert profile["email"] == "feddrick100@yahoo.com"
    assert profile["name_first"] == "Feddrick"
    assert profile["name_last"] == "Aquino"
    assert profile["handle_str"] == "feddrickaquino"

    with pytest.raises(Exception):
        profile = user_profile (token, (user_id + 1))
    clear()
