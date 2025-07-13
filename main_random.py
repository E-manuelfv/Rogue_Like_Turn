# Importação de classes do projeto
from src.Hero import Hero
from src.enemy import Goblin, Orc, Dragon
from src.Weapon import *
from src.shop import Shop
from src.Battle import battle, clear, delay
import random
import sys

# Lista de cenários de batalha predefinidos (grupos de inimigos)
battle_scenarios = [
    [Goblin("Goblin", hp=25, attack=5, defense=2, level=1)],
    [Goblin("Goblin", hp=20, attack=6, defense=2, level=1), Goblin("Goblin", hp=20, attack=6, defense=2, level=1)],
    [Orc("Orc", hp=40, attack=10, defense=5, level=2)],
    [Orc("Orc", hp=35, attack=8, defense=4, level=2), Goblin("Goblin", hp=20, attack=5, defense=2, level=1)],
    [Dragon("Dragão Boss", hp=100, attack=20, defense=10, level=3)],
]

def show_weapon_choices():
    print("\nEscolha sua arma inicial:")
    print("1. Espada - Alto dano único (70% precisão)")
    print("   Poder: Chance de golpe crítico (2x dano)")
    print("2. Arco - Ataques precisos (95% precisão)")
    print("   Poder: Dano verdadeiro (ignora parte da defesa)")
    print("3. Cajado - Ataques em área (85% precisão)")
    print("   Poder: Chance de aplicar queimadura (dano contínuo)")

def main():
    print("=== Rogue Like - Modo Aleatório ===")
    hero = Hero("Herói")      # personagem do jogador
    shop = Shop()             # inicializa a loja

    # Escolha da arma inicial
    show_weapon_choices()
    
    try:
        escolha = int(input("\nEscolha sua arma inicial (1-3): "))
        if 1 <= escolha <= 3:
            # Cria a arma escolhida
            if escolha == 1:
                weapon = Sword()
            elif escolha == 2:
                weapon = Bow()
            else:
                weapon = Staff()
            hero.choose_weapon(weapon)
        else:
            print("Escolha inválida. Você recebeu uma Espada por padrão.")
            hero.choose_weapon(Sword())
    except ValueError:
        print("Entrada inválida. Você recebeu uma Espada por padrão.")
        hero.choose_weapon(Sword())

    delay(1)
    clear()
    print(f"\nVocê equipou: {hero.weapon.name}")
    print("Você também recebeu 1 poção de cura.")
    input("\nDigite qualquer tecla para começar as batalhas...")

    batalhas_vencidas = 0

    # Loop principal do jogo
    while hero.hp > 0:
        clear() # limpa tela

        # Seleção de inimigos baseada no progresso
        if batalhas_vencidas < 3:
            possible_scenarios = [scenario for scenario in battle_scenarios[0:3] if len(scenario) > 0]
            enemies = random.choice(possible_scenarios) if possible_scenarios else [Goblin("Goblin", hp=25, attack=5, defense=2, level=1)]
        elif batalhas_vencidas == 3:
            enemies = battle_scenarios[4] if len(battle_scenarios[4]) > 0 else [Dragon("Dragão Boss", hp=100, attack=20, defense=10, level=3)]
        else:
            possible_scenarios = [scenario for scenario in battle_scenarios if len(scenario) > 0]
            enemies = random.choice(possible_scenarios) if possible_scenarios else [Orc("Orc", hp=40, attack=10, defense=5, level=2)]

        print(f"\nBatalha {batalhas_vencidas + 1} - {len(enemies)} inimigo(s)")
        print(f"Arma atual: {hero.weapon.name}")
        
        venceu = battle(hero, enemies)  # inicia batalha

        if not venceu:
            delay(1)
            print("\nVocê morreu! Reiniciando jogo com melhorias mantidas...")
            input("Pressione Enter para continuar...")
            main()
            return
        else:
            batalhas_vencidas += 1
            print(f"\nBatalha {batalhas_vencidas} vencida! Ouro atual: {hero.gold}")
            
            # Atualiza a loja com novas armas se necessário
            shop.update_inventory(batalhas_vencidas)
            
            # Opção de compra
            try:
                shop.show_shop()
                compra = input("\nDeseja comprar algo? (1-3 para comprar, 0 para continuar): ")
                if compra.isdigit():
                    compra = int(compra)
                    if compra > 0:
                        shop.buy(hero, compra)
            except Exception as e:
                print(f"Erro na loja: {e}")
            
            input("\nPressione Enter para próxima batalha...")

if __name__ == "__main__":
    main()