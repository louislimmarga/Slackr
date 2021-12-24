import os
import io
import re
import time
import datetime
import urllib.request
import urllib.error
from PIL import Image, ImageFile
from copy import deepcopy
from random import randint, choices
from flask_cors import CORS
from flask_mail import Mail, Message
from flask import Flask, request, send_from_directory
from werkzeug.exceptions import HTTPException
from werkzeug.utils import secure_filename
from changes.Error import AccessError
#new ones
from changes.data_backend import getUsersList, ValueError, save
from changes.helper_func import decodeToken, searchUserByEmail, checkUserLoggedIn, checkUIdValid, isValidEmail, checkEmailExist, checkHandleExist, getsizes, createImageName

def get_userInfo(function):
    def wrapper(uToken=None, *args):
        userInfo = decodeToken(uToken)
        userInfo = searchUserByEmail(userInfo['email'])  
        checkUserLoggedIn(uToken, userInfo)  
        return function(userInfo, *args)
    return wrapper

def check_u_id(function):
    def wrapper(userInfo, u_id=None, *args):
        if checkUIdValid(u_id) == False:
            raise ValueError(description="User with u_id is not a valid user")
        return function(userInfo, u_id, *args)
    return wrapper

def check_name(function):
    def wrapper(userInfo, user_first_name=None, user_last_name=None, *args):
        if len(user_first_name) > 50 or len(user_first_name) < 1:
            raise ValueError(description="First name is not between 1 and 50 characters in length")
        if len(user_last_name) > 50 or len(user_last_name) < 1:
            raise ValueError(description="Last name is not between 1 and 50 characters in length")
        return function(userInfo, user_first_name, user_last_name, *args)
    return wrapper

def check_email(function):
    def wrapper(userInfo, email=None, *args):
        if isValidEmail(email) == False:
            raise ValueError(description="Changing to an invalid email.")
        if checkEmailExist(email) == True:
            raise ValueError(description="Email address is already used.")
        return function(userInfo, email, *args)
    return wrapper

def check_handle(function):
    def wrapper(userInfo, user_handle=None, *args):
        if len(user_handle) > 20 or len(user_handle) < 3:
            raise ValueError(description="handle_str must be between 3 and 20.")
        if checkHandleExist(user_handle) == True:
            raise ValueError(description="handle is already used.")
        return function(userInfo, user_handle, *args)
    return wrapper

@get_userInfo
@check_u_id
def user_profile(userInfo, u_id):
    usersList = getUsersList()
    returnData = {}

    for user in usersList['users']:
        if user['u_id'] == u_id:
            returnData = {'u_id': user['u_id'],
                          'email': user['email'],
                          'name_first': user['name_first'],
                          'name_last': user['name_last'],
                          'handle_str': user['handle'],
                          'profile_img_url': user['profile_img_url']}

    return returnData

@get_userInfo
@check_name
def user_profile_setname(userInfo, user_first_name, user_last_name):
    userInfo['name_first'] = user_first_name
    userInfo['name_last'] = user_last_name
    save()
    return {}

@get_userInfo
@check_email
def user_profile_setemail(userInfo, email):
    userInfo['email'] = email
    #basically logging out every tokens the user previously had
    userInfo['tokens'].clear()
    save()
    return {}

@get_userInfo
@check_handle
def user_profile_sethandle(userInfo, user_handle):
    userInfo['handle'] = user_handle
    save()
    return {}

@get_userInfo
def user_profiles_uploadphoto(userInfo, imgURL, xStart, yStart, xEnd, yEnd):
    formats = {
        'image/jpg': 'JPG',
        'image/jpeg': 'JPEG',
        'image/png': 'PNG',
        'image/gif': 'GIF'
    }
    #see whether urllib.request.(Request/urlopen) need to be closed
    urlRequest = urllib.request.Request(imgURL)
    #checking whether the url exists
    try:
        urlResponse = urllib.request.urlopen(urlRequest)
    except:
        raise ValueError(description="Invalid img_url passed in")
    #checking the HTTP response status code
    if urlResponse.getcode() != 200:
        raise ValueError(description=f"An error code of {response.getcode()} was returned when openning img_url")
    #checking a valid Content-Type of picture
    contentType = urlResponse.info().get('Content-Type')
    try:
        format = formats[contentType]
    except:
        raise ValueError(description="Not a supported image format")
    myBytesStream = io.BytesIO(urlResponse.read())
    img = Image.open(myBytesStream)
    imageSize = getsizes(imgURL)
    if imageSize[1] == None:
        raise ValueError(description="Unable to get the size of the picture")
    xMax, yMax = imageSize[1]
    if xStart < 0 or yStart < 0 or xEnd > xMax or yEnd > yMax or xStart >= xEnd or yStart >= yEnd:
        raise ValueError(description="Cropping outside the dimension of the image")
    #Crop the image according to the dimension specified 
    #and save the image to current directory
    croppedImg = img.crop((xStart, yStart, xEnd, yEnd))
    #createImageName ensures the filename is unique
    #and then store the img_url on the user's usersList
    fileName = createImageName(imgURL.rpartition('/')[-1])
    #Try,except block for pytest to not give error when running this line of code
    #without flask running
    try:
        profileImgURL = request.host_url + 'imgurl/' + fileName
    except:
        profileImgURL = None
        
    userInfo['profile_img_url'] = profileImgURL
    fileName = secure_filename(fileName) 
    croppedImg.save(os.path.join('.', 'pictures', fileName), format=format)
    myBytesStream.close()
    img.close()
    croppedImg.close()
    save()
    return {}
  
def imgurl_function(name):
    imagePath = os.path.join('.', 'pictures', name)
    isExist = os.path.exists(imagePath)
    if not isExist:
        raise ValueError(description="Image does not exist")
    return send_from_directory(directory='pictures', filename=name)

@get_userInfo  
def users_all(userInfo):
    usersList = getUsersList()
    
    returnData = {'users' : []}
    for user in usersList['users']:
        returnData['users'].append({'u_id': user['u_id'],
                                    'email': user['email'],
                                    'name_first': user['name_first'],
                                    'name_last': user['name_last'],
                                    'handle_str': user['handle'],
                                    'profile_img_url': user['profile_img_url']})
    return returnData
    
