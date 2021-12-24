"""Flask server"""

import hashlib
import jwt
import os
import pickle
import re
import sys
import time
import datetime 
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


usersList = {'users' : []}
channelsList = []
channelsMessages = []
resetCodes = []
if(os.path.exists('usersData.p')):
    usersList = pickle.load(open('usersData.p','rb'))

if(os.path.exists('channelsData.p')):
    channelsList = pickle.load(open('channelsData.p','rb'))

if(os.path.exists('resetCodes.p')):
    resetCodes = pickle.load(open('resetCodes.p','rb'))

SECRET = 'little Auth.py'

'''DATABASE UTILISATION FUNCTIONS'''
def save():
    global usersList
    global channelsList
    global resetCodes
    with open('usersData.p','wb') as FILE:
        pickle.dump(usersList, FILE)
    with open('channelsData.p','wb') as FILE:
        pickle.dump(channelsList,FILE)
    with open('resetCodes.p', 'wb') as FILE:
        pickle.dump(resetCodes,FILE)
    
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
    raise ValueError(description = "Invalid channel_id passed in")
    
def decodeToken(token):
    try:
        return jwt.decode(token.encode('utf-8'),SECRET,algorithm='HS256')
    except:
        raise AccessError(description = "Invalid token passed in")

def searchUserByID(uID):
    usersList = getUsersList()
    for user in usersList['users']:
        if(user['u_id'] == uID):
            return user
    return None
    
def checkUserLoggedIn(token,user):
    if(token not in user['tokens']):
        raise AccessError(description = "Authorised user is not logged in")
    return

def joinUserToChannel(channel,user):
    channel['members_id'].append(user['u_id'])
    user['joinedChannel_id'].append(channel['channel_id'])
    
def leaveUserToChannel(channel,user):
    channel['members_id'].remove(user['u_id'])
    user['joinedChannel_id'].remove(channel['channel_id'])
    if(user['u_id'] in channel['owners_id']):
        channel['owners_id'].remove(user['u_id'])

def searchChannelInChannelsMessages(channel_id):
    global channelsMessages
    for channel in channelsMessages:
        if(channel['channel_id'] == channel_id):
            return channel
    raise ValueError(description = "Invalid channel_id passed in")
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
    raise ValueError(description = "Email does not exist")
 
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


@APP.route('/auth/passwordreset/request', methods=['POST'])
def auth_passwordreset_request():
    global resetCodes
    userEmail = request.form.get('email')
    user = searchUserByEmail(userEmail)
    if(user == None):
        raise ValueError(description = "Email does not exist")
    mail = Mail(APP)
    #ensures that the new resetCode is unique
    newResetCode = randint(10000,99999)
    for i in range(len(resetCodes)):
            if(resetCodes[i]['resetCode'] == newResetCode):
                newResetCode = randint(10000,99999)
                i = 0
    try:
        msg = Message("Your reset code for the slackr product",
            sender="W17A.TeamJin@gmail.com",
            recipients=[userEmail])
        msg.body = f"Dear our valued user,\n\nYour reset code is {newResetCode}.\n\nThank you."
        mail.send(msg)
        #bottom line of code ensure a user can only have
        #one reset code at a time
        userExist = False
        for i in range(len(resetCodes)):
            if(resetCodes[i]['email'] == userEmail):
                userExist = True
                resetCodes[i]['resetCode'] = newResetCode
        if(userExist == False):
            resetCodes.append({'email' : userEmail, 'resetCode' : newResetCode})
        save()
        return dumps({})
    except:
        raise ValueError(description = "Unable to send email to the user")

@APP.route('/auth/passwordreset/reset', methods=['POST'])
def auth_passwordreset_reset():
    #I assume resetCode contain an int
    global resetCodes
    resetCode = request.form.get('reset_code')
    newPassword = request.form.get('new_password')
    resetCode = int(resetCode)
    if(len(newPassword) < 6):
        raise ValueError(description = "Password less than 6 character")
        
    for i in range(len(resetCodes)):
        if(resetCodes[i]['resetCode'] == resetCode):
            user = searchUserByEmail(resetCodes[i]['email'])
            user['password'] = hashPassword(newPassword)
            resetCodes.remove(resetCodes[i])
            save()
            return dumps({})
    raise ValueError(description = "Invalid reset code")

'''CHANNEL FUNCTIONS BELOW'''
@APP.route('/channel/invite', methods=['POST'])
def channel_invite():
    uToken = request.form.get('token')
    currChannelID = int(request.form.get('channel_id'))
    invitedUserID = int(request.form.get('u_id'))
    invitingUserInfo = decodeToken(uToken)
    invitingUserInfo = searchUserByEmail(invitingUserInfo['email'])
    checkUserLoggedIn(uToken,invitingUserInfo)
    if(currChannelID not in invitingUserInfo['joinedChannel_id']):
        raise ValueError(description = "Inviting user is not a part of channel_id passed in")
    invitedUserInfo = searchUserByID(invitedUserID)
    if(invitedUserInfo == None):
        raise ValueError(description = "u_id does not refer to valid user")
    currChannelInfo = searchChannelByID(currChannelID)
    if(invitedUserID in currChannelInfo['members_id']):
        raise ValueError(description = "Inviting an already member of the channel")
    joinUserToChannel(currChannelInfo,invitedUserInfo)
    save()
    return dumps({})
    
@APP.route('/channel/details', methods=['GET'])
def channel_details():
    uToken = request.args.get('token')
    currChannelID = int(request.args.get('channel_id'))
    userInfo = decodeToken(uToken)
    userInfo = searchUserByEmail(userInfo['email'])
    checkUserLoggedIn(uToken,userInfo)
    currChannelInfo = searchChannelByID(currChannelID)
    if(currChannelID not in userInfo['joinedChannel_id']):
        raise ValueError("User does not belong to the channel")
    #I initially assume owner_members and all_members can't overlap
    channelDetail = {'name' : currChannelInfo['name'],
                     'owner_members' : [],
                     'all_members' : []}
    for user_id in currChannelInfo['owners_id']:
        currUser = searchUserByID(user_id)
        currUserDetail = {'u_id' : user_id,
                          'name_first' : currUser['name_first'],
                          'name_last' : currUser['name_last']}
        channelDetail['owner_members'].append(currUserDetail)
    for user_id in currChannelInfo['members_id']:
        currUser = searchUserByID(user_id)
        currUserDetail = {'u_id' : user_id,
                          'name_first' : currUser['name_first'],
                          'name_last' : currUser['name_last']}
        #Bottom codes preventing overlapping between owner_members and
        #all_members
        if(currUserDetail not in channelDetail['owner_members']):
            channelDetail['all_members'].append(currUserDetail)
    return dumps(channelDetail)
            
@APP.route('/channel/messages', methods=['GET'])
def channel_messages():
    uToken = request.args.get('token')
    currChannelID = int(request.args.get('channel_id'))
    startIndex = int(request.args.get('start'))
    userInfo = decodeToken(uToken)
    userInfo = searchUserByEmail(userInfo['email'])
    checkUserLoggedIn(uToken,userInfo)
    currChannelMessagesInfo = searchChannelInChannelsMessages(currChannelID)
    if(currChannelID not in userInfo['joinedChannel_id']):
        raise ValueError(description = "User is not in the channel")
    totalNumMessages = len(currChannelInfo['messages'])
    if(startIndex >= totalNumMessages):
        raise ValueError(description = "There is no more message to be shown")
    #i want to know when does a startIndex return an out of bound messages from
    #the channel
    #note if totalNumMessages  = 51, end would correspond to 50 if startIndex = 0
    #so basically, channel/messages return 51 message each time
    end = startIndex + 50
    endIndex = end
    if(startIndex + 50 + 1 > totalNumMessages):
        end = -1
        endIndex = totalNumMessages - 1
    #end index would adapt to whether it want to loop through everything from start
    #to start+50 or from start to the end of the list (in case start+50 is out of bound)
    i = startIndex
    messagesToReturn = {'messages' : [], 'start' : startIndex, 'end' : end}
    while(i <= endIndex):
        messagesToReturn['messages'].append(currChannelMessagesInfo['messages'][i])
        i = i + 1
    return dumps(messagesToReturn)
    
@APP.route('/channel/leave', methods=['POST'])
def channel_leave():
    uToken = request.form.get('token')
    currChannelID = int(request.form.get('channel_id'))
    userInfo = decodeToken(uToken)
    userInfo = searchUserByEmail(userInfo['email'])
    checkUserLoggedIn(uToken,userInfo)
    currChannelInfo = searchChannelByID(currChannelID)
    if(currChannelID not in userInfo['joinedChannel_id']):
        raise ValueError(description = "User leaving a not joined channel")
    leaveUserToChannel(currChannelInfo,userInfo)
    save()
    return dumps({})

@APP.route('/channel/join', methods=['POST'])
def channel_join():
    uToken = request.form.get('token')
    currChannelID = int(request.form.get('channel_id'))
    userInfo = decodeToken(uToken)
    userInfo = searchUserByEmail(userInfo['email'])
    checkUserLoggedIn(uToken,userInfo)
    currChannelInfo = searchChannelByID(currChannelID)
    if(currChannelID in userInfo['joinedChannel_id']):
        raise ValueError(description = "User has previously joined channel_id")
    #up until now, valid user, valid channel, user not belonging to channel.
    #if user is owner/admin of slacker, make user immediately join the channel
    #if not, check whether the channel is private or not
    #if no, then make the user join the channel
    if(userInfo['permission_id'] != 3):
        joinUserToChannel(currChannelInfo,userInfo)
    else:
        if(currChannelInfo['isPublic'] == False):
            raise ValueError(description = "Member of slackr trying to join a private channel")
        joinUserToChannel(currChannelInfo,userInfo)
    save()
    return dumps({})
        
@APP.route('/channel/addowner', methods=['POST'])
def channel_addowner():
    uToken = request.form.get('token')
    currChannelID = int(request.form.get('channel_id'))
    toBeOwnerID = int(request.form.get('u_id'))
    authUser = decodeToken(uToken)
    authUserInfo = searchUserByEmail(authUser['email'])
    checkUserLoggedIn(uToken,authUserInfo)
    currChannelInfo = searchChannelByID(currChannelID)
    #AccessError when "auth user not an owner of the slackr as well as not an owner of this channel"
    if(authUserInfo['permission_id'] == 3 and authUserInfo['u_id'] not in currChannelInfo['owners_id'] ):
        raise AccessError(description = "Authorised user not an owner of slackr and channel")
    #by this time, i can ensure that authUser is an owner of the channel(either being a real
    #channel owner or through being an admin/owner of slackr)
    if(toBeOwnerID not in currChannelInfo['members_id']):
        raise ValueError(description = "Making a non member an owner of the channel")
    if(toBeOwnerID in currChannelInfo['owners_id']):
        raise ValueError(description = "User is already an owner of the channel")
    currChannelInfo['owners_id'].append(toBeOwnerID)
    save()
    return dumps({})
    
    
@APP.route('/channel/removeowner', methods=['POST'])
def channel_removeowner():
    uToken = request.form.get('token')
    currChannelID = int(request.form.get('channel_id'))
    toBeRemovedOwnerID = int(request.form.get('u_id'))
    authUser = decodeToken(uToken)
    authUserInfo = searchUserByEmail(authUser['email'])
    checkUserLoggedIn(uToken,authUserInfo)
    currChannelInfo = searchChannelByID(currChannelID)
    #AccessError when "auth user not an owner of the slackr as well as not an owner of this channel"
    if(authUserInfo['permission_id'] == 3 and authUserInfo['u_id'] not in currChannelInfo['owners_id']):
        raise AccessError(description = "Authorised user not an owner of slackr and channel")
    #by this time, i can ensure that authUser is an owner of the channel(either being a real
    #channel owner or through being an admin/owner of slackr)
    if(toBeRemovedOwnerID not in currChannelInfo['members_id']):
        raise ValueError(description = "Removing the ownership of a non member")
    if(toBeRemovedOwnerID not in currChannelInfo['owners_id']):
        raise ValueError(description = "Removing the ownership of a non-owner")
    currChannelInfo['owners_id'].remove(toBeRemovedOwnerID)
    save()
    return dumps({})

@APP.route('/channels/list', methods=['GET'])
def channels_list():
    global channelsList
    uToken = request.args.get('token')
    userInfo = decodeToken(uToken)
    userInfo = searchUserByEmail(userInfo['email'])
    checkUserLoggedIn(uToken,userInfo)
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
    checkUserLoggedIn(uToken,userInfo)
    allChannel = {'channels' : []}
    for channel in channelsList:
        if(channel['isPublic'] == True or any(joinedChannelID == channel['channel_id'] for joinedChannelID in userInfo['joinedChannel_id'])):
            allChannel['channels'].append({'channel_id': channel['channel_id'],
                                           'name' : channel['name']})
        
    return dumps(allChannel)

@APP.route('/channels/create', methods=['POST'])
def channels_create():
    global channelsList
    global channelsMessages
    uToken = request.form.get('token')
    channelName = request.form.get('name')
    isPublic = request.form.get('is_public')
    userInfo = decodeToken(uToken)
    userInfo = searchUserByEmail(userInfo['email'])
    checkUserLoggedIn(uToken,userInfo)
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
    channelsMessages.append({'channel_id' : newChannelID, 'messages' : []})
    save()
    return dumps({'channel_id' : newChannelID})
         
if __name__ == '__main__':
    APP.run(port=6666)
