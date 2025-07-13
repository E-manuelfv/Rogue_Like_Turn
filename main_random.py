# Importação de classes do projeto
from src.Hero import Hero
from src.enemy import Goblin, Orc, Dragon
from src.Weapon import *
from src.shop import Shop
from src.Battle import battle, clear
import random

# Lista de cenários de batalha predefinidos (grupos de inimigos)
battle_scenarios = [
    [Goblin("Goblin", hp=20, attack=5, defense=2, level=1)],
    [Goblin("Goblin", hp=25, attack=6, defense=2, level=1), Goblin("Goblin", hp=25, attack=6, defense=2, level=1)],
    [Orc("Orc", hp=40, attack=10, defense=5, level=2)],
    [Orc("Orc", hp=35, attack=8, defense=4, level=2), Goblin("Goblin", hp=20, attack=5, defense=2, level=1)],
    [Dragon("Dragão Boss", hp=100, attack=20, defense=10, level=3)],
]

def main():
    print("=== Rogue Like - Modo Aleatório ===")
    hero = Hero("Herói")      # cria o personagem do jogador
    shop = Shop()             # inicializa a loja

    # Escolha da arma inicial
    shop.show_shop()
    escolha = int(input("Escolha sua arma inicial: "))
    try:
        if 1 <= escolha <= 3:
            hero.choose_weapon(shop.inventory[escolha - 1])
    except ValueError:
        hero.choose_weapon(shop.inventory[0]) # arma padrão caso escolha inválida

    print("Você também recebeu 1 poção de cura.")
    input("Digite qualquer tecla para começar as batalhas...")

    batalhas_vencidas = 0

    # Loop principal do jogo
    while hero.hp > 0:
        clear() # limpa tela

        if batalhas_vencidas < 3:
            enemies = random.choice(battle_scenarios[0:3])  # escolhe batalha aleatória sem poder ser o Boss
        elif batalhas_vencidas == 3:
            enemies = random.choice(battle_scenarios[4])  # Batalha com o Boss
        else:
            enemies = random.choice(battle_scenarios)  # escolhe batalha aleatória

        venceu = battle(hero, enemies)             # inicia batalha

        if not venceu:
            # caso o herói morra, reinicia o jogo (mantendo progresso)
            print("Você morreu! Reiniciando jogo com melhorias mantidas...")
            main()
            return
        else:
            batalhas_vencidas += 1
            print(f"Batalha {batalhas_vencidas} vencida. Ouro atual: {hero.gold}")
            shop.show_shop()
            compra = int(input("Deseja comprar algo? "))
            shop.buy(hero, compra) # compra opcional na loja
            input("Pressione Enter para próxima batalha...")

if __name__ == "__main__":
    main()
