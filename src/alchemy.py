"""Alchemy related classes"""
import time
from itertools import combinations_with_replacement

from src.elements.cocktail import Cocktail
from src.elements.ingredient import Ingredient

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


class Alchemy:
    """
    Alchemy is a set of Cocktails.
    """
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
        """
        Calculate a cocktail from the given combination of ingredients.
        :param ingredients:
        :return: None
        """
        cocktail = Cocktail(ingredients)
        self.all_cocktails.append(cocktail)

    def get_all_possible_cocktails(self):
        all_combinations = self.generate_all_possible_combinations()
        for combination in all_combinations:
            self.cocktail_from_combination(combination)

    def generate_all_possible_combinations(self):
        """
        Given the maximum possible amount of ingredients in a cocktail
        generate the cocktails.
        :return: list
        """
        result = []
        for i in range(self.cocktail_ing_amount):
            result += self.generate_combinations_of_length(i + 1)
        print(f'All possible combinations amount is: {len(result)}')
        return result

    def generate_combinations_of_length(self, ingredients_amount: int = 1):
        """
        Given the amount of ingredients in a cocktail generate all possible cocktails from all known ingredients.
        :param ingredients_amount:
        :return: list
        """
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

    @staticmethod
    def get_cocktail_diff(cocktail_1, cocktail_2):
        ingredients_diff = []
        for ing in cocktail_1.ingredients_list:
            if ing not in cocktail_2.ingredients_list:
                ingredients_diff.append(ing)
        return ingredients_diff

    def get_equivalent_cocktails(self, base_cocktail: Cocktail, cocktails):
        """
        Consider two cocktails to be equivalent when
        active effects are the same
        and toxin levels are the same
        and combinations of ingredients differ by 1 ingredient
        :param base_cocktail:
        :param cocktails:
        :return:
        """
        result = []
        final_result = [base_cocktail]
        for cocktail in cocktails:
            # all active effects should be the same
            # toxin lvl should be the same
            base_effects = base_cocktail.result_powered_effects_dict.keys()
            current_effects = cocktail.result_powered_effects_dict.keys()
            if base_effects == current_effects \
                    and cocktail.toxin == base_cocktail.toxin:
                result.append(cocktail)
        for cocktail in result:
            # cocktails ingredients may differ in 1 ingredient
            diff = self.get_cocktail_diff(cocktail, base_cocktail)
            if len(diff) == 1 \
                    and abs(len(base_cocktail.ingredients_list) - len(cocktail.ingredients_list)) <= 1:
                final_result.append(cocktail)
        return final_result

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

