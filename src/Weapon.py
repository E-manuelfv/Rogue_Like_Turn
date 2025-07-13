import random

class Weapon:
    def __init__(self, name, base_damage, accuracy, attack_type, special_effect=None):
        self.name = name
        self.base_damage = base_damage
        self.accuracy = accuracy
        self.attack_type = attack_type  # 'single', 'aoe', 'dot'
        self.special_effect = special_effect

    def attack(self, target=None, targets=None):
        if self.attack_type == 'single':
            return self._single_attack(target)
        elif self.attack_type == 'aoe':
            return self._aoe_attack(targets)
        elif self.attack_type == 'dot':
            return self._dot_attack(target)

    def _single_attack(self, target):
        # Ataque único com maior dano
        damage = self.base_damage * (1.5 if random.random() < self.accuracy else 0)
        return [(target, damage)]

    def _aoe_attack(self, targets):
        # Ataque em área com dano reduzido
        results = []
        for target in targets:
            damage = self.base_damage * 0.7 * (1 if random.random() < self.accuracy else 0)
            results.append((target, damage))
        return results

    def _dot_attack(self, target):
        # Ataque com dano contínuo
        initial_damage = self.base_damage * 0.5 * (1 if random.random() < self.accuracy else 0)
        dot_damage = self.base_damage * 0.3
        return [(target, initial_damage, dot_damage, 2)]  # 2 turnos de DOT

class Sword(Weapon):
    def __init__(self):
        super().__init__("Espada", base_damage=10, accuracy=0.7, attack_type='single')
        
    def _single_attack(self, target):
        # Ataque único com chance de crítico
        if random.random() < 0.2:  # 20% de chance
            return [(target, self.base_damage * 2)]
        return super()._single_attack(target)

class Bow(Weapon):
    def __init__(self):
        super().__init__("Arco", base_damage=6, accuracy=0.95, attack_type='single')
        
    def _single_attack(self, target):
        # Ataque preciso que ignora parte da defesa
        damage = self.base_damage * (1 if random.random() < self.accuracy else 0)
        return [(target, damage, True)]  # Flag para dano verdadeiro

class Staff(Weapon):
    def __init__(self):
        super().__init__("Cajado", base_damage=5, accuracy=0.85, attack_type='aoe')
        
    def _aoe_attack(self, targets):
        # Ataque em área com chance de aplicar efeito
        results = []
        for target in targets:
            damage = self.base_damage * 0.6 * (1 if random.random() < self.accuracy else 0)
            if random.random() < 0.3:  # 30% de chance de aplicar queimação
                results.append((target, damage, self.base_damage * 0.2, 3))  # DOT por 3 turnos
            else:
                results.append((target, damage))
        return results