
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from collections import OrderedDict
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import  declarative_base
from datetime import datetime

import getpass
import  hashlib, binascii, os

# from utils.datatable import DataTable



mysql_passwd = getpass.getpass("Enter MySQL password: ")         # Cannot be ran on Pycharm. BUt of course in terminal
################################
engine = create_engine(f'mysql://root:{mysql_passwd}@localhost:3306/posbox')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()
################################
def hash_password(password):
    salt = hashlib.sha512(os.urandom(64)).hexdigest().encode('ascii')
    password_hash = hashlib.pbkdf2_hmac('sha512',password.encode('utf-8'),
    salt, 100000)
    password_hash = binascii.hexlify(password_hash)
    return (salt+password_hash).decode('ascii')


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    username = Column(String(20), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    designation = Column(String(20), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(engine)

# class AdminWindow(BoxLayout):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#
#         content = self.ids.scrn_content
#         users = self.get_users()
#         usertable = DataTable(table=users)
#         content.add_widget(usertable)
#
#         # Display Products
#         product_scrn = self.ids.scrn_product_content
#         products = self.get_products()
#         prod_table = DataTable(table=products)
#         product_scrn.add_widget(prod_table)
#
#
#     def get_users(self):
#         # mydb = mysql.connector.connect(
#         #     host = "localhost",
#         #     user = 'root',
#         #     password = mysql_passwd,
#         #     database = 'poxbox'
#         # )
#         # mycursor = mydb.cursor()
#
#         _users = OrderedDict()
#         _users['first_names'] = {}
#         _users['last_names'] = {}
#         _users['user_names'] = {}
#         _users['password'] = {}
#         _users['designations'] = {}
#
#         sql =
#
#         first_names = []
#         last_names = []
#         usernames = []
#         passwords = []
#         designations = []
#
#         for user in users.find():
#             first_names.append(user['first_name'])
#             last_names.append(user['last_name'])
#             usernames.append(user['username'])
#             pwd = user['password']
#             if len(pwd) > 10:
#                 pwd = pwd[:10] + '...'
#             passwords.append(pwd)
#             designations.append(user['designation'])
#         user_length = len(first_names)
#         index = 0
#         while index < user_length:
#             _users['first_names'][index] = first_names[index]
#             _users['last_names'][index] = last_names[index]
#             _users['usernames'][index] = usernames[index]
#             _users['passwords'][index] = passwords[index]
#             _users['designations'][index] = designations[index]
#
#             index += 1
#         return _users
#
#     def get_products(self):
#
#
#
#
#         _stocks = OrderedDict()
#         _stocks['product_code'] = {}
#         _stocks['product_name'] = {}
#         _stocks['product_weight'] = {}
#         _stocks['in_stock'] = {}
#         _stocks['sold'] = {}
#         _stocks['last_purchase'] = {}
#
#         product_code = []
#         product_name = []
#         product_weight = []
#         in_stock = []
#         sold = []
#         last_purchase = []
#
#         for product in products.find():
#             product_code.append(product['product_code'])
#             pdctname = product['product_name']
#             if len(pdctname) > 10:
#                 pdctname = pdctname[::10] + '...'
#             product_name.append(product[pdctname])
#             product_weight.append(product['product_weight'])
#             in_stock.append(product['in_stock'])
#             sold.append(product['sold'])
#             last_purchase.append(product['last_purchase'])
#
#         product_length = len(product_code)
#         index = 0
#         while index < product_length:
#             _stocks['product_code'][index] = product_code[index]
#             _stocks['product_name'][index] = product_name[index]
#             _stocks['product_weight'][index] = product_weight[index]
#             _stocks['in_stock'][index] = in_stock[index]
#             _stocks['sold'][index] = sold[index]
#             _stocks['last_purchase'][index] = last_purchase[index]
#             index += 1
#         return _stocks
#
#     def change_screen(self, instance):
#         if instance.text == 'Manage Products':
#             self.ids.scrn_mngr.current = 'scrn_product_content'
#         elif instance.text == "Manage Users":
#             self.ids.scrn_mngr.current = 'scrn_content'
#         else:
#             self.ids.scrn_mngr.current = 'scrn_analysis'
#
#
# class AdminApp(App):
#     def build(self):
#         self.icon = "/mnt/Downloads/Pictures/arch.png"
#         return AdminWindow()
#
#
# if __name__ == '__main__':
#     AdminApp().run()
#
