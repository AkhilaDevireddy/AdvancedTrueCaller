from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from datetime import timedelta

from security import authenticate, identity
from resources.user import UserRegister, ContactsList, Contact, ContactName


app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
app.secret_key = 'AdvancedTC'
api = Api(app)

jwt = JWT(app, authenticate, identity)


api.add_resource(UserRegister, '/register')
api.add_resource(ContactsList, '/contacts')
api.add_resource(Contact, '/contact/<string:phone_num>')
api.add_resource(ContactName, '/contactname/<string:contact_name>')


if __name__ == '__main__':
    app.run(debug=True)  # important to mention debug=True
