import pytest
import datetime
from changes.data_backend import reset_data
from changes.auth_backend import auth_register
from changes.channel_backend import channels_create, channel_invite, channel_messages
from changes.standup_backend import standup_start, standup_send, standup_active
from clearDatabase import clear

def test_standup_active():
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
    
    #not an authorized user inside the channel trying to standup_active
    with pytest.raises(Exception):
        standup_active(token2, channel_id['channel_id'])

    #check status of a non active standup
    status = standup_active(token, channel_id['channel_id'])
    assert status['is_active'] == False

    time_finish = standup_start(token, channel_id['channel_id'], 0.1)

    #check status of an active standup
    status = standup_active(token, channel_id['channel_id'])
    assert status['is_active'] == True
    assert status['time_finish'] == time_finish['time_finish']

    clear()
