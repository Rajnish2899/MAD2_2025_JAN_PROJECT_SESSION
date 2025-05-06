from flask import current_app as app ,jsonify

# I can not do the following because we will be importing everything from module inside the app not from app into other module as they it will be become a circular importing 

# from .app import app


from flask_security import auth_required , roles_required , current_user , roles_accepted
# flask session is required for the browser which will have session cookies and backend require token to get the authentication


@app.route('/admin')
@auth_required('token') # Authentication
@roles_required('admin') # RBAC / Authorization
def admin_home():
    return "<h1>This is admin</h1>"


@app.route('/user')
@auth_required('token')
@roles_required('user')
# @roles_required(['user' , 'admin']) # and 
# @roles_accepted(['user' , 'admin']) # OR
 
def user_home():
    user = current_user # this will be from session as session will be all info (complete user object)
    return jsonify({
        "username" : user.username,
        "email" : user.email ,
        "password" : user.password
    })
