class Weapon:
    def __init__(self, name, damage, accuracy):
        self.name = name
        self.damage = damage
        self.accuracy = accuracy

class Sword(Weapon):
    def __init__(self):
        super().__init__("Espada", damage=8, accuracy=0.8)

class Bow(Weapon):
    def __init__(self):
        super().__init__("Arco", damage=5, accuracy=0.9)

class Staff(Weapon):
    def __init__(self):
        super().__init__("Cajado", damage=4, accuracy=0.95)
