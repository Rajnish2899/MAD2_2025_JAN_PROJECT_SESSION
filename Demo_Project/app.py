# we have created a application folder , which will have the all the files which will be connected to the app.py

# config.py - will have configuration like we need to connect flask application with database , we need to connect the flask app with flask security .

# models.py - will have the models

# routes.py - will have some end points 

# As we dont start using celery , we will do our tasks using virtual environment , for that we will open the terminal and we will type python -m venv .myenv

# we have to activate this virtual environment and then have to install flask its dependencies , flask sqlalchemy and flask security.

# To activate we have to "myenv\Scripts\activate"


from flask import Flask 
from application.database import db
from application.models import User , Role
from application.config import LocalDevelopmentConfig
from flask_security import Security , SQLAlchemyUserDatastore


def create_app():
    app = Flask(__name__)
    # app.config['SQLALCHEMY_DATABASE_URI']
    # app.config['SECRET_KEY']
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    datastore = SQLAlchemyUserDatastore(db , User , Role)
    app.security = Security(app,datastore)
    app.app_context().push()
    return app 

app = create_app()


if __name__ == "__main__":
    app.run()