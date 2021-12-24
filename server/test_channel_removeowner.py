import pytest
from changes.data_backend import reset_data
from changes.auth_backend import auth_register
from changes.channel_backend import channels_create, channel_addowner, channel_removeowner, channel_join
from clearDatabase import clear

#check valid token first
def test_invalid_token():
    reset_data()
    userInfo = auth_register("feddrickaquino@hotmail.com","myPassword","Feddrick","Aquino")
    channelInfo = channels_create(userInfo['token'],"Feddrick's Channel",False)
    with pytest.raises(Exception):
    #passed a random invalid token
        channel_removeowner(token="randomToken",channel_id=channelInfo['u_id'],to_be_removed_owner_id=userInfo['u_id'])
    clear()
         
#if token valid, check channel exist
def test_channel_not_exist():
    reset_data()
    userInfo = auth_register("feddrick@hotmail.com","myPassword","Feddrick","Aquino")
    with pytest.raises(Exception):
    #passed a channel_id that does not exist
        channel_removeowner(token=userInfo['token'],channel_id=123,to_be_removed_owner_id=userInfo['u_id'])       
    clear()
         
 #if token valid and channel exist, check whether the calling user a member of the channel       
def test_non_member_call_function():
    reset_data()
    firstUserInfo = auth_register("tonyStark@hotmail.com","tonyPassword","Tony","Stark")
    secondUserInfo = auth_register("tomHolland@hotmail.com","tomHollandPassword","Tom","Holland")
    
    channelInfo = channels_create(firstUserInfo['token'],"Tony's Channel", False)
    
    with pytest.raises(Exception):
        channel_removeowner(token=secondUserInfo['token'],channel_id=channelInfo['channel_id'],to_be_removed_owner_id=firstUserInfo['u_id'])
    clear()
      
#if calling user a member of channel, check whether he is the owner of the channel 
def test_not_owner_call_function():
    reset_data()
    firstUserInfo = auth_register("marvelyn@hotmail.com","marvelynPassword","Mar","Velyn")
    secondUserInfo = auth_register("tomHardy@hotmail.com","tomPassword","Tom","Hardy")
    #first user create a public channel
    channelInfo = channels_create(firstUserInfo['token'],"Cool Channel", 'true')
    #second user join the public channel
    channel_join(secondUserInfo['token'],channelInfo['channel_id'])
    with pytest.raises(Exception):
    #second user, who is just a member, try to channel_removeowner() the ownership of the first user. This would result in AccessError.
        channel_removeowner(token=secondUserInfo['token'],channel_id=channelInfo['channel_id'],to_be_removed_owner_id=firstUserInfo['u_id'])
        
    clear()

#test when a member of slackr trying to remove ownership of
#slackr admin/owner in a channel   
def test_owner_remove_ownership_slackr_admin_owner_in_channel():
    reset_data()
    firstUserInfo = auth_register("jim@hotmail.com","marvelynPassword","Jimmy","Recipe")
    secondUserInfo = auth_register("tam@hotmail.com","tomPassword","Tam","Hardy")
    #first user create a public channel
    channelInfo = channels_create(firstUserInfo['token'],"Cool Channel", 'true')
    #second user join the public channel
    channel_join(secondUserInfo['token'],channelInfo['channel_id'])
    channel_addowner(firstUserInfo['token'], channelInfo['channel_id'], secondUserInfo['u_id'])
    with pytest.raises(Exception):
    #second user, who is now an owner of the channel, try to channel_removeowner() the ownership of the first user. This would result in AccessError.
        channel_removeowner(token=secondUserInfo['token'],channel_id=channelInfo['channel_id'],to_be_removed_owner_id=firstUserInfo['u_id'])
    clear() 
    
#if everything on top satisfied, check whether the "to be removed ownership" user is a member of the channel
def test_addowner_to_non_member():
    reset_data()
    firstUserInfo = auth_register("chrisHemsworth@hotmail.com","chrisPassword","Chris","Hemsworth")
    
    channelInfo = channels_create(firstUserInfo['token'],"Chris' Channel", False)
    
    with pytest.raises(Exception):
    #random non-existant user id
        channel_removeowner(token=firstUserInfo['token'],channel_id=channelInfo['channel_id'],to_be_removed_owner_id=5321666)
    clear()
    
#if the user is a member, check whether he is a non-owner i.e. default member
def test_already_an_owner():
    reset_data()
    firstUserInfo = auth_register("dedy@hotmail.com","dedyPassword","Dedy","Hari")
    secondUserInfo = auth_register("marlon@yahoo.com","marlonPassword","Marlon","Brando")
    #create a public channel and second user joins it
    channelInfo = channels_create(firstUserInfo['token'],"myChannel",'true')
    channel_join(secondUserInfo['token'],channelInfo['channel_id'])
    
    with pytest.raises(Exception):
    #an owner is removing ownership from a non-owner member
        channel_removeowner(token=firstUserInfo['token'],channel_id=channelInfo['channel_id'],to_be_removed_owner_id=secondUserInfo['u_id'])
    clear()
         
def test_channel_removeowner_working():
    reset_data()
    firstUserInfo = auth_register("Adam@hotmail.com","adamPassword","Adam","Reynold")
    secondUserInfo = auth_register("Cody@yahoo.com","codyPassword","Cody","Walker")
    thirdUserInfo = auth_register("Damien@yahoo.com","damienPassword","Damien","Cook")
    #create a public channel and second and third users join it
    channelInfo = channels_create(firstUserInfo['token'],"Adam Channel",'true')
    channel_join(secondUserInfo['token'],channelInfo['channel_id'])
    channel_join(thirdUserInfo['token'],channelInfo['channel_id'])
    #first user make second user an owner of the channel
    channel_addowner(token=firstUserInfo['token'],channel_id=channelInfo['channel_id'],to_be_owner_id=secondUserInfo['u_id'])
    #second user make third an owner (to show that channel_addowner() working i.e. second user is really an owner)
    channel_addowner(token=secondUserInfo['token'],channel_id=channelInfo['channel_id'],to_be_owner_id=thirdUserInfo['u_id'])
    #first user remove ownership from second and third user
    channel_removeowner(token=firstUserInfo['token'],channel_id=channelInfo['channel_id'],to_be_removed_owner_id=secondUserInfo['u_id'])
    channel_removeowner(token=firstUserInfo['token'],channel_id=channelInfo['channel_id'],to_be_removed_owner_id=thirdUserInfo['u_id'])
    with pytest.raises(Exception):
    #second user, who ownership was removed, try to channel_addowner() third user. This should give me an AccessError.
        channel_addowner(token=secondUserInfo['token'],channel_id=channelInfo['channel_id'],to_be_owner_id=thirdUserInfo['u_id'])
    clear()
    
        

        
