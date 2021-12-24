import pytest
import datetime
from changes.data_backend import reset_data
from changes.auth_backend import auth_register
from changes.channel_backend import channels_create, channel_invite, channel_messages
from changes.standup_backend import standup_start, standup_send
from clearDatabase import clear

def test_standup_send():
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
        time_finish = standup_start(token, 1, 60)

    channel_id = channels_create(token, "test", 'true')    #assuming true = public

    #no standup is running
    with pytest.raises(Exception):
        standup_send(token, channel_id['channel_id'], "HELLO")

    #not an authorized user that has been invited
    with pytest.raises(Exception):
        time_finish = standup_start(token2, channel_id['channel_id'], 60)
    
    #we assume that standup function will return all the messages sent during the 15 minute window in one message seperated by \n

    time_finish = standup_start(token, channel_id['channel_id'], 0.1)
    standup_send(token, channel_id['channel_id'], "Hello how are you")
    myMessage = ''

    #not an authorized user is trying to standup_send
    with pytest.raises(Exception):
        standup_send(token2, channel_id['channel_id'], "HELLLLLLLLLO")

    for i in range(1001):
        myMessage = myMessage + 'a'
    with pytest.raises(Exception):
        standup_send(token, channel_id['channel_id'], myMessage)
    clear()
