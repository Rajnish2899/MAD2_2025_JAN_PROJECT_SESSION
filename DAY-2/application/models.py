# from flask_sqlalchemy import SQLAlchemy
from .database import db

# if we dont give the . , models.py will start searching the db in root folder , but it is in the same folder where the mdoels.py is so we have to give this . , which is known as root directory.

from flask_security import UserMixin , RoleMixin

class User(db.Model,UserMixin):
    # required for flask-security
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String , unique = True , nullable = False)
    username = db.Column(db.String , unique = True , nullable = False)
    password = db.Column(db.String , nullable = False)
    fs_uniquifier = db.Column(db.String , unique = True , nullable = False)
    # this is a kind of token which will safeguard our end point , like if a normal customer wants to access the admin page this will protect that from doing so. this will protect the api's
    active = db.Column(db.Boolean , default = True)
    roles = db.relationship('Role',backref = 'bearer',secondary = 'users_roles' )
    # through this using user.roles we can retrieve the role of a particular user
    # using backref , role.bearer this will give the list of users having same role
    # users_roles get converted into UsersRole as the table name
    # camelcase words are class name whereas small letters words are table name 
    # to ensure that flask-security gets applied on these models we have to use the UserMixin  and RoleMixin


# one limitation of the structured database is one table can have any level of complexity

class Role(db.Model , RoleMixin): 
    id = db.Column(db.Integer , primary_key = True)
    name = db.Column(db.String , unique = True , nullable = False)
    description = db.Column(db.String)

# many-to-many

# here we will create an association table 

class UsersRoles(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    user_id = db.Column(db.Integer , db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer , db.ForeignKey('role.id'))


