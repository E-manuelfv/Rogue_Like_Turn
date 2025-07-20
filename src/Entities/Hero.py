class Hero:
    def __init__(self, name, hp=100, attack=10, defense=5):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.gold = 0
        self.weapon = None
        self.potions = 1
        self.level = 1
        self.xp = 0  # Adicionando atributo de experiência
        self.xp_to_level = 50  # XP necessário para subir de nível

    def choose_weapon(self, weapon):
        self.weapon = weapon

    def take_damage(self, damage):
        self.hp = max(0, self.hp - damage)
        return self.hp <= 0

    def use_potion(self):
        if self.potions > 0:
            self.hp = min(self.max_hp, self.hp + 50)
            self.potions -= 1
            return True
        return False

    def add_xp(self, amount):
        """Adiciona experiência e verifica se subiu de nível"""
        self.xp += amount
        if self.xp >= self.xp_to_level:
            self.level_up()
            return True
        return False

    def level_up(self):
        """Aumenta o nível do herói"""
        self.level += 1
        self.max_hp += 10
        self.hp = self.max_hp  # Cura completamente ao subir de nível
        self.attack += 2
        self.defense += 1
        self.xp = 0
        self.xp_to_level = self.level * 50  # Aumenta o XP necessário para o próximo nível
        return True