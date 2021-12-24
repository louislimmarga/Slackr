import datetime
import threading
from changes.Error import AccessError
from changes.data_backend import createMessageID, save, ValueError
from changes.helper_func import decodeToken, searchUserByEmail, checkUserLoggedIn, searchChannelInChannelsMessages, timeMessageSendlater, searchChannelByMessageID, searchChannelByID, searchMessageInChannel
from changes.user_backend import get_userInfo

def check_valid(function):
    def wrapper(userInfo, channelID=None, uMessage=None, *args):
        if len(uMessage) > 1000:
            raise ValueError(description="Message exceeded 1000 character")
        
        if channelID not in userInfo['joinedChannel_id']:
            raise AccessError(description="User is not in the channel")
        
        
        return function(userInfo, channelID, uMessage, *args)
    return wrapper

def check_ownersender(function):
    def wrapper(userInfo, MessageID, *args):
        currChannelsMessagesInfo = searchChannelByMessageID(MessageID)
        currChannelInfo = searchChannelByID(currChannelsMessagesInfo['channel_id'])
        #by this time, message ID exist
        #raise error when user is just a usual member of channel and the slackr AND 
        #he is not the one who send the message
        messageDetail = searchMessageInChannel(currChannelsMessagesInfo, MessageID)
        if userInfo['u_id'] != messageDetail['u_id'] and userInfo['u_id'] not in currChannelInfo['owners_id'] and userInfo['permission_id'] == 3:
            raise AccessError(description="Authorised user is neither the message owner nor is the owner of the channel")
        return function(userInfo, MessageID, *args)
    return wrapper

def check_react(function):
    def wrapper(userInfo, messageID, reactID, *args):
        currChannelsMessagesInfo = searchChannelByMessageID(messageID)
        currChannelInfo = searchChannelByID(currChannelsMessagesInfo['channel_id'])
        if userInfo['u_id'] not in currChannelInfo['members_id']:
            raise AccessError(description="User is not in the channel")
        if reactID != 1:
            raise ValueError(description="react_id is not valid")
        return function(userInfo, messageID, reactID, *args)
    return wrapper

def check_pin(function):
    def wrapper(userInfo, MessageID, *args):
        currChannelsMessagesInfo = searchChannelByMessageID(MessageID)
        currChannelInfo = searchChannelByID(currChannelsMessagesInfo['channel_id'])
        #assuming that admin/owner also needs to join channel before able to pin
        #a message 
        if userInfo['permission_id'] == 3:
            raise ValueError(description="Authorised user is not an admin/owner of slackr")
        if userInfo['u_id'] not in currChannelInfo['members_id']:
            raise AccessError(description="User is not in the channel")
        return function(userInfo, MessageID, *args)
    return wrapper

@get_userInfo
@check_valid
def message_sendlater(userInfo, channelID, uMessage, timeToSent):
    currentTime = datetime.datetime.now()
    currentTimeSinceEpoch = currentTime.timestamp()
    
    currChannelMessagesInfo = searchChannelInChannelsMessages(channelID)

    if timeToSent < currentTimeSinceEpoch:
        raise ValueError(description="time_sent is a time in the past")
    newMessageID = createMessageID()
    senderID = userInfo['u_id']
    reacts = [{'react_id' : 1,
               'u_ids' : []}]
    messageDetail = {'message_id' : newMessageID,
                     'u_id' : senderID,
                     'message' : uMessage,
                     'time_created' : timeToSent,
                     'reacts' : reacts,
                     'is_pinned' : False}
    myTimer = threading.Timer(timeToSent-currentTimeSinceEpoch, timeMessageSendlater, 
                              args=[currChannelMessagesInfo, messageDetail])
    myTimer.start()
    save()
    return {'message_id' : newMessageID}

    #ensure latest message at the front of the list

@get_userInfo
@check_valid
def message_send(userInfo, channelID, uMessage):
    frontOfList = 0
    currChannelMessagesInfo = searchChannelInChannelsMessages(channelID)
    senderID = userInfo['u_id']
    newMessageID = createMessageID()
    timeCreated = datetime.datetime.now()
    timeSinceEpoch = timeCreated.timestamp()
    #is_this_user_reacted only need to be considered when someone did
    #channel/messages
    reacts = [{'react_id' : 1,
               'u_ids' : []}]
    messageDetail = {'message_id' : newMessageID,
                     'u_id' : senderID,
                     'message' : uMessage,
                     'time_created' : timeSinceEpoch,
                     'reacts' : reacts,
                     'is_pinned' : False}
    #ensure latest message at the front of the list
    currChannelMessagesInfo['messages'].insert(frontOfList, messageDetail)
    save()
    return {'message_id' : newMessageID}

@get_userInfo
@check_ownersender
def message_remove(userInfo, removedMessageID):
    currChannelsMessagesInfo = searchChannelByMessageID(removedMessageID)
    messageDetail = searchMessageInChannel(currChannelsMessagesInfo, removedMessageID)

    #by this time, user have the permission to delete the valid message
    currChannelsMessagesInfo['messages'].remove(messageDetail)
    save()
    return {}

@get_userInfo
@check_ownersender
def message_edit(userInfo, toBeEditedMessageID, newMessage):
    currChannelsMessagesInfo = searchChannelByMessageID(toBeEditedMessageID)
    currChannelInfo = searchChannelByID(currChannelsMessagesInfo['channel_id'])
    messageDetail = searchMessageInChannel(currChannelsMessagesInfo, toBeEditedMessageID)
    
    if newMessage == "":
    #delete message
        currChannelsMessagesInfo['messages'].remove(messageDetail)
    else:
        messageDetail['message'] = newMessage
    save()
    return {}

@get_userInfo
@check_react
def message_react(userInfo, messageID, reactID):
    currChannelsMessagesInfo = searchChannelByMessageID(messageID)
    messageDetail = searchMessageInChannel(currChannelsMessagesInfo, messageID)

    if int(userInfo['u_id']) in messageDetail['reacts'][0]['u_ids']:
        raise ValueError(description="User has reacted using this react_id")

    messageDetail['reacts'][0]['u_ids'].append(userInfo['u_id'])
    save()
    return {}

@get_userInfo
@check_react
def message_unreact(userInfo, messageID, reactID):
    currChannelsMessagesInfo = searchChannelByMessageID(messageID)
    messageDetail = searchMessageInChannel(currChannelsMessagesInfo, messageID)

    if int(userInfo['u_id']) not in messageDetail['reacts'][0]['u_ids']:
        raise ValueError(description="User has not reacted using this react_id")

    messageDetail['reacts'][0]['u_ids'].remove(userInfo['u_id'])
    save()
    return {}

@get_userInfo
@check_pin
def message_pin(userInfo, toBePinnedMessageID):
    currChannelsMessagesInfo = searchChannelByMessageID(toBePinnedMessageID)
    messageDetail = searchMessageInChannel(currChannelsMessagesInfo, toBePinnedMessageID)
    
    if messageDetail['is_pinned'] == True:
        raise ValueError(description="Pinning an already pinned message")

    messageDetail['is_pinned'] = True
    save()
    return {}

@get_userInfo
@check_pin
def message_unpin(userInfo, toBeUnpinnedMessageID):
    currChannelsMessagesInfo = searchChannelByMessageID(toBeUnpinnedMessageID)
    messageDetail = searchMessageInChannel(currChannelsMessagesInfo, toBeUnpinnedMessageID)

    if messageDetail['is_pinned'] == False:
        raise ValueError(description="Unpinning an already unpinned message")

    messageDetail['is_pinned'] = False
    save()
    return {}
