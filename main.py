from src.Entities.Hero import Hero
from src.Entities.Weapon import Sword, Bow, Staff
from src.Game.Utils import generate_enemies
from src.Game.Shop import Shop, shop_menu
from src.Game.Battle import battle, defeat
import random

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