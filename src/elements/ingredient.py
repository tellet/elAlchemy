class Ingredient:
    """
    Ingredient is a combination of effects with their powers.
    Ingredient can be a part of monstro, mineral and plant.
    Ingredient might be magic.
    Ingredient has  unique name.
    """
    def __init__(self,
                 name: str,
                 effects: dict,
                 monstro: bool = False,
                 mineral: bool = False,
                 magic: bool = False,
                 plant: bool = False):
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
