from src.Entities.Weapon import Sword, Bow, Staff
from src.Entities.Potions import HealthPotion
from src.Game.Utils import clear, delay

class Shop:
    def __init__(self, hero):
        self.hero = hero
        self.weapons = [Sword(), Bow(), Staff()]
        self.potions = [
            HealthPotion(size='small'),
            HealthPotion(size='medium'),
            HealthPotion(size='large')
        ]
        self.upgrade_cost_multiplier = 1

    def update_inventory(self, hero_level):
        """Atualiza o inventário da loja com base no nível do herói"""
        # Limpa os inventários atuais
        self.weapons = []
        self.potions = [
            HealthPotion(size='small'),
            HealthPotion(size='medium'),
            HealthPotion(size='large')
        ]
        
        # Adiciona armas básicas
        self.weapons.append(Sword())
        self.weapons.append(Bow())
        self.weapons.append(Staff())
        
        # Adiciona versões aprimoradas conforme o nível do herói
        if hero_level >= 3:
            sharp_sword = Sword()
            sharp_sword.sharpen()
            
            strong_bow = Bow()
            strong_bow.name = "Arco Longo"
            strong_bow.base_damage = 8
            strong_bow.accuracy = 0.90
            
            arcane_staff = Staff()
            arcane_staff.name = "Cajado Arcano"
            arcane_staff.base_damage = 7
            arcane_staff.accuracy = 0.88
            
            self.weapons.extend([sharp_sword, strong_bow, arcane_staff])
            
            # Adiciona poções melhores
            self.potions.append(HealthPotion(size='large'))
        
        if hero_level >= 5:
            legendary_sword = Sword()
            legendary_sword.name = "Espada Lendária"
            legendary_sword.base_damage = 16
            legendary_sword.accuracy = 0.85
            legendary_sword.special_effect = "Golpes Críticos Devastadores"
            
            master_bow = Bow()
            master_bow.name = "Arco Mestre"
            master_bow.base_damage = 10
            master_bow.accuracy = 0.95
            master_bow.special_effect = "Penetração Total"
            
            eldritch_staff = Staff()
            eldritch_staff.name = "Cajado Élfico"
            eldritch_staff.base_damage = 9
            eldritch_staff.accuracy = 0.92
            eldritch_staff.special_effect = "Chamas Élficas"
            
            self.weapons.extend([legendary_sword, master_bow, eldritch_staff])
            
            # Adiciona poções premium
            self.potions.append(HealthPotion(potency=75, size='premium'))
            
            self.upgrade_cost_multiplier = 1 + (hero_level * 0.1)

    def show_shop(self, menu_type='main'):
        """Mostra itens da loja com opção para diferentes menus"""
        clear()
        print("\n=== Loja ===")
        print(f"Ouro disponível: {self.hero.gold:.1f}")
        
        if menu_type == 'main':
            print("\n1 - Armas")
            print("2 - Poções")
            print("0 - Sair")
        elif menu_type == 'weapons':
            print("\nArmas disponíveis:")
            for i, weapon in enumerate(self.weapons):
                price = self._calculate_weapon_price(weapon)
                print(f"{i+1} - {weapon.name} (Dano: {weapon.base_damage}, Precisão: {weapon.accuracy*100:.0f}%, Preço: {price:.1f} ouro)")
            print("0 - Voltar")
        elif menu_type == 'potions':
            print("\nPoções disponíveis:")
            for i, potion in enumerate(self.potions):
                price = self._calculate_potion_price(potion)
                print(f"{i+1} - {potion.name} (Cura: {potion.potency} HP, Usos: {potion.max_uses}, Preço: {price:.1f} ouro)")
            print("0 - Voltar")

    def _calculate_weapon_price(self, weapon):
        """Calcula preço de armas com arredondamento"""
        base_price = weapon.base_damage * 5 + weapon.accuracy * 20
        # Aumenta preço para armas lendárias/especiais
        if "Lendária" in weapon.name or "Mestre" in weapon.name or "Élfico" in weapon.name:
            base_price *= 1.5
        return round(base_price * self.upgrade_cost_multiplier, 1)

    def _calculate_potion_price(self, potion):
        """Calcula preço de poções baseado em sua eficácia"""
        base_price = potion.potency * 2 + potion.max_uses * 10
        # Aumenta preço para poções premium
        if potion.size == 'premium':
            base_price *= 1.3
        return round(base_price * self.upgrade_cost_multiplier, 1)

    def buy_weapon(self, hero, choice):
        """Lógica de compra de armas"""
        try:
            if 1 <= choice <= len(self.weapons):
                weapon = self.weapons[choice - 1]
                price = self._calculate_weapon_price(weapon)
                
                if hero.gold >= price:
                    # Verifica se é arma lendária ou especial
                    is_special = any(x in weapon.name for x in ["Lendária", "Mestre", "Élfico"])
                    
                    if hero.weapon and type(hero.weapon).__name__ == type(weapon).__name__ and not is_special:
                        self._upgrade_weapon(hero, weapon)
                    else:
                        hero.choose_weapon(weapon)
                        print(f"\n✅ {weapon.name} equipada!")
                    
                    hero.gold -= price
                    print(f"Ouro restante: {hero.gold:.1f}")
                else:
                    print(f"\n❌ Ouro insuficiente! Precisa de {price:.1f} (tem {hero.gold:.1f})")
            else:
                print("\n⚠️ Opção inválida!")
        except Exception as e:
            print(f"\n❌ Erro na compra: {e}")
        
        input("\nPressione Enter para continuar...")

    def buy_potion(self, hero, choice):
        """Lógica segura para compra de poções"""
        try:
            if 1 <= choice <= len(self.potions):
                potion = self.potions[choice - 1]
                price = self._calculate_potion_price(potion)
                
                if hero.gold >= price:
                    if hasattr(hero, 'add_to_inventory'):
                        if hero.add_to_inventory(potion):
                            hero.gold -= price
                            print(f"\n✅ {potion.name} adicionada ao inventário!")
                            print(f"Ouro restante: {hero.gold:.1f}")
                        else:
                            print("\n❌ Erro ao adicionar poção ao inventário!")
                    else:
                        # Fallback para heróis sem o método
                        if not hasattr(hero, 'potions'):
                            hero.potions = []
                        hero.potions.append(potion)
                        hero.gold -= price
                        print(f"\n✅ {potion.name} adicionada ao inventário!")
                        print(f"Ouro restante: {hero.gold:.1f}")
                else:
                    print(f"\n❌ Ouro insuficiente! Precisa de {price:.1f} (tem {hero.gold:.1f})")
            else:
                print("\n⚠️ Opção inválida!")
        except Exception as e:
            print(f"\n❌ Erro na compra: {e}")
        
        input("\nPressione Enter para continuar...")

    def _upgrade_weapon(self, hero, new_weapon):
        """Lógica específica para melhorias de armas"""
        # Se for uma espada normal
        if isinstance(new_weapon, Sword) and hasattr(new_weapon, 'sharpen'):
            if new_weapon.sharpened:
                hero.weapon.base_damage += 3
                hero.weapon.accuracy = min(0.95, hero.weapon.accuracy + 0.05)
                print(f"\n⚔️ {new_weapon.name} melhorada para versão superior!")
            else:
                hero.weapon.sharpen()
                print(f"\n⚔️ Espada afiada!")
        else:
            # Melhoria padrão para outras armas
            hero.weapon.base_damage += 2
            hero.weapon.accuracy = min(0.95, hero.weapon.accuracy + 0.04)
            print(f"\n🔧 {new_weapon.name} aprimorada!")

def shop_menu(hero, shop):
    """Menu de compras completo com submenus"""
    while True:
        shop.show_shop('main')
        
        try:
            choice = input("\nEscolha uma opção: ")
            
            if choice == '0':
                break
            elif choice == '1':  # Menu de armas
                weapon_menu(hero, shop)
            elif choice == '2':  # Menu de poções
                potion_menu(hero, shop)
            else:
                print("Opção inválida!")
                delay(1)
        except ValueError:
            print("Digite um número válido!")
            delay(1)

def weapon_menu(hero, shop):
    """Submenu para compra de armas"""
    while True:
        shop.show_shop('weapons')
        
        try:
            choice = int(input("\nEscolha uma arma (0 para voltar): "))
            
            if choice == 0:
                break
            else:
                shop.buy_weapon(hero, choice)
        except ValueError:
            print("Digite um número válido!")
            delay(1)

def potion_menu(hero, shop):
    """Submenu para compra de poções"""
    while True:
        shop.show_shop('potions')
        
        try:
            choice = int(input("\nEscolha uma poção (0 para voltar): "))
            
            if choice == 0:
                break
            else:
                shop.buy_potion(hero, choice)
        except ValueError:
            print("Digite um número válido!")
            delay(1)