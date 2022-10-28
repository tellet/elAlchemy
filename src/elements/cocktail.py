from src.elements.ingredient import Ingredient


class Cocktail:
    """
    Cocktail is a set of Ingredients.
    """
    def __init__(self, ingredients):
        self.ingredients = ingredients
        ingredients_sum = self.get_ingredients_sum()
        self.receipt = ingredients_sum.name
        self.result_effects_dict = ingredients_sum.effects
        self.toxin = ingredients_sum.effects.get('Токсин', 0)
        self.result_powered_effects_dict = self.get_power_effects()
        self.is_effective = self.is_effective()
        self.ingredients_set = set()
        self.ingredients_list = []
        for ing in self.ingredients:
            self.ingredients_set.add(ing.name)
            self.ingredients_list.append(ing.name)

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
