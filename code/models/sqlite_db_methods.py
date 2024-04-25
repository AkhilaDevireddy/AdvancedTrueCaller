import sqlite3


class SqliteBase:
    def __init__(self):
        self.connection = sqlite3.connect('data.db', check_same_thread=False)
        self.cursor = self.connection.cursor()

    def close_connection(self):
        self.connection.commit()
        self.connection.close()


class UsersTable(SqliteBase):
    def __init__(self):
        SqliteBase.__init__(self)
        self.table_name = "users"
        self.initialize()
    
    def initialize(self):
        create_users_table = "CREATE TABLE IF NOT EXISTS {t_n}(user_phone_num VARCHAR(10) PRIMARY KEY, username text, password text, email_address text)".format(t_n=self.table_name)
        self.cursor.execute(create_users_table)

    def get_user_by_phn(self, phone_num):
        query = "SELECT * FROM {t_n} WHERE user_phone_num=?".format(t_n=self.table_name)
        result = self.cursor.execute(query, (phone_num, ))
        return result

    def get_users_by_username(self, username):
        query = "SELECT * FROM {t_n} WHERE username=?".format(t_n=self.table_name)
        result = self.cursor.execute(query, (username, ))
        return result

    def create_user(self, phone_num, username, password, email_address):
        query = "INSERT INTO {t_n} VALUES(?, ?, ?, ?)".format(t_n=self.table_name)
        self.cursor.execute(query, (phone_num, username, password, email_address))


class ContactsTable(SqliteBase):
    def __init__(self):
        SqliteBase.__init__(self)
        self.table_name = "contacts"
        self.initialize()
    
    def initialize(self):
        create_contacts_table = "CREATE TABLE IF NOT EXISTS {t_n}(contact_phone_num VARCHAR(10) PRIMARY KEY, contact_name text, is_spam bool)".format(t_n=self.table_name)
        self.cursor.execute(create_contacts_table)

    def get_all_contacts(self):
        query = "SELECT * FROM {t_n}".format(t_n=self.table_name)
        result = self.cursor.execute(query)
        return result

    def get_contact_by_phn(self, phone_num):
        query = "SELECT * FROM {t_n} WHERE contact_phone_num=?".format(t_n=self.table_name)
        result = self.cursor.execute(query, (phone_num, ))
        return result

    def get_contact_by_name(self, contact_name):
        query = "SELECT * FROM {t_n} WHERE contact_name LIKE ?".format(t_n=self.table_name)
        result = self.cursor.execute(query, ('%'+contact_name+'%', ))
        return result

    def create_contact(self, phone_num, contact_name, is_spam):
        query = "INSERT OR IGNORE INTO {t_n} VALUES(?, ?, ?)".format(t_n=self.table_name)
        self.cursor.execute(query, (phone_num, contact_name, is_spam))

    def update_contact_spam(self, phone_num, contact_name, is_spam):
        query = "UPDATE {t_n} SET contact_name=?, is_spam=? WHERE contact_phone_num=?".format(t_n=self.table_name)
        self.cursor.execute(query, (contact_name, is_spam, phone_num))


class UsersContactsRelationShip(SqliteBase):
    def __init__(self):
        SqliteBase.__init__(self)
        self.table_name = "ContactsRelationship"
        self.initialize()
    
    def initialize(self):
        create_relship_contacts_table = "CREATE TABLE IF NOT EXISTS {t_n}(users VARCHAR(10), contacts VARCHAR(10), PRIMARY KEY (users, contacts), CONSTRAINT Constr_ContactsRelationship_Users_fk FOREIGN KEY Users_fk (Users) REFERENCES Users (user_phone_num) ON DELETE CASCADE ON UPDATE CASCADE, CONSTRAINT Constr_ContactsRelationship_Contacts_fk FOREIGN KEY Contacts_fk (contacts) REFERENCES contacts (contact_phone_num) ON DELETE CASCADE ON UPDATE CASCADE)".format(t_n=self.table_name)
        self.cursor.execute(create_relship_contacts_table)

    def get_all_contacts_of_user(self, user_phone_num):
        query = "SELECT contacts.* FROM contacts JOIN ContactsRelationship ON contacts.contact_phone_num=ContactsRelationship.users WHERE ContactsRelationship.users=?".format(t_n=self.table_name)
        result = self.cursor.execute(query, (user_phone_num, ))
        return result

    def get_all_users_with_contact(self, contact_phone_num):
        query = "SELECT users.* FROM users JOIN ContactsRelationship ON users.user_phone_num=ContactsRelationship.users WHERE ContactsRelationship.contacts=?".format(t_n=self.table_name)
        result = self.cursor.execute(query, (contact_phone_num, ))
        return result
