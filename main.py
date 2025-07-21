from src.Entities.Hero import Hero
from src.Entities.Weapon import Sword, Bow, Staff
from src.Entities.Potions import HealthPotion
from src.Game.Prologue import initial_prologue
from src.Game.Utils import EnemyBattle, delay
from src.Game.Shop import Shop
from src.Game.Battle import battle, defeat
from src.Game.Save_Load import save_game, load_game
import random
import sys

def main():
    print("=== Rogue Like RPG ===")

    # Carrega ou cria novo herói
    hero = load_game()

    if hero:
        print(f"\nHerói carregado: {hero.name} (Nível {hero.level})")
        print(f"HP: {hero.hp}/{hero.max_hp} | Ouro: {hero.gold} | XP: {hero.xp}/{hero.xp_to_level}")
        choice = input("\nContinuar (1) ou Novo Jogo (2)? ")
        if choice == "2":
            hero = Hero(input("\nDigite um nome para seu personagem: "))
            initial_prologue(hero.name)
    else:
        hero = Hero(input("\nDigite um nome para seu personagem: "))
        initial_prologue(hero.name)
    
    shop = Shop(hero=hero)

    # Primeira vez - escolha de arma
    if hero.level == 1 and not hero.weapon:
        print("\n=== Escolha sua Arma Inicial ===")
        weapons = [Sword(), Bow(), Staff()]
        for i, weapon in enumerate(weapons):
            print(f"{i+1} - {weapon.name} (Dano: {weapon.base_damage})")
        
        try:
            choice = int(input("\nEscolha sua arma inicial (1-3): "))
            if 1 <= choice <= 3:
                hero.choose_weapon(weapons[choice-1])
            else:
                hero.choose_weapon(Sword())
        except:
            hero.choose_weapon(Sword())
        
        # Presente inicial
        hero.potions.append(HealthPotion(size='small'))
        print("\nVocê recebeu 1 Poção de Cura Pequena!")
        input("\nPressione Enter para começar sua jornada...")

    while True:
        # Atualiza loja conforme nível do herói
        shop.update_inventory(hero.level)
        
        # Gera inimigos balanceados
        scenarios = EnemyBattle.generate_enemies(hero_level=hero.level)
        
        # Verifica se é batalha contra chefe
        if hero.level >= 5 and not EnemyBattle.boss_defeated:
            EnemyBattle.boss_fight_variable = True
            enemies_data = scenarios[-1]  # Pega o cenário do dragão
            print(f"\n🐉 BATALHA CONTRA {enemies_data['name'].upper()}! 🐉")
        else:
            enemies_data = random.choice(scenarios[:-1])  # Exclui o dragão das escolhas normais
            print(f"\n=== BATALHA CONTRA {enemies_data['name'].upper()} ===")
        
        # Batalha
        won = battle(hero, enemies_data['enemies'])
        
        if not won:
            hero = defeat(hero)
            save_game(hero)
            
            choice = input("\n1) Tentar novamente\n2) Voltar à loja\n3) Sair\nEscolha: ")
            if choice == "2":
                        hero.gold += 100
                        while True:
                            shop.show_shop('main')
                            try:
                                choice = input("\nEscolha uma opção (1-Armas, 2-Poções, 0-Sair): ")
                                
                                if choice == '0':
                                    break
                                elif choice == '1':
                                    # Menu de armas
                                    while True:
                                        shop.show_shop('weapons')
                                        try:
                                            weapon_choice = int(input("\nEscolha uma arma (0-Voltar): "))
                                            if weapon_choice == 0:
                                                break
                                            shop.buy_weapon(hero, weapon_choice)
                                        except ValueError:
                                            print("Digite um número válido!")
                                elif choice == '2':
                                    # Menu de poções
                                    while True:
                                        shop.show_shop('potions')
                                        try:
                                            potion_choice = int(input("\nEscolha uma poção (0-Voltar): "))
                                            if potion_choice == 0:
                                                break
                                            shop.buy_potion(hero, potion_choice)
                                        except ValueError:
                                            print("Digite um número válido!")
                                else:
                                    print("Opção inválida!")
                            except Exception as e:
                                print(f"Erro: {e}")
                            
                            # Sai do loop da loja
                            break

            elif choice == "3":
                return
            else:
                if not hasattr(hero, 'potions') or not isinstance(hero.potions, list):
                    hero.potions = []
                hero.potions.append(HealthPotion(size='small'))
                print("Você ganhou uma poção de cura pequena como consolação!")
            continue
        
        # Recompensas pós-batalha
        xp_gain = enemies_data['xp']
        gold_gain = random.randint(enemies_data['gold_min'], enemies_data['gold_max'])
        
        print(f"\nVocê ganhou {xp_gain} XP e {gold_gain} de ouro!")
        hero.gold += gold_gain
        leveled_up = hero.add_xp(xp_gain)
        
        # Verifica se derrotou o chefe
        if 'is_boss' in enemies_data and enemies_data['is_boss']:
            EnemyBattle.boss_defeated = True
            print("\n⭐ VOCÊ DERROTOU O DRAGÃO BOSS! ⭐")
        
        # Loja pós-batalha
        while True:
            shop.show_shop('main')
            try:
                choice = input("\nEscolha uma opção (1-Armas, 2-Poções, 0-Sair): ")
                
                if choice == '0':
                    break
                elif choice == '1':
                    # Menu de armas
                    while True:
                        shop.show_shop('weapons')
                        try:
                            weapon_choice = int(input("\nEscolha uma arma (0-Voltar): "))
                            if weapon_choice == 0:
                                break
                            shop.buy_weapon(hero, weapon_choice)
                        except ValueError:
                            print("Digite um número válido!")
                elif choice == '2':
                    # Menu de poções
                    while True:
                        shop.show_shop('potions')
                        try:
                            potion_choice = int(input("\nEscolha uma poção (0-Voltar): "))
                            if potion_choice == 0:
                                break
                            shop.buy_potion(hero, potion_choice)
                        except ValueError:
                            print("Digite um número válido!")
                else:
                    print("Opção inválida!")
            except Exception as e:
                print(f"Erro: {e}")
            
            # Sai do loop da loja
            break

        # Continua para próxima batalha
        print("\nProgresso salvo automaticamente.")
        input("\nPressione Enter para continuar para a próxima batalha...")

def is_frozen():
    """Verifica se o jogo foi compilado pelo PyInstaller"""
    return hasattr(sys, '_MEIPASS')

if __name__ == "__main__":
    if is_frozen():
        print("Modo executável detectado!")
    main()