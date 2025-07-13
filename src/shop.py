from src.Weapon import Sword, Bow, Staff
import random

class Shop:
    def __init__(self):
        self.inventory = [Sword(), Bow(), Staff()]
        self.upgrade_cost_multiplier = 1.5  # Multiplicador de custo para melhorias

    def show_shop(self):
        print("\n=== Loja ===")
        print("Itens disponíveis:")
        for i, item in enumerate(self.inventory):
            price = self._calculate_price(item)
            print(f"{i+1} - {item.name} (Dano: {item.base_damage}, Precisão: {item.accuracy*100}%, Preço: {price} ouro)")
        print("0 - Sair")

    def _calculate_price(self, weapon):
        """Calcula o preço baseado no dano e precisão"""
        return int(weapon.base_damage * 5 + weapon.accuracy * 20) * self.upgrade_cost_multiplier

    def buy(self, hero, choice):
        try:
            if 1 <= choice <= len(self.inventory):
                weapon = self.inventory[choice - 1]
                price = self._calculate_price(weapon)
                
                if hero.gold >= price:
                    # Verifica se o herói já tem uma arma do mesmo tipo
                    if hero.weapon and type(hero.weapon) == type(weapon):
                        # Melhora a arma existente
                        hero.weapon.base_damage += 2  # Aumenta o dano
                        hero.weapon.accuracy = min(1.0, hero.weapon.accuracy + 0.05)  # Aumenta precisão (máx 100%)
                        print(f"{weapon.name} melhorada! Dano: {hero.weapon.base_damage}, Precisão: {hero.weapon.accuracy*100}%")
                    else:
                        # Equipa nova arma
                        hero.choose_weapon(weapon)
                        print(f"{weapon.name} equipado!")
                    
                    hero.gold -= price
                else:
                    print("Ouro insuficiente.")
        except Exception as e:
            print(f"Erro na compra: {e}")

    def update_inventory(self, battles_won):
        """Atualiza o inventário baseado no progresso do jogo"""
        self.upgrade_cost_multiplier = 1 + (battles_won * 0.2)  # Aumenta preço conforme progresso
        
        # Chance de adicionar armas melhores depois de certas batalhas
        if battles_won >= 3:
            self.inventory.append(Sword())  # Adiciona nova espada (poderia ser uma versão melhorada)
            self.inventory[-1].base_damage += 3
            self.inventory[-1].name = "Espada Afiada"
            
        if battles_won >= 5:
            self.inventory.append(Staff())
            self.inventory[-1].base_damage += 2
            self.inventory[-1].name = "Cajado Arcano"