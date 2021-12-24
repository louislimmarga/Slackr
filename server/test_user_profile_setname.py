import pytest
from changes.data_backend import reset_data
from changes.auth_backend import auth_register
from changes.user_backend import user_profile, user_profile_setname
from clearDatabase import clear

def test_user_profile_setname ():
    reset_data()
    register_info = auth_register("feddrick100@yahoo.com", "123456", "Feddrick", "Aquino")

    token = register_info["token"]
    user_id = register_info["u_id"]
    profile = user_profile (token, user_id)
    assert profile["name_first"] == "Feddrick"
    assert profile["name_last"] == "Aquino"
    
    user_profile_setname (token, "Jason", "Jin")

    profile = user_profile (token, user_id)

    assert profile["name_first"] == "Jason"
    assert profile["name_last"] == "Jin"

    # more than 50 characters
    with pytest.raises(Exception):
        user_profile_setname (token, "1234567890123245678901234567890123456789012345678901234567890", "Jin")
    with pytest.raises(Exception):
        user_profile_setname (token, "Jason", "1234567890123245678901234567890123456789012345678901234567890")
    with pytest.raises(Exception):
        user_profile_setname (token, "1234567890123245678901234567890123456789012345678901234567890", "1234567890123245678901234567890123456789012345678901234567890")
    clear()
    


