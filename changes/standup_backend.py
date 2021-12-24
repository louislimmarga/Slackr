import datetime
from changes.Error import AccessError
from changes.helper_func import decodeToken, searchUserByEmail, checkUserLoggedIn, searchChannelByID, searchChannelInChannelsTimer, startTimer
from changes.data_backend import createMessageID, save, ValueError
from changes.user_backend import get_userInfo

def get_userInfo(function):
    def wrapper(token=None, *args):
        user_info = decodeToken(token)
        user_info = searchUserByEmail(user_info['email'])  
        checkUserLoggedIn(token, user_info)
        return function(user_info, *args)
    return wrapper

def standup_start_argument_valid(function):
    def wrapper(user_info, channel_id=None, length=None, *args):
        searchChannelByID(channel_id)
        if channel_id not in user_info['joinedChannel_id']:
            raise AccessError(description="User is not member of channel")
        curr_channel_timer = searchChannelInChannelsTimer(channel_id)
        if curr_channel_timer['isTimerStarted'] == True:
            raise ValueError(description="A stand up is currently running in the channel")
        return function(user_info, curr_channel_timer, length)
    return wrapper

@get_userInfo
@standup_start_argument_valid
def standup_start(userInfo, currChannelTimer, lengthOfStandup):
    currChannelTimer['starterID'] = userInfo['u_id']
    newMessageID = createMessageID()
    startTimer(currChannelTimer, lengthOfStandup, newMessageID)
    timeFinishSinceEpoch = currChannelTimer['timeFinishes'].timestamp()
    save()
    return {'time_finish' : timeFinishSinceEpoch}

@get_userInfo
def standup_active(userInfo, channelID):
    searchChannelByID(channelID)
    if channelID not in userInfo['joinedChannel_id']:
        raise AccessError(description="User is not member of channel")
    standupStatus = {}
    currChannelTimer = searchChannelInChannelsTimer(channelID)
    if currChannelTimer['isTimerStarted'] == False:
        standupStatus['is_active'] = False
        standupStatus['time_finish'] = None
    else:
        standupStatus['is_active'] = True
        timeFinish = currChannelTimer['timeFinishes']
        timeFinishSinceEpoch = timeFinish.timestamp()
        standupStatus['time_finish'] = timeFinishSinceEpoch
    return standupStatus

@get_userInfo
def standup_send(userInfo, channelID, uMessage):
    searchChannelByID(channelID)
    if channelID not in userInfo['joinedChannel_id']:
        raise AccessError(description="User is not member of channel")
    currChannelTimer = searchChannelInChannelsTimer(channelID)
    if currChannelTimer['isTimerStarted'] == False:
        raise ValueError(description="There is no standup currently running")
    if len(uMessage) > 1000:
        raise ValueError(description="Message exceeded 1000 character")
    currChannelTimer['messageQueue'].insert(0, {'handle' : userInfo['handle'],
                                                'message' : uMessage})
    save()
    return {}
    