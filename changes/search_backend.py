from copy import deepcopy
from flask_cors import CORS
from flask_mail import Mail, Message
from flask import Flask, request, send_from_directory
from werkzeug.exceptions import HTTPException
from changes.Error import AccessError
from changes.data_backend import save, ValueError, getChannelsMessages
from changes.helper_func import decodeToken, searchUserByEmail, checkUserLoggedIn, searchChannelInChannelsMessages
from changes.user_backend import get_userInfo

@get_userInfo
def search(userInfo, query):
    channelsMessages = getChannelsMessages()
    messages = []
    
    for channel_id in userInfo['joinedChannel_id']:
        channel_message = searchChannelInChannelsMessages(channel_id)
        for item in channel_message['messages']:
            message = item['message']
            if message.find(query) != -1:
                temp = deepcopy(item)
                if userInfo['u_id'] in temp['reacts'][0]['u_ids']:
                    temp['reacts'][0]['is_this_user_reacted'] = True
                else:
                    temp['reacts'][0]['is_this_user_reacted'] = False
                messages.append(temp)
            
    return {'messages': messages}
