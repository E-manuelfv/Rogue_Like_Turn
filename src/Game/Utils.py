from src.Entities.Enemy import Dragon, Goblin, Orc
import os, time

class EnemyBattle:
    boss_fight_variable = False
    boss_defeated = False

    @staticmethod
    def generate_enemies(hero_level):
        """Gera inimigos balanceados para o nível do herói com informações completas"""
        base_hp = 20 + (hero_level * 2)
        base_attack = 8 + (2 * hero_level)
        base_defense = 2 + hero_level
        
        # Dicionário de recompensas base por tipo de inimigo
        reward_templates = {
            'goblin': {
                'xp': 15 + (hero_level * 3),
                'gold_min': 5 + hero_level,
                'gold_max': 10 + (hero_level * 2)
            },
            'orc': {
                'xp': 30 + (hero_level * 5),
                'gold_min': 10 + (hero_level * 2),
                'gold_max': 20 + (hero_level * 3)
            },
            'dragon': {
                'xp': 100 + (hero_level * 10),
                'gold_min': 50 + (hero_level * 5),
                'gold_max': 100 + (hero_level * 10)
            }
        }

        scenarios = [
            {
                'name': 'Goblin Solitário',
                'enemies': [Goblin("Goblin", hp=int(base_hp*1.2), attack=base_attack, defense=base_defense)],
                'xp': reward_templates['goblin']['xp'],
                'gold_min': reward_templates['goblin']['gold_min'],
                'gold_max': reward_templates['goblin']['gold_max']
            },
            {
                'name': 'Dupla de Goblins (BUFF)',
                'enemies': [
                    Goblin("Goblin", hp=base_hp, attack=int(base_attack*1.2), defense=base_defense),
                    Goblin("Goblin", hp=base_hp, attack=int(base_attack*1.2), defense=base_defense)
                ],
                'xp': reward_templates['goblin']['xp'] * 2,
                'gold_min': reward_templates['goblin']['gold_min'] * 2,
                'gold_max': reward_templates['goblin']['gold_max'] * 2
            },
            {
                'name': 'Orc Guerreiro',
                'enemies': [Orc("Orc", hp=int(base_hp*1.8), attack=int(base_attack*1.5), defense=int(base_defense*1.5))],
                'xp': reward_templates['orc']['xp'],
                'gold_min': reward_templates['orc']['gold_min'],
                'gold_max': reward_templates['orc']['gold_max']
            },
            {
                'name': 'Orc e Goblin',
                'enemies': [
                    Orc("Orc", hp=int(base_hp*1.5), attack=int(base_attack*1.3), defense=int(base_defense*1.3)),
                    Goblin("Goblin", hp=base_hp, attack=base_attack, defense=base_defense)
                ],
                'xp': reward_templates['orc']['xp'] + reward_templates['goblin']['xp'],
                'gold_min': reward_templates['orc']['gold_min'] + reward_templates['goblin']['gold_min'],
                'gold_max': reward_templates['orc']['gold_max'] + reward_templates['goblin']['gold_max']
            },
            {
                'name': 'Dragão Boss',
                'enemies': [Dragon("Dragão Boss", hp=int(base_hp*3), attack=int(base_attack*2), defense=int(base_defense*2))],
                'xp': reward_templates['dragon']['xp'],
                'gold_min': reward_templates['dragon']['gold_min'],
                'gold_max': reward_templates['dragon']['gold_max'],
                'is_boss': True
            }
        ]
        
        return scenarios

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def delay(seconds):
    time.sleep(seconds)
