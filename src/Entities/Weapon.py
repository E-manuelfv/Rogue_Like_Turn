import random

class Weapon:
    def __init__(self, name, base_damage, accuracy, attack_type, special_effect=None):
        self.name = name
        self.base_damage = base_damage
        self.accuracy = accuracy
        self.attack_type = attack_type  # 'single', 'aoe', 'dot'
        self.special_effect = special_effect

    def attack(self, target=None, targets=None):
        """Handle all attack types with safe defaults"""
        if not (target or targets):
            return [(None, 0)]  # Safe default for invalid targets
            
        if self.attack_type == 'aoe':
            return self._aoe_attack(targets or [target])
        elif self.attack_type == 'dot':
            return self._dot_attack(target or targets[0])
        else:  # Default to single attack
            return self._single_attack(target or targets[0])

    def _single_attack(self, target):
        """Standard single-target attack"""
        hit = random.random() < self.accuracy
        damage = self.base_damage * (1.5 if hit else 0)
        return [(target, damage)]

    def _aoe_attack(self, targets):
        """Area of effect attack"""
        if not targets:
            return []
            
        return [
            (target, self.base_damage * 0.7 * (1 if random.random() < self.accuracy else 0))
            for target in targets
        ]

    def _dot_attack(self, target):
        """Damage over time attack"""
        hit = random.random() < self.accuracy
        initial_dmg = self.base_damage * 0.5 * (1 if hit else 0)
        dot_dmg = self.base_damage * 0.3
        return [(target, initial_dmg, dot_dmg, 2)]  # 2 turns of DOT

class Sword(Weapon):
    def __init__(self, sharpened=False):
        """
        Inicializa a espada comum ou afiada
        :param sharpened: Se True, cria uma espada afiada
        """
        self.sharpened = sharpened
        base_name = "Espada Afiada" if sharpened else "Espada"
        base_damage = 13 if sharpened else 10
        accuracy = 0.75 if sharpened else 0.7
        
        super().__init__(
            name=base_name,
            base_damage=base_damage,
            accuracy=accuracy,
            attack_type='single',
            special_effect="Golpe Crítico Melhorado" if sharpened else "Golpe Crítico"
        )
        
    def _single_attack(self, target):
        """Lógica de ataque com crítico melhorado para espada afiada"""
        crit_chance = 0.25 if self.sharpened else 0.2
        crit_multiplier = 2.2 if self.sharpened else 2.0
        
        if random.random() < crit_chance:
            damage = self.base_damage * crit_multiplier
            crit_type = "CRÍTICO PODEROSO!" if self.sharpened else "Crítico!"
            print(f"⚔️ {crit_type}")
            return [(target, damage)]
        
        return super()._single_attack(target)

    def sharpen(self):
        """Transforma esta espada em uma versão afiada"""
        if not self.sharpened:
            self.sharpened = True
            self.name = "Espada Afiada"
            self.base_damage = 13
            self.accuracy = 0.75
            self.special_effect = "Golpe Crítico Melhorado"
            return True
        return False

class Bow(Weapon):
    def __init__(self):
        super().__init__(
            name="Arco", 
            base_damage=12,
            accuracy=0.95,
            attack_type='single',
            special_effect="Armor Penetration"
        )
        
    def _single_attack(self, target):
        damage = self.base_damage * (1 if random.random() < self.accuracy else 0)
        return [(target, damage, True)]  # True marks armor-penetrating damage


class Staff(Weapon):
    def __init__(self):
        super().__init__(
            name="Cajado",
            base_damage=10,
            accuracy=0.85,
            attack_type='aoe',
            special_effect="Burn"
        )
        
    def _aoe_attack(self, targets):
        results = []
        for target in targets:
            damage = self.base_damage * 0.6 * (1 if random.random() < self.accuracy else 0)
            if random.random() < 0.3:  # 30% burn chance
                results.append((target, damage, self.base_damage * 0.2, 3))  # 3-turn burn
            else:
                results.append((target, damage))
        return results