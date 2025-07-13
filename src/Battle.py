# importa todas as classes e funções do projeto
from src.Hero import *
from src.enemy import *
from src.Weapon import *
from src.HUD import HUD
import random, os, time

# função para limpar a tela do console (compatível com Windows ou Linux/Mac)
def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

# função que aplica um pequeno atraso (para ritmo do jogo)
def delay(timer):
    time.sleep(timer)

# função principal de batalha, gerencia o combate entre o herói e um grupo de inimigos
def battle(hero, enemies):
    print(f"\n-- Batalha contra {[e.name for e in enemies]} --")
    
    # laço da batalha continua enquanto existirem inimigos e o herói estiver vivo
    while enemies and hero.hp > 0:
        # desenha barra de HP do herói
        HUD.draw_hp_bar(hero.hp, hero.max_hp)
        print("\nSeu turno!")
        print("1 - Atacar\n2 - Defender\n3 - Curar")

        # laço para garantir que a ação seja válida (só aceita 1, 2 ou 3)
        action = 0
        while action not in [1, 2, 3]:
            try:
                action = int(input("Escolha sua ação: "))
            except ValueError:
                action = 0
            if action not in [1, 2, 3]:
                print("Opção inválida, tente novamente.")

        # ação de ataque
        if action == 1:
            # lista todos os inimigos vivos
            for idx, e in enumerate(enemies):
                print(f"{idx+1} - {e.name} (HP: {e.hp})")

            # laço para garantir que a escolha de alvo seja válida
            target = -1
            while target not in range(len(enemies)):
                try:
                    target = int(input("Escolha o alvo: ")) - 1
                except ValueError:
                    target = -1
                if target not in range(len(enemies)):
                    print("Alvo inválido, tente novamente.")

            # herói ataca o alvo escolhido
            hero.attack_enemy(enemies[target])

            delay(0.1)

            # verifica se o inimigo foi derrotado
            if enemies[target].hp <= 0:
                print(f"{enemies[target].name} derrotado!")
                gold_gain = random.randint(5, 15) * enemies[target].level
                hero.gold += gold_gain
                print(f"Ganhou {gold_gain} ouro!")
                del enemies[target]

            delay(0.1)

        # ação de defesa
        elif action == 2:
            hero.defend()

        # ação de cura
        elif action == 3:
            hero.heal()

        # turno dos inimigos
        enemy_damage(hero, enemies)

    # retorna True se o herói sobreviveu, ou False se morreu
    return hero.hp > 0

# função separada para processar o ataque dos inimigos
def enemy_damage(hero, enemies):
    clear()  # limpa tela a cada rodada para manter visual limpo
    for enemy in enemies:
        enemy.attack_hero(hero)
        if hero.hp <= 0:
            print(f"Você foi derrotado por {enemy.name}!")
            break
