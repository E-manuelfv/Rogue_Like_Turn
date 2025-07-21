from src.Entities.Enemy import Dragon, Goblin, Orc
import os, time

class EnemyBattle():
    boss_fight_variable = False

    @staticmethod
    def generate_enemies(hero_level):
        """Gera inimigos balanceados para o nível do herói"""
        base_hp = 20 + (hero_level * 2)
        base_attack = 8 + (2 * hero_level)
        base_defense = 2 + hero_level
        scenarios = [
            [Goblin("Goblin", hp=int(base_hp*1.2), attack=base_attack, defense=base_defense)],
            [Goblin("Goblin", hp=base_hp, attack=base_attack, defense=base_defense),
            Goblin("Goblin", hp=base_hp, attack=base_attack, defense=base_defense)],
            [Orc("Orc", hp=int(base_hp*1.8), attack=int(base_attack*1.5), defense=int(base_defense*1.5))],
            [Orc("Orc", hp=int(base_hp*1.5), attack=int(base_attack*1.3), defense=int(base_defense*1.3)),
            Goblin("Goblin", hp=base_hp, attack=base_attack, defense=base_defense)],
            [Dragon("Dragão Boss", hp=int(base_hp*3), attack=int(base_attack*2), defense=int(base_defense*2))]
        ]
        return scenarios


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def delay(seconds):
    time.sleep(seconds)
