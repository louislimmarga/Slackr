"""Flask server"""
import re
import time
import hashlib
import jwt
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

usersList = {'users' : []}
channelsList = []
SECRET = 'little Auth.py'
'''CLASSES BELOW'''
class ValueError(HTTPException):
    code = 400
    message = "No message specified"
'''========'''
'''CHANNEL HELPER FUNCTIONS BELOW '''
def createChannel_ID():
    global channelsList
    newID = randint(100000,199999)
    #The loop is to make sure no users have the same u_id
    #NOTE: guaranteed to be infinite loop if number of channel > 99999
    for i in range(len(channelsList)):
        if(newID == channelsList[i]['channel_id']):
            newID = randint(100000,199999)
            i = 0
    return newID

def searchChannelByID(channel_id):
    global channelsList
    for channel in channelsList:
        if(channel['channel_id'] == channel_id):
            return channel
    return None
'''MESSAGE HELPER FUNCTIONS BELOW'''
def decodeToken(token):
    try:
        return jwt.decode(token.encode('utf-8'),SECRET,algorithm='HS256')
    except:
        raise AccessError(description = "Invalid token passed in")



'''AUTH HELPER FUNCTIONS BELOW'''
def getUsersList():
    global usersList
    return usersList
    
def isValidEmail(email):  
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if(re.search(regex,email)):  
        return True 
    else:  
        return False
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

def encodeToken(dictionary):
    global SECRET
    return jwt.encode(dictionary, SECRET, algorithm='HS256').decode('utf-8')
    
def searchUserByEmail(email):
    usersList = getUsersList()
    for user in usersList['users']:
        if(user['email'] == email):
            return user
    return None

def searchUserByID(uID):
    usersList = getUsersList()
    for user in usersList['users']:
        if(user['u_id'] == uID):
            return user
    return None
        
'''======='''

'''DO AUTH FUNCTIONS BELOW'''
@APP.route('/auth/logout', methods=['POST'])
def auth_logout():
    uToken = request.form.get('token')
    try:
        tokenPayload = jwt.decode(uToken.encode('utf-8'), SECRET, algorithms=['HS256'])
        user = searchUserByEmail(tokenPayload['email'])
        if(uToken in user['tokens']):
            user['tokens'].remove(uToken)
            print(user)
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
    print(user)
    return dumps({'u_id' : user['u_id'], 'token' : newToken})
    
@APP.route('/auth/register', methods=['POST'])
def auth_register():
    usersList = getUsersList()
    uEmail = request.form.get('email')
    uPassword = request.form.get('password')
    uFirstName = request.form.get('name_first')
    uLastName = request.form.get('name_last')
    print(uEmail,uPassword,uFirstName,uLastName)
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
    print("It is not able to encode token")
    newToken = encodeToken({'email' : uEmail, 'timestamp' : time.time()})
    print("It actually able to encode token")
    print(newToken)
    usersList['users'].append({'email' : uEmail, 
                               'password' : hashPassword(uPassword),
                               'handle' : newHandle,
                               'u_id' : newU_ID,
                               'tokens' : [newToken],
                               'joinedChannel_id' : []})
    #using user's email and current time to create a secret token    
    return dumps({'u_id' : newU_ID, 'token' : newToken})

'''CHANNEL FUNCTIONS BELOW'''
@APP.route('/channel/invite', methods=['POST'])
def channel_invite():
    uToken = request.form.get('token')
    currChannelID = int(request.form.get('channel_id'))
    invitedUserID = int(request.form.get('u_id'))
    invitingUserInfo = decodeToken(uToken)
    invitingUserInfo = searchUserByEmail(invitingUserInfo['email'])
    if currChannelID not in invitingUserInfo['joinedChannel_id']:
        raise ValueError(description = "Inviting user is not a part of channel_id passed in")
    invitedUserInfo = searchUserByID(invitedUserID)
    if(invitedUserInfo == None):
        raise ValueError(description = "u_id does not refer to valid user")
    currChannelInfo = searchChannelByID(currChannelID)
    if(invitedUserID in currChannelInfo['members_id']):
        raise ValueError(description = "Inviting an already member of the channel")
    currChannelInfo['members_id'].append(invitedUserID)
    invitedUserInfo['joinedChannel_id'].append(currChannelID)
    return dumps({})
    
@APP.route('/channel/details', methods=['GET'])
def channel_details():
    pass  

@APP.route('/channel/messages', methods=['GET'])
def channel_messages():
    pass  
    
@APP.route('/channel/leave', methods=['POST'])
def channel_leave():
    pass 

@APP.route('/channel/join', methods=['POST'])
def channel_join():
    pass 

@APP.route('/channel/addowner', methods=['POST'])
def channel_addowner():
    pass 
    
@APP.route('/channel/removeowner', methods=['POST'])
def channel_removeowner():
    pass     

@APP.route('/channels/list', methods=['GET'])
def channels_list():
    global channelsList
    uToken = request.args.get('token')
    userInfo = decodeToken(uToken)
    userInfo = searchUserByEmail(userInfo['email'])
    if(uToken not in userInfo['tokens']):
        raise AccessError(description = "Invalid token passed in")
    userJoinedChannel = {'channels' : []}
    for joinedChannel_id in userInfo['joinedChannel_id']:
        for channel in channelsList:
            if(channel['channel_id'] == joinedChannel_id):
                userJoinedChannel['channels'].append({'channel_id' : joinedChannel_id,
                                                      'name' : channel['name']})
                break
    return dumps(userJoinedChannel)
    
 
@APP.route('/channels/listall', methods=['GET'])
def channels_listall():
    global channelsList
    uToken = request.args.get('token')
    userInfo = decodeToken(uToken)
    userInfo = searchUserByEmail(userInfo['email'])
    if(uToken not in userInfo['tokens']):
        raise AccessError(description = "Invalid token passed in")
    allChannel = {'channels' : []}
    for channel in channelsList:
        if(channel['isPublic'] == True or any(joinedChannelID == channel['channel_id'] for joinedChannelID in userInfo['joinedChannel_id'])):
            allChannel['channels'].append({'channel_id': channel['channel_id'],
                                           'name' : channel['name']})
        
    return dumps(allChannel)

@APP.route('/channels/create', methods=['POST'])
def channels_create():
    global channelsList
    uToken = request.form.get('token')
    channelName = request.form.get('name')
    isPublic = request.form.get('is_public')
    userInfo = decodeToken(uToken)
    userInfo = searchUserByEmail(userInfo['email'])
    if(uToken not in userInfo['tokens']):
        raise AccessError(description = "Invalid token passed in")
    if(len(channelName) > 20):
        raise ValueError(description = "Name is more than 20 characters")
    newChannelID = createChannel_ID()
    #stores the channel_id the user joined in their user info
    #reducing time complexities from O(n*m) to O(n) where n is number
    #of channel and m is number of user in the channel
    userInfo['joinedChannel_id'].append(newChannelID)
    channelsList.append({'channel_id' : newChannelID,
                         'name' : channelName,
                         'owners_id' : [userInfo['u_id']],
                         'members_id' : [userInfo['u_id']]})
    #NOTE: be aware that we do not know whether isPublic here is
    if(isPublic == 'True'):
        channelsList[len(channelsList)-1]['isPublic'] = True
    else:
        channelsList[len(channelsList)-1]['isPublic'] = False
        
    return dumps({'channel_id' : newChannelID})
         
if __name__ == '__main__':
    APP.run(port=6666)
