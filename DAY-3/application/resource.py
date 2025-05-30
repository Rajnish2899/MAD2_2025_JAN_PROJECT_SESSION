# flask-restful has been added to the environment through pip install flask-restful , so we can use it .
# we will create the restful classes and that will be done for the end points of apis given in the routes_and_apis.md 
# Transaction based api

# - /api/get
# - /api/create
# - /api/update/<trans_id> # this update is for the users
# - /api/delete/<trans_id>

from flask_restful import Api , Resource , reqparse

# here in case of API reqparse is used to parse the request body , the way the flask restful deals with the request body is different from  the routes where we use request.get_json(). 

# here the object reqparse , we create the reqparse and we define what are attributes that will be added to the body apart from those nothing will be added.

from .models import *
from flask_security import auth_required , roles_required  , current_user,roles_accepted

# through flask_restful all the CRUD related to the particular element clubbed together 
# through restful we can do request parsing and marshaling of the data - through this we can decide what to show and what to hide .

# Now we will create API object 

api = Api()

def roles_list(roles):
    role_list = []
    for role in roles:
        role_list.append(role.name)
    return role_list

# to add the information into database and this information will be provided by the request body and we get the info from it using reqparse

parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('type')
parser.add_argument('date')
parser.add_argument('source')
parser.add_argument('destination')
parser.add_argument('description')





class TransApi(Resource):
    @auth_required('token')
    @roles_accepted('user','admin')
    # In case of routes we define the view function using the name whatever we want but in the case of Api , function have to be defined by their method we want to apply
    def get(self):
        transactions = []
        # restful api can not show object retrived from db so it will have to convert into json 
        trans_jsons = []
        # now to decide what to show we have to verify whether the logged in user is a user or a admin
        if "admin" in roles_list(current_user.roles):
            transactions = Transaction.query.all()
        else:
            transactions = current_user.trans
        for transaction in transactions:
            this_trans = {}
            this_trans["id"] = transaction.id
            this_trans["name"] = transaction.name
            this_trans["type"] = transaction.type
            this_trans["date"] = transaction.date
            this_trans["delivery"] = transaction.delivery
            this_trans["source"] = transaction.source
            this_trans["destination"] = transaction.destination
            this_trans["internal_status"] = transaction.internal_status
            this_trans["delivery_status"] = transaction.delivery_status
            this_trans["description"] = transaction.description
            this_trans["user"] = transaction.user_id
            trans_jsons.append(this_trans)

        if trans_jsons :
            return trans_jsons
        return{
            "message" : "No transaction found"
        },404
    

    @auth_required('token')
    @roles_required('user')
    def post(self):
        args = parser.parse_args()
        try :
            transaction = Transaction(name = args["name"],
                                  type = args["type"],
                                  date = args["type"],
                                  source = args["type"],
                                  destination = args["destination"],
                                  discription = args["discription"],
                                  user_id = current_user.id)
        
            db.session.add(transaction)
            db.session.commit()
            return{
                "message":"transaction created successfully"
            }

        except:
            return{
                "message" : "One or more required fields are missing"
            },400


api.add_resource(TransApi,'/api/get' , '/api/create')
# In case of routes we first create the end-point then we define the view function , whereas in case of api we define the view function first then we create the end-point

