import pytest
from changes.data_backend import reset_data
from changes.auth_backend import auth_register
from changes.user_backend import user_profile, user_profiles_uploadphoto, imgurl_function
from clearDatabase import clear, clearPictures

def test_invalid_url():
    reset_data()
    fourOfour_code_url = "http://google.com/za51"
    non_existing_url = "http://z52382.com"
    register_info = auth_register("feddrick100@yahoo.com", "123456", "Feddrick", "Aquino")
    token = register_info["token"]
    user_id = register_info["u_id"]
    with pytest.raises(Exception):
        user_profiles_uploadphoto(token, fourOfour_code_url, 0, 0, 50, 50)
    with pytest.raises(Exception):
        user_profiles_uploadphoto(token, non_existing_url, 0, 0, 50, 50)
    clear()

def test_user_profiles_uploadphoto ():
    reset_data()
    valid_img_url = "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png"
    invalid_img_url = "https://www.google.com/?client=safari"
    register_info = auth_register("feddrick100@yahoo.com", "123456", "Feddrick", "Aquino")
    token = register_info["token"]
    user_id = register_info["u_id"]
    profile = user_profile (token, user_id)
    # if url is invalid
    with pytest.raises(Exception): 
        user_profiles_uploadphoto (token, invalid_img_url, 0, 0, 50, 50)

    # if the dimension is not within the image at the url
    with pytest.raises(Exception): 
        user_profiles_uploadphoto (token, valid_img_url, 0, 0, 2131231231, 1132412341234)
    user_profiles_uploadphoto (token, valid_img_url, 0, 0, 80, 80)
    user_profiles_uploadphoto (token, valid_img_url, 0, 0, 100, 100)
    with pytest.raises(Exception): 
        imgurl_function("unknown_file.jpg")
    try:
        imgurl_function("firstAvatar.jpg")
    except:
        pass

    clear()
    clearPictures()
