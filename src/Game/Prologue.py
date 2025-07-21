# Aqui foi para garantir minha nota máxima!
from src.Game.Utils import clear
import time

def print_with_delay(text, delay=2):
    print(text)
    time.sleep(delay)

def initial_prologue(hero_name):
    clear()
    print_with_delay(r"""
  ____   _   _  _   _   ____  _____  _   _  _   _   _____ _   _ ____   _   _ 
 |  _ \ | | | || \ | | / ___ | ____|| | | || \ | | |_   _| | | |  _  \| \ | | 
 | | | || | | ||  \| || | __ |  _| || | | ||  \| |   | | | | | | |_) ||  \| |
 | |_| || |_| || |\  || |_| || |___|| |_| || |\  |   | | | |_| |  _  /| |\  | 
 |____/  \___/ |_| \_| \___/ |_____| \___/ |_| \_|   |_|  \___/|_| \_\|_| \_|
                                                                           
    """,3)
    print_with_delay("\nEm um vasto reino assolado pela guerra...")
    print_with_delay("A princesa Neméia foi sequestrada por um dragão alado que domina o campo aberto.")
    print_with_delay(f"\n{hero_name}, um bravo guerreiro, recebe a missão de resgatá-la.")
    print_with_delay("Mas a jornada não será fácil. Ele enfrentará perigosos inimigos como:")
    print_with_delay("- Orcs sedentos por sangue")
    print_with_delay("- Goblins traiçoeiros que espreitam nas sombras")
    print_with_delay("\nO dragão aguarda em um campo devastado, entre as cinzas de batalhas passadas...")

    print_with_delay(r"""
                        ____====-_  _-====____
                    _-~~             ~~-_
                   _-~                 ~-_ 
                  /         \/|\/         \ 
                 |       /~~\___/~~\       |
                 |      |    /###\   |     |
                  \     \   |#####| /     / 
                   \     \  |#####|/     / 
                    \_____\_|_____|_____/ 
    """)

    print_with_delay("\nEmpunhe sua espada, vista sua armadura...")
    print_with_delay("A batalha pela salvação de Neméia começa agora!")
    input("\nPressione ENTER para embarcar nesta jornada épica! \n")
    clear()