from src.data.spirits import KNOWN_SPIRITS_UPGRADES_DICT


class Spirit:
    def __init__(self, name: str, effects: dict):
        self.name = name
        self.effects = effects

    def improved_singletons(self, effects: dict):
        res = []
        for key in effects.keys():
            tmp = {key: val for key, val in effects.items()}
            key_replace = KNOWN_SPIRITS_UPGRADES_DICT[key]
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
            key_replace_1 = KNOWN_SPIRITS_UPGRADES_DICT[key_1]
            key_replace_2 = KNOWN_SPIRITS_UPGRADES_DICT[key_2]
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
            key_replace_1 = KNOWN_SPIRITS_UPGRADES_DICT[key_1]
            key_replace_2 = KNOWN_SPIRITS_UPGRADES_DICT[key_2]
            key_replace_3 = KNOWN_SPIRITS_UPGRADES_DICT[key_3]
            tmp[key_replace_1] = tmp.pop(key_1)
            tmp[key_replace_2] = tmp.pop(key_2)
            tmp[key_replace_3] = tmp.pop(key_3)
            res.append(tmp)
        return res

    # Spirits only apply to those effects with power 4
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


def get_known_spirits():
    return [
        Spirit('Спирт', {'any': 1}),
        Spirit('Крепкий спирт', {'any': 2}),
        Spirit('Махакамский спирт', {'any': 3}),
        Spirit('Настойка из мандрагоры', {'any': 3, 'Токсин': -1}),
        Spirit('Алкогест', {'any': 3, 'Replace 1 ingr with catalyzer': True}),
    ]
