from src.Weapon import Weapon
import random

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

    def choose_weapon(self, weapon: Weapon):
        self.weapon = weapon
        print(f"{self.name} equipou a arma {weapon.name}.")

    def attack_enemy(self, enemy):
        if not self.weapon:
            print("Nenhuma arma equipada!")
            return
        hit_chance = random.random()
        if hit_chance <= self.weapon.accuracy:
            damage = self.weapon.damage + self.attack - enemy.defense
            damage = max(1, damage)
            enemy.take_damage(damage)
            print(f"{self.name} causou {damage} ao {enemy.name}.")
        else:
            print(f"{self.name} errou o ataque!")

    def defend(self):
        print(f"{self.name} se prepara para defender o próximo ataque.")
        self.defense *= 2

    def heal(self):
        if self.potions > 0:
            self.hp = min(self.max_hp, self.hp + 30)
            self.potions -= 1
            print(f"{self.name} usou uma poção de cura! HP restaurado para {self.hp}.")
        else:
            print("Sem poções de cura!")

    def take_damage(self, amount):
        reduced = amount - self.defense
        reduced = max(1, reduced)
        self.hp -= reduced
        print(f"{self.name} sofreu {reduced} de dano. HP restante: {self.hp}")
        self.defense = max(5, self.defense // 2)  # reset defesa se estava defendendo
