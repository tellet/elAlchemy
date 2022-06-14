from src.alchemy import Alchemy, of_type, Cocktail


class AlchemyUtils:
    def __init__(self, known_ingredients: [dict], desired_toxin_lvl=2):
        self.alchemy = Alchemy(known_ingredients)
        self.desired_toxin_lvl = desired_toxin_lvl

    def calculate_cocktails(self, effect: str) -> (set, set, []):
        ingredients = set()
        receipts = set()
        cocktails = []
        with open(f'cocktails/{effect}_cocktails.txt', 'w', encoding="utf8") as f:
            f.write('*********************************************************************************\n')
            f.write(f'What are the cocktails with {effect} effect?\n')
            f.write('*********************************************************************************\n')
            for cocktail in self.alchemy.get_effective_cocktails():
                if cocktail.result_effects_dict.get(effect, 0) >= 4 \
                        and cocktail.result_effects_dict.get('Токсин', 0) <= self.desired_toxin_lvl:
                    f.write(str(cocktail) + '\n')
                    cocktails.append(cocktail)
                    ingredients = ingredients.union(cocktail.ingredients_set)
                    receipts.add(cocktail.receipt)

        ing_list = [x for x in ingredients]
        ing_list = sorted(ing_list)
        rec_list = [x for x in receipts]
        rec_list = sorted(rec_list)
        with open(f'cocktails/{effect}_cocktail_ingredients.txt', 'w', encoding="utf8") as f:
            for ing in ing_list:
                f.write(f'{ing}, ({of_type(ing)})\n')
        with open(f'cocktails/{effect}_receipts.txt', 'w', encoding="utf8") as f:
            for itm in rec_list:
                f.write(f'{itm}\n')
        return ingredients, receipts, cocktails

    def get_cocktails_with_all_effects(self, effects: [str]) -> list[Cocktail]:
        ingredients = set()
        receipts = set()
        cocktails = []
        with open(f'cocktails/desired_cocktails.txt', 'w', encoding="utf8") as f:
            f.write('*********************************************************************************\n')
            f.write(f'What are the cocktails with all desired effects?\n')
            f.write('*********************************************************************************\n')
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
                        f.write(str(cocktail) + '\n')
                        cocktails.append(cocktail)
                        ingredients = ingredients.union(cocktail.ingredients_set)
                        receipts.add(cocktail.receipt)
        ing_list = [x for x in ingredients]
        ing_list = sorted(ing_list)
        rec_list = [x for x in receipts]
        rec_list = sorted(rec_list)
        with open(f'cocktails/desired_cocktail_ingredients.txt', 'w', encoding="utf8") as f:
            for ing in ing_list:
                f.write(f'{ing}, ({of_type(ing)})\n')
        with open(f'cocktails/desired_receipts.txt', 'w', encoding="utf8") as f:
            for itm in rec_list:
                f.write(f'{itm}\n')

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
