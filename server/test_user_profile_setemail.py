import pytest
from changes.data_backend import reset_data
from changes.auth_backend import auth_register, auth_login
from changes.user_backend import user_profile, user_profile_setemail
from clearDatabase import clear

def test_user_setemail ():
    reset_data()
    register_info = auth_register("feddrick100@yahoo.com", "123456", "Feddrick", "Aquino")

    token = register_info["token"]
    user_id = register_info["u_id"]

    user_profile_setemail (token, "jasonjin@gmail.com")
    
    login_info = auth_login("jasonjin@gmail.com", "123456")
    token = login_info["token"]
    profile = user_profile (token, user_id)

    assert profile["email"] == "jasonjin@gmail.com"

    register_info2 = auth_register("feddrick100@yahoo.com", "123456", "Feddrick", "Aquino")

    #check for same email and invalid email
    with pytest.raises(Exception):
        user_profile_setemail (token, "feddrick100@yahoo.com")
    with pytest.raises(Exception):
        user_profile_setemail (token, "feddrick.com")
    clear()
