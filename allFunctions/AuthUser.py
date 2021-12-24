import hashlib
import jwt
import os
import pickle
import re
import time
from Error import AccessError
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mail import Mail, Message
from json import dumps
from random import randint
from werkzeug.exceptions import HTTPException

'''Error function handle'''
def defaultHandler(err):
    response = err.get_response()
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

'''======'''

APP = Flask(__name__)
APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)
CORS(APP)
'''FLASK SENDING EMAIL SETUP'''
APP.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = 'W17A.TeamJin@gmail.com',
    MAIL_PASSWORD = "123JinJan456"
)
'''========'''

# Intialization
usersList = {
    'users' : [],
}
if (os.path.exists('usersData.p')):
    usersList = pickle.load(open('usersData.p', 'rb'))

SECRET = 'little Auth.py'

# Helper functions
############################### Taken from auth.py #########################################
def getUsersList():
    global usersList
    return usersList

def isValidEmail(email):  
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if(re.search(regex,email)):  
        return True 
    else:  
        return False

def checkEmailExist(email):
    usersList = getUsersList()
    if(any((user['email'] == email) for user in usersList['users'])):
        return True
    return False

def encodeToken(dictionary):
    global SECRET
    return jwt.encode(dictionary, SECRET, algorithm='HS256').decode('utf-8')

def decodeToken(token):
    try:
        return jwt.decode(token.encode('utf-8'),SECRET,algorithm='HS256')
    except:
        raise AccessError(description = "Invalid token passed in")

def checkUserLoggedIn(token,user):
    if(token not in user['tokens']):
        raise AccessError(description = "Authorised user is not logged in")
    return

def searchUserByEmail(email):
    usersList = getUsersList()
    for user in usersList['users']:
        if(user['email'] == email):
            return user
    raise ValueError(description = "Email does not exist")


def save():
    global usersList
    with open("usersData.p", "wb") as FILE:
        pickle.dump(usersList, FILE)
    
def hashPassword(password):
    return hashlib.sha256(password.encode()).hexdigest()
    
def createHandle(firstName,lastName):
    usersList = getUsersList()
    newHandle = firstName.lower() + lastName.lower()
    #The loop would add a random integer to the user handle if
    #it has been used by other user
    for i in range(len(usersList['users'])):
        if(newHandle == usersList['users'][i]['handle']):
            newHandle = newHandle + str(i)
            i = 0
    return newHandle
    
def createU_ID():
    usersList = getUsersList()
    newU_ID = randint(1,10000)
    #The loop is to make sure no users have the same u_id
    #NOTE: guaranteed to be infinite loop if number of user > 10000
    for i in range(len(usersList['users'])):
        if(newU_ID == usersList['users'][i]['u_id']):
            newU_ID = randint(1,10000)
            i = 0
    return newU_ID
###########################################################################
def checkHandleExist(handle_str):
    usersList = getUsersList()
    if any((user['handle'] == handle_str) for user in usersList['users']):
        return True
    return False

def checkToken(token):
    userInfo = decodeToken(token)
    userInfo = searchUserByEmail(userInfo['email'])
    checkUserLoggedIn(token, userInfo)

def checkUIdValid(u_id):
    usersList = getUsersList()
    
    for user in usersList['users']:
        num_u_id = int(user['u_id'])
        u_id = int(u_id)
        if num_u_id == u_id:
            return True
    return False

def searchUserByUId(u_id):
    usersList = getUsersList()
    for user in usersList['users']:
        if(user['u_id'] == u_id):
            return user
    raise ValueError(description = "U_ID does not exist")
##########################################################
@APP.route('/auth/logout', methods=['POST'])
def auth_logout():
    uToken = request.form.get('token')
    try:
        tokenPayload = jwt.decode(uToken.encode('utf-8'), SECRET, algorithms=['HS256'])
        user = searchUserByEmail(tokenPayload['email'])
        if(uToken in user['tokens']):
            user['tokens'].remove(uToken)
            save()
            return dumps({'is_success' : True})
        return dumps({'is_success' : False})
    except:
        raise AccessError(description = "Invalid token passed in")

@APP.route('/auth/login', methods=['POST'])
def auth_login():
    usersList = getUsersList()
    uEmail = request.form.get('email')
    uPassword = request.form.get('password')
    if(isValidEmail(uEmail) is False):
        raise ValueError(description = "Invalid email passed in")
    user = searchUserByEmail(uEmail)
    if(user == None):
        raise ValueError(description = "Email does not exist")
    if(hashPassword(uPassword) != user['password']):
        raise ValueError(description = "Invalid password")
    newToken = encodeToken({'email' : user['email'], 'timestamp' : time.time()})
    user['tokens'].append(newToken)
    save()
    return dumps({'u_id' : user['u_id'], 'token' : newToken})
    
@APP.route('/auth/register', methods=['POST'])
def auth_register():
    usersList = getUsersList()
    uEmail = request.form.get('email')
    uPassword = request.form.get('password')
    uFirstName = request.form.get('name_first')
    uLastName = request.form.get('name_last')
    isFirst = False
    if(isValidEmail(uEmail) is False):
        raise ValueError(description = "Invalid email passed in")

    for user in usersList['users']:
        if(user['email'] == uEmail):
            raise ValueError(description = "Email already used")

    if(len(uPassword) < 6):
        raise ValueError(description = "Password less than 6 character")

    if(len(uFirstName) > 50 or len(uFirstName) < 1 
        or len(uLastName) > 50 or len(uLastName) < 1):
        raise ValueError(description = "First or last name is not between 1 to 50 characters inclusive")
    newHandle = createHandle(uFirstName,uLastName)
    newU_ID = createU_ID()
    newToken = encodeToken({'email' : uEmail, 'timestamp' : time.time()})
    if(len(usersList['users']) == 0):
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
                               'permission_id' : 3
                               })
    if(isFirst == True):
        usersList['users'][0]['permission_id'] = 1
    save()
    #using user's email and current time to create a secret token    
    return dumps({'u_id' : newU_ID, 'token' : newToken})
##########################################################
# Functions
@APP.route('/user/profile', methods=['GET'])
def user_profile():
    uToken = request.args.get('token')
    userInfo = decodeToken(uToken)
    userInfo = searchUserByEmail(userInfo['email'])
    u_id = request.args.get('u_id')
    
    checkUserLoggedIn(uToken,userInfo)
    if checkUIdValid(u_id) == False:
        raise ValueError("User with u_id is not a valid user")

    for user in usersList['users']:
        if user['email'] == userInfo['email']:
            save()
            return dumps(user['email'] + "\n" + user['name_first'] + "\n" + user['name_last'] + "\n" + user['handle'])


@APP.route('/user/profile/setname', methods=['PUT'])
def user_profile_setname():
    uToken = request.form.get('token')
    checkToken(uToken)
    
    userInfo = decodeToken(uToken)
    userInfo = searchUserByEmail(userInfo['email'])

    user_first_name = request.form.get('name_first')
    user_last_name = request.form.get('name_last')

    if len(user_first_name) > 50 or len(user_first_name) < 1:
        raise ValueError("First name is not between 1 and 50 characters in length")
    if len(user_last_name) > 50 or len(user_last_name) < 1:
        raise ValueError("Last name is not between 1 and 50 characters in length")
        
    for user in usersList['users']:
        if user['email'] == userInfo['email']:
            save()
            user['name_first'] = user_first_name
            user['name_last'] = user_last_name

    return dumps({})

@APP.route('/user/profile/setemail', methods=['PUT'])
def user_profile_setemail():
    uToken = request.form.get('token')
    checkToken(uToken)

    userInfo = decodeToken(uToken)
    userInfo = searchUserByEmail(userInfo['email'])

    email = request.form.get('email')

    if isValidEmail(email) == False:
        raise ValueError ("Invalid email.")

    if checkEmailExist(email) == True:
        raise ValueError ("Email address is already used.")

    for user in usersList['users']:
        if user['email'] == userInfo['email']:
            save()
            user['email'] = email

    return dumps({})

@APP.route('/user/profile/sethandle', methods=['PUT'])
def user_profile_sethandle():
    uToken = request.form.get('token')
    checkToken(uToken)

    userInfo = decodeToken(uToken)
    userInfo = searchUserByEmail(userInfo['email'])

    user_handle = request.form.get('handle')

    if len(user_handle) > 20 or len(user_handle) < 3:
        raise ValueError("handle_str must be between 3 and 20.")

    if checkHandleExist(user_handle) == True:
        raise ValueError("handle is already used.")

    for user in usersList['users']:
        if user['email'] == userInfo['email']:
            save()
            user['handle'] = user_handle

    return dumps({})
    

#@APP.route('user/profiles/uploadphoto', methods=['POST'])
#def user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):

if __name__ == '__main__':
    APP.run(port=7823)
