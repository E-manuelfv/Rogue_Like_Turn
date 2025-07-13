from src.Hero import Hero
from src.enemy import Goblin, Orc, Dragon
from src.Weapon import Sword, Bow, Staff
from src.shop import Shop
import random
import os
import time

def clear():
    """Limpa a tela do console"""
    os.system('cls' if os.name == 'nt' else 'clear')

def delay(seconds):
    """Adiciona um atraso controlado"""
    time.sleep(seconds)

def battle(hero, enemies):
    """Sistema principal de batalha"""
    clear()
    print("╔════════════════════════════╗")
    print(f"║  BATALHA CONTRA {len(enemies)} INIMIGO(S) ║")
    print("╚════════════════════════════╝")
    delay(1)
    
    while True:
        # Filtra apenas inimigos vivos
        alive_enemies = [e for e in enemies if e.hp > 0]
        
        # Turno do Herói
        print(f"\n{hero.name} - Nível {hero.level} | XP: {hero.xp}/{hero.xp_to_level}")
        print(f"HP: {hero.hp}/{hero.max_hp} | Poções: {hero.potions}")
        
        if not alive_enemies:  # Verifica se todos estão mortos
            victory(hero)
            return True
            
        print("Inimigos:")
        for i, enemy in enumerate(alive_enemies):  # Mostra apenas vivos
            print(f"{i+1}. {enemy.name} - HP: {enemy.hp}/{enemy.max_hp}")
        
        action = input("\nAção: (1) Atacar (2) Poção (3) Defender: ").strip()
        
        defending = False
        defense_bonus = 0
        
        if action == "1":  # Ataque
            if len(alive_enemies) > 1:
                try:
                    target = int(input("Escolha o alvo (número): ")) - 1
                    if 0 <= target < len(alive_enemies):
                        execute_attack(hero, alive_enemies[target], enemies)
                    else:
                        print("Alvo inválido!")
                        delay(1)
                except ValueError:
                    print("Digite um número válido!")
                    delay(1)
            else:
                execute_attack(hero, alive_enemies[0], enemies)
                
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
        
        # Atualiza lista de inimigos vivos
        alive_enemies = [e for e in enemies if e.hp > 0]
        if not alive_enemies:
            victory(hero)
            return True
        
        # Turno dos Inimigos (apenas os vivos)
        for enemy in alive_enemies:
            damage = max(1, enemy.attack - (hero.defense + defense_bonus))
            print(f"\n{enemy.name} ataca! {damage} de dano")
            hero.take_damage(damage)
            
            if hero.hp <= 0:
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
        attack_results = hero.weapon.attack(target=target)
        
        for result in attack_results:
            if len(result) >= 2:
                t, dmg = result[0], result[1]
                t.take_damage(dmg)
                print(f"Causando {dmg} de dano!")
                
                if t.hp <= 0:
                    print(f"{t.name} foi derrotado!")
                    if t in enemies:
                        enemies.remove(t)  # Remove completamente da lista de inimigos
                delay(0.5)
    else:
        damage = max(1, hero.attack - target.defense)
        target.take_damage(damage)
        print(f"Causando {damage} de dano!")
        
        if target.hp <= 0:
            print(f"{target.name} foi derrotado!")
            if target in enemies:
                enemies.remove(target)  # Remove completamente da lista de inimigos
        delay(0.5)

def victory(hero):
    """Processa vitória"""
    clear()
    reward = 10 * hero.level
    hero.gold += reward
    
    print("╔════════════════════════════╗")
    print("║        VITÓRIA!           ║")
    print("╚════════════════════════════╝")
    print(f"\nRecompensa: {reward} ouro")
    
    # Adiciona XP e verifica level up
    xp_gained = 30
    print(f"Experiência: +{xp_gained} XP")
    if hero.add_xp(xp_gained):
        print("\n★ ★ ★ LEVEL UP! ★ ★ ★")
        print(f"Novo nível: {hero.level}")
    
    delay(2)

def defeat():
    """Processa derrota"""
    clear()
    print("╔════════════════════════════╗")
    print("║        DERROTA...         ║")
    print("╚════════════════════════════╝")
    print("\nSeu herói foi derrotado...")
    delay(2)

# Lista de cenários de batalha

def main():
    print("=== Rogue Like RPG ===")
    hero_name = input("Digite um nome para seu personagem: ")
    hero = Hero(hero_name)
    shop = Shop()

    # Escolha inicial de arma
    shop.show_shop()
    try:
        choice = int(input("Escolha sua arma inicial (1-3): "))
        weapons = [Sword(), Bow(), Staff()]
        if 1 <= choice <= 3:
            hero.choose_weapon(weapons[choice-1])
        else:
            hero.choose_weapon(Sword())
    except:
        hero.choose_weapon(Sword())

    print("\nVocê recebeu 1 poção de cura!")
    input("Pressione Enter para começar...")

    battles_won = 0
    
    battle_scenarios = [
    [Goblin("Goblin", hp=25 ** hero.level, attack=15 ** hero.level, defense=2 ** hero.level, level=1)],
    [Goblin("Goblin", hp=20 ** hero.level, attack=15 ** hero.level, defense=2 ** hero.level, level=1), 
     Goblin("Goblin", hp=20 ** hero.level, attack=16 ** hero.level, defense=2 ** hero.level, level=1)],
    [Orc("Orc", hp=40 ** hero.level, attack=20 ** hero.level, defense=5 ** hero.level, level=2)],
    [Orc("Orc", hp=35 ** hero.level, attack=18 ** hero.level, defense=4 ** hero.level, level=2), 
     Goblin("Goblin", hp=20 ** hero.level, attack=15 ** hero.level, defense=2 ** hero.level, level=1)],
    [Dragon("Dragão Boss", hp=100, attack=30 ** hero.level, defense=10, level=3)],
]


    while hero.hp > 0:
        clear()
        
        # Seleção de inimigos baseada no progresso
        if battles_won < 3:
            enemies = random.choice(battle_scenarios[:3])
        elif battles_won == 3:
            enemies = battle_scenarios[4]
        else:
            enemies = random.choice(battle_scenarios)
        
        # Garante que há inimigos
        enemies = [e for e in enemies if e is not None]
        if not enemies:
            enemies = [Goblin("Goblin", hp=25, attack=5, defense=2, level=1)]

        won = battle(hero, enemies)
        
        if not won:
            print("Reiniciando jogo...")
            delay(2)
            main()
            return
        
        battles_won += 1
        shop.update_inventory(battles_won)
        
        # Opção de compra após batalha
        shop.show_shop()
        try:
            print(f"Você tem: {hero.gold}, moedas de ouro")
            choice = int(input("Deseja comprar algo? (0 para pular): "))
            if choice != 0:
                shop.buy(hero, choice)
        except:
            pass

        input("Pressione Enter para próxima batalha...")

if __name__ == "__main__":
    main()