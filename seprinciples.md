# Software Engineering Principles

## Refactoring

In the end of iteration 2, we found out that our implementation of the backend is really **rigid and immobile**, because we have our backend functions immediately wrapped around with our flask server. Our implementation disallowed us to test our backend using pytest and so one of the major change that was made were pulling out our backend function from our flask server.

### Splitting backend and flask

The result that comes with our changes was instead of having one giant file containing all the backend and flask, we splitted it onto:

- One flask file, and
   - server.py
- Nine backend file
   - auth_backend.py, channel_backend.py, data_backend.py, helper_func.py, message_backend.py, search_backend.py, standup_backend.py, user_backend.py , user_permission_change.py.
   
This gave us tremendous flexibility as now we can actually create a pytest for each of this file, and easily assign the refactoring job to each of us. Now our code were significantly **less rigid and immobile**.

### DRY and Encapsulation through Decorators

We used decorator to apply the **Don't Repeat Yourself (DRY)** and **encapsulation** principle. Through decorators, we reduced the repitition of error checking and database access. The **benefit of encapsulation** comes if in the future we would want to change how we access our database, we would only need to edit what are inside the decorator instead of having to go through every function and edit them. An example showing how we changed our function through decorators.

**Iteration 2 code:**

```python
def channel_invite(uToken, currChannelID, invitedUserID):
    invitingUserInfo = decodeToken(uToken)
    invitingUserInfo = searchUserByEmail(invitingUserInfo['email'])
    checkUserLoggedIn(uToken, invitingUserInfo)
    currChannelInfo = searchChannelByID(currChannelID)
    if currChannelID not in invitingUserInfo['joinedChannel_id']:
        raise ValueError(description="Inviting user is not a part of channel_id passed in")
    invitedUserInfo = searchUserByID(invitedUserID)
    if invitedUserInfo is None:
        raise ValueError(description="u_id does not refer to valid user")
    if invitedUserID in currChannelInfo['members_id']:
        raise ValueError(description="Inviting an already member of the channel")
    currChannelInfo['members_id'].append(invitedUserInfo['u_id'])
    invitedUserInfo['joinedChannel_id'].append(currChannelInfo['channel_id'])
    save()
    return {}
```

**Iteration 3 code:**

```python
def get_userInfo(function):
    def wrapper(token=None, *args, **kwargs):
        user_info = decodeToken(token)
        user_info = searchUserByEmail(user_info['email'])  
        checkUserLoggedIn(token, user_info)
        return function(user_info, *args, **kwargs)
    return wrapper
    
def channel_invite_argument_valid(function):
    def wrapper(user_info, channel_id=None, invited_user_id=None):
        invited_user_info = searchUserByID(invited_user_id)
        channel_info = searchChannelByID(channel_id)
        if channel_id not in user_info['joinedChannel_id']:
            raise AccessError(description="User is not part of channel")
        if invited_user_info is None:
            raise ValueError(description="u_id does not refer to valid user")
        if invited_user_id in channel_info['members_id']:
            raise ValueError(description="Inviting an already member of the channel")
        return function(user_info, channel_info, invited_user_info)
    return wrapper

@get_userInfo
@channel_invite_argument_valid
def channel_invite(invitingUserInfo, currChannelInfo, invitedUserInfo):
    currChannelInfo['members_id'].append(invitedUserInfo['u_id'])
    invitedUserInfo['joinedChannel_id'].append(currChannelInfo['channel_id'])
    save()
    return {}
```

As you can see, the channel_invite for iteration 3 shrunk from really many line of code to only 4. The function now would **only** need to worry about how to actually manipulate the database to invite someone to a given channel. Every error checking and access to database were taken care by the decorators **get_userInfo and channel_invite_argument_valid**. And other functions would also able to utilize the **get_userInfo** decorator too, which would result in overall less repetition in accessing the database. Some function e.g. channels_list and channels_listall can have the same decorator for error checking, which also reduces the repetition in error checking.
