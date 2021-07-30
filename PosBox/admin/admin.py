from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from collections import OrderedDict
import mysql.connector
import sys
from utils.datatable import DataTable



class AdminWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
        mydb = mysql.connector.connect(
            host = "localhost",
            user = 'root',
            password = mysql_passwd,
            database = 'poxbox'
        )
        mycursor = mydb.cursor()

        _users = OrderedDict()
        _users['first_names'] = {}
        _users['last_names'] = {}
        _users['user_names'] = {}
        _users['password'] = {}
        _users['designations'] = {}

        sql =

        first_names = []
        last_names = []
        usernames = []
        passwords = []
        designations = []

        for user in users.find():
            first_names.append(user['first_name'])
            last_names.append(user['last_name'])
            usernames.append(user['username'])
            pwd = user['password']
            if len(pwd) > 10:
                pwd = pwd[:10] + '...'
            passwords.append(pwd)
            designations.append(user['designation'])
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




        _stocks = OrderedDict()
        _stocks['product_code'] = {}
        _stocks['product_name'] = {}
        _stocks['product_weight'] = {}
        _stocks['in_stock'] = {}
        _stocks['sold'] = {}
        _stocks['last_purchase'] = {}

        product_code = []
        product_name = []
        product_weight = []
        in_stock = []
        sold = []
        last_purchase = []

        for product in products.find():
            product_code.append(product['product_code'])
            pdctname = product['product_name']
            if len(pdctname) > 10:
                pdctname = pdctname[::10] + '...'
            product_name.append(product[pdctname])
            product_weight.append(product['product_weight'])
            in_stock.append(product['in_stock'])
            sold.append(product['sold'])
            last_purchase.append(product['last_purchase'])

        product_length = len(product_code)
        index = 0
        while index < product_length:
            _stocks['product_code'][index] = product_code[index]
            _stocks['product_name'][index] = product_name[index]
            _stocks['product_weight'][index] = product_weight[index]
            _stocks['in_stock'][index] = in_stock[index]
            _stocks['sold'][index] = sold[index]
            _stocks['last_purchase'][index] = last_purchase[index]
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

