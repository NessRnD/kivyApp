import json
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.network.urlrequest import UrlRequest

class AuthApp(App):
    def build(self):
        layout = GridLayout(cols=1, padding=10)

        self.username_input = TextInput(text="Username", multiline=False)
        self.password_input =TextInput(text="Password", password=True, multiline=False)

        register_button = Button(text="Register")
        register_button.bind(on_press=self.register)

        login_button = Button(text="Login")
        login_button.bind(on_press=self.login)

        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(register_button)
        layout.add_widget(login_button)

        return layout

    import json

    def register(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        if username and password:
            headers = {'Content-Type': 'application/json'}
            body = json.dumps({'username': username, 'password': password})
            UrlRequest(
                'http://localhost:8000/api/auth/register/',
                req_body=body,
                req_headers=headers,
                on_success=self.handle_response,
                on_error=self.handle_error
            )
        else:
            self.show_error("Введите логин и пароль")

    def login(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        if username and password:
            headers = {'Content-Type': 'application/json'}
            body = json.dumps({'username': username, 'password': password})
            UrlRequest(
                'http://localhost:8000/api/auth/login/',
                req_body=body,
                req_headers=headers,
                on_success=self.handle_response,
                on_error=self.handle_error
            )
        else:
            self.show_error("Введите логин и пароль")

    def handle_response(self, req, result):
        if req.url.endswith('login/'):
            self.token = result['token']
            self.show_success("Авторизация прошла успешно!")
        else:
            self.show_success("Регистрация прошла успешно!")

    def handle_error(self, req, error):
        self.show_error(f"Ошибка: {error}")

    def show_error(self, message):
        popup = Popup(
            title='Ошибка',
            content=Label(text=message),
            size_hint=(None, None),
            size=(200, 100)
        )
        popup.open()

    def show_success(self, message):
        popup = Popup(
            title='Успех',
            content=Label(text=message),
            size_hint=(None, None),
            size=(200, 100)
        )
        popup.open()

if __name__ == '__main__':
    AuthApp().run()

