1. We assume that we are going raise an exception when a function is passed in an invalid token.
2. We assume that initially, there is no user. So every email that we passes into auth_login initially will raise an exception.
3. We assume that initially, there are no channel exist. So everytime we call the function channel_invite(), channel_details(), channel_messages(), channel_leave(), channel_join(), channel_addowner(), channel_removeowner(), message_sendlater() and standup_start().
4. We assume that, if I am a user, once I did channels_create(), I would immediately be the owner/member of the channel.
5. We assume that message_send() will raise an error if the calling user is not part of the "channel_id" passed into the function.
6. We assume that we will be building our own AccessError.
7. For channel_messages, we assume that we will be returning the value of the 'messages' key in a LIST OF DICTIONARY with the 0 index as the most recent message in the channel.
8. We assume message_send() raises an Exception when: the channel_id does not exist; and the user calling the function is not a member of the channel_id.
9. We assume a user need to be only an owner of a channel(i.e. he does not need to be owner of slackr) to be able to call channel_addowner().
10. We assume someone need to join a channel first before becoming an owner of the channel.
11. We assume channel_messages() will return an empty list in the value of 'messages' key if there are no message in the channel. (to test message_remove)
12. We assume that, the only valid react_id is 1. This react_id of 1 would correspond to the "thumbs up" react that UNSW has asked for. Other than 1, it would be an invalid react_id
