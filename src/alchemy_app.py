from functools import partial

from kivy.app import App
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.properties import ListProperty, DictProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, ScreenManager, ScreenManagerException
from kivy.uix.scrollview import ScrollView

from src.alchemy_oracle import AlchemyOracle
from src.alchemy import KNOWN_INGREDIENTS, COMMON, ALL_ROUND, RARE, KNOWN_EFFECTS, EFFECTS_DICT, HEAL_DICT, UNIQUE
from src.app_utils import is_base_color, split_into_pages, change_color


class ImageButton(ButtonBehavior, Image):
    pass


class MainWindow(Screen):
    def show_cat(self):
        self.add_widget(Image(source='images/cat_logo.png'))


class DataPage(Screen):
    def __init__(self, data, page, pages_count, source: str, **kw):
        super(DataPage, self).__init__(**kw)
        self.data = data
        self.page = page
        self.pages_count = pages_count
        self.source = source

        self.root_grid = GridLayout(cols=1)
        self.add_widget(self.root_grid)

        self.scroll = ScrollView(do_scroll_x=True, do_scroll_y=True)
        self.grid = GridLayout(cols=1, size_hint=(None, None))
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.grid.bind(minimum_width=self.grid.setter('width'))
        for item in data:
            tmp_lbl = Label(text=item, size_hint=(None, None), size=(800, 50), padding_y=50)
            tmp_lbl.font_size = tmp_lbl.height / 3
            self.grid.add_widget(tmp_lbl)

        self.scroll.add_widget(self.grid)
        self.root_grid.add_widget(self.scroll)

        self.back_btn = Button(
            text='Назад',
            size_hint=(.5, .1),
            pos_hint={"bottom": 1.0, "right": 1.0},
            background_color=[1, 2, 1, 3]
        )
        self.back_btn.font_size = self.back_btn.height / 3
        self.back_btn.bind(on_press=self.go_back_main)
        self.root_grid.add_widget(self.back_btn)
        # first page of many
        if page == 0 and pages_count > 1:
            self.next_btn = Button(
                text='Следующая стр',
                size_hint=(.5, .1),
                pos_hint={"bottom": 1.0, "right": 1.0},
                background_color=[1, 2, 1, 3]
            )
            self.next_btn.font_size = self.next_btn.height / 3
            self.next_btn.bind(on_press=partial(self.go_to_next_page, source))
            self.root_grid.add_widget(self.next_btn)
        # middle page of many
        if 0 < page < pages_count - 1:
            self.next_btn = Button(
                text='Следующая стр',
                size_hint=(.5, .1),
                pos_hint={"bottom": 1.0, "right": 1.0},
                background_color=[1, 2, 1, 3]
            )
            self.next_btn.font_size = self.next_btn.height / 3
            self.next_btn.bind(on_press=partial(self.go_to_next_page, source))
            self.root_grid.add_widget(self.next_btn)

            self.previous_btn = Button(
                text='Предыдущая стр',
                size_hint=(.5, .1),
                pos_hint={"bottom": 1.0, "left": 1.0},
                background_color=[1, 2, 1, 3]
            )
            self.previous_btn.font_size = self.previous_btn.height / 3
            self.previous_btn.bind(on_press=partial(self.go_to_previous_page, source))
            self.root_grid.add_widget(self.previous_btn)
        # last page of many
        if page == pages_count - 1 and pages_count > 1:
            self.previous_btn = Button(
                text='Предыдущая стр',
                size_hint=(.5, .1),
                pos_hint={"bottom": 1.0, "left": 1.0},
                background_color=[1, 2, 1, 3]
            )
            self.previous_btn.bind(on_press=partial(self.go_to_previous_page, source))
            self.root_grid.add_widget(self.previous_btn)

    def go_to_next_page(self, source, button):
        self.parent.current = f'{source}_page_{self.page + 1}'
        self.parent.transition.direction = "left"

    def go_to_previous_page(self, source, button):
        self.parent.current = f'{source}_page_{self.page - 1}'
        self.parent.transition.direction = "right"

    def go_back_main(self, button):
        self.parent.current = self.source
        self.parent.transition.direction = "right"


class EffectsOnlyWindow(Screen):
    effects = ListProperty()
    cocktails = ListProperty()
    scroll = ScrollView()
    go_button = Button()

    def on_enter(self, *args):
        root_grid = self.manager.ids['effects_only_root_grid']
        self.scroll = ScrollView(do_scroll_x=False, do_scroll_y=True)
        grid = GridLayout(cols=1, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        for item in KNOWN_EFFECTS:
            tmp_btn = Button(text=item, size_hint_y=None)
            if item in self.effects:
                change_color(tmp_btn)
            tmp_btn.bind(on_press=partial(self.manage, item))
            grid.add_widget(tmp_btn)
        self.scroll.add_widget(grid)
        root_grid.add_widget(self.scroll)
        self.go_button = Button(
            text='Узнать зелья',
            size_hint=(1, .1),
            pos_hint={'bottom': 1.0},
            background_color=[1, 2, 1, 3]
        )
        self.go_button.font_size = self.go_button.height / 3
        self.go_button.bind(on_press=self.calculate_cocktails)
        root_grid.add_widget(self.go_button)

    def manage(self, item, button):
        color = change_color(button)
        self.manage_effects(item, color)

    def manage_effects(self, item, color):
        flag = is_base_color(color)
        if flag:
            if item in self.effects:
                self.effects.remove(item)
        else:
            self.effects.append(item)

    def calculate_cocktails(self, button):
        print(f'________Calculate cocktails from all known ingredients with all `{self.effects}` effects.________')
        alchemy_ingredients = []
        for item in KNOWN_INGREDIENTS.keys():
            alchemy_ingredients.append(item)
        toxin_lvl = 1
        oracle = AlchemyOracle(alchemy_ingredients, toxin_lvl)
        desired_cocktails = oracle.calculate_cocktails_with_effects(self.effects)
        self.cocktails = [str(x) for x in desired_cocktails]
        print(f'Found {len(self.cocktails)} cocktails.')
        if len(self.cocktails) == 0:
            self.parent.current = 'no_cocktails_window'
            self.parent.transition.direction = "left"
        else:
            self.parent.current = self.show_results()
            self.parent.transition.direction = "left"

    def show_results(self):
        result_pages = split_into_pages(self.cocktails)
        pages_amount = len(result_pages)
        for k in range(pages_amount):
            tmp_screen = DataPage(
                name=f'effects_only_window_page_{k}',
                data=result_pages[k],
                page=k,
                pages_count=pages_amount,
                source='effects_only_window'
            )
            try:
                old_screen = self.manager.get_screen(f'effects_only_window_page_{k}')
                self.manager.remove_widget(old_screen)
            except ScreenManagerException:
                pass
            self.manager.add_widget(tmp_screen)
        return 'effects_only_window_page_0'

    def on_leave(self, *args):
        self.manager.ids['effects_only_root_grid'].remove_widget(self.scroll)
        self.manager.ids['effects_only_root_grid'].remove_widget(self.go_button)


class IngredientsOnlyWindow(Screen):
    ingredients = DictProperty()
    cocktails = ListProperty()
    scroll = ScrollView()
    go_button = Button()

    def on_enter(self, *args):
        self.ingredients = []
        self.cocktails = []
        root_grid = self.manager.ids['ings_only_root_grid']
        self.scroll = ScrollView(do_scroll_x=False, do_scroll_y=True)
        grid = GridLayout(cols=1, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        tmp_btn = Button(text='повсеместные', size_hint_y=None)
        tmp_btn.font_size = tmp_btn.height / 3
        tmp_btn.bind(on_press=partial(self.manage, ALL_ROUND))
        grid.add_widget(tmp_btn)

        tmp_btn = Button(text='распространённые', size_hint_y=None)
        tmp_btn.font_size = tmp_btn.height / 3
        tmp_btn.bind(on_press=partial(self.manage, COMMON))
        grid.add_widget(tmp_btn)

        tmp_btn = Button(text='редкие', size_hint_y=None)
        tmp_btn.font_size = tmp_btn.height / 3
        tmp_btn.bind(on_press=partial(self.manage, RARE))
        grid.add_widget(tmp_btn)

        tmp_btn = Button(text='уникальные', size_hint_y=None)
        tmp_btn.font_size = tmp_btn.height / 3
        tmp_btn.bind(on_press=partial(self.manage, UNIQUE))
        grid.add_widget(tmp_btn)

        tmp_btn = Button(text='выбрать', size_hint_y=None)
        tmp_btn.font_size = tmp_btn.height / 3
        tmp_btn.bind(on_press=self.select_ingredients)
        grid.add_widget(tmp_btn)

        self.scroll.add_widget(grid)
        root_grid.add_widget(self.scroll)

        self.go_button = Button(
            text='Узнать зелья',
            size_hint=(1, .1),
            pos_hint={'bottom': 1.0},
            background_color=[1, 2, 1, 3]
        )
        self.go_button.font_size = self.go_button.height / 3
        self.go_button.bind(on_press=self.calculate_cocktails)
        root_grid.add_widget(self.go_button)

    def manage(self, selected_ings, button):
        color = change_color(button)
        self.manage_ings_lists(selected_ings, color)

    def manage_ings_lists(self, selected_ings, color):
        flag = is_base_color(color)
        if not flag:
            for k, v in selected_ings.items():
                self.ingredients[k] = v
        else:
            for k in selected_ings.keys():
                if k in self.ingredients.keys():
                    self.ingredients.pop(k)

    def select_ingredients(self, *args):
        self.parent.current = 'ingredients_selection_window'
        self.parent.transition.direction = "left"

    def calculate_cocktails(self, *args):
        print(f'________________Calculate cocktails from {len(self.ingredients.keys())} ingredients.________________')
        alchemy_ingredients = []
        for item in self.ingredients.keys():
            alchemy_ingredients.append(item)
        toxin_lvl = 1
        oracle = AlchemyOracle(alchemy_ingredients, toxin_lvl)
        desired_cocktails = oracle.calculate_all_cocktails()
        self.cocktails = [str(x) for x in desired_cocktails]
        print(f'Found {len(self.cocktails)} cocktails.')
        if len(self.cocktails) == 0:
            self.parent.current = 'no_cocktails_window'
            self.parent.transition.direction = "left"
        else:
            self.parent.current = self.show_results()
            self.parent.transition.direction = "left"

    def show_results(self):
        result_pages = split_into_pages(self.cocktails)
        pages_amount = len(result_pages)
        for k in range(pages_amount):
            tmp_screen = DataPage(
                name=f'ingredients_only_window_page_{k}',
                data=result_pages[k],
                page=k,
                pages_count=pages_amount,
                source='ingredients_only_window'
            )
            try:
                old_screen = self.manager.get_screen(f'ingredients_only_window_page_{k}')
                self.manager.remove_widget(old_screen)
            except ScreenManagerException:
                pass
            self.manager.add_widget(tmp_screen)
        return 'ingredients_only_window_page_0'

    def on_leave(self, *args):
        self.manager.ids['ings_only_root_grid'].remove_widget(self.scroll)
        self.manager.ids['ings_only_root_grid'].remove_widget(self.go_button)


class IngredientsSelectionWindow(Screen):
    ingredients = ListProperty()
    cocktails = ListProperty()
    scroll = ScrollView()
    go_button = Button()

    def on_enter(self, *args):
        root_grid = self.manager.ids['ings_selection_root_grid']
        self.scroll = ScrollView(do_scroll_x=False, do_scroll_y=True)
        grid = GridLayout(cols=1, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        for item in sorted(KNOWN_INGREDIENTS.keys()):
            tmp_btn = Button(text=item, size_hint_y=None)
            if item in self.ingredients:
                change_color(tmp_btn)
            tmp_btn.font_size = tmp_btn.height / 3
            tmp_btn.bind(on_press=partial(self.manage, item))
            grid.add_widget(tmp_btn)

        self.scroll.add_widget(grid)
        root_grid.add_widget(self.scroll)
        self.go_button = Button(
            text='Узнать зелья',
            size_hint=(1, .1),
            pos_hint={'bottom': 1.0},
            background_color=[1, 2, 1, 3]
        )
        self.go_button.font_size = self.go_button.height / 3
        self.go_button.bind(on_press=self.calculate_cocktails)
        root_grid.add_widget(self.go_button)

    def calculate_cocktails(self, button):
        print(f'________________Calculate cocktails from selected {self.ingredients}.________________')
        alchemy_ingredients = self.ingredients
        toxin_lvl = 1
        oracle = AlchemyOracle(alchemy_ingredients, toxin_lvl)
        desired_cocktails = oracle.calculate_all_cocktails()
        self.cocktails = [str(x) for x in desired_cocktails]
        print(f'Found {len(self.cocktails)} cocktails.')
        if len(self.cocktails) == 0:
            self.parent.current = 'no_cocktails_window'
            self.parent.transition.direction = "left"
        else:
            self.parent.current = self.show_results()
            self.parent.transition.direction = "left"

    def show_results(self):
        result_pages = split_into_pages(self.cocktails)
        pages_amount = len(result_pages)
        for k in range(pages_amount):
            tmp_screen = DataPage(
                name=f'ingredients_selection_window_page_{k}',
                data=result_pages[k],
                page=k,
                pages_count=pages_amount,
                source='ingredients_selection_window'
            )
            try:
                old_screen = self.manager.get_screen(f'ingredients_selection_window_page_{k}')
                self.manager.remove_widget(old_screen)
            except ScreenManagerException:
                pass
            self.manager.add_widget(tmp_screen)
        return 'ingredients_selection_window_page_0'

    def manage(self, item, button):
        color = change_color(button)
        self.manage_ingredients(item, color)

    def manage_ingredients(self, ingredient, color):
        flag = is_base_color(color)
        if flag:
            if ingredient in self.ingredients:
                self.ingredients.remove(ingredient)
        else:
            self.ingredients.append(ingredient)

    def on_leave(self, *args):
        self.manager.ids['ings_selection_root_grid'].remove_widget(self.scroll)
        self.manager.ids['ings_selection_root_grid'].remove_widget(self.go_button)


class BothEffectsWindow(Screen):
    effects = ListProperty()
    scroll = ScrollView()

    def on_enter(self, *args):
        root_grid = self.manager.ids['both_effects_root_grid']
        self.scroll = ScrollView(do_scroll_x=False, do_scroll_y=True)
        grid = GridLayout(cols=1, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        for item in KNOWN_EFFECTS:
            tmp_btn = Button(text=item, size_hint_y=None)
            if item in self.effects:
                change_color(tmp_btn)
            tmp_btn.font_size = tmp_btn.height / 3
            tmp_btn.bind(on_press=partial(self.manage, item))
            grid.add_widget(tmp_btn)
        self.scroll.add_widget(grid)
        root_grid.add_widget(self.scroll)

    def manage(self, item, button):
        color = change_color(button)
        self.manage_effect(item, color)

    def manage_effect(self, item, color):
        flag = is_base_color(color)
        if flag:
            if item in self.effects:
                self.effects.remove(item)
        else:
            self.effects.append(item)

    def on_leave(self, *args):
        self.manager.ids['both_effects_root_grid'].remove_widget(self.scroll)


class BothIngredientsWindow(Screen):
    effects = ListProperty()
    ingredients = ListProperty()
    cocktails = ListProperty()
    scroll = ScrollView()
    go_button = Button()

    def on_enter(self, *args):
        self.effects = self.manager.ids['both_effects_window'].effects
        root_grid = self.manager.ids['both_ings_root_grid']
        self.scroll = ScrollView(do_scroll_x=False, do_scroll_y=True)
        grid = GridLayout(cols=1, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        for item in sorted(KNOWN_INGREDIENTS.keys()):
            tmp_btn = Button(text=item, size_hint_y=None)
            tmp_btn.font_size = tmp_btn.height / 3
            tmp_btn.bind(on_press=partial(self.manage, item))
            grid.add_widget(tmp_btn)

        self.scroll.add_widget(grid)
        root_grid.add_widget(self.scroll)
        self.go_button = Button(
            text='Узнать зелья',
            size_hint=(1, .1),
            pos_hint={'bottom': 1.0},
            background_color=[1, 2, 1, 3]
        )
        self.go_button.font_size = self.go_button.height / 3
        self.go_button.bind(on_press=self.calculate_cocktails)
        root_grid.add_widget(self.go_button)

    def manage(self, item, button):
        color = change_color(button)
        self.manage_ingredients(item, color)

    def manage_ingredients(self, ingredient, color):
        flag = is_base_color(color)
        if flag:
            if ingredient in self.ingredients:
                self.ingredients.remove(ingredient)
        else:
            self.ingredients.append(ingredient)

    def calculate_cocktails(self, button):
        print(f'_________Calculate cocktails from {len(self.ingredients)} '
              f'given ingredient(s) and {len(self.effects)} effects._________')
        alchemy_ingredients = self.ingredients
        toxin_lvl = 1
        oracle = AlchemyOracle(alchemy_ingredients, toxin_lvl)
        desired_cocktails = oracle.calculate_cocktails_with_effects(self.effects)
        self.cocktails = [str(x) for x in desired_cocktails]
        print(f'Found {len(self.cocktails)} cocktails.')
        if len(self.cocktails) == 0:
            self.parent.current = 'no_cocktails_window'
            self.parent.transition.direction = "left"
        else:
            self.parent.current = self.show_results()
            self.parent.transition.direction = "left"

    def show_results(self):
        result_pages = split_into_pages(self.cocktails)
        pages_amount = len(result_pages)
        for k in range(pages_amount):
            tmp_screen = DataPage(
                name=f'both_ings_window_page_{k}',
                data=result_pages[k],
                page=k,
                pages_count=pages_amount,
                source='both_ings_window'
            )
            try:
                old_screen = self.manager.get_screen(f'both_ings_window_page_{k}')
                self.manager.remove_widget(old_screen)
            except ScreenManagerException:
                pass
            self.manager.add_widget(tmp_screen)
        return 'both_ings_window_page_0'

    def on_leave(self, *args):
        self.manager.ids['both_ings_root_grid'].remove_widget(self.scroll)
        self.manager.ids['both_ings_root_grid'].remove_widget(self.go_button)


class NoCocktailsWindow(Screen):
    pass


class EffectsDictionaryWindow(Screen):
    scroll = ScrollView()

    def on_enter(self, *args):
        root_grid = self.manager.ids['effects_dict_root_grid']
        self.scroll = ScrollView(do_scroll_x=True, do_scroll_y=True)
        grid = GridLayout(cols=1, size_hint_y=None, size_hint_x=None)
        grid.bind(minimum_height=grid.setter('height'))
        grid.bind(minimum_size=grid.setter('size'))
        for k, v in EFFECTS_DICT.items():
            tmp = f'{k} {v}'
            tmp_lbl = Label(text=tmp, size_hint_y=None, size_hint_x=None, width=2000)
            tmp_lbl.font_size = tmp_lbl.height / 3
            grid.add_widget(tmp_lbl)
        self.scroll.add_widget(grid)
        root_grid.add_widget(self.scroll)

    def on_leave(self, *args):
        self.manager.ids['effects_dict_root_grid'].remove_widget(self.scroll)


class HealDictionaryWindow(Screen):
    scroll = ScrollView()

    def on_enter(self, *args):
        root_grid = self.manager.ids['heal_dict_root_grid']
        self.scroll = ScrollView(do_scroll_x=True, do_scroll_y=True)
        grid = GridLayout(cols=1, size_hint_y=None, size_hint_x=None)
        grid.bind(minimum_height=grid.setter('height'))
        grid.bind(minimum_size=grid.setter('size'))
        for k, v in HEAL_DICT.items():
            tmp = f'{k}: {v}'
            tmp_lbl = Label(text=tmp, size_hint_y=None, size_hint_x=None, width=2000)
            tmp_lbl.font_size = tmp_lbl.height / 3
            grid.add_widget(tmp_lbl)
        self.scroll.add_widget(grid)
        root_grid.add_widget(self.scroll)

    def on_leave(self, *args):
        self.manager.ids['heal_dict_root_grid'].remove_widget(self.scroll)


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("src/multi.kv")


class AlchemyApp(App):
    def build(self):
        return kv
