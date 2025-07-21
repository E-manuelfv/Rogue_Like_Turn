from src.Entities.Potions import HealthPotion

class Hero:
    def __init__(self, name, hp=100, attack=10, defense=5):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.gold = 0
        self.weapon = None
        self.potions = []  # Agora será uma lista de objetos Potion
        self.level = 1
        self.xp = 0
        self.xp_to_level = 50

    def choose_weapon(self, weapon):
        self.weapon = weapon

    def take_damage(self, damage):
        self.hp = max(0, self.hp - damage)
        return self.hp <= 0

    def use_potion(self, potion_index=0):
        """Usa uma poção específica do inventário (padrão: primeira poção)
        
        Args:
            potion_index: Índice da poção a ser usada (0 para a primeira)
        
        Returns:
            bool: True se a poção foi usada com sucesso, False caso contrário
        """
        # Verificação de segurança da lista de poções
        if not hasattr(self, 'potions'):
            self.potions = []
            print("Inventário de poções vazio!")
            return False
            
        if not isinstance(self.potions, list):
            print("Erro no sistema de poções! Reiniciando inventário...")
            self.potions = []
            return False
        
        # Verifica se há poções disponíveis
        if not self.potions:
            print("Você não tem poções no inventário!")
            return False
        
        # Valida o índice
        try:
            potion = self.potions[potion_index]
        except IndexError:
            print(f"Índice de poção inválido! Você tem {len(self.potions)} poção(s).")
            return False
        
        # Aplica o efeito da poção
        heal_amount = potion.potency
        self.hp = min(self.max_hp, self.hp + heal_amount)
        
        # Atualiza os usos restantes
        potion.remaining_uses -= 1
        print(f"Você usou {potion.name} e recuperou {heal_amount} HP!")
        print(f"HP atual: {self.hp}/{self.max_hp}")
        
        # Remove a poção se não tiver mais usos
        if potion.remaining_uses <= 0:
            removed_potion = self.potions.pop(potion_index)
            print(f"{removed_potion.name} foi consumida completamente!")
        
        return True
    
    def add_xp(self, amount):
        self.xp += amount
        if self.xp >= self.xp_to_level:
            self.level_up()
            return True
        return False

    def level_up(self):
        self.level += 1
        self.max_hp += 10
        self.hp = self.max_hp
        self.attack += 2
        self.defense += 1
        self.xp = 0
        self.xp_to_level = self.level * 50
        print(f"\n⭐ PARABÉNS! Você subiu para o nível {self.level}! ⭐")
        return True

    def show_status(self):
        """Mostra status completo do herói"""
        print(f"\n=== STATUS DE {self.name.upper()} ===")
        print(f"Vida: {self.hp}/{self.max_hp}")
        print(f"Ataque: {self.attack} | Defesa: {self.defense}")
        print(f"Nível: {self.level} | XP: {self.xp}/{self.xp_to_level}")
        print(f"Ouro: {self.gold}")
        
        if self.weapon:
            print(f"\nArma: {self.weapon.name} (Dano: +{self.weapon.base_damage})")
        
        print("\nPoções:")
        if not self.potions:
            print("Nenhuma poção no inventário")
        else:
            for i, potion in enumerate(self.potions):
                print(f"{i+1} - {potion.name} (Cura: {potion.potency} HP, Usos: {potion.remaining_uses}/{potion.max_uses})")

    def add_potion(self, potion):
        """Adiciona uma poção de forma segura"""
        if not hasattr(self, 'potions') or not isinstance(self.potions, list):
            self.potions = []
        self.potions.append(potion)

    def add_to_inventory(self, item):
        """Adiciona um item (poção) ao inventário de forma segura"""
        if not hasattr(self, 'potions') or not isinstance(self.potions, list):
            self.potions = []  # Garante que potions é uma lista
        
        if isinstance(item, HealthPotion):
            self.potions.append(item)
            return True
        return False