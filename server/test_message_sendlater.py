import pytest
import datetime 
import time
from changes.data_backend import reset_data
from changes.auth_backend import auth_register
from changes.channel_backend import channels_create, channel_messages 
from changes.message_backend import message_send, message_sendlater
from clearDatabase import clear
    
def test_message_sendlater():
    reset_data()
    userInfo = auth_register("abdul@yahoo.com","abdulPassword","Abdul","Temon")
    userInfo2 = auth_register("abduuul@yahoo.com","abdulPassword","Abduuuuuuul","Temmmmmon")
    currentTime = datetime.datetime.now()
    
    channelInfo = channels_create(userInfo['token'],"Abdul's channel",'true')
    
    #user is not in channel
    with pytest.raises(Exception):
        message_sendlater(userInfo2['token'], channelInfo['channel_id'], "message", currentTime.timestamp())

    #create string of 1001 characters
    myList = []
    for i in range(1001):
        myList.append("a")
    myMessage = "".join(myList)
    #message exceeds 1000 characters
    with pytest.raises(Exception):
        message_sendlater(userInfo['token'], channelInfo['channel_id'], myMessage, currentTime.timestamp())

    #time is in the past
    with pytest.raises(Exception):
        message_sendlater(userInfo['token'], channelInfo['channel_id'], "message", currentTime.timestamp() - 100)
    
    #testing if message_sendlater works as intended
    currentTime = datetime.datetime.now()
    message_sendlater(userInfo['token'], channelInfo['channel_id'], "firstMessage", currentTime.timestamp() + 1)
    message_sendlater(userInfo['token'], channelInfo['channel_id'], "secondMessage", currentTime.timestamp() + 2)

    time.sleep(3)
    channelMessages = channel_messages(userInfo['token'],channelInfo['channel_id'],0)

    assert channelMessages['start'] == 0
    assert channelMessages['end'] == -1
    #testing the 1 index is the index conatining 'message': "second message"
    assert channelMessages['messages'][0]['u_id'] == userInfo['u_id']
    assert channelMessages['messages'][0]['message'] == "secondMessage"
    #testing the 2 index is the index conatining 'message': "first message"
    assert channelMessages['messages'][1]['u_id'] == userInfo['u_id']
    assert channelMessages['messages'][1]['message'] == "firstMessage"

    clear()
    
