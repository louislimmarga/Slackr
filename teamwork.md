# Teamwork

## Meetings

We decided that we will be meeting atleast 3 time everyweek, on Tuesday, Thursday and Friday. If we can't have a group meeting during either Tuesday or Friday, we will try to change it to another day during the same week. We felt like 3 times a week is enough to make sure everyone in the group is up do date to what everyone is doing in the group and give plenty amount of time to refactor our code.

## Agile Practices

### Standups

We did something similar to **standup** as in the agile practice method, where each of us talk through what they have done since the last meeting, what trouble they are currently facing and what they are going to do about it. Then we as a group try to see whether we can come up with a better solution to the problem. Main reason we did this is that we found this practice to be the most effective way in expressing what we have done and what problem we encountered before this meeting.

### Sprints

We try to simulate how agile **sprints/iterations** practice works. In a group meeting, we would plan what functions we need to finish refactoring before the next meeting. If one of us were unable to finish the work in time, the unfinished work would be added to the next iterations with additional new work to have a flexibility in our plans. During each iteration, we would also try to see whether there could be improvement in our planning e.g. whether we assigned too much task during one iteration that resulted in unfinished work. 

### Pair Programming

During our meeting, we would often do pair programming. We found that this method allowed us to generate more idea with better quality when we were refactoring our codes.

## When things did not go as planned

We would arrange an extra meeting to discuss about what the issue is. During this meeting, we would come up with a solution as a group and if possible, resolve the issue during the meeting. If face-to-face meeting is not possible, we would resolve it through Facebook messenger.

## How we arrange multiple people working on same code

We split the project into 9 different code files:

- auth_backend.py 
   - Contains all the auth/ functions.
- channel_backend.py 
   - Contains all the channel/ functions.
- data_backend.py
   - Contains all of our database i.e. global variables that we used to store data.
- helper_func.py
   - Contains all helper functions that we made.
- message_backend.py 
   - Contains all the message/ functions.
- search_backend.py 
   - Contains search function.
- standup_backend.py 
   - Contains standup/start, standup/send, and standup/active.
- user_backend.py 
   - Contains all the user/ functions.
- user_permission_change
   - contains admin/userpermission/change/.

Main reasons to do this so that we **won't have merge conflicts**, because each of us will be working on seperate files. We would assign each of us at least 1 file to be refactored. 

## Task Boards

We maintains communication on the functions we are doing by using the tasks board in gitlab. Each task in the board would correspond to one function, and the person who is doing that function need to assign himself to the task in the gitlab task board. Then, if someone is working on refactoring a function, he would need to add the task to the **Refactoring** column and once he finished, he would need to close the task.
