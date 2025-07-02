from abc import ABC, abstractmethod
import random

class Enemy(ABC):
    def __init__(self, name, hp, attack, defense, level=1):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.level = level

    @abstractmethod
    def attack_hero(self, hero):
        pass

    def take_damage(self, amount):
        damage = amount - self.defense
        damage = max(1, damage)
        self.hp -= damage
        print(f"{self.name} sofreu {damage} de dano. HP restante: {self.hp}")

class Dragon(Enemy):
    def attack_hero(self, hero):
        attack_type = random.choice(["garras", "fogo"])
        if attack_type == "garras":
            damage = self.attack + 5
        else:
            damage = self.attack + 10
        hero.take_damage(damage)
        print(f"{self.name} atacou {hero.name} com {attack_type} causando {damage}.")

class Goblin(Enemy):
    def attack_hero(self, hero):
        boost = random.choice([0, 2])  # goblins podem se fortalecer em grupo
        damage = self.attack + boost
        hero.take_damage(damage)
        print(f"{self.name} golpeou {hero.name} causando {damage}.")
