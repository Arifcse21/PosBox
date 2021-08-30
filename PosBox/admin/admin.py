from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from  kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
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
    sold = Column(Integer, nullable=True)
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
        content = self.ids.scrn_contents
        users = self.get_users()
        usertable = DataTable(table=users)
        content.add_widget(usertable)

        # Display Products
        product_scrn = self.ids.scrn_product_contents
        products = self.get_products()
        prod_table = DataTable(table=products)
        product_scrn.add_widget(prod_table)

    def get_users(self):
        users = session.query(Users)

        _users = OrderedDict()
        _users['First Names'] = {}
        _users['Last Names'] = {}
        _users['Usernames'] = {}
        _users['Passwords'] = {}
        _users['Designations'] = {}

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
            _users['First Names'][index] = first_names[index]
            _users['Last Names'][index] = last_names[index]
            _users['Usernames'][index] = usernames[index]
            _users['Passwords'][index] = passwords[index]
            _users['Designations'][index] = designations[index]

            index += 1
        return _users

    def add_user_fields(self):
        target = self.ids.ops_fields
        target.clear_widgets()
        crud_fname = TextInput(hint_text="First Name", multiline = False)
        crud_lname = TextInput(hint_text="Last Name", multiline = False)
        crud_uname = TextInput(hint_text="Username", multiline = False)
        crud_pwd = TextInput(hint_text="Password", multiline = False)
        crud_des = Spinner(text="Operator", values=["Operator", "Administrator" ])
        crud_submit = Button(text="Add", size_hint_x=None, width=100,
                             on_release=lambda x:self.add_user(crud_fname.text, crud_lname.text, crud_uname.text, crud_pwd.text, crud_des.text))

        target.add_widget(crud_fname)
        target.add_widget(crud_lname)
        target.add_widget(crud_uname)
        target.add_widget(crud_pwd)
        target.add_widget(crud_des)
        target.add_widget(crud_submit)

    
    def add_user(self, fname, lname, uname, pwd, des):
        content = self.ids.scrn_contents
        content.clear_widgets()

        user = Users(first_name=fname, last_name=lname,
                     username=uname,
                     password=hash_password(pwd),
                     designation=des, date=datetime.now())
        session.add(user)
        session.commit()

        users = self.get_users()
        usertable = DataTable(table=users)
        content.add_widget(usertable)


    def update_user_fields(self):
        info = self.ids.info
        info.text = "[color=#0000FF]N.B: All fields should be filled![/color]"
        target = self.ids.ops_fields
        target.clear_widgets()
        crud_fname = TextInput(hint_text="First Name", multiline = False)
        crud_lname = TextInput(hint_text="Last Name", multiline = False)
        crud_uname = TextInput(hint_text="Username", multiline = False)
        crud_pwd = TextInput(hint_text="Password", multiline = False)
        crud_des = Spinner(text="Operator", values=["Operator", "Administrator" ])
        crud_submit = Button(text="Update", size_hint_x=None, width=100,
                             on_release=lambda x:self.update_user(crud_fname.text, crud_lname.text, crud_uname.text, crud_pwd.text, crud_des.text))

        target.add_widget(crud_uname)
        target.add_widget(crud_fname)
        target.add_widget(crud_lname)
        target.add_widget(crud_pwd)
        target.add_widget(crud_des)

        target.add_widget(crud_submit)


    def update_user(self, fname, lname, uname, pwd, des):
        content = self.ids.scrn_contents
        content.clear_widgets()

        user = session.query(Users).filter(Users.username == uname).first()
        user.first_name = fname
        user.last_name = lname
        user.password = hash_password(pwd)
        user.designation = des



        session.commit()

        users = self.get_users()
        usertable = DataTable(table=users)
        content.clear_widgets()
        content.add_widget(usertable)


    def remove_user_fields(self):
        target = self.ids.ops_fields
        target.clear_widgets()
        crud_user = TextInput(hint_text="Username", multiline = False)
        crud_submit = Button(text="Remove", size_hint_x=None, width=100,
                             on_release=lambda x: self.remove_user(crud_user.text))
        target.add_widget(crud_user)
        target.add_widget(crud_submit)

    def remove_user(self, username):
        content = self.ids.scrn_contents
        content.clear_widgets()
        user = session.query(Users).filter(Users.username == username).first()
        session.delete(user)
        session.commit()

        users = self.get_users()
        usertable = DataTable(table=users)
        content.clear_widgets()
        content.add_widget(usertable)

    def get_products(self):
        products = session.query(Stocks)

        _stocks = OrderedDict()
        _stocks['Product code'] = {}
        _stocks['Product name'] = {}
        _stocks['Product weight'] = {}
        _stocks['Product price'] = {}
        _stocks['Discount'] = {}
        _stocks['In stock'] = {}
        _stocks['Sold'] = {}
        _stocks['Last fillup'] = {}

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
            try:
                sold.append(product.sold)
            except KeyError:
                sold.append("")
            try:
                last_fillup.append(product.last_fillup)
            except KeyError:
                last_fillup.append("")

        product_length = len(product_code)
        index = 0
        while index < product_length:
            _stocks['Product code'][index] = product_code[index]
            _stocks['Product name'][index] = product_name[index]
            _stocks['Product weight'][index] = product_weight[index]
            _stocks['Product price'][index] = product_price[index]
            _stocks['Discount'][index] = discount[index]
            _stocks['In stock'][index] = in_stock[index]
            _stocks['Sold'][index] = sold[index]
            _stocks['Last fillup'][index] = last_fillup[index]
            index += 1
        return _stocks

    def add_product_fields(self):
        target = self.ids.ops_fields_p
        target.clear_widgets()


        crud_code = TextInput(hint_text="Product Code", multiline = False)
        crud_name = TextInput(hint_text="Product Name", multiline = False)
        crud_weight = TextInput(hint_text="Weight", multiline = False)
        crud_price = TextInput(hint_text="Price", multiline = False)
        crud_discount = TextInput(hint_text="Discount", multiline = False)
        crud_number = TextInput(hint_text="Number of items", multiline = False)
        crud_submit = Button(text="Add Product", size_hint_x=None, width=100, on_release = lambda x:
                             self.add_product(crud_code.text, crud_name.text, crud_weight.text, crud_price.text, crud_discount.text,
                                crud_number.text ))


        target.add_widget(crud_code)
        target.add_widget(crud_name)
        target.add_widget(crud_weight)
        target.add_widget(crud_price)
        target.add_widget(crud_discount)
        target.add_widget(crud_number)
        target.add_widget(crud_submit)

    def add_product(self,code, name, weight, price, discnt, items):
        content = self.ids.scrn_product_contents
        content.clear_widgets()

        # instock = session.query(Stocks).filter(Stocks.product_code == code ).first()
        # print(instock.in_stock)

        product = Stocks(product_code = code, product_name=name,
                         product_weight=weight, product_price=price,
                         discount=discnt,
                         in_stock = items,
                         last_fillup = datetime.now())
        session.add(product)
        session.commit()

        products = self.get_products()
        producttable = DataTable(table=products)
        content.add_widget(producttable)

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

