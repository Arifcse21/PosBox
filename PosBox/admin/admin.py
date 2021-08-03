
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from collections import OrderedDict
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import  declarative_base
from datetime import datetime
import getpass
import  hashlib, binascii, os
from utils.datatable import DataTable


mysql_passwd = getpass.getpass("Enter MySQL password: ")         # Cannot be ran on Pycharm. BUt of course in terminal
db_name = "posbox"
################################
engine = create_engine(f'mysql://root:{mysql_passwd}@localhost:3306/{db_name}')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()
################################
def hash_password(password):
    salt = hashlib.sha256(os.urandom(64)).hexdigest().encode('ascii')
    password_hash = hashlib.pbkdf2_hmac('sha256',password.encode('utf-8'),
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
    date = Column(DateTime, default=datetime.utcnow, nullable=False)


class Stocks(Base):
    __tablename__ = "stocks"
    id = Column(Integer, primary_key=True, nullable=False)
    product_code = Column(String(50), nullable=False)
    product_name = Column(String(100), nullable=False)
    product_weight = Column(Float(), nullable=False)
    product_price = Column(Float(), nullable=False)
    discount = Column(Float(), nullable=True)
    in_stock = Column(Integer, nullable=False)
    sold = Column(Integer, nullable=False)
    last_fillup = Column(DateTime, nullable=False)



# Base.metadata.create_all(engine)

# user1 = Users(first_name = "Abdullah Al", last_name = "Arif", username = "Arif2743", password = hash_password("arif"), designation = "Administrator")
#
# user2 = Users(first_name = "Abdullah", last_name = "Soyaib", username = "Brovai", password = hash_password("brovai"), designation = "Moderator")
#
# user3 = Users(first_name = "Safayat", last_name = "Sandid", username = "Nohan", password = hash_password("nohan"), designation = "Editor")
#
# user4 = Users(first_name = "Sadika", last_name = "Jahan", username = "saba", password = hash_password("saba"), designation = "Administrator")


# session.add_all([user2, user3, user4])
# session.commit()


class AdminWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Display Users
        content = self.ids.scrn_content
        users = self.get_users()
        usertable = DataTable(table=users)
        content.add_widget(usertable)

        # Display Products
        product_scrn = self.ids.scrn_product_content
        products = self.get_products()
        prod_table = DataTable(table=products)
        product_scrn.add_widget(prod_table)

    def get_users(self):
        users = session.query(Users)

        _users = OrderedDict()
        _users['first_names'] = {}
        _users['last_names'] = {}
        _users['usernames'] = {}
        _users['passwords'] = {}
        _users['designations'] = {}

        first_names = []
        last_names = []
        usernames = []
        passwords = []
        designations = []

        for user in users:
            first_names.append(user.first_name)
            last_names.append(user.last_name)
            usernames.append(user.username)
            pwd = user.password
            if len(pwd) > 10:
                pwd = pwd[:10] + '...'
            passwords.append(pwd)
            designations.append(user.designation)
        # print(first_names, last_names, usernames, passwords, designations)
        user_length = len(first_names)
        index = 0
        while index < user_length:
            _users['first_names'][index] = first_names[index]
            _users['last_names'][index] = last_names[index]
            _users['usernames'][index] = usernames[index]
            _users['passwords'][index] = passwords[index]
            _users['designations'][index] = designations[index]

            index += 1
        return _users


    def get_products(self):
        products = session.query(Stocks)

        _stocks = OrderedDict()
        _stocks['product_code'] = {}
        _stocks['product_name'] = {}
        _stocks['product_weight'] = {}
        _stocks['product_price'] = {}
        _stocks['discount'] = {}
        _stocks['in_stock'] = {}
        _stocks['sold'] = {}
        _stocks['last_fillup'] = {}

        product_code = []
        product_name = []
        product_weight = []
        product_price = []
        discount = []
        in_stock = []
        sold = []
        last_fillup = []

        for product in products:
            product_code.append(product.product_code)
            pdctname = product.product_name
            if len(pdctname) > 20:
                pdctname = pdctname[:20] + '...'
            product_name.append(pdctname)
            product_weight.append(product.product_weight)
            product_price.append(product.product_price)
            discount.append(product.discount)
            in_stock.append(product.in_stock)
            sold.append(product.sold)
            last_fillup.append(product.last_fillup)

        product_length = len(product_code)
        index = 0
        while index < product_length:
            _stocks['product_code'][index] = product_code[index]
            _stocks['product_name'][index] = product_name[index]
            _stocks['product_weight'][index] = product_weight[index]
            _stocks['product_price'][index] = product_price[index]
            _stocks['discount'][index] = discount[index]
            _stocks['in_stock'][index] = in_stock[index]
            _stocks['sold'][index] = sold[index]
            _stocks['last_fillup'][index] = last_fillup[index]
            index += 1
        return _stocks

    def change_screen(self, instance):
        if instance.text == 'Manage Products':
            self.ids.scrn_mngr.current = 'scrn_product_content'
        elif instance.text == "Manage Users":
            self.ids.scrn_mngr.current = 'scrn_content'
        else:
            self.ids.scrn_mngr.current = 'scrn_analysis'


class AdminApp(App):
    def build(self):
        self.icon = "/mnt/Downloads/Pictures/arch.png"
        return AdminWindow()


if __name__ == '__main__':
    AdminApp().run()

