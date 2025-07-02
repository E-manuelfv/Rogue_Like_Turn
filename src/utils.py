import random
from src.enemy import Dragon, Goblin

def generate_enemy_wave(stage):
    enemies = []
    for _ in range(stage + 1):
        if random.random() < 0.5:
            enemies.append(Dragon("Dragão", hp=50, attack=15, defense=5, level=stage))
        else:
            enemies.append(Goblin("Goblin", hp=30, attack=10, defense=3, level=stage))
    return enemies
