from src.Entities.Hero import Hero
from src.Game.Prologue import initial_prologue
from src.Entities.Weapon import Sword, Bow, Staff
from src.Game.Utils import EnemyBattle, delay
from src.Game.Shop import Shop, shop_menu
from src.Game.Battle import battle, defeat
from src.Game.Save_Load import save_game, load_game
import random, sys

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
            initial_prologue(hero.name) # Prólogo do jogo
    else:
        hero = Hero(input("Digite um nome para seu personagem: "))
        initial_prologue(hero) # Prólogo do jogo
    
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
        scenarios = EnemyBattle.generate_enemies(hero.level)
        
        # Progressão de dificuldade
        if hero.level < 4:
            available_scenarios = scenarios[:3]
        elif 4 >= hero.level < 6:
            available_scenarios = scenarios[:4]
        elif hero.level == 6:
            EnemyBattle.boss_fight_variable = True
            delay(1) # Preparação para o Dragão...
            print(" 🐉 Um Dragão sobrevoa a área!...")
        else:
            available_scenarios = scenarios
        
        if EnemyBattle.boss_fight_variable:
            enemies = scenarios[-1]
        else:
            enemies = random.choice(available_scenarios)
        
        # Batalha
        won = battle(hero, enemies)
        delay(1) # Preparação para o Dragão...
        print("Você se aproxima do Dragão 🐉...")
        
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
            if 1 <= choice <= len(shop.inventory):
                shop.buy(hero, choice)
        except:
            pass
        
        save_game(hero)  # Salva progresso
        input("Pressione Enter para próxima batalha...")

# Adicional para criar um executável do jogo
def is_frozen():
    """Verifica se o jogo foi compilado pelo PyInstaller"""
    return hasattr(sys, '_MEIPASS')

if is_frozen():
    print("Modo executável detectado!")
    # Ajuste caminhos de arquivos aqui
else:
    print("Modo desenvolvimento")

if __name__ == "__main__":
    main()