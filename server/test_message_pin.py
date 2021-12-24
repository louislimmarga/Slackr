import pytest
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
    
    with pytest.raises(Exception):
    #above codes generate a valid msgID so that i can be sure the function below raises Exception solely from an invalid token
        message_pin("randomToken",msgID)
    clear()

def test_user_not_member_of_channel():
    reset_data()
    firstUserInfo = auth_register("dedy@yahoo.com",'dedyPassword',"Dedy","Hariady")
    secondUserInfo = auth_register("panny@yahoo.com",'pannyPassword',"Panny","Lai")
    
    channelInfo = channels_create(secondUserInfo['token'],"Panny's Channel",'true')
    message_send(secondUserInfo['token'],channelInfo['channel_id'],"new message")
    
    channelMessages = channel_messages(secondUserInfo['token'],channelInfo['channel_id'],0)
    #check index 0 contains 'message' : "new message"
    assert channelMessages['messages'][0]['message'] == "new message"
    msgID = channelMessages['messages'][0]['message_id']
    
    with pytest.raises(Exception):
    #first user, who is a slackr admin but not a member of the channel, trying to pin a message from the channel
        message_pin(firstUserInfo['token'],msgID)
    clear()

def test_not_existing_message_id():
    reset_data()
    userInfo = auth_register("ivanny@yahoo.com",'ivannyPassword',"Ivanny","Lestari")
    channelInfo = channels_create(userInfo['token'],"Ivanny's Channel",'true')
    with pytest.raises(Exception):
    #passing in a random non-existant message_id
        message_pin(userInfo['token'],7412)
    clear()

def test_user_not_admin():
    reset_data()
    firstUserInfo = auth_register("Larry@yahoo.com",'larryPassword',"Larry","Crab")
    secondUserInfo = auth_register("teresa@yahoo.com",'teresaPassword',"Teresa","Wu")
    
    channelInfo = channels_create(secondUserInfo['token'],"Teresa's Channel",'true')
    message_send(secondUserInfo['token'],channelInfo['channel_id'],"new message")
    
    channelMessages = channel_messages(secondUserInfo['token'],channelInfo['channel_id'],0)
    #check index 0 contains 'message' : "new message"
    assert channelMessages['messages'][0]['message'] == "new message"
    msgID = channelMessages['messages'][0]['message_id']
    
    with pytest.raises(Exception):
    #second user, who are a member of the channel but not an admin of slackr, tries to pin his message
        message_pin(secondUserInfo['token'],msgID)
    clear()
    
def test_pinning_already_pinned_message():
    reset_data()
    userInfo = auth_register("reynold@yahoo.com",'ryanPassword',"Ryan","Reynold")
    channelInfo = channels_create(userInfo['token'],"Ryan's Channel",'true')
    message_send(userInfo['token'],channelInfo['channel_id'],"new message")
    channelMessages = channel_messages(userInfo['token'],channelInfo['channel_id'],0)
    #check index 0 contains 'message' : "new message"
    assert channelMessages['messages'][0]['message'] == "new message"
    msgID = channelMessages['messages'][0]['message_id']
    
    message_pin(userInfo['token'],msgID)
    with pytest.raises(Exception):
    #user is pinning an already pinned message
        message_pin(userInfo['token'],msgID)
    clear()
    
def test_message_pin_working():
    reset_data()
    userInfo = auth_register("marry@yahoo.com",'marryPassword',"Marry","Riana")
    channelInfo = channels_create(userInfo['token'],"Marry's Channel",'true')
    message_send(userInfo['token'],channelInfo['channel_id'],"new message")
    channelMessages = channel_messages(userInfo['token'],channelInfo['channel_id'],0)
    #check index 0 contains 'message' : "new message"
    assert channelMessages['messages'][0]['message'] == "new message"
    msgID = channelMessages['messages'][0]['message_id']
    #User pins his message, and if the function is implemented correctly, message_unpin() would not raises an exception. And just to be explicit, after user unpin the message, user should be able to pin the message again.
    message_pin(userInfo['token'],msgID)
    message_unpin(userInfo['token'],msgID)
    message_pin(userInfo['token'],msgID)
    clear()

        

