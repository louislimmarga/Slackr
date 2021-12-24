usersList = {'users' : []}
channelsList = []
channelsMessages = []
resetCodes = []
unusedMessageID = 1
channelsTimer = [] 

def searchChannelInChannelsMessages(channel_id):
    global channelsMessages
    for channel in channelsMessages:
        if(channel['channel_id'] == channel_id):
            return channel
    raise ValueError(description = "Invalid channel_id passed in")


@APP.route('/search', methods=['GET'])
def search():
    #(token, query_str)
    #{ messages: [] }
    global channelsMessage
    messages = []
    uToken = request.args.get('token')
    query = request.args.get('query_str')

    userInfo = decodeToken(uToken)
    userInfo = searchUserByEmail(userInfo['email'])

    for channel in userInfo['joinedChannel_id']:
        channel_id = searchChannelInChannelsMessages(channel)

        for text in channel_id:
            queryFound = text.find(query)
            if queryFound != -1:
                messages.append(text)

    return dumps(messages)




