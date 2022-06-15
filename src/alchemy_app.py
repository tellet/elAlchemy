from functools import partial

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, VariableListProperty, ListProperty, ObjectProperty, NumericProperty
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, ScreenManager

from alchemy_utils import AlchemyUtils
from src.alchemy import KNOWN_INGREDIENTS


class MainWindow(Screen):
    def print_smth(self):
        self.add_widget(Image(source='images/cat_logo.png'))


class BothWindow(Screen):
    pass


class EffectsOnlyWindow(Screen):
    effects = ListProperty()
    cocktails = ListProperty()
    cocktails_str = StringProperty()

    def manage_effects(self, effect, value):
        if value:
            self.effects.append(effect)
        else:
            self.effects.remove(effect)

    def calculate_cocktails(self):
        print('________________Calculate cocktails from all known ingredients.________________')
        alchemy_ingredients = []
        for item in KNOWN_INGREDIENTS.keys():
            alchemy_ingredients.append(item)
        toxin_lvl = 1
        oracle = AlchemyUtils(alchemy_ingredients, toxin_lvl)
        print(f'________________Is there a cocktail with all the `{self.effects}` effects?________________')
        desired_cocktails = oracle.get_cocktails_with_all_effects(self.effects)
        if not desired_cocktails:
            print('No desired cocktails found')
        self.cocktails = [x.receipt for x in desired_cocktails]
        print(f'Found {len(self.cocktails)} cocktails with all desired effects.')
        self.cocktails_str = '\n'.join(self.cocktails)
        # self.cocktails_str = '\n'.join(self.cocktails[0:100])


class CocktailsFromEffectsOnlyWindow(Screen):
    cocktails = ListProperty()
    next_btn = Button(
        text="Next",
        size_hint=(.5, .1),
        pos_hint={"bottom": 1.0, "left": 1.0},
        font_size=14
    )

    def show_100_cocktails(self, cocktails, *args):
        print(args)
        page_size = 500
        if len(cocktails) <= page_size:
            return '\n'.join(cocktails)
        result = '\n'.join(cocktails[0:page_size])
        # self.remove_widget(self.next_btn)
        # self.next_btn.bind(on_press=partial(self.show_100_cocktails, cocktails[page_size:]))
        # self.grid.add_widget(self.next_btn)
        return result


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
