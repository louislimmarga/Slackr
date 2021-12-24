import os
import pickle
from werkzeug.exceptions import HTTPException
from json import dumps
from flask_cors import CORS
from flask_mail import Mail, Message
from flask import Flask, request, send_from_directory

#the data structure we are using for the whole project
usersList = {'users' : []}
channelsList = []
channelsMessages = []
resetCodes = []
unusedMessageID = 1
channelsTimer = [] 
usersImageNames = []

if os.path.exists('usersData.p'):
    usersList = pickle.load(open('usersData.p', 'rb'))
if os.path.exists('channelsData.p'):
    channelsList = pickle.load(open('channelsData.p', 'rb'))
if os.path.exists('resetCodes.p'):
    resetCodes = pickle.load(open('resetCodes.p', 'rb'))    
if os.path.exists('channelsMessages.p'):
    channelsMessages = pickle.load(open('channelsMessages.p', 'rb'))
if os.path.exists('unusedMessageID.p'):
    unusedMessageID = pickle.load(open('unusedMessageID.p', 'rb'))
if os.path.exists('channelsTimer.p'):
    channelsTimer = pickle.load(open('channelsTimer.p', 'rb'))
if os.path.exists('usersImageNames.p'):
    usersImageNames = pickle.load(open('usersImageNames.p', 'rb'))

SECRET = 'little Auth.py'

#Database utilisation function
def save():
    global usersList
    global channelsList
    global resetCodes
    global channelsMessages
    global unusedMessageID
    global channelsTimer
    global usersImageNames
    with open('usersData.p', 'wb') as FILE:
        pickle.dump(usersList, FILE)
    with open('channelsData.p', 'wb') as FILE:
        pickle.dump(channelsList, FILE)
    with open('resetCodes.p', 'wb') as FILE:
        pickle.dump(resetCodes, FILE)
    with open('channelsMessages.p', 'wb') as FILE:
        pickle.dump(channelsMessages, FILE)  
    with open('unusedMessageID.p', 'wb') as FILE:
        pickle.dump(unusedMessageID, FILE)
    with open('channelsTimer.p', 'wb') as FILE:
        pickle.dump(channelsTimer, FILE)
    with open('usersImageNames.p', 'wb') as FILE:
        pickle.dump(usersImageNames, FILE)
    
#Error functions handle
def defaultHandler(err):
    response = err.get_response()
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response
    
#Redefining ValueError to be in HTTP format
class ValueError(HTTPException):
    code = 400
    message = "No message specified"
 
def createMessageID():
    global unusedMessageID
    newMessageID = unusedMessageID
    unusedMessageID += 1
    return newMessageID 
 
def getUsersList():
    global usersList
    return usersList
def getChannelsList():
    global channelsList
    return channelsList
def getChannelsMessages():
    global channelsMessages
    return channelsMessages
def getResetCodes():
    global resetCodes
    return resetCodes
def getChannelsTimer():
    global channelsTimer
    return channelsTimer
def getUsersImageNames():
    global usersImageNames
    return usersImageNames
def getSECRET():
    global SECRET
    return SECRET
    
def reset_data():
    global usersList
    global channelsList
    global resetCodes
    global channelsMessages
    global unusedMessageID
    global channelsTimer
    global usersImageNames
    usersList = {'users' : []}
    channelsList = []
    channelsMessages = []
    resetCodes = []
    unusedMessageID = 1
    channelsTimer = [] 
    usersImageNames = []
