usersList = {'users' : []}
channelsList = []
channelsMessages = []
resetCodes = []
unusedMessageID = 1
channelsTimer = [] 

@APP.route('/admin/userpermission/change', methods=['POST'])
def user_permission_change():
    uToken = request.form.get('token')
    u_id = request.form.get('u_id')
    permission_id = request.form.get('permission_id')

    userInfo = decodeToken(uToken)
    
    if int(permission_id) < 1 or int(permission_id) > 3:
        raise ValueError("permission_id does not refer to a value permission_id")

    if checkUIdValid(u_id) == False:
        raise ValueError("User with u_id is not a valid user")

    for user in usersList['users']:
        if user['u_id'] == int(u_id):
            change_user_id = int(user['permission_id'])
            break

    for user in usersList['users']:
        if user['email'] == userInfo['email']:
            if int(user['permission_id']) == 3:
                raise AccessError("The authorised user is not an admin or owner")
            if int(user['permission_id']) == 2 and change_user_id == 1:
                raise AccessError("The authorised user is not an owner. Cannot change owner permission_id")

    for user in usersList['users']:
        if user['u_id'] == int(u_id):
            user['permission_id'] = permission_id
    save()

    return ({})
