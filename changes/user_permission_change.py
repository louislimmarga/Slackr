from flask_cors import CORS
from flask_mail import Mail, Message
from flask import Flask, request, send_from_directory
from werkzeug.exceptions import HTTPException
from changes.Error import AccessError
from changes.data_backend import save, ValueError
from changes.helper_func import decodeToken, searchUserByEmail, checkUserLoggedIn, checkUIdValid, searchUserByID
from changes.user_backend import get_userInfo, check_u_id

def check_permission(function):
    def wrapper(userInfo, u_id, permission_id, *args):
        permission_id = int(permission_id)
        changedPermissionUser = searchUserByID(u_id)

        if permission_id < 1 or permission_id > 3:
            raise ValueError(description="permission_id is not valid")
        if userInfo['permission_id'] == 3:
            raise AccessError(description="The authorised user is not an admin or owner")
        if userInfo['permission_id'] == 2:
            if permission_id == 1:
                raise ValueError(description="Admin can not raise someone to an owner of slackr")
            if changedPermissionUser['permission_id'] == 1:
                raise ValueError(description="Admin can not change the permission of an owner of slackr")
                
        return function(changedPermissionUser, u_id, permission_id, *args)
    return wrapper

@get_userInfo
@check_u_id
@check_permission
def admin_userpermission_change(changedPermissionUser, u_id, permission_id):    
    #if i am admin, i upgrade someone to admin/owner, where i can't do the latter one
    #if i am owner, i upgrade change anyone to admin/owner
    #if i am admin, i can only downgrade someone to a user
    #if i am owner, i can downgrade anyone to admin/member (even owner)
    changedPermissionUser['permission_id'] = permission_id
    save()
    return {}
