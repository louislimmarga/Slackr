import pytest
from changes.data_backend import reset_data
from changes.auth_backend import auth_login, auth_register, auth_passwordreset_reset
from clearDatabase import clear

#how do you know this is a valid reset code?
def test_invalid_password():
    reset_data()
    with pytest.raises(Exception):
        auth_passwordreset_reset("ETHg", "GGWP")
    with pytest.raises(Exception):
        auth_passwordreset_reset("HKWm", "1234")
    with pytest.raises(Exception):
        auth_passwordreset_reset("JKWW", "")
    clear()      
        
def test_invalid_reset_code():
    reset_data()
    with pytest.raises(Exception):
        auth_passwordreset_reset("123456789890-", "jason1234565,./")
    with pytest.raises(Exception):
        auth_passwordreset_reset("invalidcode", "hongjijin110")
    clear()
        
        

    
