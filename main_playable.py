from src.Hero import Hero
from src.enemy import *
from src.Weapon import *
from src.shop import Shop
from src.utils import generate_enemy_wave
import random, os

def main():
    print("=== Bem-vindo ao Rogue Like ===")
    hero = Hero("Herói")
    shop = Shop()
    
    # Escolha arma inicial
    shop.show_shop()
    escolha = int(input("Escolha sua arma inicial: "))
    if 1 <= escolha <= 3:
        hero.choose_weapon(shop.inventory[escolha - 1])
    else:
        hero.choose_weapon(shop.inventory[0])
    print("Você também recebeu 1 poção de cura.")
    input("Digite qualquer tecla para prosseguir... ")

    
    stage = 1
    while stage <= 3:
        clear()
        print(f"\n-- Estágio {stage} --")
        if stage < 3:
            enemies = generate_enemy_wave(stage)
        else:
            enemies = [Dragon("Dragão Boss", hp=100, attack=20, defense=10, level=stage)]
        
        while enemies and hero.hp > 0:
            print("\nSeu turno!")
            print("1 - Atacar\n2 - Defender\n3 - Curar")
            action = int(input("Escolha sua ação: "))
            if action == 1:
                for idx, e in enumerate(enemies):
                    print(f"{idx+1} - {e.name} (HP: {e.hp})")
                target = int(input("Escolha o alvo: ")) - 1
                hero.attack_enemy(enemies[target])
                if enemies[target].hp <= 0:
                    print(f"{enemies[target].name} derrotado!")
                    gold_gain = random.randint(5, 15) * enemies[target].level
                    hero.gold += gold_gain
                    print(f"Ganhou {gold_gain} ouro!")
                    del enemies[target]
            elif action == 2:
                hero.defend()
            elif action == 3:
                hero.heal()

            # inimigos atacam
            for enemy in enemies:
                enemy.attack_hero(hero)
                if hero.hp <= 0:
                    break

        if hero.hp <= 0:
            print("Você morreu! Reiniciando jogo com melhorias mantidas...")
            main()  # reinicia mantendo melhorias
            return
        else:
            if stage < 3:
                print(f"Estágio {stage} completo. Você tem {hero.gold} ouro.")
                shop.show_shop()
                compra = int(input("Deseja comprar algo? "))
                shop.buy(hero, compra)
            stage += 1

    print("Parabéns! Você venceu o jogo derrotando o boss!")

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

if __name__ == "__main__":
    main()
