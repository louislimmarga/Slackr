import pytest
from changes.data_backend import reset_data
from changes.user_permission_change import admin_userpermission_change
from changes.auth_backend import auth_register
from clearDatabase import clear

def test_admin_userpermission_change ():
    reset_data()
    register_info = auth_register("feddrick100@yahoo.com","123456","Feddrick","Aquino")
    token = register_info["token"]
    user_id = register_info["u_id"]

    #first user is owner

    register_info2 = auth_register("jasonjin@gmail.com","123456","Jason","Jin")
    token2 = register_info2["token"]
    user_id2 = register_info2["u_id"]

    register_info3 = auth_register("jason@gmail.com","123456","Jasn","Jn")
    token3 = register_info3["token"]
    user_id3 = register_info3["u_id"]

    #user is not an admin or owner
    with pytest.raises(Exception):
        admin_userpermission_change(token2, user_id, 3)

    #permission_id does not refer to a value permission 
    with pytest.raises(Exception):
        admin_userpermission_change(token, user_id2, 100)

    #u_id does not refer to a valid user
    with pytest.raises(Exception):
        admin_userpermission_change(token, user_id + user_id2, 3)
    
    admin_userpermission_change(token, user_id2, 2)

    #user 2 which is an admin is trying to change a from permission 3 to 1
    with pytest.raises(Exception):
        admin_userpermission_change(token2, user_id3, 1)

    admin_userpermission_change(token2, user_id3, 2)

    #user 2 which is admin try to remove ownership of first user
    with pytest.raises(Exception):
        admin_userpermission_change(token2, user_id, 3)
        
    clear()
