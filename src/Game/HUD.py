
class HUD:
    @staticmethod
    def draw_hp_bar(current_hp, max_hp, bar_length=20):
        """
        Desenha uma barra de vida proporcional usando o caractere '|'.
        """
        filled_length = int(bar_length * current_hp // max_hp)
        empty_length = bar_length - filled_length
        bar = '|' * filled_length + '.' * empty_length
        print(f"HP: [{bar}] {current_hp}/{max_hp}")
