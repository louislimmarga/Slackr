# Teamwork

## Meetings

We decided that we will be meeting atleast 3 time everyweek, on Tuesday, Thursday and Friday. If we can't have a group meeting during either Tuesday or Friday, we will try to change it to another day during the same week. We felt like 3 times a week is enough to make sure everyone in the group is up do date to what everyone is doing in the group.

## Method

We did something similar to 'standup' as in the agile practice method, where each of us talk through what they have done since the last meeting, what trouble they are currently facing and what they are going to do about it. Then we as a group try to see whether we can come up with a better solution to the problem.

We also uses **Facebook messengers** so that we can communicate with the team wherever we are. 

## How we arrange multiple people working on same code

We split the project into 5 different code files:

- auth.py 
   - Contains all the auth/ functions. Were emphasised to be finished first, since all other functions needs to have a user before being able to be used.
- channel.py 
   - Contains all the channel/ functions.
- message.py 
   - Contains all the message/ functions.
- user.py 
   - Contains all the user/ functions.
- standup.py 
   - Contains standup/start and standup/send.
- search.py 
   - Contains search.
- userPermissionChange
   - contains admin/userpermission/change/.
   
Main reasons to do this so that we won't **have merge conflicts**, because each of us will be working on seperate files. If one of us have finished auth.py, we start integrating auth.py and channel.py (in AuthChannel.py) and then _test_ it. Then we would integrate AuthChannel.py with message.py (in AuthChannelMessage.py) and so on. By doing this, we are making sure our code successfully integrate with eachother from the start.

### Task Boards

We maintains communication on the functions we are doing by using the tasks board, which was filled with iteration 1 users stories. Each users story would correspond to one function, and the person who is doing that function need to assign himself to the user story in the task board. Then we would always need to indicate in what stage we are currently in e.g. **to do, doing, testing, or finished** by constantly updating the board.

## Plan

We try to simulate how agile **sprints/iterations** practice works. In a group meeting, we would plan what functions that we will need to finish by the time we have our next meeting. If one of us were unable to finish the work in time, the unfinished work would be added to the next iterations with additional new work to have a flexibility in our plans. During each iteration, we would also try to see whether there could be improvement in our planning e.g. whether we assigned too much task during one iteration that resulted in unfinished work. 
