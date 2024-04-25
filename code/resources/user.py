from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.sqlite_db_methods import UsersTable, ContactsTable


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("phone_num", 
                        type=int, 
                        required=True, 
                        help="phone_num is a mandatory field")
    parser.add_argument("username", 
                        type=str, 
                        required=True, 
                        help="username is a mandatory field")
    parser.add_argument("password", 
                        type=str, 
                        required=True, 
                        help="password is a mandatory field")

    def post(self):
        data = self.parser.parse_args()
        users_db_obj = UsersTable()
        result = users_db_obj.get_user_by_phn(phone_num=data['phone_num'])
        row = result.fetchone()
        if row:
            msg = {"message": "Phone Number '{ph_num}' already exists".format(ph_num=data['phone_num'])}, 409
        else:
            users_db_obj.create_user(phone_num=data['phone_num'], username=data['username'], password=data['password'], email_address=data.get('email_address', 'NULL'))
            msg = {"message": "Phone Number '{ph_num}' is successfully registered".format(ph_num=data['phone_num'])}, 201
            users_db_obj.close_connection()
            Contact().add_contact_to_table(phone_num=data['phone_num'], contact_name=data['username'])
        return msg


class UserLogin:
    def __init__(self, phone_num, username, password, email_address):
        self.id = int(phone_num)
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        user_table_conns = UsersTable()
        result = user_table_conns.get_users_by_username(username=username)
        row = result.fetchone()
        if row:
            user_details = cls(*row)
        else:
            user_details = None
        user_table_conns.close_connection()
        return user_details

    @classmethod
    def find_by_phn(cls, phone_num):
        user_table_conns = UsersTable()
        result = user_table_conns.get_user_by_phn(phone_num=phone_num)
        row = result.fetchone()
        if row:
            user_details = cls(*row)
        else:
            user_details = None
        user_table_conns.close_connection()
        return user_details


class Contact(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("contacts_phone_num", 
                        type=int, 
                        required=True, 
                        help="contacts_phone_num is a mandatory field")
    parser.add_argument("contact_name", 
                        type=str, 
                        required=True, 
                        help="contact_name is a mandatory boolean field with 0 or 1 values")
    parser.add_argument("is_spam", 
                        type=bool, 
                        required=True, 
                        help="is_spam is a mandatory boolean field with 0 or 1 values")
    @jwt_required()
    def put(self, phone_num):
        data = self.parser.parse_args()
        contacts_db_obj = ContactsTable()
        result = contacts_db_obj.get_contact_by_phn(phone_num=phone_num)
        row = result.fetchone()
        if row:
            contacts_db_obj.update_contact_spam(phone_num=data['contacts_phone_num'], contact_name=data['contact_name'], is_spam=data['is_spam'])
            msg = {"message": "Contact Number '{ph_num}' is successfully Updated.".format(ph_num=data['contacts_phone_num'])}, 409
        else:
            contacts_db_obj.create_contact(phone_num=data['contacts_phone_num'], contact_name=data['contact_name'], is_spam=data['is_spam'])
            msg = {"message": "Contact Number '{ph_num}' is successfully added to the Contacts List.".format(ph_num=data['contacts_phone_num'])}, 201
        contacts_db_obj.close_connection()
        return msg

    @jwt_required()
    def get(self, phone_num):
        contacts_db_obj = ContactsTable()
        result = contacts_db_obj.get_contact_by_phn(phone_num=phone_num)
        row = result.fetchone()
        if row:
            item = {"Phone_Number": row[0], "Name": row[1], "Is_Spam": row[2]}
        else:
            item = {"message": "No Such Phone Number Found"}
        contacts_db_obj.close_connection()
        return {'contact': item}, 200

    def add_contact_to_table(self, phone_num, contact_name):
        contacts_db_obj = ContactsTable()
        result = contacts_db_obj.get_contact_by_phn(phone_num=phone_num)
        contact_row = result.fetchone()
        if not contact_row:
            contacts_db_obj.create_contact(phone_num=phone_num, contact_name=contact_name, is_spam=0)
        contacts_db_obj.close_connection()


class ContactName(Resource):
    @jwt_required()
    def get(self, contact_name):
        contacts_db_obj = ContactsTable()
        result = contacts_db_obj.get_contact_by_name(contact_name=contact_name)
        items = list()
        for row in result:
            items.append({'Phone_Number': row[0], "Name": row[1], 'Is_Spam': row[2]})
        contacts_db_obj.close_connection()
        return {'contacts': items}, 200


class ContactsList(Resource):
    @jwt_required()
    def get(self):
        contacts_db_obj = ContactsTable()
        result = contacts_db_obj.get_all_contacts()
        items = list()
        for row in result:
            items.append({'Phone_Number': row[0], "Name": row[1], 'Is_Spam': row[2]})
        contacts_db_obj.close_connection()
        return {'contacts': items}, 200
