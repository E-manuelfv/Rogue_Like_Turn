from src.Hero import Hero
from src.enemy import Goblin, Orc, Dragon
from src.Weapon import Sword, Bow, Staff
from src.shop import Shop
import random
import os
import time
import pickle

# Sistema de Save/Load
def save_game(hero):
    with open('save.dat', 'wb') as f:
        pickle.dump(hero, f)

def load_game():
    try:
        with open('save.dat', 'rb') as f:
            return pickle.load(f)
    except:
        return None

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def delay(seconds):
    time.sleep(seconds)

def generate_enemies(hero_level):
    """Gera inimigos balanceados para o nível do herói"""
    base_hp = 20 + (hero_level * 5)
    base_attack = 8 + (2 * hero_level)
    base_defense = 2 + hero_level
    scenarios = [
        [Goblin("Goblin", hp=int(base_hp*1.2), attack=base_attack, defense=base_defense)],
        [Goblin("Goblin", hp=base_hp, attack=base_attack, defense=base_defense),
         Goblin("Goblin", hp=base_hp, attack=base_attack, defense=base_defense)],
        [Orc("Orc", hp=int(base_hp*1.8), attack=int(base_attack*1.5), defense=int(base_defense*1.5))],
        [Orc("Orc", hp=int(base_hp*1.5), attack=int(base_attack*1.3), defense=int(base_defense*1.3)),
         Goblin("Goblin", hp=base_hp, attack=base_attack, defense=base_defense)],
        [Dragon("Dragão Boss", hp=int(base_hp*5), attack=int(base_attack*3), defense=int(base_defense*2))]
    ]
    return scenarios

def battle(hero, enemies):
    """Sistema principal de batalha"""
    clear()
    print("╔══════════════════════════════╗")
    print(f"║  BATALHA CONTRA {len(enemies)} INIMIGO(S) ║")
    print("╚══════════════════════════════╝")
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
                print(f"{hero.name} recuperou 50 HP!")
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
                defeat(hero)
                return False
            delay(1)
        
        input("\nPressione Enter para continuar...")
        clear()

def execute_attack(hero, target, enemies):
    """Executa um ataque com verificação de arma"""
    print(f"\n{hero.name} ataca {target.name}!")
    delay(0.5)
    
    if not hero.weapon:
        # Ataque básico sem arma
        damage = max(1, hero.attack - target.defense)
        target.take_damage(damage)
        print(f"Causando {damage} de dano com ataque básico!")
    else:
        try:
            # Ataque com arma
            if hero.weapon.attack_type == 'aoe':
                attack_results = hero.weapon.attack(targets=enemies)
            else:
                attack_results = hero.weapon.attack(target=target)
            
            for result in attack_results:
                if len(result) >= 2:
                    t, dmg = result[0], result[1]
                    t.take_damage(dmg)
                    print(f"Causando {dmg} de dano com {hero.weapon.name}!")
                    
                    if t.hp <= 0:
                        print(f"{t.name} foi derrotado!")
                        enemies.remove(t)
        except AttributeError:
            # Fallback para ataque básico se houver problema com a arma
            damage = max(1, hero.attack - target.defense)
            target.take_damage(damage)
            print(f"Causando {damage} de dano com ataque básico!")
    
    if target.hp <= 0 and target in enemies:
        enemies.remove(target)
    delay(0.5)

def victory(hero):
    """Processa vitória"""
    clear()
    reward = 10 * hero.level
    hero.gold += reward
    
    print("╔═══════════════════════════╗")
    print("║        VITÓRIA!           ║")
    print("╚═══════════════════════════╝")
    print(f"\nRecompensa: {reward} ouro")
    
    # Adiciona XP e verifica level up
    xp_gained = 30
    print(f"Experiência: +{xp_gained} XP")
    if hero.add_xp(xp_gained):
        print("\n★ ★ ★ LEVEL UP! ★ ★ ★")
        print(f"Novo nível: {hero.level}")
    
    delay(2)

def defeat(hero):
    """Processa derrota mantendo progresso"""
    clear()
    print("╔════════════════════════════╗")
    print("║        DERROTA...         ║")
    print("╚════════════════════════════╝")
    print("\nSeu herói foi derrotado, mas mantém seu progresso!")
    
    # Revive o herói com 50% de HP
    hero.hp = max(1, hero.max_hp // 2)  # Garante pelo menos 1 HP
    hero.potions = 1
    
    print(f"\n{hero.name} revive com {hero.hp}/{hero.max_hp} HP")
    print(f"Poções resetadas: {hero.potions}")
    print(f"Nível mantido: {hero.level}")
    print(f"XP atual: {hero.xp}/{hero.xp_to_level}")
    delay(3)
    return hero  # Retorna o herói modificado

def shop_menu(hero, shop):
    """Menu de compras com tratamento melhorado"""
    while True:
        clear()
        shop.show_shop()
        print(f"\nOuro: {hero.gold:.1f}")
        
        try:
            choice = int(input("Escolha o item (1-6) ou 0 para sair: "))
            
            if choice == 0:
                break
            elif 1 <= choice <= len(shop.inventory):
                shop.buy(hero, choice)
                input("\nPressione Enter para continuar...")
            else:
                print("Opção inválida!")
                delay(1)
        except ValueError:
            print("Digite um número válido!")
            delay(1)

def main():
    print("=== Rogue Like RPG ===")
    
    # Carrega ou cria novo herói
    hero = load_game()
    if hero:
        print(f"Herói carregado: {hero.name} (Nível {hero.level})")
        print(f"HP: {hero.hp}/{hero.max_hp} | Ouro: {hero.gold} | XP: {hero.xp}/{hero.xp_to_level}")
        choice = input("Continuar (1) ou Novo Jogo (2)? ")
        if choice == "2":
            hero = Hero(input("Digite um nome para seu personagem: "))
    else:
        hero = Hero(input("Digite um nome para seu personagem: "))
    
    shop = Shop()

    if not hero.weapon:
        hero.choose_weapon(Sword())
    
    # Primeira vez - escolha de arma
    if hero.level == 1 and not hero.weapon:
        shop.show_shop()
        try:
            choice = int(input("Escolha sua arma inicial (1-3): "))
            weapons = [Sword(), Bow(), Staff()]
            hero.choose_weapon(weapons[choice-1] if 1 <= choice <= 3 else Sword())
        except:
            hero.choose_weapon(Sword())
        print("\nVocê recebeu 1 poção de cura!")
        input("Pressione Enter para começar...")

    while True:
        # Gera inimigos balanceados
        scenarios = generate_enemies(hero.level)
        
        # Progressão de dificuldade
        if hero.level < 5:
            available_scenarios = scenarios[:3]
        elif 5 <= hero.level < 10:
            available_scenarios = scenarios[:4]
        else:
            available_scenarios = scenarios
        
        enemies = random.choice(available_scenarios)
        
        # Batalha
        won = battle(hero, enemies)
        
        if not won:
            hero = defeat(hero)  # Recebe o herói atualizado
            save_game(hero)
            
            choice = input("\n1) Tentar novamente\n2) Voltar à loja\n3) Sair\nEscolha: ")
            if choice == "2":
                shop_menu(hero, shop)  # Chamada correta da função
            elif choice == "3":
                return
            continue
        
        # Progressão pós-batalha
        shop.update_inventory(hero.level)
        shop.show_shop()
        try:
            print(f"Ouro: {hero.gold}")
            choice = int(input("Comprar item ou Continuar? "))
            if 1 <= choice <= 3:
                shop.buy(hero, choice)
        except:
            pass
        
        save_game(hero)  # Salva progresso
        input("Pressione Enter para próxima batalha...")

if __name__ == "__main__":
    main()