usersList = {'users' : []}
channelsList = []
channelsMessages = []
resetCodes = []
unusedMessageID = 1
channelsTimer = [] 
#Standup helper functions 

def searchChannelInChannelsTimer(channel_id):
    global channelsTimer
    for channel in channelsTimer:
        if channel['channel_id'] == channel_id:
            return channel
    raise ValueError(description="Channel does not exist")

def startTimer(currChannelTimer):
    secondsLong = 1 * 60
    currChannelTimer['isTimerStarted'] = True
    currChannelTimer['timeStarted'] = datetime.datetime.now()
    myTimer = threading.Timer(secondsLong, stopStandup, args=[currChannelTimer])
    myTimer.start()
    save()
    return
    
def stopStandup(currChannelTimer):
    nMessage = len(currChannelTimer['messageQueue'])
    messagePackage = ""
    currChannelTimer['isTimerStarted'] = False
    frontOfList = 0
    del currChannelTimer['timeStarted']
    for i in range(nMessage-1, -1, -1):
        currHandle = currChannelTimer['messageQueue'][i]['handle']
        currMessage = currChannelTimer['messageQueue'][i]['message']
        messagePackage = messagePackage + f"{currHandle}: {currMessage}"
        #bottom code prevent 2 newline on the end of the messagePackage
        #when it is displayed on front end
        print("Here is my messagePackaged: " + messagePackage)
        if i != 0:
            messagePackage = messagePackage + "\n"
    
    currChannelMessages = searchChannelInChannelsMessages(currChannelTimer['channel_id'])
    newMessageID = createMessageID()
    standupStarterID = currChannelTimer['starterID']
    timeCreated = datetime.datetime.now()
    timeSinceEpoch = timeCreated.replace(tzinfo=datetime.timezone.utc).timestamp()
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
    
#Standup functions
@APP.route('/standup/start', methods=['POST'])
def standup_start():
    fifteenMinutesInSeconds = 15 * 60
    uToken = request.form.get('token')
    channelID = int(request.form.get('channel_id'))
    userInfo = decodeToken(uToken)
    userInfo = searchUserByEmail(userInfo['email'])
    checkUserLoggedIn(uToken, userInfo)
    searchChannelByID(channelID)
    if channelID not in userInfo['joinedChannel_id']:
        raise AccessError(description="User is not member of channel")
    currChannelTimer = searchChannelInChannelsTimer(channelID)
    if currChannelTimer['isTimerStarted'] == True:
        raise ValueError(description="A stand up is currently running in the channel")
    currChannelTimer['starterID'] = userInfo['u_id']
    print("I am in startTimer()")
    startTimer(currChannelTimer)
    print("Out of startTimer()")
    timeStartedSinceEpoch = currChannelTimer['timeStarted'].replace(tzinfo=datetime.timezone.utc).timestamp()
    save()
    return dumps({'time_finish' : timeStartedSinceEpoch + fifteenMinutesInSeconds})
    
@APP.route('/standup/send', methods=['POST'])
def standup_send():
    uToken = request.form.get('token')
    channelID = int(request.form.get('channel_id'))
    uMessage = request.form.get('message')
    userInfo = decodeToken(uToken)
    userInfo = searchUserByEmail(userInfo['email'])
    checkUserLoggedIn(uToken, userInfo)
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
    return dumps({})
