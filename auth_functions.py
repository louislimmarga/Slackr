#flasks staff
from flask import Flask, request
from json import dumps
import re
import random
import string
import hashlib

app = Flask(__name__)

def valid_email():
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if(re.search(regex,email)):  
        return True 
          
    else:  
        return False
        
users_list = {'users': []} 


def get_users_list():
    global users_list
    return users_list
    
    
def random_string():
    ran_number = random.randint(1,6)
    letters= string.ascii_lowercase
    return ''.join(random.sample(letters,ran_number))    

def new_handle(uFirstName, uLastName):
    new_list = get_users_list()
    handle = uFirstName.lower() + uLastName.lower()
    if len(handle) > 20:
        handle = handle[0:20]
    number = len(new_list['users'])
    for i in number:
        if new_list['users'][i]['handle'] == handle:
            rand_letters = random_string()
            handle = handle + rand_letters
    return handle           

def newID():
    new_list = get_users_list()
    Id = random.randint(1,10000)
    length = len(new_list['users'])
    for i in length:
        if new_list['users'][i]['u_id'] == Id:
            Id = random.randint(1, 10000)
    return ID
    
def EncodeToken(dictionary):
    global secret
    jwt.encode(dictionary, SECRET, algorithm='HS256').decode('utf-8')
    

@app.route('/auth/register/', methods = ['POST'])
def auth_register():
    new_list = get_users_list()
    uEmail = request.form.get('Email')
    uPassword = request.form.get('password')
    uFirstName = request.form.get('FirstName')
    uLastName = request.form.get('LastName')
    if valid_email(uEmail) is False:
        raise ValueError(Descrption == 'Email entered is not a valid email')
    for i in usersList['users']['Email']:
        if i == uEmail:
            raise ValueError(Description== 'Email address is already being used by another user')
    if len(uPassword) < 6:
        raise ValueError(Descrption == 'Password entered is less than 6 characters long')
    if len(uFirstName) < 1 or len(uFirstName) > 50:
        raise ValueError(Description = 'name_last is not between 1 and 50 characters in length')
    if len(uLastName) < 1 or len(uLastName) > 50:
        raise ValueError(description == 'name_last is not between 1 and 50 characters in length')
    u_id = newID()
    #didnt understand the encode token part and the first part
    newToken = encodeToken({'email' : uEmail, 'timestamp' : time.time()})
    '''
        if(isFirst == True):
        usersList['users'][0]['permission_id'] = 1
    save()
    '''
    handle = new_handle(uFirstName, uLastName)
    new_list['users'].append({
                            'Email' : uEmail,
                            'name_first' : uFirstName, 
                            'name_last' : uLastName,
                            'handle' : handle,
                            'password': hashPassword(uPassword),
                            'u_id': u_id,
                            'tokens': newToken
                             })
    return dumps({'u_id': u_id, 'token': newToken})

def search_user_by_email(email):
    global users_list:
    for user in users_list['users']:
        if user['Email'] == email:
            return user
    return None

#dont understand!
def hashPassword(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/auth/login', methods = ['POST'])
def auth_login():
    user = get_users_list()
    email = request.form.get('Email')
    password = request.form.get('password')
    length = len(user['users'])
    if valid_email(email) is False:
        raise ValueError(description = 'Email entered is not a valid email')   
    curr_user = search_user_by_email(email)
    if curr_user == None:  
        raise ValueError(description = 'Email entered does not belong to a user') 
    for elem in user['user']:
        if elem['Email'] == email and elem['password'] != password:
            raise ValueError(description: 'Password is not correct')
        elif elem['Email'] == email and elem['password'] == password:
            u_id = elem['u_id']
            token = elem['token']
    return dumps({ 'u_id':u_id, 'token':token})
    



if __name__ == '__main__':
    app.run(port = 58888)
    
             
