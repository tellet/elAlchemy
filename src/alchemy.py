"""Alchemy related classes"""
import time
from concurrent.futures import ThreadPoolExecutor
from itertools import combinations_with_replacement


class Spirit:
    KNOWN_SPIRITS_UPGRADES = {
        'Очищение': 'Антитоксин',
        'Лечение болезни': 'Антитоксин',
        'Обезболивающее': 'Стабилизация',
        'Восстановление': '???',
        'Имунноукрепляющее': 'Защита от ядов',
        'Слабость(Яд)': '???',
        'Сила': 'Антитоксин',
        'Стойкость': 'Безумие(Яд)(Ментальное)'
    }

    def __init__(self, name: str, effects: dict):
        self.name = name
        self.effects = effects

    def improved_singletons(self, effects: dict):
        res = []
        for key in effects.keys():
            tmp = {key: val for key, val in effects.items()}
            key_replace = self.KNOWN_SPIRITS_UPGRADES[key]
            tmp[key_replace] = tmp.pop(key)
            res.append(tmp)
        return res

    @staticmethod
    def generate_pairs(arr: list):
        pairs = []
        for i in range(0, len(arr) - 1):
            for j in range(i + 1, len(arr)):
                pairs.append((i, j))
        return pairs

    def improved_pairs(self, effects: dict):
        if len(effects) < 2:
            return self.improved_singletons(effects)
        res = []
        keys_list = [key for key in effects.keys()]
        for i, j in self.generate_pairs(keys_list):
            tmp = {key: val for key, val in effects.items()}
            key_1 = keys_list[i]
            key_2 = keys_list[j]
            key_replace_1 = self.KNOWN_SPIRITS_UPGRADES[key_1]
            key_replace_2 = self.KNOWN_SPIRITS_UPGRADES[key_2]
            tmp[key_replace_1] = tmp.pop(key_1)
            tmp[key_replace_2] = tmp.pop(key_2)
            res.append(tmp)
        return res

    @staticmethod
    def generate_triples(arr: list):
        triples = []
        for i in range(0, len(arr) - 2):
            for j in range(i + 1, len(arr) - 1):
                for k in range(i + 2, len(arr)):
                    triples.append((i, j, k))
        return triples

    def improved_triples(self, effects: dict):
        if len(effects) < 3:
            return self.improved_pairs(effects)
        res = []
        keys_list = [key for key in effects.keys()]
        for i, j, k in self.generate_triples(keys_list):
            tmp = {key: val for key, val in effects.items()}
            key_1 = keys_list[i]
            key_2 = keys_list[j]
            key_3 = keys_list[k]
            key_replace_1 = self.KNOWN_SPIRITS_UPGRADES[key_1]
            key_replace_2 = self.KNOWN_SPIRITS_UPGRADES[key_2]
            key_replace_3 = self.KNOWN_SPIRITS_UPGRADES[key_3]
            tmp[key_replace_1] = tmp.pop(key_1)
            tmp[key_replace_2] = tmp.pop(key_2)
            tmp[key_replace_3] = tmp.pop(key_3)
            res.append(tmp)
        return res

    def apply_upgrades(self, effects_to_improve: dict):
        to_improve = self.effects['any']
        # cocktail has X (1 or more) power effects (4 or more), select 1/2/3 subsets of those effects
        if to_improve == 1:
            return self.improved_singletons(effects_to_improve)
        if to_improve == 2:
            return self.improved_pairs(effects_to_improve)
        if to_improve == 3:
            return self.improved_triples(effects_to_improve)
        return None


class Catalyzer:
    def __init__(self, name, activation_effects=None, conditions=None):
        self.name = name
        if activation_effects:
            self.activation_effects = {key: activation_effects[key] for key in sorted(activation_effects)}
        else:
            self.activation_effects = None
        if conditions:
            self.conditions = {key: conditions[key] for key in sorted(conditions)}
        else:
            self.conditions = None

    def __str__(self):
        return f'{self.name}'


class Ingredient:
    def __init__(self, name: str, effects: dict, monstro: bool = False, mineral: bool = False, magic: bool = False, plant: bool = False):
        self.name = name
        self.effects = {key: effects[key] for key in sorted(effects)}
        self.monstro = monstro
        self.mineral = mineral
        self.plant = plant
        self.magic = magic

    def __str__(self):
        return f'{self.name}'

    def __add__(self, other):
        names = self.name.split('+')
        names.extend(other.name.split('+'))
        sum_name = '+'.join(sorted(names))

        sum_effects = {key: val for key, val in self.effects.items()}
        for key in other.effects.keys():
            if key in sum_effects:
                sum_effects[key] = sum_effects[key] + other.effects[key]
            else:
                sum_effects[key] = other.effects[key]
        return Ingredient(sum_name, sum_effects)

    def __eq__(self, other):
        if self.name != other.name:
            return False
        if len(self.effects) != len(other.effects):
            return False
        for key, val in self.effects.items():
            if other.effects[key] != val:
                return False
        return True


KNOWN_EFFECTS = [
    'Очищение',
    'Обезболивающее',
    'Восстановление',
    'Имунноукрепляющее',
    'Слабость(Яд)',
    'Сила',
    'Стойкость',
    'Лечение болезни',
    'Ясновидение(Ментальное)(m)',
    'Правда(Яд)(Ментальное)(m)',
    'Защита от проклятий(m)'
]

EFFECTS_DICT = {
    'Очищение': 'Сбросьте все зелья которые на вас действуют',
    'Обезболивающее': 'Доп карта жизни в госпитале',
    'Восстановление': 'Вдвое ускорено восстановление в госпитале',
    'Имунноукрепляющее': 'При получении болезни сбросьте болезнь и это зелье',
    'Слабость(Яд)': 'Нельзя пользоваться оружием, доспехи не работают',
    'Сила': 'Можно рвать верёвки, переносить 2 макроресурса за раз, помогает в данжах',
    'Стойкость': 'Иммунитет к пыткам и оглушению',
    'Cтабилизация': '=Обезболивающее, Нельзя умереть в тяжёлом ранении',
    'Лечение болезни': 'Позволяет аткивировать лечение определённых болезней при соблюдении определённых условий',
    'Защита от ядов': '=Имунноукрепляющее, При получении ядовитого зелья или превышения максимума интоксикации, сбросьте полученное зелье и это зелье',
    'Безумие (Яд) (Ментальное)': '=Стойкость, Агрессия ко всем окружающим. В тяжёлом ранении можно бегать. Вдвое сокращает время в тяжёлом ранении',
    'Антитоксин': 'В итоговое зелье не пишется, просто вычтите из Токсина, Значение токсина не может быть меньше 0',
    'Ясновидение(Ментальное)(m)': 'Можете задать вопрос региональщику, ответ не гарантирован',
    'Правда(Яд)(Ментальное)(m)': 'Вы не можете лгать',
    'Чистый разум': '=Ясновидение(Ментальное)(m), Иммунитет к ментальным эффектам',
    'Антипатия': '=Правда(Яд)(Ментальное)(m), Вас не добивают монстры',
    'Подавление магии': '=Защита от проклятий(m), На вас не действуют небоевые заклинания',
    'Востановление магии': '=Восстановление, Разово сбрасывает все Магические откаты (кулдауны) мага',
    'Защита от проклятий(m)': 'При получении проклятья, сбросьте его'
}

HEAL_DICT = {
    'Чесотка': 'Лечение болезни+Восстановление',
    'Гангрена': 'Лечение болезни+Очищение',
    'Столбняк': 'Лечение болезни+Спирт+Три разных ингридиента',
    'Мозговая горячка': 'Лечение болезни+Защита от ядов',
    'Чахотка': 'Лечение болезни+Магическая слабость',
    'Шанкра': 'Лечение болезни+Обезболивающее',
    'Холера': 'Лечение болезни+Стойкость+Не более двух ингридиентов',
    'Малярия': 'Лечение болезни+Крепкий спирт+Защита от ядов+Не токсичное',
    'Огневка': 'Лечение болезни+Ясновидение',
    'Костеломка': 'Лечение болезни+Стойкость+Спирт',
    'Аквагенная волдырница': 'Лечение болезни+Имунноукрепляющее+Токсин',
    'Глазная гниль': 'Лечение болезни+Стабилизация+Защита от ядов+Токсин',
    'Болотная лихорадка': 'Лечение болезни+Имунноукрепляющее',
    'Чернокровие': 'Лечение болезни+Безумие+Спирт',
    'Хорея': 'Лечение болезни+Сила',
    'Лунная болезнь': 'Лечение болезни+Чистый разум+Крепкий спирт',
}


KNOWN_INGREDIENTS = {
    'Вороний глаз': Ingredient('Вороний глаз', {'Восстановление': 1, 'Токсин': 1, 'Защита от проклятий(m)': 1}, magic=True, plant=True),
    'Мышехвост': Ingredient('Мышехвост', {'Обезболивающее': 1, 'Стойкость': 1, 'Токсин': 1}, plant=True),
    'Берберка': Ingredient('Берберка', {'Лечение болезни': 2, 'Имунноукрепляющее': 1, 'Слабость(Яд)': 3, 'Токсин': 1}, plant=True),
    'Аренария': Ingredient('Аренария', {'Очищение': 1, 'Лечение болезни': 1, 'Стойкость': 1}, plant=True),
    'Чистолист': Ingredient('Чистолист', {'Очищение': 1, 'Обезболивающее': 1, 'Восстановление': 1, 'Стойкость': 1}, plant=True),
    'Безмер': Ingredient('Безмер', {'Лечение болезни': 1, 'Обезболивающее': 1}, plant=True),
    'Вербена': Ingredient('Вербена', {'Очищение': 2, 'Имунноукрепляющее': 1}, plant=True),
    'Волкобой': Ingredient('Волкобой', {'Обезболивающее': 2, 'Имунноукрепляющее': 1}, plant=True),
    'Волокна хна': Ingredient('Волокна хна', {'Очищение': 1, 'Сила': 1, 'Стойкость': 2}, plant=True),
    'Дождевик': Ingredient('Дождевик', {'Очищение': 1, 'Ясновидение(Ментальное)(m)': 1}, magic=True, plant=True),
    'Душистый перец': Ingredient('Душистый перец', {'Очищение': 1, 'Сила': 1}, plant=True),
    'Ласточкина трава': Ingredient('Ласточкина трава',
                                   {'Лечение болезни': 1, 'Восстановление': 3, 'Имунноукрепляющее': 1}, plant=True),
    'Мирт': Ingredient('Мирт', {'Очищение': 2}, plant=True),
    'Гинация': Ingredient('Гинация', {'Очищение': 1, 'Лечение болезни': 1}, plant=True),
    'Чемерица': Ingredient('Чемерица', {'Обезболивающее': 1, 'Восстановление': 1}, plant=True),
    'Собачья петрушка': Ingredient('Собачья петрушка', {'Очищение': 1, 'Сила': 1}, plant=True),
    'Одуванчик': Ingredient('Одуванчик', {'Слабость(Яд)': 1}, plant=True),
    'Баллиса': Ingredient('Баллиса', {'Очищение': 1, 'Восстановление': 1, 'Сила': 1}, plant=True),
    'Подорожник': Ingredient('Подорожник', {'Очищение': 1, 'Восстановление': 1, 'Стойкость': 2}, plant=True),
    # Распространённые растения
    'Грибы-шибальцы': Ingredient('Грибы-шибальцы', {'Обезболивающее': 2, 'Слабость(Яд)': 2, 'Токсин': 1, 'Ясновидение(Ментальное)(m)': 1}, magic=True, plant=True),
    'Кровостой': Ingredient('Кровостой', {'Обезболивающее': 2, 'Восстановление': 2, 'Токсин': 1}, plant=True),
    'Раног': Ingredient('Раног', {'Очищение': 1, 'Стойкость': 1, 'Токсин': 1}, plant=True),
    'Спорынья': Ingredient('Спорынья', {'Обезболивающее': 2, 'Восстановление': 2, 'Токсин': 2}, plant=True),
    'Каприфоль': Ingredient('Каприфоль', {'Лечение болезни': 1, 'Обезболивающее': 1, 'Восстановление': 1, 'Имунноукрепляющее': 1}, plant=True),
    'Нострикс': Ingredient('Нострикс', {'Имунноукрепляющее': 2, 'Стойкость': 1}, plant=True),
    'Омела': Ingredient('Омела', {'Очищение': 3}, plant=True),
    'Паутинник': Ingredient('Паутинник', {'Ясновидение(Ментальное)(m)': 2, 'Правда(Яд)(Ментальное)(m)': 1}, magic=True, plant=True),
    'Переступень': Ingredient('Переступень', {'Обезболивающее': 1, 'Слабость(Яд)': 2, 'Сила': 1}, plant=True),
    'Роголистник': Ingredient('Роголистник', {'Сила': 1, 'Ясновидение(Ментальное)(m)': 1, 'Правда(Яд)(Ментальное)(m)': 1}, magic=True, plant=True),
    'Хмель': Ingredient('Хмель', {'Очищение': 2, 'Имунноукрепляющее': 2, 'Слабость(Яд)': 2}, plant=True),
    # Распространённые минералы
    'Княжеская вода': Ingredient('Княжеская вода', {
        'Лечение болезни': 1, 'Восстановление': 1, 'Стойкость': 1, 'Токсин': 1, 'Ясновидение(Ментальное)(m)': 1
    }, mineral=True, magic=True),
    'Соли': Ingredient('Соли', {'Сила': 2, 'Токсин': 1}, mineral=True),
    'Ртуть': Ingredient('Ртуть', {'Лечение болезни': 2, 'Слабость(Яд)': 2, 'Токсин': 2}, mineral=True),
    'Сера': Ingredient('Сера', {'Слабость(Яд)': 1, 'Токсин': 2}, mineral=True),
    'Винный камень': Ingredient('Винный камень', {'Очищение': 3, 'Имунноукрепляющее': 1, 'Стойкость': 2}, mineral=True),
    # Распространённые части монстров
    'Печень монстра': Ingredient('Печень монстра', {'Имунноукрепляющее': 2, 'Стойкость': 2, 'Токсин': 1}, monstro=True),
    'Кровь трупоеда': Ingredient('Кровь трупоеда', {'Восстановление': 3, 'Токсин': 2}, monstro=True),
    'Слюна нежити': Ingredient('Слюна нежити', {'Обезболивающее': 4, 'Слабость(Яд)': 4, 'Токсин': 3}, monstro=True),
    'Яд эндриаги': Ingredient('Яд эндриаги', {'Восстановление': 4, 'Токсин': 5, 'Ясновидение(Ментальное)(m)': 4}, monstro=True, magic=True),
    # Редкие растения
    'Сенжигорн': Ingredient('Сенжигорн', {
        'Лечение болезни': 1,
        'Обезболивающее': 1,
        'Восстановление': 1,
        'Стойкость': 1,
        'Имунноукрепляющее': 1,
        'Очищение': 1,
        'Слабость(Яд)': 1,
        'Сила': 1,
        'Ясновидение(Ментальное)(m)': 1, 'Правда(Яд)(Ментальное)(m)': 1, 'Защита от проклятий(m)': 1,
        'Токсин': 1
    }, magic=True, plant=True),
    'Двоерог': Ingredient('Двоерог', {
        'Обезболивающее': 1,
        'Сила': 2,
        'Стойкость': 3,
        'Ясновидение(Ментальное)(m)': 1,
        'Токсин': 1
    }, magic=True, plant=True),
    'Белая плесень': Ingredient('Белая плесень',
                                {'Обезболивающее': 3, 'Ясновидение(Ментальное)(m)': 3, 'Правда(Яд)(Ментальное)(m)': 2, 'Токсин': 2}, magic=True, plant=True),
    'Мандрагора': Ingredient('Мандрагора', {
        'Токсин': 3,
        'Лечение болезни': 2,
        'Имунноукрепляющее': 3,
        'Ясновидение(Ментальное)(m)': 2, 'Правда(Яд)(Ментальное)(m)': 2, 'Защита от проклятий(m)': 1,
        'Стойкость': 3
    }, magic=True, plant=True),
    'Зубр-трава': Ingredient('Зубр-трава', {'Лечение болезни': 1, 'Сила': 3, 'Стойкость': 3}, plant=True),
    # Редкие минералы
    'Беозар': Ingredient('Беозар', {'Очищение': 4, 'Лечение болезни': 2, 'Слабость(Яд)': 2}, mineral=True),
    # Редкие монстры
    'Феромоны': Ingredient('Феромоны', {'Токсин': 1, 'Ясновидение(Ментальное)(m)': 3, 'Правда(Яд)(Ментальное)(m)': 3}, magic=True, monstro=True),
    'Светлая эссенция': Ingredient('Светлая эссенция', {
        'Токсин': 1,
        'Очищение': 4,
        'Ясновидение(Ментальное)(m)': 4, 'Правда(Яд)(Ментальное)(m)': 4, 'Защита от проклятий(m)': 2,
        'Стойкость': 2
    }, magic=True, monstro=True),
    'Секреции монстра': Ingredient('Секреции монстра', {'Токсин': 2, 'Сила': 4}, monstro=True),
    'Тёмная эсенция': Ingredient('Тёмная эсенция', {'Токсин': 2, 'Слабость(Яд)': 4, 'Ясновидение(Ментальное)(m)': 4, 'Правда(Яд)(Ментальное)(m)': 4},
                                 magic=True, monstro=True),
    'Костный мозг': Ingredient('Костный мозг',
                               {'Токсин': 3, 'Лечение болезни': 4, 'Обезболивающее': 4, 'Имунноукрепляющее': 4}, monstro=True),
    'Эктоплазма': Ingredient('Эктоплазма', {
        'Токсин': 3,
        'Очищение': 3,
        'Обезболивающее': 3,
        'Восстановление': 3,
        'Ясновидение(Ментальное)(m)': 4, 'Правда(Яд)(Ментальное)(m)': 4, 'Защита от проклятий(m)': 1
    }, magic=True, monstro=True),
    'Желчь': Ingredient('Желчь', {
        'Токсин': 4,
        'Очищение': 3,
        'Лечение болезни': 2,
        'Слабость(Яд)': 2,
        'Сила': 3
    }, monstro=True),
    # Уникальные растения
    'Кора проклятого дуба': Ingredient('Кора проклятого дуба', {
        'Токсин': 2, 'Слабость(Яд)': 4, 'Ясновидение(Ментальное)(m)': 4, 'Защита от проклятий(m)': 4
    }, magic=True, plant=True),
    # Уникальные минералы
    'Толчёный жемчуг': Ingredient('Толчёный жемчуг', {
        'Имунноукрепляющее': 1,
        'Слабость(Яд)': 3,
        'Ясновидение(Ментальное)(m)': 3, 'Защита от проклятий(m)': 2
    }, magic=True, mineral=True),
    'Фосфор': Ingredient('Фосфор', {'Токсин': 2, 'Слабость(Яд)': 2, 'Правда(Яд)(Ментальное)(m)': 2}, magic=True, mineral=True),
    # Уникальные части монстров
    'Кровь альпа': Ingredient('Кровь альпа', {
        'Токсин': 2,
        'Очищение': 1,
        'Лечение болезни': 3,
        'Восстановление': 4,
        'Стойкость': 4
    }, monstro=True),
    'Глаза эндриаги': Ingredient('Глаза эндриаги', {'Токсин': 2, 'Восстановление': 4, 'Ясновидение(Ментальное)(m)': 4}, magic=True, monstro=True),
    'Кровь гуля': Ingredient('Кровь гуля', {'Токсин': 3, 'Восстановление': 3, 'Сила': 3}, monstro=True),
    'Костный мозг гуля': Ingredient('Костный мозг гуля', {
        'Токсин': 4,
        'Лечение болезни': 4,
        'Обезболивающее': 4,
        'Восстановление': 2,
        'Имунноукрепляющее': 4,
        'Сила': 4
    }, monstro=True),
    'Магическая пыль': Ingredient('Магическая пыль', {
        'Очищение': 2,
        'Лечение болезни': 3,
        'Обезболивающее': 3,
        'Восстановление': 3,
        'Имунноукрепляющее': 3,
        'Стойкость': 4,
    }, monstro=True),
    'Смола лешего': Ingredient('Смола лешего', {
        'Лечение болезни': 4, 'Имунноукрепляющее': 4, 'Сила': 4, 'Ясновидение(Ментальное)(m)': 4
    }, magic=True, monstro=True)
}

ALL_ROUND = {
    'Вороний глаз': Ingredient('Вороний глаз', {'Восстановление': 1, 'Токсин': 1, 'Защита от проклятий(m)': 1}, magic=True, plant=True),
    'Мышехвост': Ingredient('Мышехвост', {'Обезболивающее': 1, 'Стойкость': 1, 'Токсин': 1}, plant=True),
    'Берберка': Ingredient('Берберка', {'Лечение болезни': 2, 'Имунноукрепляющее': 1, 'Слабость(Яд)': 3, 'Токсин': 1}, plant=True),
    'Аренария': Ingredient('Аренария', {'Очищение': 1, 'Лечение болезни': 1, 'Стойкость': 1}, plant=True),
    'Чистолист': Ingredient('Чистолист', {'Очищение': 1, 'Обезболивающее': 1, 'Восстановление': 1, 'Стойкость': 1}, plant=True),
    'Безмер': Ingredient('Безмер', {'Лечение болезни': 1, 'Обезболивающее': 1}, plant=True),
    'Вербена': Ingredient('Вербена', {'Очищение': 2, 'Имунноукрепляющее': 1}, plant=True),
    'Волкобой': Ingredient('Волкобой', {'Обезболивающее': 2, 'Имунноукрепляющее': 1}, plant=True),
    'Волокна хна': Ingredient('Волокна хна', {'Очищение': 1, 'Сила': 1, 'Стойкость': 2}, plant=True),
    'Дождевик': Ingredient('Дождевик', {'Очищение': 1, 'Ясновидение(Ментальное)(m)': 1}, magic=True, plant=True),
    'Душистый перец': Ingredient('Душистый перец', {'Очищение': 1, 'Сила': 1}, plant=True),
    'Ласточкина трава': Ingredient('Ласточкина трава',
                                   {'Лечение болезни': 1, 'Восстановление': 3, 'Имунноукрепляющее': 1}, plant=True),
    'Мирт': Ingredient('Мирт', {'Очищение': 2}, plant=True),
    'Гинация': Ingredient('Гинация', {'Очищение': 1, 'Лечение болезни': 1}, plant=True),
    'Чемерица': Ingredient('Чемерица', {'Обезболивающее': 1, 'Восстановление': 1}, plant=True),
    'Собачья петрушка': Ingredient('Собачья петрушка', {'Очищение': 1, 'Сила': 1}, plant=True),
    'Одуванчик': Ingredient('Одуванчик', {'Слабость(Яд)': 1}, plant=True),
    'Баллиса': Ingredient('Баллиса', {'Очищение': 1, 'Восстановление': 1, 'Сила': 1}, plant=True),
    'Подорожник': Ingredient('Подорожник', {'Очищение': 1, 'Восстановление': 1, 'Стойкость': 2}, plant=True),
}

COMMON = {
    # Распространённые растения
    'Грибы-шибальцы': Ingredient('Грибы-шибальцы', {'Обезболивающее': 2, 'Слабость(Яд)': 2, 'Токсин': 1, 'Ясновидение(Ментальное)(m)': 1}, magic=True, plant=True),
    'Кровостой': Ingredient('Кровостой', {'Обезболивающее': 2, 'Восстановление': 2, 'Токсин': 1}, plant=True),
    'Раног': Ingredient('Раног', {'Очищение': 1, 'Стойкость': 1, 'Токсин': 1}, plant=True),
    'Спорынья': Ingredient('Спорынья', {'Обезболивающее': 2, 'Восстановление': 2, 'Токсин': 2}, plant=True),
    'Каприфоль': Ingredient('Каприфоль', {'Лечение болезни': 1, 'Обезболивающее': 1, 'Восстановление': 1, 'Имунноукрепляющее': 1}, plant=True),
    'Нострикс': Ingredient('Нострикс', {'Имунноукрепляющее': 2, 'Стойкость': 1}, plant=True),
    'Омела': Ingredient('Омела', {'Очищение': 3}, plant=True),
    'Паутинник': Ingredient('Паутинник', {'Ясновидение(Ментальное)(m)': 2, 'Правда(Яд)(Ментальное)(m)': 1}, magic=True, plant=True),
    'Переступень': Ingredient('Переступень', {'Обезболивающее': 1, 'Слабость(Яд)': 2, 'Сила': 1}, plant=True),
    'Роголистник': Ingredient('Роголистник', {'Сила': 1, 'Ясновидение(Ментальное)(m)': 1, 'Правда(Яд)(Ментальное)(m)': 1}, magic=True, plant=True),
    'Хмель': Ingredient('Хмель', {'Очищение': 2, 'Имунноукрепляющее': 2, 'Слабость(Яд)': 2}, plant=True),
    # Распространённые минералы
    'Княжеская вода': Ingredient('Княжеская вода', {
        'Лечение болезни': 1, 'Восстановление': 1, 'Стойкость': 1, 'Токсин': 1, 'Ясновидение(Ментальное)(m)': 1
    }, mineral=True, magic=True),
    'Соли': Ingredient('Соли', {'Сила': 2, 'Токсин': 1}, mineral=True),
    'Ртуть': Ingredient('Ртуть', {'Лечение болезни': 2, 'Слабость(Яд)': 2, 'Токсин': 2}, mineral=True),
    'Сера': Ingredient('Сера', {'Слабость(Яд)': 1, 'Токсин': 2}, mineral=True),
    'Винный камень': Ingredient('Винный камень', {'Очищение': 3, 'Имунноукрепляющее': 1, 'Стойкость': 2}, mineral=True),
    # Распространённые части монстров
    'Печень монстра': Ingredient('Печень монстра', {'Имунноукрепляющее': 2, 'Стойкость': 2, 'Токсин': 1}, monstro=True),
    'Кровь трупоеда': Ingredient('Кровь трупоеда', {'Восстановление': 3, 'Токсин': 2}, monstro=True),
    'Слюна нежити': Ingredient('Слюна нежити', {'Обезболивающее': 4, 'Слабость(Яд)': 4, 'Токсин': 3}, monstro=True),
    'Яд эндриаги': Ingredient('Яд эндриаги', {'Восстановление': 4, 'Токсин': 5, 'Ясновидение(Ментальное)(m)': 4}, monstro=True, magic=True)
}

RARE = {
    'Сенжигорн': Ingredient('Сенжигорн', {
        'Лечение болезни': 1,
        'Обезболивающее': 1,
        'Восстановление': 1,
        'Стойкость': 1,
        'Имунноукрепляющее': 1,
        'Очищение': 1,
        'Слабость(Яд)': 1,
        'Сила': 1,
        'Ясновидение(Ментальное)(m)': 1, 'Правда(Яд)(Ментальное)(m)': 1, 'Защита от проклятий(m)': 1,
        'Токсин': 1
    }, magic=True, plant=True),
    'Двоерог': Ingredient('Двоерог', {
        'Обезболивающее': 1,
        'Сила': 2,
        'Стойкость': 3,
        'Ясновидение(Ментальное)(m)': 1,
        'Токсин': 1
    }, magic=True, plant=True),
    'Белая плесень': Ingredient('Белая плесень',
                                {'Обезболивающее': 3, 'Ясновидение(Ментальное)(m)': 3, 'Правда(Яд)(Ментальное)(m)': 2, 'Токсин': 2}, magic=True, plant=True),
    'Мандрагора': Ingredient('Мандрагора', {
        'Токсин': 3,
        'Лечение болезни': 2,
        'Имунноукрепляющее': 3,
        'Ясновидение(Ментальное)(m)': 2, 'Правда(Яд)(Ментальное)(m)': 2, 'Защита от проклятий(m)': 1,
        'Стойкость': 3
    }, magic=True, plant=True),
    'Зубр-трава': Ingredient('Зубр-трава', {'Лечение болезни': 1, 'Сила': 3, 'Стойкость': 3}, plant=True),
    # Редкие минералы
    'Беозар': Ingredient('Беозар', {'Очищение': 4, 'Лечение болезни': 2, 'Слабость(Яд)': 2}, mineral=True),
    # Редкие монстры
    'Феромоны': Ingredient('Феромоны', {'Токсин': 1, 'Ясновидение(Ментальное)(m)': 3, 'Правда(Яд)(Ментальное)(m)': 3}, magic=True, monstro=True),
    'Светлая эссенция': Ingredient('Светлая эссенция', {
        'Токсин': 1,
        'Очищение': 4,
        'Ясновидение(Ментальное)(m)': 4, 'Правда(Яд)(Ментальное)(m)': 4, 'Защита от проклятий(m)': 2,
        'Стойкость': 2
    }, magic=True, monstro=True),
    'Секреции монстра': Ingredient('Секреции монстра', {'Токсин': 2, 'Сила': 4}, monstro=True),
    'Тёмная эсенция': Ingredient('Тёмная эсенция', {'Токсин': 2, 'Слабость(Яд)': 4, 'Ясновидение(Ментальное)(m)': 4, 'Правда(Яд)(Ментальное)(m)': 4},
                                 magic=True, monstro=True),
    'Костный мозг': Ingredient('Костный мозг',
                               {'Токсин': 3, 'Лечение болезни': 4, 'Обезболивающее': 4, 'Имунноукрепляющее': 4}, monstro=True),
    'Эктоплазма': Ingredient('Эктоплазма', {
        'Токсин': 3,
        'Очищение': 3,
        'Обезболивающее': 3,
        'Восстановление': 3,
        'Ясновидение(Ментальное)(m)': 4, 'Правда(Яд)(Ментальное)(m)': 4, 'Защита от проклятий(m)': 1
    }, magic=True, monstro=True),
    'Желчь': Ingredient('Желчь', {
        'Токсин': 4,
        'Очищение': 3,
        'Лечение болезни': 2,
        'Слабость(Яд)': 2,
        'Сила': 3
    }, monstro=True)
}

UNIQUE = {
    'Кора проклятого дуба': Ingredient('Кора проклятого дуба', {
        'Токсин': 2, 'Слабость(Яд)': 4, 'Ясновидение(Ментальное)(m)': 4, 'Защита от проклятий(m)': 4
    }, magic=True, plant=True),
    # Уникальные минералы
    'Толчёный жемчуг': Ingredient('Толчёный жемчуг', {
        'Имунноукрепляющее': 1,
        'Слабость(Яд)': 3,
        'Ясновидение(Ментальное)(m)': 3, 'Защита от проклятий(m)': 2
    }, magic=True, mineral=True),
    'Фосфор': Ingredient('Фосфор', {'Токсин': 2, 'Слабость(Яд)': 2, 'Правда(Яд)(Ментальное)(m)': 2}, magic=True, mineral=True),
    # Уникальные части монстров
    'Кровь альпа': Ingredient('Кровь альпа', {
        'Токсин': 2,
        'Очищение': 1,
        'Лечение болезни': 3,
        'Восстановление': 4,
        'Стойкость': 4
    }, monstro=True),
    'Глаза эндриаги': Ingredient('Глаза эндриаги', {'Токсин': 2, 'Восстановление': 4, 'Ясновидение(Ментальное)(m)': 4}, magic=True, monstro=True),
    'Кровь гуля': Ingredient('Кровь гуля', {'Токсин': 3, 'Восстановление': 3, 'Сила': 3}, monstro=True),
    'Костный мозг гуля': Ingredient('Костный мозг гуля', {
        'Токсин': 4,
        'Лечение болезни': 4,
        'Обезболивающее': 4,
        'Восстановление': 2,
        'Имунноукрепляющее': 4,
        'Сила': 4
    }, monstro=True),
    'Магическая пыль': Ingredient('Магическая пыль', {
        'Очищение': 2,
        'Лечение болезни': 3,
        'Обезболивающее': 3,
        'Восстановление': 3,
        'Имунноукрепляющее': 3,
        'Стойкость': 4,
    }, monstro=True),
    'Смола лешего': Ingredient('Смола лешего', {
        'Лечение болезни': 4, 'Имунноукрепляющее': 4, 'Сила': 4, 'Ясновидение(Ментальное)(m)': 4
    }, magic=True, monstro=True)
}

KNOWN_CATALYZERS = [
    Catalyzer('Двоерог', activation_effects={'фисштех': True}),
    Catalyzer('Грибы-шибальцы', activation_effects={'Обезболивающее': True}),
    Catalyzer('Омела', activation_effects={'Токсин': -2}, conditions={'Очищение': 4}),
    Catalyzer('Хмель', activation_effects={'Слабость(Яд)': True}, conditions={'Безумие(Яд)(Ментальное)': 4}),
    Catalyzer('Княжеская вода', activation_effects={
        'Ясновидение(Ментальное)(m)': False,
        'Правда(Яд)(Ментальное)(m)': False,
        'Чистый разум': False,
        'Антипатия': False,
        'Защита от проклятий(m)': False,
        'Подавление магии': False,
        'Востановление магии': False
    }, conditions=None),
    Catalyzer('Соли', activation_effects={'Минерал, все эффекты': 3}),
    Catalyzer('Ртуть', activation_effects={'Дополнительные свойства для активации лечения': False}),
    Catalyzer('Сера', activation_effects={'Монстр, все эффекты': 3}),
    Catalyzer('Кровь трупоеда', activation_effects={'Монстр, все эффекты': 3}, conditions={'Защита от проклятий(m)': 4}),
    Catalyzer('Слюна нежити', {'Разговор': False}, conditions=None),
    Catalyzer('Яд эндриаги', {'Слабость(Яд)': True, 'Магическая Слабость(Яд)': True}, conditions=None),
    Catalyzer('Правда(Яд)(Ментальное)(m)', {'Надо ответить': True}, conditions=None),
    Catalyzer('Мандрагора', {'all effects, one plant': 3}, conditions=None),
    Catalyzer('Зубр-трава', {'rituals power': 'x2'}, conditions=None),
    Catalyzer('Беозар', {'Токсин': 0}, conditions=None),
    Catalyzer('Светлая эсенция', {'Поднять нежитью': False}, conditions=None),
    Catalyzer('Секреции монстра', {'Магическая Слабость(Яд)': True}, conditions=None),
    Catalyzer('Тёмная эсенция', {'Смерть': True}, conditions=None),
    Catalyzer('Толчёный жемчуг', {'кулдаун': False}, conditions=None),
    Catalyzer('Фосфор', {'Длительность': 2}, conditions=None),
    Catalyzer('Кровь альпа', {'Токсин': '# of different ingr'}, conditions=None),
    Catalyzer('Кровь гуля', {'Восстановление': True, 'Сила': True}, conditions=None),
    Catalyzer('Магическая пыль', {'Немагические эффекты': False}, conditions=None),
    Catalyzer('Смола лешего', {'Длительность': 100500}, conditions=None),

]

KNOWN_SPIRITS_UPGRADES = [
    {'Очищение': 'Антитоксин'},
    {'Лечение болезни': 'Антитоксин'},
    {'Обезболивающее': 'Стабилизация'},
    {'Восстановление': 'Восстановление магии'},
    {'Имунноукрепляющее': 'Защита от ядов'},
    {'Слабость(Яд)': 'Магическая Слабость(Яд)'},
    {'Сила': 'Антитоксин'},
    {'Стойкость': 'Безумие(Яд)(Ментальное)'},
    {'Ясновидение(Ментальное)(m)': 'Чистый разум'},
    {'Правда(Яд)(Ментальное)(m)': 'Антипатия'},
    {'Защита от проклятий(m)': 'Подавление магии'}
]

# Spirits only apply to those effects with power 4
KNOWN_SPIRITS = [
    Spirit('Спирт', {'any': 1}),
    Spirit('Крепкий спирт', {'any': 2}),
    Spirit('Махакамский спирт', {'any': 3}),
    Spirit('Настойка из мандрагоры', {'any': 3, 'Токсин': -1}),
    Spirit('Алкогест', {'any': 3, 'Replace 1 ingr with catalyzer': True}),
]


def of_type(ingredient_name: str) -> str:
    if ALL_ROUND.get(ingredient_name):
        return 'повсеместные'
    if COMMON.get(ingredient_name):
        return 'распространенные'
    if RARE.get(ingredient_name):
        return 'редкие'
    if UNIQUE.get(ingredient_name):
        return 'уникальные'
    return 'unknown'


class Cocktail:
    def __init__(self, ingredients):
        self.ingredients = ingredients
        ingredients_sum = self.get_ingredients_sum()
        self.receipt = ingredients_sum.name
        self.result_effects_dict = ingredients_sum.effects
        self.toxin = ingredients_sum.effects.get('Токсин', 0)
        self.result_powered_effects_dict = self.get_power_effects()
        self.is_effective = self.is_effective()
        self.ingredients_set = set()
        for ing in self.ingredients:
            self.ingredients_set.add(ing.name)

    def get_ingredients_sum(self) -> Ingredient:
        ingredients_sum = self.ingredients[0]
        tmp_len = len(self.ingredients)
        for i in range(1, tmp_len):
            ingredients_sum = ingredients_sum + self.ingredients[i]
        return ingredients_sum

    def get_power_effects(self) -> dict:
        result_dict = {}
        for key, value in self.result_effects_dict.items():
            if value >= 4:
                result_dict[key] = value
        return result_dict

    def is_effective(self):
        return len(self.result_powered_effects_dict.keys()) > 0

    def is_magic(self):
        """
        Check if cocktail has got a magic powered (>= 4) effect.
        :return: bool
        """
        for key in self.result_powered_effects_dict.keys():
            if '(m)' in key:
                return True
        return False

    def __str__(self):
        tmp = {key: val for key, val in self.result_powered_effects_dict.items()}
        tmp['Токсин'] = self.toxin
        return f'{self.receipt} {tmp}'

    def __eq__(self, other):
        if len(self.result_effects_dict) != len(other.result_effects_dict):
            return False
        for key, val in self.result_effects_dict.items():
            if key not in other.result_effects_dict or other.result_effects_dict[key] != val:
                return False
        return True


class Alchemy:
    def __init__(self, ingredients):
        if not ingredients:
            raise ValueError('Should be at least 1 ingredient')
        self.given_ingredients = sorted(ingredients)
        self.known_ingredients = []
        for name in sorted(ingredients):
            self.known_ingredients.append(KNOWN_INGREDIENTS[name])
        self.ing_amount = len(self.known_ingredients)
        self.cocktail_ing_amount = 4
        self.all_cocktails = []
        self.get_all_possible_cocktails()
        self.effective_cocktails = self.get_effective_cocktails()

    def cocktail_from_combination(self, ingredients):
        cocktail = Cocktail(ingredients)
        self.all_cocktails.append(cocktail)

    def get_all_possible_cocktails(self):
        all_combinations = self.generate_all_possible_combinations()
        for combination in all_combinations:
            self.cocktail_from_combination(combination)

    def generate_all_possible_combinations(self):
        result = []
        for i in range(self.cocktail_ing_amount):
            result += self.generate_combinations_of_length(i + 1)
        print(f'All possible combinations amount is: {len(result)}')
        return result

    def generate_combinations_of_length(self, ingredients_amount: int = 1):
        result = []
        tmp_result = combinations_with_replacement(self.given_ingredients, ingredients_amount)
        for itm in tmp_result:
            tmp_ingredients = [KNOWN_INGREDIENTS[x] for x in itm]
            result.append(tmp_ingredients)
        print(f'All possible cocktails ({ingredients_amount} ingr-s) amount is: {len(result)}')
        return result

    def get_effective_cocktails(self):
        """
        Select those cocktails with at least one effect of power >= 4.
        :return: list of Cocktails
        """
        result = []
        for cocktail in self.all_cocktails:
            if cocktail.is_effective:
                result.append(cocktail)
        print(f'Effective cocktails amount is: {len(result)}')
        return result

    def get_magic_cocktails(self):
        """
        Select those cocktails with at least one magic effect of power >= 4.
        :return: list of Cocktails
        """
        result = []
        for cocktail in self.all_cocktails:
            if cocktail.is_effective and cocktail.is_magic():
                result.append(cocktail)
        return result

    def get_equivalent_cocktails(self, base_cocktail: Cocktail):
        result = []
        for cocktail in self.get_effective_cocktails():
            if cocktail == base_cocktail:
                result.append(cocktail)
        return result

    @staticmethod
    def get_all_spirited_cocktails_from_base(base_cocktail: Cocktail, known_spirits) -> None:
        for spirit in known_spirits:
            power_effects = {key: val for key, val in base_cocktail.result_effects_dict.items() if val >= 4}
            weak_effects = {key: val for key, val in base_cocktail.result_effects_dict.items() if val < 4}
            print(f'\n\nCheck `{spirit.name}` application on `{power_effects}`:')
            spirited_effects = spirit.apply_upgrades(power_effects)
            if spirited_effects:
                for _ in spirited_effects:
                    _.update(weak_effects)
                    print(_)
            else:
                print('Unknown.')


if __name__ == '__main__':
    alchemy_ingredients = []
    for item in KNOWN_INGREDIENTS.keys():
        alchemy_ingredients.append(item)
    print(f'Ingredients amount is: {len(alchemy_ingredients)}')
    start = time.time()
    oracle = Alchemy(alchemy_ingredients)
    end = time.time()
    print("The time of execution of above program is :", end - start)

