from datetime import datetime

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

TEXT_SIZE = 14


class AlchemyApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.6, 0.7)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.window.add_widget(Image(source='images/cat_logo.png'))

        self.age_request = Label(
            text="Enter",
            font_size=TEXT_SIZE,
            color="#ffffff",
            bold=True
        )
        self.window.add_widget(self.age_request)

        self.date = TextInput(
            multiline=False,
            padding_y=(30, 30),
            size_hint=(1, 0.7),
            font_size=TEXT_SIZE
        )
        self.window.add_widget(self.date)

        self.button = Button(
            text="Calculate Age",
            size_hint=(0.5, 0.5),
            bold=True,
            font_size=TEXT_SIZE
        )
        self.button.bind(on_press=self.get_age)
        self.window.add_widget(self.button)

    def get_age(self, event):
        today = datetime.today().year
        dob = self.date.text
        age = int(today) - int(dob)
        self.age_request.text = "You are " + str(int(age)) + " years old"

    def build(self):
        return self.window
