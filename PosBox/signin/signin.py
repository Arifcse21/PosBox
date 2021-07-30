from kivy.app import App
from kivy.uix.boxlayout import BoxLayout


class SignInWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def validate_user(self):
        user = self.ids.usrnm_field
        passwd = self.ids.passwd_field
        info = self.ids.info

        uname = user.text
        password = passwd.text

        if uname == '' or password == '':
            info.text = "[color=#FF0000]Username and/or password required![/color]"
        elif uname == "admin" and password == "admin":
            info.text = "[color=#0000FF]Logged in successfully.[/color]"
        else:
            info.text = "[color=#FF0000]Invalid Username and/or Password![/color]"

class SignInApp(App):
    def build(self):
        return SignInWindow()


if __name__ == '__main__':
    ap = SignInApp()
    ap.run()
