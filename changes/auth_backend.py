import time
from random import randint, choices
from flask_cors import CORS
from flask_mail import Mail, Message
from flask import Flask, request, send_from_directory
from werkzeug.exceptions import HTTPException
import jwt
from changes.Error import AccessError
from changes.data_backend import getUsersList, getResetCodes, getSECRET, save, ValueError
from changes.helper_func import decodeToken, checkEmailExist, searchUserByEmail, isValidEmail, hashPassword, encodeToken, getUsersList, createHandle, createU_ID

def auth_login_argument_valid(function):
    def wrapper(email=None, password=None):
        if isValidEmail(email) is False:
            raise ValueError(description="Invalid email passed in")
        if len(password) < 6:
            raise ValueError(description="Password less than 6 character")
        user = searchUserByEmail(email)
        if hashPassword(password) != user['password']:
            raise ValueError(description="Invalid password")
        return function(user, password)
    return wrapper

def auth_register_argument_valid(function):
    def wrapper(email=None, password=None, name_first=None, name_last=None):
        if isValidEmail(email) is False:
            raise ValueError(description="Invalid email passed in")
        if checkEmailExist(email) is True:
            raise ValueError(description="Email already used")
        if len(password) < 6:
            raise ValueError(description="Password less than 6 character")
        if(len(name_first) > 50 or len(name_first) < 1 or
           len(name_last) > 50 or len(name_last) < 1):
            raise ValueError(description="First or last name is not between 1 to 50 characters inclusive")
        return function(email, password, name_first, name_last)
    return wrapper

def valid_password(function):
    def wrapper(reset_code=None, new_password=None):
        if len(new_password) < 6:
            raise ValueError(description="Password less than 6 character")
        return function(reset_code, new_password)
    return wrapper

#Auth functions             
def auth_logout(uToken):
    SECRET = getSECRET()
    try:
        tokenPayload = decodeToken(uToken)
        user = searchUserByEmail(tokenPayload['email'])
        if uToken in user['tokens']:
            user['tokens'].remove(uToken)
            save()
            return {'is_success' : True}
        return {'is_success' : False}
    except:
        raise AccessError(description="Invalid token passed in")


@auth_login_argument_valid
def auth_login(user, uPassword):   
    newToken = encodeToken({'email' : user['email'], 'timestamp' : time.time()})
    user['tokens'].append(newToken)
    save()
    return {'u_id' : user['u_id'], 'token' : newToken}

@auth_register_argument_valid
def auth_register(uEmail, uPassword, uFirstName, uLastName):
    usersList = getUsersList()
    isFirst = False
    newHandle = createHandle(uFirstName, uLastName)
    newU_ID = createU_ID()
    newToken = encodeToken({'email' : uEmail, 'timestamp' : time.time()})
    #profile_img_url to the default avatar a new user got
    try: 
        avatarPath = request.host_url + 'imgurl/' + 'firstAvatar.jpg'
    except:
        avatarPath = None
    if len(usersList['users']) == 0:
    #if this is the first user to sign up
        isFirst = True
    usersList['users'].append({'email' : uEmail, 
                               'password' : hashPassword(uPassword),
                               'name_first' : uFirstName,
                               'name_last' : uLastName,
                               'handle' : newHandle,
                               'u_id' : newU_ID,
                               'tokens' : [newToken],
                               'joinedChannel_id' : [],
                               'permission_id' : 3,
                               'profile_img_url': avatarPath
                              })
    if isFirst == True:
        usersList['users'][0]['permission_id'] = 1
    save()
    #using user's email and current time to create a secret token    
    return {'u_id' : newU_ID, 'token' : newToken}

@valid_password
def auth_passwordreset_reset(resetCode, newPassword):
    #I assume resetCode contain an int
    resetCodes = getResetCodes()
    for i in range(len(resetCodes)):
        if resetCodes[i]['resetCode'] == resetCode:
            user = searchUserByEmail(resetCodes[i]['email'])
            user['password'] = hashPassword(newPassword)
            resetCodes.remove(resetCodes[i])
            save()
            return {}
    raise ValueError(description="Invalid reset code")

