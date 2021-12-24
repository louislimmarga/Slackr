# Assurance.md

## Importance of verification and validation

In the second iteration, we need to implement the backend functions. This means that we need to verify and validate our functions to assure that the backend function is fit for purpose.


Verifications are done in order to make sure that our functions have been built right. We use several testing to verify our functions:


- Unit testing : The first test we did is unit testing. Since we grouped the functions separately according to their main route (such as user, channel, auth, messages), we tested the functions according to their main route. Unit testing needs to be done correctly to make sure that each module works as they are intended to. Therefore, we test all our functions individually as well as within their groups (e.g. auth/login and auth/logout are in one group, user/profile and user/profile/setname are in one group, etc) manually so we could control the data and evaluate the processes. We also test all possible cases to know that it meets its specification and behave as intended. However, we are still not sure that our functions could work when we integrate different group together.
- Integration testing : Integration testing occurs after unit testing. We integrate all our modules together and test it in order to evaluate and verify our functions. We make sure that each modules work with each other perfectly without any errors. Since we did unit testing before integration testing, we only encounter small error because of miscommunications. We tested our program by grouping together the groups(user, channel, auth, messages) in order to make a major part of the system and then test them. This approach saves time since we could immediately know if the functions do not work properly when integrated with other group. Black box testing will be used first in order to know if the functions work as intended. Then if there are some errors, we must fix our code in order to make sure that the functions work together and data could flow across the modules.
- System testing : We need to make sure that our backend code works with the frontend once we integrate them. We need to make sure that the backend does not cause any bug on the frontend of the program. We could not do much for system testing because it is a rather small project. The usability testing is obsolete since the frontend are made by the tutors. We could still test it on different operating system to make sure that it could work on different OS.


Validation refers to if the software satisfies and fits the inteded use which means that the software must meet the user requirements. Since we don't have any customers or users, we consider our own teammates as our customers and users. Firstly we integrate the backend and frontend, then we follow the specification of the project and compare it to slack so we could get a general idea what would be the user requirements. Then we tested all the functionality of our project. Once we are satisfied with how our project works, we stop the testing.


## Method 


We mainly test our function **manually** using:

*Advanced REST Client

*Postman

For every functions, after we have finished them, we would run the backend and start interacting with the function via the API client. For every different argument that we passed into the function, we would expect it to return a specific thing to the API client. If the function is working and returning something that is wrong, we would go back to the codes and look for what causes it to return the wrong value. If the functions return a 500 error, we know that something must be wrong in our code. 

We would also check for functions' error. We would deliberately send an invalid argument to the functions (e.g. invalid token, invalid u_id, etc...) and we would expect it to raises a 400 error on the backend. 

For a function that does not return anything, we would need to rely on other functions that allow us to test it. For example, to test whether **message/send** actually sends the right message to a channel, we would use **channel/messages** to check it.

 
### Importance


We would place emphasise on finishing a functions that allow us to test another functions first. This allows us to always have a way to test a function that we have just finished. For example, we would need to finish auth/register or auth/login before we can use channel/create, so we would momentarily focus our attention on finishing the auth functions first. This way of doing the function **step by step** make it more efficient to test our functions without having to wait for someone to finish their function first before an individual can actually test the functions they made.


### Scenario


Here a scenario on how we would test our function:


- Feddrick just finished message/send and now would like to test his functions. He run the backend, and open up Advanced REST Client.
- He would need first need to register, get the token, and create a channel using his token.
   - {'u_id': 52, 'token': 'randomToken'}
   - {'channel_id': 123}
- He then try to do send/message a valid message to the channel, but received an 500 error code on the backend. He stopped the server, went to look and fix a line of code that he forgot to put in.
- Now he run the server again, try to do message/send a message _"Feddrick first message"_ to the channel, and now it worked!
   - he get a dictionary {'message_id' : 1} 
   - Now he do channel/messages on the channel_id 123, and expect it to return a dictionary that contains _"Feddrick first message"_. But for some reason, the message that shows up in the list is empty.
   - So, he went back to his code, and found out that he forget to add a line to update the channel's data base to contain the new message.
   - He do all the steps above again now he got the right list containg _"Feddrick first message"_.
- He then continued testing his message/send by passing in a message with **more than 1000 characters**, and he got a **400** error code which is what he expected.


## User criteria

As an admin, I want to be able to make other user an admin so that I can have multiple admin.

    - During the process, the current admins should be listed      
    - If the person is already an admin, it should pop up a message

As a user, I want to be able to search for a message so that I could find the exact message that I am looking for easily. 

    - For any words with any length I enter, the closest result should instantly pop up
    - If there are no matching result, it should display something like 'nothing found'
    - For any results displayed, it should indicate the approximate time
    - Confirming search by enter

As a user, I want to be able to customise the handle of my profile so that I can change my current profile handle.

    - Before changing the handle, I should be able to see my current handle
    - If no change is made, it should pop up a quick message
    - If the profile handle is longer than 20 words, it should stop my action
    
As a user, I want to be able to edit my profile email address so that I can add or change my current profile email. 

    - If I didn't enter a valid email address, an alert message should appear
    - If the email I wish to add is already in use, it should indicate it
    
As a user, I want to be able to upload a photo to my profile so that I can have a profile picture.

    - I should be able to upload a load by selecting a path in the local machine
    - I should only be able to upload correct types of files Eg:JPG

As a user, I want to be able to edit my profile first and last name so that I can change my current name. 

    - Not just English but words from any language should be able to be entered
    - the system will stop my action if the first name or last name is 50 characters or longer

As a user, I want to be able to view someone's profile so that I can clearly see who is the user. 

    - I should be able to view the profile by clicking on peoples' icon
    - All the details such as email should instantaneously pop up as a I click

As a user, I want to be able to do a standup in a channel so that I can do a short progress update with other members of the channel.
    -
    -

As a user, I want to be able to send messages later so that I do not have to open the Slackr product when I want to send a message in the future. 

    - Should be able to decide the time delay of sending the message
    - it should display the available time delay options eg:1hr, 5hr, 1day...
    - If the message is sent, the user will get a get quick message
    - Should be able to cancel the message delay if the message has not been sent it

As a user, I want to be able to delete a message so that I can remove a message that I do not like.

    - When deleting a message, the system should be asking for a confirmation one more time just in case the user changes mind and it is an important message
    - Once the message is deleted, I should not be able find it using the search function
    
As a user, I want to be able to un-react to a message so that I can show that I do not like the message anymore   
   
    - clicking a message, there should be several options available eg: a sad face
    - Next time I log in, the sad face should still appear on the message
    - if the message is already being liked or displayed, I should be able to change it 

As a user, I want to be able to react to a message so that I can show that I do like the message 

    - clicking a message, there should be several options available eg: a smiley face
    - Next time I log in, the sad face should still appear on the message
    - if the message is already being liked or displayed, I should be able to change it 

As a user, I want to be able to unpin messages so that I do not have to keep track of messages that are not important anymore. 

    - Unpin message by double clicking the message
    - The unpined message should now be in the same font size, color as the other message
    
As a user, I want to be able to pin messages so that I can keep track of important messages.

    - Pin message by double clicking the important message
    - The message should now be surrounded with a default green color with the regular fone size and style
    - I should be able to modify the pin message setting Eg:pinned message will now be in red colour and bigger font size
    
As a user, I want to be able to edit messages so that I can correct my mistakes.

    - any valid inputs from the keyboard should be able to typed in
    - not just English but any other language should be able to typed in
    - finish typing and sending message to the opponent when I press enter
    - start the message on the new lines automatically when the number of characters exceed the limit
    - swap lines not when exceeded the limit but by also clicking ctrl enter

As an owner of a channel, I want to be able to make other member an owner of my channel so that I can have someone other than me in charge when I am absent.

    - I should be able to search the person who I want to make the owner of the channel just in case there are too many members
    - Once I make the other person the owner of the channel, I should instantly lose all the privilege all of an owner
    - The new owner should receive a system message of indication

As a user, I want to be able to join a channel I am currently not a member of so that I can start communicating with other members in the channel

    - I should be able to request to join a channel by searching for its channel id or channel name
    - As soon as the owner of the channel agress the joining request, I will receive a quick message
    - I should be able to explore all the chat history of a channel I joined channel
    - If the channel id or the channel name doesn't exist, it should pop up message such as 'channel does not exist'

As a member of a channel, I want to be able to send messages to the channel so that I can communicate with other members of the channel

    - any valid inputs from the keyboard should be able to typed in and sent
    - words from any language should be treated as valid inputs
    - GIFS or icons should also be available to send
    - able to send pictures by browing the local directory

As a member of a channel, I want to be able to see messages so that I can communicate with other members of the channel.

    - Unless the user gets kicked out, the user should be able to scroll up and see all the messages sent from all the users since the creation of the channel
    - The user should be able to search for a message and the closest matching term should pop up
    - Anything that could be done to the private message should be able to done to the channel message

As a member of a channel, I want to be able to see the channel name so that I know which channel I am currently at. 

    - If the channel name exceeds a certain length, I should be  able click it and view its full name
    - When I click the channel name, not just the name but its details such as channel_id, admin and owner should pop up
    
As a user, I want to be able to set the name of my channel so that I can organize the channel around a topic.

    - Channel name does not have to be necessarily in English, it can be any language
    - Channel name can not exceed a certain length
    - Channel name can be modified anytimes at any time by the channel owner
    
As a user, I want to see all the direct messages so that I can respond to other people in the shortest time.

    - The notificaiton sound for a direct message should be different to a channel message
    - There should be a number on every icon of a user's frind, indicating how many unread messages there are. If 0, no indication

As a user, I want to be able to set channel to be private so that I can prevent other unwanted user from joining my channel. 

    -Not just during the creation of a channel but the owner of the channel should be able to change a channel to private or public at any time he wanted
    -On the channel's setting page, there should be a selection for the user such that the owner can easily turn the channel to private or public simply by clicking once

As a member of a channel, I want to be able to leave a channel so that I can leave a channel I do not want to be in. 

    -I should be able to leave a channel simply by clicking the exit channel option the channel's setting page
    -Once quitted a channel, I should not be able to view the message any more and the channel icon's icon should be removed from the message list on the left recent messages side

As a member of a channel, I want to be able to see who are the owner and the admins of the channel so that I know who is in charge of the channel.

    -If a message was sent by the owner of a channel or an admin, there should be an indication near their icons. Eg: the owner's icon get coloured in green
    -I can also view the admins of a channel by clicking the channel name on the chatting interafacing and clicking the option view channel member details

As a member of a channel, I want to be able to see all the members in the channel so that I am aware of who I am communicating with in the channel

    -I can view all the admins of a channel by clicking the channel name on the channel anme and clicking the option 'view channel member details'
    -the admins, owner and the rest of the team members should be displayed with some difference

As a user, I want to be able to list all the channel that I am in so that I am able to access the channel that I want easily.

    -All the channel could be put into a category and all the friends of a user are put into a category such that when I click the channel's category, all the channels which I have joined are displayed
    -If I wish to access a channel, simply click the channel icon

As a user, I want to be able to browse all channel so that I can join a channel I am currently not a member of. 

    -There should be a option available on the interface called 'browse all channels' such that when I click, it displays all the public channels of the slackr app
    -Beside every channel, there should be an option such as 'join channel' so that I can request to join a channel

As a user, I want to be able to reset my password by receiving an system email so that I can recover my account in case I forgot my password. 

    -When I enter an email that doesnt belong to any user, it should pop up an alert message
    -If the email is valid, there should be a quick message poping up saying things like 'verificaiton email has been sent'
    -Once I click the reset password option on the login page, it will redirect me to a new page asking for my registered email

As a user, I want to be able to create a public channel so that I can communicate with other members.

    -During the creation of a channel, I should be select whether the channel is private or public simply by clicking one of the option
    
As a user, I want to be able to login with email and password so that I can use the Slackr product.

    -If the entered email does not exist, it should pop up a message saying 'email does not exist'
    -If the password is wrong, it should pop up a message saying 'wrong password'
    -If a wrong password has been entered 3 or more times in a row, pop up a message 'would you like to reset your password?'
    -confirm my input for email and password by pressing enter key or clicking the 'login' word the on the interface
    
As an unregistered user, I want to be able to register on the registration page by entering my first and last name so that I can start using the Slackr product

    -On the login page, the should be an option called 'register' available under the login word and when I click, it will take me to a new URL
    -On the new page, it will ask for my email, password, first name, last name
    -for password shorter than 6 characters or fist_name longer than 50 characters, it should pop up an alert message
    -If the email is already used, message such as 'email already in use should pop up'
    -a u_id will be generated for every user who has registered successfully
    
As a user, I want to be able to logout of my account so that other people can not access my account in my absence. 

    -I should be able to logout my account simply by clickin the logout button on the top right corner
    -After logged out, I should enter my email and password again if I wish to access the account 
