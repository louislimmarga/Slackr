import pytest
from changes.data_backend import reset_data
from changes.auth_backend import auth_login, auth_register
from clearDatabase import clear

def test_invalid_email():
    reset_data()
    with pytest.raises(Exception):
        #registering with invalid email (incorrect format) 
        auth_register("feddrick100yahoo.com ","123456","Feddrick","Aquino")
    clear()
        
def test_invalid_password():
    reset_data()
    with pytest.raises(Exception):
        #password less than 5 character
        auth_register("feddrick100@yahoo.com ","123","Feddrick","Aquino")
    clear()
        
def test_register_already_used_email():
    reset_data()
    #register with already registered email
    auth_register("bananaPie@gmail.com","validPassword","Sally","Bob")
    with pytest.raises(Exception):
        auth_register("bananaPie@gmail.com","myPassword","David","Beckham")
    clear()
        
def test_invalid_name():
    reset_data()
    with pytest.raises(Exception):
    #case when first name is more than 50 characters long 
        auth_register("feddrick40@yahoo.com","password123","thisIsMoreThan50characterslong3032343638404244464850e","Dedy")
    with pytest.raises(Exception):
    #case when last name is more than 50 characters long
        auth_register("bobby@yahoo.com","password123","Marrie","thisIsMoreThan50characterslong3032343638404244464850e")
    clear()
    
def test_auth_register_working():
    reset_data()
    register_info = auth_register("maria@hotmail.com","password123","Maria","Sean")
    #if auth_register works, the bottom won't raises an exception
    login_info = auth_login("maria@hotmail.com","password123")
    assert register_info["u_id"] == login_info["u_id"]
    clear()
    
def test_auth_create_mutiple_handle():
    reset_data()
    register_info1 = auth_register("feddrick@hotmail.com","password123","Feddrick","Aquino")
    register_info2 = auth_register("fedd@hotmail.com","password123","Feddrick","Aquino")
    register_info3 = auth_register("Timothius@hotmail.com","password123","Timothius","AndratamaTanary")

def test_short_password():
    reset_data()
    with pytest.raises(Exception):
        #cases where the password is too short
        auth_register("maria@hotmail.com","23","Maria","Sean")
    clear()
