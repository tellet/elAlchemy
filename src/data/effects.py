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