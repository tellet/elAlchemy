from kivy.app import App
from kivy.core.text import Label
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, ScreenManager


class MainWindow(Screen):
    def print_smth(self):
        self.add_widget(Image(source='images/cat_logo.png'))


class BothWindow(Screen):
    pass


class EffectsOnlyWindow(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

    def show_cocktails(self):
        print(self.ids)
        self.ids.effects_only_screen_lbl.text = "THIS IS IT!"


class CocktailsFromEffects(Screen):
    pass


class IngredientsOnlyWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("src/multi.kv")


class AlchemyApp(App):
    def build(self):
        return kv
