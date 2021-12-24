import pytest
from changes.data_backend import reset_data
from changes.auth_backend import auth_register
from changes.channel_backend import channels_create, channel_messages, channel_join, channel_addowner
from changes.message_backend import message_react, message_unreact, message_send
from clearDatabase import clear

def test_invalid_token():
    reset_data()
    userInfo = auth_register("feddrick@yahoo.com",'myPassword',"Feddrick","Aquino")
    channelInfo = channels_create(userInfo['token'],"Feddrick's Channel",'true')
    message_send(userInfo['token'],channelInfo['channel_id'],"new message")
    channelMessages = channel_messages(userInfo['token'],channelInfo['channel_id'],0)
    #check index 0 contains 'message' : "new message"
    assert channelMessages['messages'][0]['message'] == "new message"
    msgID = channelMessages['messages'][0]['message_id']
    #user reacts to the message first
    message_react(userInfo['token'],msgID,1)
    with pytest.raises(Exception):
    #above codes generate a valid msgID so that i can be sure the function below raises Exception solely from an invalid token
        message_unreact("randomToken",msgID,1)
    clear()
        
def test_not_existing_message_id():
    reset_data()
    userInfo = auth_register("ivanny@yahoo.com",'ivannyPassword',"Ivanny","Lestari")
    channelInfo = channels_create(userInfo['token'],"Ivanny's Channel",'true')
    with pytest.raises(Exception):
    #passing in a random non-existant message_id
        message_unreact(userInfo['token'],7412,1)
        
def test_invalid_react_id():
    userInfo = auth_register("alexandra@yahoo.com",'alexandraPassword',"Alexandra","Pitasio")
    channelInfo = channels_create(userInfo['token'],"Alexandra's Channel",'true')
    message_send(userInfo['token'],channelInfo['channel_id'],"new message")
    channelMessages = channel_messages(userInfo['token'],channelInfo['channel_id'],0)
    #check index 0 contains 'message' : "new message"
    assert channelMessages['messages'][0]['message'] == "new message"
    msgID = channelMessages['messages'][0]['message_id']
    message_react(userInfo['token'],msgID,1)
    with pytest.raises(Exception):
    #passing in an invalid react_id (i.e react_id other than 1)
        message_unreact(userInfo['token'],msgID,1665)
    clear()
          
def test_unreact_already_unreacted_message():
    reset_data()
    userInfo = auth_register("artour@yahoo.com",'artourPassword',"Artour","Babaev")
    channelInfo = channels_create(userInfo['token'],"Artour's Channel",'true')
    message_send(userInfo['token'],channelInfo['channel_id'],"new message")
    channelMessages = channel_messages(userInfo['token'],channelInfo['channel_id'],0)
    #check index 0 contains 'message' : "new message"
    assert channelMessages['messages'][0]['message'] == "new message"
    msgID = channelMessages['messages'][0]['message_id']
    
    with pytest.raises(Exception):
        message_unreact(userInfo['token'],msgID,1)
    
    message_react(userInfo['token'],msgID,1)
    message_unreact(userInfo['token'],msgID,1)
    
    with pytest.raises(Exception):
        message_unreact(userInfo['token'],msgID,1)
    clear()
    
def test_message_unreact_working():
    reset_data()
    userInfo = auth_register("artour@yahoo.com",'artourPassword',"Artour","Babaev")
    channelInfo = channels_create(userInfo['token'],"Artour's Channel",'true')
    message_send(userInfo['token'],channelInfo['channel_id'],"new message")
    channelMessages = channel_messages(userInfo['token'],channelInfo['channel_id'],0)
    #check index 0 contains 'message' : "new message"
    assert channelMessages['messages'][0]['message'] == "new message"
    msgID = channelMessages['messages'][0]['message_id']
    #if message_unreact() was implemented correctly, the second call to message_react() would not raises an Exception
    message_react(userInfo['token'],msgID,1)
    message_unreact(userInfo['token'],msgID,1)
    message_react(userInfo['token'],msgID,1)
    clear()

def test_message_unreact_not_user_in_channel():
    reset_data()
    userInfo = auth_register("artour@yahoo.com",'artourPassword',"Artour","Babaev")
    channelInfo = channels_create(userInfo['token'],"Artour's Channel",'true')
    userInfo2 = auth_register("alexandra@yahoo.com",'alexandraPassword',"Alexandra","Pitasio")
    message_send(userInfo['token'],channelInfo['channel_id'],"new message")
    channelMessages = channel_messages(userInfo['token'],channelInfo['channel_id'],0)
    #check index 0 contains 'message' : "new message"
    assert channelMessages['messages'][0]['message'] == "new message"
    msgID = channelMessages['messages'][0]['message_id']
    #if message_unreact() was implemented correctly, the second call to message_react() would not raises an Exception
    message_react(userInfo['token'],msgID,1)
    #userInfo2 is in the channel
    with pytest.raises(Exception):
        message_unreact(userInfo2['token'],msgID,1)
    clear()
