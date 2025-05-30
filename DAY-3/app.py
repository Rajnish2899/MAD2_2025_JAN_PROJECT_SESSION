from flask import Flask 
from application.database import db
from application.models import User , Role
from application.config import LocalDevelopmentConfig
from flask_security import Security , SQLAlchemyUserDatastore , hash_password
from application.resource import api # we can do * also but we just need the api object , after this we have to connect the api with app through api.init_app(app)

def create_app():
    app = Flask(__name__)
    # app.config['SQLALCHEMY_DATABASE_URI']
    # app.config['SECRET_KEY']
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    api.init_app(app)
    datastore = SQLAlchemyUserDatastore(db , User , Role)
    app.security = Security(app,datastore)
    app.app_context().push()
    return app 

app = create_app()

with app.app_context():
    db.create_all()

    app.security.datastore.find_or_create_role(name = "admin" , description = "superuser")
    app.security.datastore.find_or_create_role(name = "user" , description = "generaluser")

    db.session.commit()

    if not app.security.datastore.find_user(email = "user0@gmail.com"):
        app.security.datastore.create_user(email = "user0@gmail.com" ,
                                           username = "admin01" ,
                                           password = hash_password("1234"),
                                           roles = ["admin","user"])

    if not app.security.datastore.find_user(email = "user1@gmail.com"):
        app.security.datastore.create_user(email = "user1@gmail.com" ,
                                           username = "user01" ,
                                           password = hash_password("1234"),
                                           roles = ["user"])
    db.session.commit()

from application.routes import *


if __name__ == "__main__":
    app.run()