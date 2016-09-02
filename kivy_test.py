from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import kivy
import os


class LoginScreen(GridLayout):

    def __init__(self, **kwargs):

        def callback(instance):
            print("Button " + instance.text + " is being pressed.")

        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 2
        self.rows = 3
        self.add_widget(Label(text='Learning Intention'))
        self.learning_intention = TextInput(multiline=True)
        self.add_widget(self.learning_intention)
        self.add_widget(Label(text='Lesson Success'))
        self.lesson_success = TextInput(multiline=True)
        self.add_widget(self.lesson_success)

        self.btn1 = Button(text="Test button")
        self.btn1.bind(on_press=callback)
        self.add_widget(self.btn1)

class MyApp(App):

    def build(self):
        return LoginScreen()


if __name__ == '__main__':
    MyApp().run()