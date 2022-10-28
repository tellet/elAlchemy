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
        Catalyzer('Кровь трупоеда', activation_effects={'Монстр, все эффекты': 3},
                  conditions={'Защита от проклятий(m)': 4}),
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
        Catalyzer('Смола лешего', {'Длительность': 100500}, conditions=None)
    ]
