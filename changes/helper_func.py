import string
import hashlib
import io
import os
import re
import threading
import time
import datetime
import jwt
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
from changes.data_backend import getUsersList, getChannelsList, getChannelsMessages, getResetCodes, getChannelsTimer, getUsersImageNames, getSECRET, save, ValueError

#Message helper functions
        
def searchChannelByMessageID(message_id):
    channelsMessages = getChannelsMessages()
    for channel in channelsMessages:
        for message in channel['messages']:
            if message_id == message['message_id']:
                return channel
    raise ValueError(description="message_id no longer exists")

def searchMessageInChannel(channel, message_id):
    for message in channel['messages']:
        if message_id == message['message_id']:
            return message
    
def timeMessageSendlater(currChannelMessages, messageDetail):
    currChannelMessages['messages'].insert(0, messageDetail)
    save()
    return
    
#Channel helper functions
def createChannel_ID():
    channelsList = getChannelsList()
    newID = randint(100000, 199999)
    #The loop is to make sure no users have the same u_id
    #NOTE: guaranteed to be infinite loop if number of channel > 99999
    for i in range(len(channelsList)):
        if newID == channelsList[i]['channel_id']:
            newID = randint(100000, 199999)
            i = 0
    return newID

def searchChannelByID(channel_id):
    channelsList = getChannelsList()
    for channel in channelsList:
        if channel['channel_id'] == channel_id:
            return channel
    raise ValueError(description="Invalid channel_id passed in")
    
def decodeToken(token):
    SECRET = getSECRET()
    try:
        return jwt.decode(token.encode('utf-8'), SECRET, algorithm='HS256')
    except:
        raise AccessError(description="Invalid token passed in")

def searchUserByID(uID):
    usersList = getUsersList()
    for user in usersList['users']:
        if user['u_id'] == uID:
            return user
    return None
    
def checkUserLoggedIn(token, user):
    if token not in user['tokens']:
        raise AccessError(description="Authorised user is not logged in")
    return None

def joinUserToChannel(channel, user):
    channel['members_id'].append(user['u_id'])
    user['joinedChannel_id'].append(channel['channel_id'])
    
def leaveUserToChannel(channel, user):
    channel['members_id'].remove(user['u_id'])
    user['joinedChannel_id'].remove(channel['channel_id'])
    if user['u_id'] in channel['owners_id']:
        channel['owners_id'].remove(user['u_id'])

def searchChannelInChannelsMessages(channel_id):
    channelsMessages = getChannelsMessages()
    for channel in channelsMessages:
        if channel['channel_id'] == channel_id:
            return channel
    raise ValueError(description="Invalid channel_id passed in")

#Auth helper functions

def checkEmailExist(email):
    usersList = getUsersList()
    if any((user['email'] == email) for user in usersList['users']):
        return True
    return False
  
def isValidEmail(email):  
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if re.search(regex, email):  
        return True 
    return False
    
def hashPassword(password):
    return hashlib.sha256(password.encode()).hexdigest()
    
def createHandle(firstName, lastName):
    usersList = getUsersList()
    newHandle = firstName.lower() + lastName.lower()
    if len(newHandle) <= 20:
        #The loop would add a random integer to the user handle if
        #it has been used by other user
        for i in range(len(usersList['users'])):
            if newHandle == usersList['users'][i]['handle']:
                newHandle = newHandle + str(i)
                i = 0
    if len(newHandle) > 20:
        #cut the character to 17 characters
        newHandle = newHandle[0:17]
        newHandle = newHandle + str(randint(0, 999))
        for i in range(len(usersList['users'])):
            if newHandle == usersList['users'][i]['handle']:
                newHandle = newHandle[0:17]
                newHandle = newHandle + str(randint(0, 999))
                i = 0
    return newHandle
    
def createU_ID():
    usersList = getUsersList()
    newU_ID = randint(1, 10000)
    #The loop is to make sure no users have the same u_id
    #NOTE: guaranteed to be infinite loop if number of user > 10000
    for i in range(len(usersList['users'])):
        if newU_ID == usersList['users'][i]['u_id']:
            newU_ID = randint(1, 10000)
            i = 0
    return newU_ID

def encodeToken(dictionary):
    SECRET = getSECRET()
    return jwt.encode(dictionary, SECRET, algorithm='HS256').decode('utf-8')
    
def searchUserByEmail(email):
    usersList = getUsersList()
    for user in usersList['users']:
        if user['email'] == email:
            return user
    raise ValueError(description="Email does not exist")
    
#User helper functions
def checkHandleExist(handle_str):
    usersList = getUsersList()
    if any((user['handle'] == handle_str) for user in usersList['users']):
        return True
    return False

def checkUIdValid(u_id):
    usersList = getUsersList()
    
    for user in usersList['users']:
        num_u_id = int(user['u_id'])
        u_id = int(u_id)
        if num_u_id == u_id:
            return True
    return False

def getsizes(url):
    # get file size *and* image size (None if not known)
    myFile = urllib.request.urlopen(url)
    size = myFile.headers.get("content-length")
    if size: 
        size = int(size)
    p = ImageFile.Parser()
    while True:
        data = myFile.read(1024)
        if not data:
            break
        p.feed(data)
        if p.image:
            return (size, p.image.size)
            break
    myFile.close()
    return(size, None)
    
def removeSpecialCharacter(string):
    #removes every special character e.g /, #, + except .
    return ''.join(e for e in string if e == '.' or e.isalnum())
    
def createImageName(initialName):
    usersImageNames = getUsersImageNames()
    nameExist = True
    finalName = initialName
    finalName = removeSpecialCharacter(finalName)
    while nameExist == True:
        if finalName not in usersImageNames:
            nameExist = False
        else:
            finalName = str(randint(0, 99)) + finalName
    usersImageNames.append(finalName)
    return finalName
  
#Standup helper fucntions

def searchChannelInChannelsTimer(channel_id):
    channelsTimer = getChannelsTimer()
    for channel in channelsTimer:
        if channel['channel_id'] == channel_id:
            return channel

def startTimer(currChannelTimer, lengthOfStandup, newMessageID):
    currChannelTimer['isTimerStarted'] = True
    currChannelTimer['timeFinishes'] = datetime.datetime.now() + datetime.timedelta(seconds=lengthOfStandup)
    myTimer = threading.Timer(lengthOfStandup, stopStandup, args=[currChannelTimer, newMessageID])
    myTimer.start()
    save()
    return
    
def stopStandup(currChannelTimer, newMessageID):
    nMessage = len(currChannelTimer['messageQueue'])
    messagePackage = ""
    currChannelTimer['isTimerStarted'] = False
    frontOfList = 0
    del currChannelTimer['timeFinishes']
    for i in range(nMessage-1, -1, -1):
        currHandle = currChannelTimer['messageQueue'][i]['handle']
        currMessage = currChannelTimer['messageQueue'][i]['message']
        messagePackage = messagePackage + f"{currHandle}: {currMessage}"
        #bottom code prevent 2 newline on the end of the messagePackage
        #when it is displayed on front end
        if i != 0:
            messagePackage = messagePackage + "\n"
    
    currChannelMessages = searchChannelInChannelsMessages(currChannelTimer['channel_id'])
    standupStarterID = currChannelTimer['starterID']
    timeCreated = datetime.datetime.now()
    timeSinceEpoch = timeCreated.timestamp()
    reacts = [{'react_id' : 1,
               'u_ids' : []}]
    messageDetail = {'message_id' : newMessageID,
                     'u_id' : standupStarterID,
                     'message' : messagePackage,
                     'time_created' : timeSinceEpoch,
                     'reacts' : reacts,
                     'is_pinned' : False}
    #ensure latest message at the front of the list
    currChannelMessages['messages'].insert(frontOfList, messageDetail)
    #clear the 'messageQueue' and 'starterID'
    currChannelTimer['messageQueue'].clear()
    del currChannelTimer['starterID']
    save()
    return
