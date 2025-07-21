# importa todas as classes e funções do projeto
from src.Entities.Hero import *
from src.Entities.Enemy import *
from src.Entities.Weapon import *
from src.Game.HUD import HUD
from src.Game.Utils import EnemyBattle, clear, delay
import sys

def battle(hero, enemies):
    """Sistema principal de batalha"""
    clear()
    if EnemyBattle.boss_fight_variable:
        print("╔══════════════════════════════╗")
        print(f"║ BATALHA CONTRA O DRAGÃO 🐲 !!║")
        print("╚══════════════════════════════╝")
    else:
        print("╔══════════════════════════════╗")
        print(f"║  BATALHA CONTRA {len(enemies)} INIMIGO(S) ║")
        print("╚══════════════════════════════╝")
    delay(1)
    
    while True:
        # Filtra apenas inimigos vivos
        alive_enemies = [e for e in enemies if e.hp > 0]
        
        # Turno do Herói
        print(f"\n{hero.name} - Nível {hero.level} | XP: {hero.xp}/{hero.xp_to_level}")
        print(f"HP: {hero.hp}/{hero.max_hp} | Poções: {len(hero.potions) if hasattr(hero, 'potions') 
                                                       and isinstance(hero.potions, list) else 0}")
        
        if not alive_enemies:  # Verifica se todos estão mortos
            victory(hero)
            return True
            
        print("Inimigos:")
        for i, enemy in enumerate(alive_enemies):  # Mostra apenas vivos
            print(f"{i+1}. {enemy.name} - HP: {enemy.hp}/{enemy.max_hp}")
        
        action = input("\nAção: (1) Atacar (2) Poção (3) Defender: ").strip()
        
        defending = False
        defense_bonus = 0
        
        if action == "1":  # Ataque
            if len(alive_enemies) > 1:
                try:
                    target = int(input("Escolha o alvo (número): ")) - 1
                    if 0 <= target < len(alive_enemies):
                        execute_attack(hero, alive_enemies[target], enemies)
                    else:
                        print("Alvo inválido!")
                        delay(1)
                except ValueError:
                    print("Digite um número válido!")
                    delay(1)
            else:
                execute_attack(hero, alive_enemies[0], enemies)
                
        elif action == "2":  # Poção
            # Verificação robusta do sistema de poções
            if not hasattr(hero, 'potions'):
                hero.potions = []
                print("Sistema de poções reiniciado!")
            
            if not isinstance(hero.potions, list):
                hero.potions = []
                print("Inventário de poções corrigido!")
            
            if hero.potions:  # Verifica se há poções
                if hero.use_potion():
                    pass
                else:
                    print("Não foi possível usar a poção!")
            else:
                print("Você não tem poções disponíveis!")
            delay(1)
            continue
            
        elif action == "3":  # Defesa
            defending = True
            defense_bonus = hero.defense * 0.5
            print(f"{hero.name} se defende! +{defense_bonus:.1f} defesa")
            delay(1)
        
        # Atualiza lista de inimigos vivos
        alive_enemies = [e for e in enemies if e.hp > 0]
        if not alive_enemies:
            victory(hero)
            return True
        
        # Turno dos Inimigos (apenas os vivos)
        for enemy in alive_enemies:
            damage = max(1, enemy.attack - (hero.defense + defense_bonus))
            print(f"\n{enemy.name} ataca! {damage} de dano")
            hero.take_damage(damage)
            
            if hero.hp <= 0:
                defeat(hero)
                return False
            delay(1)
        
        input("\nPressione Enter para continuar...")
        clear()

def execute_attack(hero, target, enemies):
    """Executa um ataque com verificação de arma"""
    print(f"\n{hero.name} ataca {target.name}!")
    delay(0.5)
    
    if not hero.weapon:
        # Ataque básico sem arma
        damage = max(1, hero.attack - target.defense)
        target.take_damage(damage)
        print(f"Causando {damage} de dano com ataque básico!")
    else:
        try:
            # Ataque com arma
            if hero.weapon.attack_type == 'aoe':
                attack_results = hero.weapon.attack(targets=enemies)
            else:
                attack_results = hero.weapon.attack(target=target)
            
            for result in attack_results:
                if len(result) >= 2:
                    t, dmg = result[0], result[1]
                    t.take_damage(dmg)
                    print(f"Causando {dmg} de dano com {hero.weapon.name}!")
                    
                    if t.hp <= 0:
                        print(f"{t.name} foi derrotado!")
                        enemies.remove(t)
        except AttributeError:
            # Fallback para ataque básico se houver problema com a arma
            damage = max(1, hero.attack - target.defense)
            target.take_damage(damage)
            print(f"Causando {damage} de dano com ataque básico!")
    
    if target.hp <= 0 and target in enemies:
        enemies.remove(target)
    delay(0.5)

def victory(hero):
    """Processa vitória"""
    clear()
    reward = 10 * hero.level
    hero.gold += reward

    print("╔═══════════════════════════╗")
    print("║        VITÓRIA!           ║")
    print("╚═══════════════════════════╝")
    print(f"\nRecompensa: {reward} ouro")

    # Adiciona XP e verifica level up
    if EnemyBattle.boss_fight_variable:
        xp_gained = 200 + 10 * hero.level
    else:
        xp_gained = 20 + 10 * hero.level
        
    print(f"Experiência: +{xp_gained} XP")
    if hero.add_xp(xp_gained):
        print("\n★ ★ ★ LEVEL UP! ★ ★ ★")
        print(f"Novo nível: {hero.level}")
    
    delay(2)

    # Verifica se foi uma luta contra o chefe final
    final_battle = EnemyBattle.boss_fight_variable
    if final_battle:
        delay(2)
        print("\nVocê derrotou o dragão cuspidor de fogo!")
        print("A princesa Neméia está a salvo em seus braços.")
        print("O reino está em festa, e seu nome será lembrado por gerações.")
        delay(3)

        print(r"""
              |\                     /)
            /\_\\__               (_//
           |   `>\-`     _._       //`)
            \ /` \\  _.-`:::`-._  //
             `    \|`    :::    `|/
                   |     :::     |
                   |.....:::.....|
                   |:::::::::::::|
                    \:::::::::::/
                     \:::::::::/
                       `-._.-'
                      
        """)
        delay(3)

        choice = input("\nDeseja continuar sua jornada mesmo após a vitória? (s/n): ").strip().lower()
        if choice != 's':
            print("\nVocê pendura sua espada e volta para casa com a princesa.")
            print("Fim da jornada... por enquanto.")
            delay(1)
            sys.exit()  # Encerra o Jogo

def defeat(hero):
    """Processa derrota mantendo progresso"""
    clear()
    print("╔════════════════════════════╗")
    print("║        DERROTA...         ║")
    print("╚════════════════════════════╝")
    print("\nSeu herói foi derrotado, mas mantém seu progresso!")
    
    # Revive o herói com 50% de HP
    hero.hp = max(1, hero.max_hp // 2)  # Garante pelo menos 1 HP
    hero.potions = 1
    
    print(f"\n{hero.name} revive com {hero.hp}/{hero.max_hp} HP")
    print(f"Poções resetadas: {hero.potions}")
    print(f"Nível mantido: {hero.level}")
    print(f"XP atual: {hero.xp}/{hero.xp_to_level}")
    delay(3)
    return hero  # Retorna o herói modificado

    
    """Executa ataque com delays narrativos e remove inimigos derrotados"""
    if hero.weapon:
        print(f"{hero.name} usa {hero.weapon.name}!", flush=True)
        delay(1)
        attack_results = hero.weapon.attack(target=target)
        
        for result in attack_results:
            if len(result) >= 2:
                target, damage = result[0], result[1]
                if damage > 0:
                    print("*SWOOSH* ", end="", flush=True)
                    delay(1)
                    print(f"Causando {damage} de dano!", flush=True)
                    delay(1)
                    target.take_damage(damage)
                    
                    if target.hp <= 0:
                        print("*CRITICAL* ", end="", flush=True)
                        delay(1)
                        print(f"{target.name} foi nocauteado!", flush=True)
                        delay(1)
                        enemies.remove(target)  # Remove o inimigo derrotado
                        return True
    else:
        print(f"{hero.name} ataca com os punhos!", flush=True)
        delay(1)
        damage = max(1, hero.attack - target.defense)
        print("*POW* ", end="", flush=True)
        delay(1)
        print(f"Causando {damage} de dano!", flush=True)
        target.take_damage(damage)
        delay(1)
        
        if target.hp <= 0:
            print(f"{target.name} cai desmaiado!", flush=True)
            delay(1)
            enemies.remove(target)  # Remove o inimigo derrotado
            return True
    return False