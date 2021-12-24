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
    
    with pytest.raises(Exception):
    #above codes generate a valid msgID so that i can be sure the function below raises Exception solely from an invalid token
        message_react("randomToken",msgID,1)
    clear()
    
def test_not_existing_message_id():
    reset_data()
    userInfo = auth_register("ivanny@yahoo.com",'ivannyPassword',"Ivanny","Lestari")
    channelInfo = channels_create(userInfo['token'],"Ivanny's Channel",'true')
    with pytest.raises(Exception):
    #passing in a random non-existant message_id
        message_react(userInfo['token'],7412,1)
    clear()
        
def test_user_not_member_of_channel():
    reset_data()
    firstUserInfo = auth_register("dedy@yahoo.com",'dedyPassword',"Dedy","Hariady")
    secondUserInfo = auth_register("panny@yahoo.com",'pannyPassword',"Panny","Lai")
    
    channelInfo = channels_create(firstUserInfo['token'],"Dedy's Channel",'true')
    message_send(firstUserInfo['token'],channelInfo['channel_id'],"new message")
    
    channelMessages = channel_messages(firstUserInfo['token'],channelInfo['channel_id'],0)
    #check index 0 contains 'message' : "new message"
    assert channelMessages['messages'][0]['message'] == "new message"
    msgID = channelMessages['messages'][0]['message_id']
    
    with pytest.raises(Exception):
    #first user, who is a slackr admin but not a member of the channel, trying to pin a message from the channel
        message_react(secondUserInfo['token'],msgID,1)
    clear()
                
        
def test_invalid_react_id():
    reset_data()
    userInfo = auth_register("alexandra@yahoo.com",'alexandraPassword',"Alexandra","Pitasio")
    channelInfo = channels_create(userInfo['token'],"Alexandra's Channel",'true')
    message_send(userInfo['token'],channelInfo['channel_id'],"new message")
    channelMessages = channel_messages(userInfo['token'],channelInfo['channel_id'],0)
    #check index 0 contains 'message' : "new message"
    assert channelMessages['messages'][0]['message'] == "new message"
    msgID = channelMessages['messages'][0]['message_id']
    
    with pytest.raises(Exception):
    #passing in an invalid react_id (i.e react_id other than 1)
        message_react(userInfo['token'],msgID,1665)
def test_react_already_reacted_message():
    userInfo = auth_register("artour@yahoo.com",'artourPassword',"Artour","Babaev")
    channelInfo = channels_create(userInfo['token'],"Artour's Channel",'true')
    message_send(userInfo['token'],channelInfo['channel_id'],"new message")
    channelMessages = channel_messages(userInfo['token'],channelInfo['channel_id'],0)
    #check index 0 contains 'message' : "new message"
    assert channelMessages['messages'][0]['message'] == "new message"
    msgID = channelMessages['messages'][0]['message_id']
    #since message_id is valid and user is a member of the channel_id corresponds to message_id, user should be able to react to the message
    message_react(userInfo['token'],msgID,1)
    with pytest.raises(Exception):
    #user reacting to an already reacted message
        message_react(userInfo['token'],msgID,1)
    clear()

def test_message_react_working():
    reset_data()
    userInfo = auth_register("artour@yahoo.com",'artourPassword',"Artour","Babaev")
    channelInfo = channels_create(userInfo['token'],"Artour's Channel",'true')
    message_send(userInfo['token'],channelInfo['channel_id'],"new message")
    channelMessages = channel_messages(userInfo['token'],channelInfo['channel_id'],0)
    #check index 0 contains 'message' : "new message"
    assert channelMessages['messages'][0]['message'] == "new message"
    msgID = channelMessages['messages'][0]['message_id']
    #if message_react() was implemented correctly, message_unreact would not raise an error.
    message_react(userInfo['token'],msgID,1)
    channelMessages = channel_messages(userInfo['token'],channelInfo['channel_id'],0)
    assert channelMessages['messages'][0]['reacts'][0]['is_this_user_reacted'] == True 
    message_unreact(userInfo['token'],msgID,1)
    clear()

        

