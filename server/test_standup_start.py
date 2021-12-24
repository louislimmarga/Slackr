import pytest
import datetime
import threading
import time
from changes.data_backend import reset_data
from changes.auth_backend import auth_register
from changes.channel_backend import channels_create, channel_invite, channel_messages, channel_join
from changes.standup_backend import standup_start, standup_send
from clearDatabase import clear

def test_standup_start():
    reset_data()
    register_info = auth_register("feddrick100@yahoo.com","123456","Feddrick","Aquino")

    token = register_info["token"]
    user_id = register_info["u_id"]

    #first user is admin

    register_info2 = auth_register("jasonjin@gmail.com","123456","Jason","Jin")

    token2 = register_info2["token"]
    user_id2 = register_info2["u_id"]

    #no channel_id
    with pytest.raises(Exception):
        time_finish = standup_start(token, 9884, 1)

    channel_id = channels_create(token, "test", 'true')    #assuming true = public
    
    #not an authorized user that has been invited
    with pytest.raises(Exception):
        time_finish = standup_start(token2, channel_id['channel_id'], 1)
    channel_join(token2, channel_id['channel_id'])
    time_finish = standup_start(token, channel_id['channel_id'], 0.3)
    with pytest.raises(Exception):
        standup_start(token, channel_id['channel_id'], 1)
    standup_send(token, channel_id['channel_id'], "a")
    standup_send(token2, channel_id['channel_id'], "b")
    time.sleep(0.5)
    channelMessages = channel_messages(token, channel_id['channel_id'], 0)
    standupMessage = channelMessages['messages'][0]['message']
    assert standupMessage == "feddrickaquino: a\njasonjin: b"
    
    clear()
    
