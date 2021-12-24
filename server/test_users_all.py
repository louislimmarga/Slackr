import pytest
from changes.data_backend import reset_data
from changes.auth_backend import auth_register
from changes.user_backend import user_profile, users_all
from clearDatabase import clear

def test_users_all():
    reset_data()
    register_info = auth_register("feddrick100@yahoo.com", "123456", "Feddrick", "Aquino")
    register_info2 = auth_register("jason@gmail.com", "123412341234", "Jason", "Jin")
    register_info3 = auth_register("jasonn@gmail.com", "123123123", "JASONNNN", "JIIN")

    token = register_info["token"]

    data = users_all(token)

    assert data['users'][0]['email'] == "feddrick100@yahoo.com"
    assert data['users'][1]['email'] == "jason@gmail.com"
    assert data['users'][2]['email'] == "jasonn@gmail.com"
    clear()