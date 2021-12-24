import pytest
from changes.data_backend import reset_data
from changes.auth_backend import auth_register
from changes.channel_backend import channels_create, channel_messages 
from changes.message_backend import message_send
from clearDatabase import clear

def test_invalid_token():
    reset_data()
    userInfo = auth_register("feddrick@yahoo.com","myPassword","Feddrick","Aquino")
    channelInfo = channels_create(userInfo['token'],"My channel",'true')
    
    with pytest.raises(Exception):
        message_send('randomToken',channelInfo['channel_id'],"This is my first message")
        
def test_channel_not_exist():
    userInfo = auth_register("feddrickaquino@yahoo.com","myPassword","Feddrick","Aquino")
    
    with pytest.raises(Exception):
        message_send(userInfo['token'],521345,"This is my first message")
        
def test_user_not_member_of_channel():
    firstUserInfo = auth_register("feddricka@yahoo.com","myPassword","Feddrick","A")
    secondUserInfo = auth_register("marlon@gmail.com","marlonPassword","Marlon","Brando")
    channelInfo = channels_create(firstUserInfo['token'],"Feddrick's channel",'true')
    with pytest.raises(Exception):
        message_send(secondUserInfo['token'],channelInfo['channel_id'],"this is message from second user")
    clear()
     
def test_message_exceed_limit():
    reset_data()
    firstUserInfo = auth_register("Tarik@yahoo.com","tarikPassword","Tarik","Ahbein")
    channelInfo = channels_create(firstUserInfo['token'],"Tarik's channel",'true')
    
    #create string of 1001 characters
    myList = []
    for i in range(1001):
        myList.append("a")
    myMessage = "".join(myList)
    
    with pytest.raises(Exception):
        message_send(firstUserInfo['token'],channelInfo['channel_id'],myMessage)
    clear()
    
def test_message_send_working():
    reset_data()
    userInfo = auth_register("abdul@yahoo.com","abdulPassword","Abdul","Temon")
    channelInfo = channels_create(userInfo['token'],"Abdul's channel",'true')
    
    message_send(userInfo['token'],channelInfo['channel_id'],"first message")
    message_send(userInfo['token'],channelInfo['channel_id'],"second message")
    #channelMessages contains dictionary that one of its values contain the messages sent to the channel
    channelMessages = channel_messages(userInfo['token'],channelInfo['channel_id'],1)
    
    '''assert channelMessages == {'messages' : [{'message_id': 1234, 'u_id': 8314, 'message': "first message", 'time_create': 1 November 2019, 'is_unread': True}], 'start' : 1, 'end' : -1}'''
    assert channelMessages['start'] == 1
    assert channelMessages['end'] == -1
    assert channelMessages['messages'][0]['u_id'] == userInfo['u_id']
    assert channelMessages['messages'][0]['message'] == "first message"
    
    
    message_send(userInfo['token'],channelInfo['channel_id'],"third message")
    channelMessages = channel_messages(userInfo['token'],channelInfo['channel_id'],0)
    
    '''assert channelMessages == {'messages' : [{'message_id': randomNumber, 'u_id': userInfo['u_id'], 'message': "third message", 'time_create': randomTime, 'is_unread': True/False},{'message_id': randomNumber, 'u_id': userInfo['u_id'], 'message': "second message", 'time_create': randomTime, 'is_unread': True/False},{'message_id': randomNumber, 'u_id': userInfo['u_id'], 'message': "first message", 'time_create': randomTime, 'is_unread': True/False}], 'start' : 0, 'end' : -1}'''
    assert channelMessages['start'] == 0
    assert channelMessages['end'] == -1
    #testing the 0 index is the index containing 'message': "third message"
    assert channelMessages['messages'][0]['u_id'] == userInfo['u_id']
    assert channelMessages['messages'][0]['message'] == "third message"
    #testing the 1 index is the index conatining 'message': "second message"
    assert channelMessages['messages'][1]['u_id'] == userInfo['u_id']
    assert channelMessages['messages'][1]['message'] == "second message"
    #testing the 2 index is the index conatining 'message': "first message"
    assert channelMessages['messages'][2]['u_id'] == userInfo['u_id']
    assert channelMessages['messages'][2]['message'] == "first message"
    clear()
    
