# pylint: disable= trailing-whitespace,line-too-long,anomalous-backslash-in-string,too-many-lines,redefined-builtin,invalid-name,global-statement,singleton-comparison,missing-function-docstring,redefined-outer-name,missing-class-docstring,useless-return,consider-using-enumerate
"""Flask server"""
import string
import hashlib
import os
import io
import pickle
import re
import sys
import threading
import time
import datetime
import urllib.request
import urllib.error
from PIL import Image, ImageFile
from copy import deepcopy
from json import dumps
from random import randint, choices
from flask_cors import CORS
from flask_mail import Mail, Message
from flask import Flask, request, send_from_directory
from werkzeug.exceptions import HTTPException
from werkzeug.utils import secure_filename
import jwt
from Error import AccessError
#newly added ones
from changes.data_backend import usersList, channelsList, channelsMessages, resetCodes, unusedMessageID, channelsTimer, usersImageNames, save, defaultHandler, ValueError 
from changes.helper_func import searchUserByEmail
from changes.auth_backend import auth_logout, auth_login, auth_register, auth_passwordreset_reset
from changes.channel_backend import channel_invite, channel_details, channel_messages, channel_leave, channel_join, channel_addowner, channel_addowner, channel_removeowner, channels_list, channels_listall, channels_create
from changes.message_backend import message_sendlater, message_send, message_remove, message_edit, message_react, message_unreact, message_pin, message_unpin
from changes.user_backend import user_profile, user_profile_setemail, user_profile_sethandle, user_profile_setname, user_profiles_uploadphoto, imgurl_function,users_all
from changes.standup_backend import standup_start, standup_active, standup_send
from changes.search_backend import search
from changes.user_permission_change import admin_userpermission_change

APP = Flask(__name__)
APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)
CORS(APP)
#Flask sending email setup
APP.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='W17A.TeamJin@gmail.com',
    MAIL_PASSWORD="123JinJan456"
)

#Auth functions
@APP.route('/auth/logout', methods=['POST'])
def flask_auth_logout():
    uToken = request.form.get('token')
    return dumps(auth_logout(uToken))

@APP.route('/auth/login', methods=['POST'])
def flask_auth_login():
    uEmail = request.form.get('email')
    uPassword = request.form.get('password')
    return dumps(auth_login(uEmail, uPassword))
    
@APP.route('/auth/register', methods=['POST'])
def flask_auth_register():
    uEmail = request.form.get('email')
    uPassword = request.form.get('password')
    uFirstName = request.form.get('name_first')
    uLastName = request.form.get('name_last')  
    return dumps(auth_register(uEmail, uPassword, uFirstName, uLastName))

@APP.route('/auth/passwordreset/request', methods=['POST'])
def flask_auth_passwordreset_request():
    global resetCodes
    userEmail = request.form.get('email')
    user = searchUserByEmail(userEmail)
    if user is None:
        raise ValueError(description="Email does not exist")
    mail = Mail(APP)
    #ensures that the new resetCode is unique
    newResetCode = randint(10000, 99999)
    for i in range(len(resetCodes)):
        if resetCodes[i]['resetCode'] == newResetCode:
            newResetCode = randint(10000, 99999)
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
            if resetCodes[i]['email'] == userEmail:
                userExist = True
                resetCodes[i]['resetCode'] = newResetCode
        if userExist == False:
            resetCodes.append({'email' : userEmail, 'resetCode' : newResetCode})
        save()
        return dumps({})
    except:
        raise ValueError(description="Unable to send email to the user") 

@APP.route('/auth/passwordreset/reset', methods=['POST'])
def flask_auth_passwordreset_reset():
    resetCode = int(request.form.get('reset_code'))
    newPassword = request.form.get('new_password')
    return dumps(auth_passwordreset_reset(resetCode, newPassword))

#Channel functions
@APP.route('/channel/invite', methods=['POST'])
def flask_channel_invite():
    uToken = request.form.get('token')
    currChannelID = int(request.form.get('channel_id'))
    invitedUserID = int(request.form.get('u_id'))
    return dumps(channel_invite(uToken, currChannelID, invitedUserID))
    
@APP.route('/channel/details', methods=['GET'])
def flask_channel_details():
    uToken = request.args.get('token')
    currChannelID = int(request.args.get('channel_id'))
    return dumps(channel_details(token=uToken, channel_id=currChannelID))
            
@APP.route('/channel/messages', methods=['GET'])
def flask_channel_messages():
    uToken = request.args.get('token')
    currChannelID = int(request.args.get('channel_id'))
    startIndex = int(request.args.get('start'))
    
    return dumps(channel_messages(uToken, currChannelID, startIndex))
    
@APP.route('/channel/leave', methods=['POST'])
def flask_channel_leave():
    uToken = request.form.get('token')
    currChannelID = int(request.form.get('channel_id'))
    return dumps(channel_leave(token=uToken, channel_id=currChannelID))

@APP.route('/channel/join', methods=['POST'])
def flask_channel_join():
    uToken = request.form.get('token')
    currChannelID = int(request.form.get('channel_id'))
    return dumps(channel_join(token=uToken, channel_id_to_join=currChannelID))
        
@APP.route('/channel/addowner', methods=['POST'])
def flask_channel_addowner():
    uToken = request.form.get('token')
    currChannelID = int(request.form.get('channel_id'))
    toBeOwnerID = int(request.form.get('u_id'))
    return dumps(channel_addowner(token=uToken, channel_id=currChannelID, to_be_owner_id=toBeOwnerID))
    
@APP.route('/channel/removeowner', methods=['POST'])
def flask_channel_removeowner():
    uToken = request.form.get('token')
    currChannelID = int(request.form.get('channel_id'))
    toBeRemovedOwnerID = int(request.form.get('u_id'))
    return dumps(channel_removeowner(token=uToken, channel_id=currChannelID, to_be_removed_owner_id=toBeRemovedOwnerID))

@APP.route('/channels/list', methods=['GET'])
def flask_channels_list():
    uToken = request.args.get('token')
    return dumps(channels_list(uToken))
    
@APP.route('/channels/listall', methods=['GET'])
def flask_channels_listall():
    uToken = request.args.get('token')
    return dumps(channels_listall(uToken))

@APP.route('/channels/create', methods=['POST'])
def flask_channels_create():
    uToken = request.form.get('token')
    channelName = request.form.get('name')
    isPublic = request.form.get('is_public')
    
    return dumps(channels_create(uToken, channelName, isPublic))
  
#Message function
@APP.route('/message/sendlater', methods=['POST'])
def flask_message_sendlater():
    uToken = request.form.get('token')
    channelID = int(request.form.get('channel_id'))
    uMessage = request.form.get('message')
    timeToSent = float(request.form.get('time_sent'))
    return dumps(message_sendlater(uToken, channelID, uMessage, timeToSent))
    
@APP.route('/message/send', methods=['POST'])
def flask_message_send():
    uToken = request.form.get('token')
    channelID = int(request.form.get('channel_id'))
    uMessage = request.form.get('message')
    return dumps(message_send(uToken, channelID, uMessage))

@APP.route('/message/remove', methods=['DELETE'])
def flask_message_remove():
    uToken = request.form.get('token')
    removedMessageID  = int(request.form.get('message_id'))
    return dumps(message_remove(uToken, removedMessageID ))
     
@APP.route('/message/edit', methods=['PUT'])
def flask_message_edit():
    uToken = request.form.get('token')
    toBeEditedMessageID = int(request.form.get('message_id'))
    newMessage = request.form.get('message')  
    return dumps(message_edit(uToken, toBeEditedMessageID, newMessage))
  
@APP.route('/message/react', methods=['POST'])
def flask_message_react():
    uToken = request.form.get('token')
    messageID = int(request.form.get('message_id'))
    reactID = int(request.form.get('react_id'))
    return dumps(message_react(uToken, messageID, reactID))
    
@APP.route('/message/unreact', methods=['POST'])
def flask_message_unreact():
    uToken = request.form.get('token')
    messageID = int(request.form.get('message_id'))
    reactID = int(request.form.get('react_id'))
    return dumps(message_unreact(uToken, messageID, reactID))

@APP.route('/message/pin', methods=['POST'])
def flask_message_pin():
    uToken = request.form.get('token')
    toBePinnedMessageID = int(request.form.get('message_id'))
    return dumps(message_pin(uToken, toBePinnedMessageID))
    
@APP.route('/message/unpin', methods=['POST'])
def flask_message_unpin():
    uToken = request.form.get('token')
    toBeUnpinnedMessageID = int(request.form.get('message_id'))
    return dumps(message_unpin(uToken, toBeUnpinnedMessageID))

#User functions
@APP.route('/user/profile', methods=['GET'])
def flask_user_profile():
    uToken = request.args.get('token')
    u_id = int(request.args.get('u_id'))
    return dumps(user_profile(uToken, u_id))

@APP.route('/user/profile/setname', methods=['PUT'])
def flask_user_profile_setname():
    uToken = request.form.get('token')
    user_first_name = request.form.get('name_first')
    user_last_name = request.form.get('name_last')
    return dumps(user_profile_setname(uToken, user_first_name, user_last_name))

@APP.route('/user/profile/setemail', methods=['PUT'])
def flask_user_profile_setemail():
    #Hayden said it is up to us to log out user immediately
    #after they set their email
    uToken = request.form.get('token')
    email = request.form.get('email')
    return dumps(user_profile_setemail(uToken, email))

@APP.route('/user/profile/sethandle', methods=['PUT'])
def flask_user_profile_sethandle():
    uToken = request.form.get('token')
    user_handle = request.form.get('handle_str')
    return dumps(user_profile_sethandle(uToken, user_handle))
    
@APP.route('/user/profiles/uploadphoto', methods=['POST'])
def flask_user_profiles_uploadphoto():
    uToken = request.form.get('token')
    imgURL = request.form.get('img_url')
    xStart = int(request.form.get('x_start'))
    yStart = int(request.form.get('y_start'))
    xEnd = int(request.form.get('x_end'))
    yEnd = int(request.form.get('y_end'))
    return dumps(user_profiles_uploadphoto(uToken, imgURL, xStart, yStart, xEnd, yEnd))
  
@APP.route('/imgurl/<name>')
def flask_imgurl_function(name):
    return imgurl_function(name)
    
@APP.route('/users/all', methods=['GET'])
def flask_users_all():
    uToken = request.args.get('token')
    return dumps(users_all(uToken))

@APP.route('/search', methods=['GET'])
def flask_search():
    uToken = request.args.get('token')
    query = request.args.get('query_str')
    return dumps(search(uToken, query))

@APP.route('/admin/userpermission/change', methods=['POST'])
def flask_admin_userpermission_change():
    uToken = request.form.get('token')
    u_id = int(request.form.get('u_id'))
    permission_id = int(request.form.get('permission_id'))
    return dumps(admin_userpermission_change(uToken, u_id, permission_id))
    
@APP.route('/standup/start', methods=['POST'])
def flask_standup_start():
    uToken = request.form.get('token')
    channelID = int(request.form.get('channel_id'))
    lengthOfStandup = float(request.form.get('length'))
    return dumps(standup_start(uToken, channelID, lengthOfStandup))
   
@APP.route('/standup/active', methods=['GET']) 
def flask_standup_active():
    uToken = request.args.get('token')
    channelID = int(request.args.get('channel_id'))
    return dumps(standup_active(uToken, channelID))

@APP.route('/standup/send', methods=['POST'])
def flask_standup_send():
    uToken = request.form.get('token')
    channelID = int(request.form.get('channel_id'))
    uMessage = request.form.get('message')
    return dumps(standup_send(uToken, channelID, uMessage))

if __name__ == '__main__':
    APP.debug = True
    APP.run(port=(sys.argv[1] if len(sys.argv) > 1 else 5000))
