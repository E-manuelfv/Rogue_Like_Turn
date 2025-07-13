# importa todas as classes e funções do projeto
from src.Hero import *
from src.enemy import *
from src.Weapon import *
from src.HUD import HUD
import random, os, time

# função para limpar a tela do console (compatível com Windows ou Linux/Mac)
def clear():
    """Limpa a tela do console"""
    os.system('cls' if os.name == 'nt' else 'clear')

# função que aplica um pequeno atraso (para ritmo do jogo)
def delay(seconds):
    """Adiciona um atraso controlado"""
    time.sleep(seconds)

import random
import time

def battle(hero, enemies):
    """Sistema principal de batalha"""
    clear()
    print("╔════════════════════════════╗")
    print(f"║  BATALHA CONTRA {len(enemies)} INIMIGO(S) ║")
    print("╚════════════════════════════╝")
    delay(1)
    
    while True:
        # Turno do Herói
        print(f"\n{hero.name} - HP: {hero.hp}/{hero.max_hp} | Poções: {hero.potions}")
        print("Inimigos:")
        for i, e in enumerate(enemies):
            print(f"{i+1}. {e.name} - HP: {e.hp}/{e.max_hp}")
        
        action = input("\nAção: (1) Atacar (2) Poção (3) Defender: ").strip()
        
        defending = False
        defense_bonus = 0
        
        if action == "1":  # Ataque
            if len(enemies) > 1:
                try:
                    target = int(input("Escolha o alvo (número): ")) - 1
                    if 0 <= target < len(enemies):
                        execute_attack(hero, enemies[target], enemies)
                    else:
                        print("Alvo inválido!")
                except ValueError:
                    print("Digite um número válido!")
            else:
                execute_attack(hero, enemies[0], enemies)
                
        elif action == "2":  # Poção
            if hero.use_potion():
                print(f"{hero.name} recuperou 20 HP!")
            else:
                print("Sem poções disponíveis!")
            delay(1)
            continue
            
        elif action == "3":  # Defesa
            defending = True
            defense_bonus = hero.defense * 0.5
            print(f"{hero.name} se defende! +{defense_bonus:.1f} defesa")
            delay(1)
        
        # Verifica fim de batalha
        enemies = [e for e in enemies if e.hp > 0]
        if not enemies:
            victory(hero)
            return True
        
        # Turno dos Inimigos
        for enemy in enemies:
            if enemy.hp > 0:
                damage = max(1, enemy.attack - (hero.defense + defense_bonus))
                print(f"\n{enemy.name} ataca! {damage} de dano")
                if hero.take_damage(damage):
                    defeat()
                    return False
                delay(1)
        
        input("\nPressione Enter para continuar...")
        clear()

def execute_attack(hero, target, enemies):
    """Executa um ataque e remove inimigos derrotados"""
    print(f"\n{hero.name} ataca {target.name}!")
    delay(0.5)
    
    if hero.weapon:
        results = hero.weapon.attack(target=target)
    else:
        damage = max(1, hero.attack - target.defense)
        results = [(target, damage)]
    
    for result in results:
        if len(result) >= 2:
            t, dmg = result[0], result[1]
            if t.take_damage(dmg):
                print(f"{t.name} foi derrotado!")
                if t in enemies:
                    enemies.remove(t)
            delay(0.5)

def victory(hero):
    """Processa vitória"""
    clear()
    reward = 10 * hero.level
    hero.gold += reward
    hero.xp += 30
    
    print("╔════════════════════════════╗")
    print("║        VITÓRIA!           ║")
    print("╚════════════════════════════╝")
    print(f"\nRecompensa: {reward} ouro")
    print(f"Experiência: +30 XP")
    
    if hero.level_up_check():
        print("\n★ ★ ★ LEVEL UP! ★ ★ ★")
    delay(2)

def defeat():
    """Processa derrota"""
    clear()
    print("╔════════════════════════════╗")
    print("║        DERROTA...         ║")
    print("╚════════════════════════════╝")
    print("\nSeu herói foi derrotado...")
    delay(2)

def _execute_attack(hero, target, enemies):
    
    """Executa ataque com delays narrativos e remove inimigos derrotados"""
    if hero.weapon:
        print(f"{hero.name} usa {hero.weapon.name}!", flush=True)
        delay(1)
        attack_results = hero.weapon.attack(target=target)
        
        for result in attack_results:
            if len(result) >= 2:
                target, damage = result[0], result[1]
                if damage > 0:
                    print("*SWOOSH* ", end="", flush=True)
                    delay(1)
                    print(f"Causando {damage} de dano!", flush=True)
                    delay(1)
                    target.take_damage(damage)
                    
                    if target.hp <= 0:
                        print("*CRITICAL* ", end="", flush=True)
                        delay(1)
                        print(f"{target.name} foi nocauteado!", flush=True)
                        delay(1)
                        enemies.remove(target)  # Remove o inimigo derrotado
                        return True
    else:
        print(f"{hero.name} ataca com os punhos!", flush=True)
        delay(1)
        damage = max(1, hero.attack - target.defense)
        print("*POW* ", end="", flush=True)
        delay(1)
        print(f"Causando {damage} de dano!", flush=True)
        target.take_damage(damage)
        delay(1)
        
        if target.hp <= 0:
            print(f"{target.name} cai desmaiado!", flush=True)
            delay(1)
            enemies.remove(target)  # Remove o inimigo derrotado
            return True
    return False