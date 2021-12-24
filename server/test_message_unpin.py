import pytest
from changes.user_permission_change import admin_userpermission_change
from changes.data_backend import reset_data
from changes.auth_backend import auth_register
from changes.channel_backend import channels_create, channel_messages, channel_join, channel_addowner
from changes.message_backend import message_pin, message_unpin, message_send
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
    message_pin(userInfo['token'],msgID)
    with pytest.raises(Exception):
    #above codes generate a valid msgID that has been PINNED so that i can be sure the function below raises Exception solely from an invalid token
        message_unpin("randomToken",msgID)
    clear()
    
def test_user_not_member_of_channel():
    reset_data()
    firstUserInfo = auth_register("dedy@yahoo.com",'dedyPassword',"Dedy","Hariady")
    secondUserInfo = auth_register("panny@yahoo.com",'pannyPassword',"Panny","Lai")
    #first user make second user an admin
    admin_userpermission_change(firstUserInfo['token'],secondUserInfo['u_id'],2)
    
    channelInfo = channels_create(secondUserInfo['token'],"Panny's Channel",'true')
    message_send(secondUserInfo['token'],channelInfo['channel_id'],"new message")
    
    channelMessages = channel_messages(secondUserInfo['token'],channelInfo['channel_id'],0)
    #check index 0 contains 'message' : "new message"
    assert channelMessages['messages'][0]['message'] == "new message"
    msgID = channelMessages['messages'][0]['message_id']
    #since the message is valid, the message has not been pinned yet, second user is an admin of slackr and a member of the channel, the function below should work
    message_pin(secondUserInfo['token'],msgID)
    with pytest.raises(Exception):
    #first user, who is a slackr admin but not a member of the channel, trying to unpin a message from the channel
        message_unpin(firstUserInfo['token'],msgID)
    clear()
    
def test_not_existing_message_id():
    reset_data()
    userInfo = auth_register("ivanny@yahoo.com",'ivannyPassword',"Ivanny","Lestari")
    channelInfo = channels_create(userInfo['token'],"Ivanny's Channel",'true')
    with pytest.raises(Exception):
    #passing in a random non-existant message_id
        message_unpin(userInfo['token'],7412)
    clear()
    
def test_user_not_admin():
    reset_data()
    firstUserInfo = auth_register("Larry@yahoo.com",'larryPassword',"Larry","Crab")
    secondUserInfo = auth_register("teresa@yahoo.com",'teresaPassword',"Teresa","Wu")
    
    #second user created a channel. first user join the channel and second user send message to the channel
    channelInfo = channels_create(secondUserInfo['token'],"Teresa's Channel",'true')
    channel_join(firstUserInfo['token'],channelInfo['channel_id'])
    message_send(secondUserInfo['token'],channelInfo['channel_id'],"new message")
    
    channelMessages = channel_messages(secondUserInfo['token'],channelInfo['channel_id'],0)
    #check index 0 contains 'message' : "new message"
    assert channelMessages['messages'][0]['message'] == "new message"
    msgID = channelMessages['messages'][0]['message_id']
    #first user pins the message
    message_pin(firstUserInfo['token'],msgID)
    with pytest.raises(Exception):
    #second user, who are a member of the channel but not an admin of slackr, tries to unpin his message
        message_unpin(secondUserInfo['token'],msgID)
    clear()
    
def test_unpinning_already_unpinned_message():
    reset_data()
    userInfo = auth_register("reynold@yahoo.com",'ryanPassword',"Ryan","Reynold")
    channelInfo = channels_create(userInfo['token'],"Ryan's Channel",'true')
    message_send(userInfo['token'],channelInfo['channel_id'],"new message")
    channelMessages = channel_messages(userInfo['token'],channelInfo['channel_id'],0)
    #check index 0 contains 'message' : "new message"
    assert channelMessages['messages'][0]['message'] == "new message"
    msgID = channelMessages['messages'][0]['message_id']
    
    with pytest.raises(Exception):
    #user is unpinning a message that has not been pinned yet
        message_unpin(userInfo['token'],msgID)
        
    message_pin(userInfo['token'],msgID)
    message_unpin(userInfo['token'],msgID)
    
    with pytest.raises(Exception):
    #user is unpinning an already unpinned message
        message_unpin(userInfo['token'],msgID)
    clear()
    
def test_message_unpin_working():
    reset_data()
    userInfo = auth_register("marry@yahoo.com",'marryPassword',"Marry","Riana")
    channelInfo = channels_create(userInfo['token'],"Marry's Channel",'true')
    message_send(userInfo['token'],channelInfo['channel_id'],"new message")
    channelMessages = channel_messages(userInfo['token'],channelInfo['channel_id'],0)
    #check index 0 contains 'message' : "new message"
    assert channelMessages['messages'][0]['message'] == "new message"
    msgID = channelMessages['messages'][0]['message_id']
    #User pins his message, and unpin his message. If message_unpin() is implemented correctly, then the second time the user do message_pin would work.
    message_pin(userInfo['token'],msgID)
    message_unpin(userInfo['token'],msgID)
    message_pin(userInfo['token'],msgID)
    clear()
    
