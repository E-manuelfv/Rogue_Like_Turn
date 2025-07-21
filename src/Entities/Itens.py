import random

class Potions:
    def __init__(self, name, effect_type, potency, duration=1, uses=1, price=0):
        """
        Classe base para todas as poções
        
        :param name: Nome da poção
        :param effect_type: Tipo de efeito ('heal', 'buff', 'debuff', etc)
        :param potency: Força do efeito principal
        :param duration: Duração em turnos (1 para efeito instantâneo)
        :param uses: Número de usos antes de acabar
        :param price: Preço na loja
        """
        self.name = name
        self.effect_type = effect_type
        self.potency = potency
        self.duration = duration
        self.remaining_uses = uses
        self.max_uses = uses
        self.price = price
        self.consumable = True
    
    def use(self, target=None, targets=None):
        """Método base para usar a poção"""
        if self.remaining_uses <= 0:
            print(f"{self.name} está vazia!")
            return None
            
        if not (target or targets):
            return None
            
        self.remaining_uses -= 1
        return self._apply_effect(target or targets[0] if targets else target)
    
    def _apply_effect(self, target):
        """Efeito específico a ser implementado pelas subclasses"""
        raise NotImplementedError("Método deve ser implementado pela subclasse")
    
    def refill(self, amount=None):
        """Recarrega os usos da poção"""
        if amount is None:
            self.remaining_uses = self.max_uses
        else:
            self.remaining_uses = min(self.max_uses, self.remaining_uses + amount)
        return self.remaining_uses
    
    def is_empty(self):
        """Verifica se a poção acabou"""
        return self.remaining_uses <= 0
    
    def __str__(self):
        return f"{self.name} ({self.remaining_uses}/{self.max_uses} usos) - {self.effect_type}"

class HealthPotion(Potions):
    def __init__(self, potency=20, size='medium'):
        """
        Poção de cura básica
        
        :param potency: Quantidade de cura (base)
        :param size: Tamanho ('small', 'medium', 'large')
        """
        sizes = {
            'small': {'name': 'Poção de Cura Pequena', 'potency': 15, 'uses': 1, 'price': 50},
            'medium': {'name': 'Poção de Cura Média', 'potency': 30, 'uses': 2, 'price': 90},
            'large': {'name': 'Poção de Cura Grande', 'potency': 50, 'uses': 3, 'price': 140}
        }
        
        size_data = sizes.get(size, sizes['medium'])
        
        super().__init__(
            name=size_data['name'],
            effect_type='heal',
            potency=size_data['potency'],
            uses=size_data['uses'],
            price=size_data['price']
        )
        
        self.size = size
        self.critical_heal_chance = 0.15  # Chance de cura crítica
    
    def _apply_effect(self, target):
        """Aplica o efeito de cura no alvo"""
        # Verifica se é uma cura crítica
        is_critical = random.random() < self.critical_heal_chance
        heal_amount = self.potency * (1.5 if is_critical else 1)
        
        # Aplica a cura no alvo (assumindo que o alvo tem um método heal)
        result = target.heal(heal_amount)
        
        # Retorna informações sobre o efeito
        return {
            'type': 'heal',
            'amount': heal_amount,
            'critical': is_critical,
            'target': target,
            'remaining_uses': self.remaining_uses
        }
    
    def upgrade_size(self):
        """Melhora o tamanho da poção"""
        size_order = ['small', 'medium', 'large']
        if self.size in size_order and size_order.index(self.size) < len(size_order) - 1:
            new_size = size_order[size_order.index(self.size) + 1]
            new_data = {
                'small': {'name': 'Poção de Cura Pequena', 'potency': 15, 'uses': 1, 'price': 50},
                'medium': {'name': 'Poção de Cura Média', 'potency': 30, 'uses': 2, 'price': 90},
                'large': {'name': 'Poção de Cura Grande', 'potency': 50, 'uses': 3, 'price': 140}
            }[new_size]
            
            self.name = new_data['name']
            self.potency = new_data['potency']
            self.max_uses = new_data['uses']
            self.remaining_uses = self.max_uses
            self.price = new_data['price']
            self.size = new_size
            return True
        return False