import pytest
from changes.data_backend import reset_data
from changes.auth_backend import auth_register
from changes.channel_backend import channels_create, channel_messages, channel_join, channel_addowner
from changes.message_backend import message_remove, message_send
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
        message_remove("randomToken",msgID)
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
    #second user, who is not a member the channel, trying to remove a message from the channel
        message_remove(secondUserInfo['token'],msgID)
    clear()
    
def test_not_existing_message_id():
    reset_data()
    userInfo = auth_register("ivanny@yahoo.com",'ivannyPassword',"Ivanny","Lestari")
    channelInfo = channels_create(userInfo['token'],"Ivanny chnl",'true')
    with pytest.raises(Exception):
    #passing in a random non-existant message_id
        message_remove(userInfo['token'], 7412)
    clear()
    
def test_user_removing_others_message():
    reset_data()
    firstUserInfo = auth_register("john@yahoo.com",'johnPassword',"John","Ghalagar")
    secondUserInfo = auth_register("adam@yahoo.com",'adamPassword',"Adam","Lambert")
    #first user create a public channel then second user joins it
    channelInfo = channels_create(firstUserInfo['token'],"John's Channel",'true')
    channel_join(secondUserInfo['token'],channelInfo['channel_id'])
    
    message_send(firstUserInfo['token'],channelInfo['channel_id'],"new message")
    
    channelMessages = channel_messages(firstUserInfo['token'],channelInfo['channel_id'],0)
    #check index 0 contains 'message' : "new message"
    assert channelMessages['messages'][0]['message'] == "new message"
    msgID = channelMessages['messages'][0]['message_id']
    
    with pytest.raises(Exception):
    #second user trying to remove first user message (which is message coming from an admin and owner of the channel)
        message_remove(secondUserInfo['token'],msgID)
    clear()
    
def test_user_remove_non_admin_message():
    reset_data()
    firstUserInfo = auth_register("joseph@yahoo.com",'josephPassword',"Joseph","Jacobs")
    secondUserInfo = auth_register("John@yahoo.com",'johnPassword',"John","Stone")
    #first user create a public channel then second user joins it
    channelInfo = channels_create(firstUserInfo['token'],"Joseph's Channel",'true')
    channel_join(secondUserInfo['token'],channelInfo['channel_id'])
    #first user make second user an owner of the channel
    channel_addowner(firstUserInfo['token'],channelInfo['channel_id'],secondUserInfo['u_id'])
    #second user, who is now an owner, send a message to channel
    message_send(secondUserInfo['token'],channelInfo['channel_id'],"new message")
    
    channelMessages = channel_messages(secondUserInfo['token'],channelInfo['channel_id'],0)
    #check index 0 contains 'message' : "new message"
    assert channelMessages['messages'][0]['message'] == "new message"
    msgID = channelMessages['messages'][0]['message_id']
    
    message_remove(secondUserInfo['token'],msgID)
    clear()
    
def test_user_remove_non_owner_message():
    reset_data()
    firstUserInfo = auth_register("alex@yahoo.com",'alexPassword',"Alex","Johnston")
    secondUserInfo = auth_register("tim@yahoo.com",'timPassword',"Tim","Smith")
    
    #second user create a public channel then first user joins it
    channelInfo = channels_create(secondUserInfo['token'],"Tim's Channel",'true')
    channel_join(firstUserInfo['token'],channelInfo['channel_id'])
    #first user, who is an admin of slackr but not an owner of the channel, send a message to the channel
    message_send(firstUserInfo['token'],channelInfo['channel_id'],"new message")
    
    channelMessages = channel_messages(firstUserInfo['token'],channelInfo['channel_id'],0)
    #check index 0 contains 'message' : "new message"
    assert channelMessages['messages'][0]['message'] == "new message"
    msgID = channelMessages['messages'][0]['message_id']
    
    message_remove(firstUserInfo['token'],msgID)
    clear()
    
def test_message_remove_working():
    reset_data()
    firstUserInfo = auth_register("Lenny@yahoo.com",'lennyPassword',"Lenny","Hu")
    channelInfo = channels_create(firstUserInfo['token'],"Lenny's Channel",'true')
    message_send(firstUserInfo['token'],channelInfo['channel_id'],"new message")
    
    channelMessages = channel_messages(firstUserInfo['token'],channelInfo['channel_id'],0)
    #check index 0 contains 'message' : "new message"
    assert channelMessages['messages'][0]['message'] == "new message"
    msgID = channelMessages['messages'][0]['message_id']
    #first user (who sent the message, is an owner of the channel, and an admin of slackr) is removing his message
    message_remove(firstUserInfo['token'],msgID)
    
    with pytest.raises(Exception):
        channelMessages = channel_messages(firstUserInfo['token'],channelInfo['channel_id'],0)
        
    message_send(firstUserInfo['token'],channelInfo['channel_id'],"first message")
    message_send(firstUserInfo['token'],channelInfo['channel_id'],"second message")
    message_send(firstUserInfo['token'],channelInfo['channel_id'],"third message")
    channelMessages = channel_messages(firstUserInfo['token'],channelInfo['channel_id'],0)
    #getting the message_id of "second message" and remove it from the channel
    assert channelMessages['messages'][0]['message'] == "third message"
    assert channelMessages['messages'][1]['message'] == "second message"
    assert channelMessages['messages'][2]['message'] == "first message"
    
    msgID = channelMessages['messages'][1]['message_id']
    message_remove(firstUserInfo['token'],msgID)
    
    #now checking whether the "second message" is gone now.
    channelMessages = channel_messages(firstUserInfo['token'],channelInfo['channel_id'],0)
    assert channelMessages['messages'][0]['message'] == "third message"
    assert channelMessages['messages'][1]['message'] == "first message"
    clear()



        

    
