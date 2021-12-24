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
from changes.Error import AccessError
from changes.data_backend import getChannelsList, getChannelsMessages, getChannelsTimer, save, ValueError
from changes.helper_func import decodeToken, searchUserByEmail, checkUserLoggedIn, searchChannelByID, searchUserByID, joinUserToChannel, leaveUserToChannel, searchChannelInChannelsMessages, createChannel_ID

#DECORATORS TO CHECK VALID ARGUMENTS

def get_userInfo(function):
    def wrapper(token=None, *args, **kwargs):
        user_info = decodeToken(token)
        user_info = searchUserByEmail(user_info['email'])  
        checkUserLoggedIn(token, user_info)
        return function(user_info, *args, **kwargs)
    return wrapper


def channel_owner_argument_valid(function):
    def wrapper(user_info, channel_id=None, 
                to_be_owner_id=None, to_be_removed_owner_id=None):
        channel_info = searchChannelByID(channel_id)
        if channel_id not in user_info['joinedChannel_id']:
            raise AccessError(description="User is not part of channel")
        if user_info['permission_id'] == 3 and user_info['u_id'] not in channel_info['owners_id']:
            raise AccessError(description="Authorised user not an owner of slackr and channel")
        if to_be_owner_id is not None:
            if to_be_owner_id not in channel_info['members_id']:
                raise ValueError(description="Making a non member an owner of the channel")      
            if to_be_owner_id in channel_info['owners_id']:
                raise ValueError(description="User is already an owner of the channel")
            return function(user_info, channel_info, to_be_owner_id)
        else:  
            if to_be_removed_owner_id not in channel_info['members_id']:
                raise ValueError(description="Removing the ownership of a non member")
            if to_be_removed_owner_id not in channel_info['owners_id']:
                raise ValueError(description="Removing the ownership of a non-owner")
            to_be_removed_owner_info = searchUserByID(to_be_removed_owner_id)
            if to_be_removed_owner_info['permission_id'] != 3:
                raise ValueError(description="Can't remove the ownership of an admin/owner of slackr")
            return function(user_info, channel_info, to_be_removed_owner_id)
    return wrapper

def channel_details_leave_argument_valid(function):
    def wrapper(user_info, channel_id=None):
        channel_info = searchChannelByID(channel_id)
        if channel_id not in user_info['joinedChannel_id']:
            raise ValueError("User does not belong to the channel")
        return function(user_info, channel_info)
    return wrapper

def channel_join_argument_valid(function):
    def wrapper(user_info, channel_id_to_join=None):
        channel_info = searchChannelByID(channel_id_to_join)
        if channel_id_to_join in user_info['joinedChannel_id']:
            raise ValueError(description="User has previously joined channel_id")
        if user_info['permission_id'] == 3 and channel_info['isPublic'] == False:
            raise ValueError(description="Member of slackr trying to join a private channel")
        return function(user_info, channel_info)
    return wrapper

def channel_invite_argument_valid(function):
    def wrapper(user_info, channel_id=None, invited_user_id=None):
        invited_user_info = searchUserByID(invited_user_id)
        channel_info = searchChannelByID(channel_id)
        if channel_id not in user_info['joinedChannel_id']:
            raise AccessError(description="User is not part of channel")
        if invited_user_info is None:
            raise ValueError(description="u_id does not refer to valid user")
        if invited_user_id in channel_info['members_id']:
            raise ValueError(description="Inviting an already member of the channel")
        return function(user_info, channel_info, invited_user_info)
    return wrapper
    
def channel_messages_argument_valid(function):
    def wrapper(user_info, channel_id=None, start=None):
        curr_channel_messages_info = searchChannelInChannelsMessages(channel_id)
        num_message_in_channel = len(curr_channel_messages_info['messages'])
        if channel_id not in user_info['joinedChannel_id']:
            raise AccessError(description="User is not part of channel")
        if start >= num_message_in_channel:
            raise ValueError(description="There is no more message to be shown")
        return function(user_info, curr_channel_messages_info, start)
        
    return wrapper
    
#CHANNEL BACKEND FUNCTIONS BELOW   
@get_userInfo
@channel_details_leave_argument_valid
def channel_details(userInfo, currChannelInfo):
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
                          'name_last' : currUser['name_last'],
                          'profile_img_url': currUser['profile_img_url']}
        channelDetail['all_members'].append(currUserDetail)
    return channelDetail
   
@get_userInfo 
@channel_details_leave_argument_valid
def channel_leave(userInfo, currChannelInfo):
    leaveUserToChannel(currChannelInfo, userInfo)
    save()
    return {}

@get_userInfo
@channel_join_argument_valid
def channel_join(userInfo, currChannelInfo):
    #if user is owner/admin of slacker, make user immediately join the channel
    #if not, check whether the channel is private or not
    #if no, then make the user join the channel
    joinUserToChannel(currChannelInfo, userInfo)
    save()
    return {}

@get_userInfo
@channel_owner_argument_valid 
def channel_addowner(authUserInfo, currChannelInfo, toBeOwnerID):
    currChannelInfo['owners_id'].append(toBeOwnerID)
    save()
    return {}

@get_userInfo
@channel_owner_argument_valid
def channel_removeowner(authUserInfo, currChannelInfo, toBeRemovedOwnerID):
    currChannelInfo['owners_id'].remove(toBeRemovedOwnerID)
    save()
    return {}

@get_userInfo
@channel_invite_argument_valid
def channel_invite(invitingUserInfo, currChannelInfo, invitedUserInfo):
    joinUserToChannel(currChannelInfo, invitedUserInfo)
    save()
    return {}

@get_userInfo
@channel_messages_argument_valid
def channel_messages(userInfo, currChannelMessagesInfo, startIndex):
    totalNumMessages = len(currChannelMessagesInfo['messages'])
    end = startIndex + 50
    endIndex = end
    #if totalNumMessages = 99, and startIndex = 50, you would show up until
    #index 99, and return -1 indicating no more message to show
    if startIndex + 50 >= totalNumMessages:
        end = -1
        endIndex = totalNumMessages - 1
    #end index would adapt to whether it want to loop through everything from start
    #to start+50 or from start to the end of the list (in case start+50 is out of bound)
    i = startIndex
    messagesToReturn = {'messages' : [], 'start' : startIndex, 'end' : end}
    while i <= endIndex:
        tempChannelsMessages = deepcopy(currChannelMessagesInfo['messages'][i])
        #check whether the authorised user's u_id is in messageDetail['reacts']['u_ids']
        #if yes add a field ' is_this_user_reacted ' as True else False
        if userInfo['u_id'] in tempChannelsMessages['reacts'][0]['u_ids']:
            tempChannelsMessages['reacts'][0]['is_this_user_reacted'] = True
        else:
            tempChannelsMessages['reacts'][0]['is_this_user_reacted'] = False
            
        messagesToReturn['messages'].append(tempChannelsMessages)
        
        i = i + 1
        
    return messagesToReturn

@get_userInfo
def channels_list(userInfo):
    channelsList = getChannelsList()
    userJoinedChannel = {'channels' : []}
    for joinedChannel_id in userInfo['joinedChannel_id']:
        for channel in channelsList:
            if channel['channel_id'] == joinedChannel_id:
                userJoinedChannel['channels'].append({'channel_id' : joinedChannel_id,
                                                      'name' : channel['name']})
    return userJoinedChannel

@get_userInfo
def channels_listall(userInfo):
    channelsList = getChannelsList()
    allChannel = {'channels' : []}
    for channel in channelsList:
        if channel['isPublic'] == True or any(joinedChannelID == channel['channel_id'] for joinedChannelID in userInfo['joinedChannel_id']):
            allChannel['channels'].append({'channel_id': channel['channel_id'],
                                           'name' : channel['name']})
        
    return allChannel
    
@get_userInfo
def channels_create(userInfo, channelName, isPublic):
    channelsList = getChannelsList()
    channelsMessages = getChannelsMessages()
    channelsTimer = getChannelsTimer()
    if len(channelName) > 20:
        raise ValueError(description="Name is more than 20 characters")
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
    if isPublic == 'true':
        channelsList[len(channelsList)-1]['isPublic'] = True
    else:
        channelsList[len(channelsList)-1]['isPublic'] = False
    channelsMessages.append({'channel_id' : newChannelID, 'messages' : []})
    channelsTimer.append({'channel_id' : newChannelID, 
                          'isTimerStarted' : False,
                          'messageQueue' : []})
    save()
    return {'channel_id' : newChannelID}
