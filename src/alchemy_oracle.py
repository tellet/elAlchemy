"""
Given the toxin level and a set of ingredients generate a full alchemy.
"""
import time

from src.alchemy import Alchemy, KNOWN_INGREDIENTS


class AlchemyOracle:
    def __init__(self, known_ingredients, desired_toxin_lvl=2):
        self.alchemy = Alchemy(known_ingredients)
        self.desired_toxin_lvl = desired_toxin_lvl

    def calculate_cocktails_with_effects(self,  effects):
        """
        From all the effective cocktails in an alchemy select only the cocktails with given effects.
        :param effects:
        :return: list
        """
        cocktails = []
        for cocktail in self.alchemy.effective_cocktails:
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

    def calculate_all_cocktails(self):
        """
        From all the effective cocktails in an alchemy select only the cocktails with given toxin level (<=).
        :return: list
        """
        cocktails = []
        for cocktail in self.alchemy.effective_cocktails:
            if cocktail.result_effects_dict.get('Токсин', 0) <= self.desired_toxin_lvl:
                cocktails.append(cocktail)
        return cocktails

    @staticmethod
    def get_popular_ingredients(cocktails) -> dict:
        """
        Given a list of cocktails count the occurrences of each ingredient.
        :param cocktails:
        :return: dict, ingredients sorted by popularity
        """
        result_popularity = {}
        for cocktail in cocktails:
            for ingredient in cocktail.ingredients:
                tmp = ingredient.name
                result_popularity[tmp] = result_popularity.get(tmp, 0) + 1
        result_popularity = sorted(result_popularity.items(), key=lambda x: x[1], reverse=True)
        return dict(result_popularity)


if __name__ == '__main__':
    oracle = AlchemyOracle(KNOWN_INGREDIENTS, 2)
    start = time.time()
    oracle.calculate_all_cocktails()
    end = time.time()
    print("The time of execution of calculate_all_cocktails is:", end - start, " seconds.")
