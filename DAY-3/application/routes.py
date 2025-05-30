from flask import current_app as app ,jsonify , request
from .database import db
from .models import User , Role

# I can not do the following because we will be importing everything from module inside the app not from app into other module as they it will be become a circular importing 

# from .app import app


from flask_security import hash_password , auth_required , roles_required , current_user , roles_accepted
# flask session is required for the browser which will have session cookies and backend require token to get the authentication

@app.route('/' , methods = ['GET'])
def home():
    return "<h1>This is my home page</h1>"

@app.route('/api/admin')
@auth_required('token') # Authentication
@roles_required('admin') # RBAC / Authorization
def admin_home():
    return "<h1>This is admin</h1>"


@app.route('/api/home')
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


@app.route('/api/register',methods=['POST'])
# @app.post('/api/register') # here we dont have to mention the methods which is POST
# Since this is an api so this will take the data in form of request body not through form using get and post , that will be done by the vue and that will trigger this api which will add the data directly into database 
def create_user():
    credentials = request.get_json()
    # get_json() this is a method of request , which will take the json and change it into dictionary.
    if not app.security.datastore.find_user(email = credentials["email"]):
        app.security.datastore.create_user(email = credentials["email"] ,
                                           username = credentials["username"] ,
                                           password = hash_password(credentials["password"]),
                                           roles = ["user"])
        db.session.commit()
        return jsonify({
            "message" : "user created successfully"
        }),201
    
    return jsonify({
        # jsonify is a method provided by flask itself and it will convert dictionary into json.
        "message" : "user already exists"
    }),400