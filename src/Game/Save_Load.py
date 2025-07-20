import pickle

# Sistema de Save/Load
def save_game(hero):
    with open('save.dat', 'wb') as f:
        pickle.dump(hero, f)

def load_game():
    try:
        with open('save.dat', 'rb') as f:
            return pickle.load(f)
    except:
        return None
