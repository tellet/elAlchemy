from itertools import chain

from alchemy_utils import AlchemyUtils
from src.alchemy import ALL_ROUND, COMMON, of_type, KNOWN_INGREDIENTS, RARE

GIVEN_INGREDIENTS = [
    'Переступень',
    'Ласточкина трава',
    'Мирт',
    'Паутинник',
    'Баллиса',
    'Собачья петрушка',
    'Чистолист',
    'Светлая эссенция',
    'Душистый перец',
    'Дождевик',
    'Зубр-трава',
    'Безмер',
    'Каприфоль',
    'Волокна хна',
    'Омела',
    'Волкобой',
    'Чемерица',
    # 'Толчёный жемчуг',
    'Одуванчик',
    'Аренария',
    'Вербена',
    'Хмель',
    'Подорожник',
    'Беозар',
    'Нострикс',
    'Феромоны',
    'Гинация',
    'Винный камень',
    'Смола лешего',
    'Магическая пыль',
    'Сенжигорн',
    'Роголистник'
]

GIVEN_POPULAR_INGREDIENTS = [
    'Зубр-трава',
    'Сенжигорн',
    'Волокна хна',
    'Подорожник',
    'Роголистник',
    'Паутинник',
    'Чистолист',
    'Переступень',
    'Волкобой',
    'Дождевик',
    'Аренария'
]


"""
  Эффекты:
    простые:
      Безумие (какой-то яд будет нужен) <- upgrade Стойкость
      Стабилизация <- upgrade Обезболивающее
      Стойкость
      Обезболивающее 
      Сила
      Имунноукрепляющее?
      Защита от ядов <- Имунноукрепляющее
      Очищение?
      Антитоксин <- Очищение
    магические:
      Защита от проклятий(m)
      Антипатия <- upgrade Правда(m)
      чистый разум <- upgrade Ясновидение(m)
"""


def intersect_sets(names_set: set[str]) -> None:
    result = {
        'растения': [],
        'минералы': [],
        'монстры': []
    }
    plants = []
    minerals = []
    monstro = []
    for ing_name in names_set:
        if KNOWN_INGREDIENTS[ing_name].monstro:
            monstro.append(f'{ing_name}, {of_type(ing_name)}')
        if KNOWN_INGREDIENTS[ing_name].mineral:
            minerals.append(f'{ing_name}, {of_type(ing_name)}')
        if KNOWN_INGREDIENTS[ing_name].plant:
            plants.append(f'{ing_name}, {of_type(ing_name)}')

    result['растения'] = sorted(plants)
    result['минералы'] = sorted(minerals)
    result['монстры'] = sorted(monstro)
    for k, v in result.items():
        print(f'{k}:')
        for itm in v:
            print(f'    {itm}')


if __name__ == '__main__':
    alchemy_ingredients = []
    for item in ALL_ROUND.keys():
        alchemy_ingredients.append(item)
    for item in COMMON.keys():
        alchemy_ingredients.append(item)
    for item in RARE.keys():
        alchemy_ingredients.append(item)
    # for item in KNOWN_INGREDIENTS.keys():
    #     alchemy_ingredients.append(item)
    # for item in GIVEN_INGREDIENTS:
    #     alchemy_ingredients.append(item)
    # for item in GIVEN_POPULAR_INGREDIENTS:
    #     alchemy_ingredients.append(item)

    toxin_lvl = 1
    oracle = AlchemyUtils(alchemy_ingredients, toxin_lvl)
    stoy_set, stoy_eff_set, stoy_arr = oracle.calculate_cocktails('Стойкость')
    obe_set, obe_eff_set, obe_arr = oracle.calculate_cocktails('Обезболивающее')
    sila_set, sila_eff_set, sila_arr = oracle.calculate_cocktails('Сила')
    immu_set, immu_eff_set, immu_arr = oracle.calculate_cocktails('Имунноукрепляющее')
    chist_set, chist_eff_set, chist_arr = oracle.calculate_cocktails('Очищение')
    zas_set, zas_eff_set, zas_arr = oracle.calculate_cocktails('Защита от проклятий(m)')
    ya_set, ya_eff_set, ya_arr = oracle.calculate_cocktails('Ясновидение(m)')
    pra_set, pra_eff_set, pra_arr = oracle.calculate_cocktails('Правда(m)')

    ings_intersection = set.intersection(
        stoy_set,
        obe_set,
        sila_set,
        immu_set,
        chist_set,
        zas_set,
        ya_set,
        pra_set
    )
    print('________________Show intersection of ingredients________________')
    intersect_sets(ings_intersection)

    print('________________Show top 11 most popular ingredients________________')
    tmp_result = list(chain(
        stoy_arr,
        obe_arr,
        sila_arr,
        immu_arr,
        chist_arr,
        zas_arr,
        ya_arr,
        pra_arr
    ))
    popular_list = oracle.get_popular_ingredients(tmp_result)
    count = 0
    for key, val in popular_list.items():
        if KNOWN_INGREDIENTS[key].plant:
            count += 1
            print(key)
        if count == 11:
            break

    print('________________Is there a cocktail with all those effects?________________')
    desired_effects = [
        # 'Стойкость',
        # 'Обезболивающее',
        # 'Сила',
        # 'Имунноукрепляющее',
        # 'Очищение',
        # 'Защита от проклятий(m)',
        'Ясновидение(m)',
        # 'Правда(m)'
    ]
    desired_cocktails = oracle.get_cocktails_with_all_effects(desired_effects)
    if not desired_cocktails:
        print('No desired cocktails found')
    for itm in desired_cocktails:
        print(itm.receipt)


