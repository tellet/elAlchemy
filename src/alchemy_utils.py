from src.alchemy import Alchemy, Cocktail


class AlchemyUtils:
    def __init__(self, known_ingredients: [dict], desired_toxin_lvl=2):
        self.alchemy = Alchemy(known_ingredients)
        self.desired_toxin_lvl = desired_toxin_lvl

    def calculate_cocktails_with_effects(self,  effects: [str]) -> list[Cocktail]:
        cocktails = []
        for cocktail in self.alchemy.get_effective_cocktails():
            tmp_set = set(effects)
            tmp_intersect = [
                key for key in set.intersection(
                    set(cocktail.result_powered_effects_dict.keys()),
                    tmp_set
                )
            ]
            if len(tmp_intersect) == len(effects):
                if cocktail.result_effects_dict.get('Токсин', 0) <= self.desired_toxin_lvl:
                    cocktails.append(cocktail)
        return cocktails

    def calculate_all_cocktails(self) -> []:
        cocktails = []
        for cocktail in self.alchemy.get_effective_cocktails():
            if cocktail.result_effects_dict.get('Токсин', 0) <= self.desired_toxin_lvl:
                cocktails.append(cocktail)
        return cocktails

    @staticmethod
    def get_popular_ingredients(cocktails: [Cocktail]) -> dict:
        result_popularity = {}
        for cocktail in cocktails:
            for ingredient in cocktail.ingredients:
                tmp = ingredient.name
                result_popularity[tmp] = result_popularity.get(tmp, 0) + 1
        result_popularity = sorted(result_popularity.items(), key=lambda x: x[1], reverse=True)
        return dict(result_popularity)
