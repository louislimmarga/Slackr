import pytest
from changes.data_backend import reset_data
from changes.auth_backend import auth_login, auth_register
from clearDatabase import clear

def test_invalid_email_password():
    reset_data()
    with pytest.raises(Exception):
        auth_login("abc123yahoo.com","123456")
    with pytest.raises(Exception):
        auth_login("abc123@yahoo.com","123")
    clear()
        
def test_auth_login_working():
    reset_data()
    register_info = auth_register("feddrick38@yahoo.com","123456","Feddrick","Aquino")
    login_info = auth_login("feddrick38@yahoo.com","123456")
    
    assert register_info["u_id"] == login_info["u_id"]
    clear()
    
def test_wrong_password():
    reset_data()
    register_info = auth_register("feddrick38@yahoo.com","123456","Feddrick","Aquino")
    with pytest.raises(Exception):
        auth_login("feddrick38@yahoo.com","wrongpassword")
    clear()
        
def test_email_not_user():
    reset_data()
    with pytest.raises(Exception):
        auth_login("pikachu@gmail.com","randomPassword")
    clear()
    
    
#for testing whether auth_login throw an exception if i put an email that does not belong to a user, i can assume that no one have registered an email yet so that putting a random valid email and password will always raise an exception


