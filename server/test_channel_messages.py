import pytest
from changes.data_backend import reset_data
from changes.auth_backend import auth_register, auth_login
from changes.channel_backend import channels_create, channel_messages
from changes.message_backend import message_send
from clearDatabase import clear

def test_channel_id_not_exist():
    reset_data()
    register_info = auth_register("feddrickaquino@gmail.com","myPassword","Feddrick","Aquino")
    #I assume initially, there are no channel exist. So initially, when i call channel_messages() with any channel_id, i will get error.
    with pytest.raises(Exception):
        channel_messages(register_info["token"],909808,"40")
    clear()
           
def test_channel_start_exceed():
    reset_data()
    register_info = auth_register("feddrick90@gmail.com","myPassword","Feddrick","Aquino")
    #made channel is public
    channelInfo = channels_create(register_info["token"],"myChannelName",'true')
    #I assume that when i do channels_create, I would immediately be a member/owner of the channel
    
    message_send(register_info["token"],channelInfo["channel_id"],"first message")
    message_send(register_info["token"],channelInfo["channel_id"],"second message")
    
    with pytest.raises(Exception):
        channel_messages(register_info["token"],channelInfo["channel_id"],3)
    with pytest.raises(Exception):
        channel_messages(register_info["token"],channelInfo["channel_id"],10)
    clear()
    
def test_user_not_member_of_channel():
    reset_data()
    firstUserInfo = auth_register("Teddy@gmail.com","myPassword","Teddy","Bear")
    secondUserInfo = auth_register("Sally@yahoo.com","validPassword","Sally","Tris")
    #first user create a channel
    channelInfo = channels_create(firstUserInfo["token"],"newChannel",'true')
    #first user send some random message to the channel
    message_send(firstUserInfo["token"],channelInfo["channel_id"],"first message")
    
    with pytest.raises(Exception):
    #second user who is not member of the channel try to call channel_messages
        channel_messages(secondUserInfo["token"],channelInfo["channel_id"],0)
    clear()
    
def test_channel_messages_working():
    reset_data()
    registerInfo = auth_register("bob@gmail.com", "bobPassword", "Bob", "Marley")
    channelInfo = channels_create(registerInfo["token"],"myChannelName",'true')
    
    message_send(registerInfo["token"],channelInfo["channel_id"],"first message")
    message_send(registerInfo["token"],channelInfo["channel_id"],"second message")
    message_send(registerInfo["token"],channelInfo["channel_id"],"third message")
    
    channelMessages = channel_messages(registerInfo["token"],channelInfo["channel_id"],0)
    assert channelMessages['start'] == 0
    assert channelMessages['end'] == -1
    #testing the 0 index is the index containing 'message': "third message"
    assert channelMessages['messages'][0]['u_id'] == registerInfo['u_id']
    assert channelMessages['messages'][0]['message'] == "third message"
    #testing the 1 index is the index conatining 'message': "second message"
    assert channelMessages['messages'][1]['u_id'] == registerInfo['u_id']
    assert channelMessages['messages'][1]['message'] == "second message"
    #testing the 2 index is the index conatining 'message': "first message"
    assert channelMessages['messages'][2]['u_id'] == registerInfo['u_id']
    assert channelMessages['messages'][2]['message'] == "first message"
    #we assume that we will return the messages in the form of a LIST OF DICTIONARY with the 0 index to be the most recent message
    '''assert returnedMessage == {'messages' : ["third message","second message","first message"], 'start' : 0, 'end' : -1}'''
    
    
    for i in range(12):
        message_send(registerInfo["token"],channelInfo["channel_id"],"aa")
        message_send(registerInfo["token"],channelInfo["channel_id"],"bb")
        message_send(registerInfo["token"],channelInfo["channel_id"],"cc")
        message_send(registerInfo["token"],channelInfo["channel_id"],"dd")
    #the bottom line of code sent the 51st message in the channel
    
    channelMessages = channel_messages(registerInfo["token"],channelInfo["channel_id"],0)
    
    assert channelMessages['start'] == 0
    assert channelMessages['end'] == 50
    #testing the 0 index is the index containing 'message': "third message"
    assert channelMessages['messages'][0]['u_id'] == registerInfo['u_id']
    assert channelMessages['messages'][0]['message'] == "dd"
    
    assert channelMessages['messages'][1]['u_id'] == registerInfo['u_id']
    assert channelMessages['messages'][1]['message'] == "cc"
    
    assert channelMessages['messages'][2]['u_id'] == registerInfo['u_id']
    assert channelMessages['messages'][2]['message'] == "bb"
    
    assert channelMessages['messages'][49]['u_id'] == registerInfo['u_id']
    assert channelMessages['messages'][49]['message'] == "second message"
    clear()
        
    
    
        

        


