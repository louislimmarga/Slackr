import pytest
from changes.data_backend import reset_data
from changes.auth_backend import auth_register
from changes.user_backend import user_profile, user_profile_sethandle
from clearDatabase import clear

def test_user_profile_sethandle ():
    reset_data()
    register_info = auth_register("feddrick100@yahoo.com", "123456", "Feddrick", "Aquino")

    token = register_info["token"]
    user_id = register_info["u_id"]
    
    profile = user_profile(token, user_id)
    assert profile["handle_str"] == "feddrickaquino"
    
    user_profile_sethandle (token, "feddrick")
    
    profile = user_profile (token, user_id)

    assert profile["handle_str"] == "feddrick"

    # more than 20 characters
    with pytest.raises(Exception):
        user_profile_sethandle (token, "123456789012345678901234567890")
    register_info2 = auth_register("dendi@yahoo.com", "123456", "Dendi", "Pudge")
    token2 = register_info2['token']
    with pytest.raises(Exception):
        user_profile_sethandle (token2, "feddrick")
    clear()
