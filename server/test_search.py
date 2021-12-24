import pytest
from changes.data_backend import reset_data
from changes.auth_backend import auth_register
from changes.channel_backend import channels_create, channel_invite
from changes.message_backend import message_send, message_react
from changes.search_backend import search
from clearDatabase import clear

def test_search ():
    reset_data()
    register_info = auth_register("feddrick100@yahoo.com","123456","Feddrick","Aquino")
    
    token = register_info["token"]

    channel_id1 = channels_create(token, "test1", 'true')    #assuming true = public
    channel_id2 = channels_create(token, "test2", 'true')
    
    message_send(token, channel_id1['channel_id'], "message in test 1")
    message_send(token, channel_id1['channel_id'], "distinct test")
    
    message_send(token, channel_id2['channel_id'], "message in test 2")
    channelMessage = message_send(token, channel_id2['channel_id'], "my own little message")

    message_react(token, channelMessage['message_id'], 1)

    all_messages = search(token, 'test')
    assert all_messages['messages'][0]['message'] == "distinct test"
    assert all_messages['messages'][1]['message'] == "message in test 1"
    assert all_messages['messages'][2]['message'] == "message in test 2"
    all_messages = search(token, 'little')
    assert all_messages['messages'][0]['message'] == "my own little message"
    all_messages = search(token, 'timtam')
    assert len(all_messages['messages']) == 0
    clear()

