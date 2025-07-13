from src.Weapon import Sword, Bow, Staff

class Shop:
    def __init__(self):
        self.inventory = [Sword(), Bow(), Staff()]

    def show_shop(self):
        print("=== Loja ===")
        for i, item in enumerate(self.inventory):
            print(f"{i+1} - {item.name} (Dano: {item.damage})")
        print("0 - Sair")

    def buy(self, hero, choice):
        while choice [0, 1, 2, 3]:
            try:
                if 1 <= choice <= len(self.inventory):
                    weapon = self.inventory[choice - 1]
                    price = 10 * weapon.damage
                    if hero.gold >= price:
                        hero.gold -= price
                        hero.choose_weapon(weapon)
                        print(f"{weapon.name} comprado!")
                    else:
                        print("Ouro insuficiente.")
            except:
                choice = 0
                print("Opção inválida.")

