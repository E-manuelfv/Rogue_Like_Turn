from abc import ABC, abstractmethod

class Enemy(ABC):
    def __init__(self, name, hp, attack, defense, level=1):
        self.name = name
        self.max_hp = hp  # Adicionando max_hp
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.level = level

    def take_damage(self, amount):
        """Garante que o HP nunca fique negativo"""
        self.hp = max(0, self.hp - amount)
        return self.hp <= 0  # Retorna True se o inimigo morreu

    @abstractmethod
    def attack_hero(self, hero):
        pass

class Goblin(Enemy):
    def attack_hero(self, hero):
        damage = self.attack
        print(f"{self.name} ataca com {damage} de dano!")
        return damage

class Orc(Enemy):
    def attack_hero(self, hero):
        damage = self.attack + 2  # Orcs dão mais dano
        print(f"{self.name} ataca com {damage} de dano!")
        return damage

class Dragon(Enemy):
    def attack_hero(self, hero):
        damage = self.attack + 5  # Dragões dão muito mais dano
        print(f"{self.name} cospe fogo causando {damage} de dano!")
        return damage