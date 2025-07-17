from src.Weapon import Sword, Bow, Staff

class Shop:
    def __init__(self):
        self.inventory = [Sword(), Bow(), Staff()]
        self.upgrade_cost_multiplier = 1 # Deixei mais fácil

    def update_inventory(self, hero_level):
        """Atualiza o inventário da loja com base no nível do herói"""
        # Limpa o inventário atual
        self.inventory = []
        
        # Adiciona armas básicas
        self.inventory.append(Sword())
        self.inventory.append(Bow())
        self.inventory.append(Staff())
        
        # Adiciona versões aprimoradas conforme o nível do herói
        if hero_level >= 3:
            # Cria versões aprimoradas das armas básicas
            sharp_sword = Sword()
            sharp_sword.sharpen()  # Usa o método sharpen que já existe
            
            strong_bow = Bow()
            strong_bow.name = "Arco Longo"
            strong_bow.base_damage = 8
            strong_bow.accuracy = 0.90
            
            arcane_staff = Staff()
            arcane_staff.name = "Cajado Arcano"
            arcane_staff.base_damage = 7
            arcane_staff.accuracy = 0.88
            
            self.inventory.extend([sharp_sword, strong_bow, arcane_staff])
        
        if hero_level >= 5:
            # Cria versões lendárias
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
            
            self.inventory.extend([legendary_sword, master_bow, eldritch_staff])
    
            # Ajusta o multiplicador de preço conforme o nível
            self.upgrade_cost_multiplier = 1 + (hero_level * 0.1)

    def show_shop(self):
        """Mostra itens com valores arredondados"""
        print("\n=== Loja ===")
        print("Itens disponíveis:")
        for i, item in enumerate(self.inventory):
            price = self._calculate_price(item)
            print(f"{i+1} - {item.name} (Dano: {item.base_damage}, Precisão: {item.accuracy*100:.0f}%, Preço: {price:.1f} ouro)")
        print("0 - Sair")
        
    def _calculate_price(self, weapon):
        """Calcula preço com arredondamento"""
        base_price = weapon.base_damage * 5 + weapon.accuracy * 20
        return round(base_price * self.upgrade_cost_multiplier, 1)  # Arredonda para 1 decimal

    def buy(self, hero, choice):
        try:
            if 1 <= choice <= len(self.inventory):
                weapon = self.inventory[choice - 1]
                price = self._calculate_price(weapon)
                
                if hero.gold >= price:
                    # Verifica se é uma melhoria ou nova arma
                    if isinstance(hero.weapon, type(weapon)):
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

    def _upgrade_weapon(self, hero, new_weapon):
        """Lógica específica para melhorias"""
        # Verifica se é uma espada para usar o método sharpen
        if isinstance(new_weapon, Sword) and hasattr(new_weapon, 'sharpen'):
            if new_weapon.sharpened:  # Se já for afiada, melhora os atributos
                hero.weapon.base_damage += 3
                hero.weapon.accuracy = min(0.95, hero.weapon.accuracy + 0.05)
                print(f"\n⚔️ {new_weapon.name} melhorada para versão superior!")
            else:  # Se não for afiada, afia
                hero.weapon.sharpen()
                print(f"\n⚔️ Espada afiada!")
        else:
            # Melhoria padrão para outras armas
            hero.weapon.base_damage += 2
            hero.weapon.accuracy = min(0.95, hero.weapon.accuracy + 0.04)
            print(f"\n🔧 {new_weapon.name} aprimorada!")