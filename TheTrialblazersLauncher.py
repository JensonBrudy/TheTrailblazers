import datetime, json, random

SAVE_FILE, LOG_FILE = "save_game.json", "game_log.txt"
PROFESSION_STATS = {"Warrior": {"atk": (5, 20), "defense": (1, 10)}, "Tanker": {"atk": (1, 10), "defense": (5, 15)}}

def log_event(message):
    with open(LOG_FILE, "a", encoding="utf-8") as file: file.write(f"[{datetime.datetime.now():%Y-%m-%d %H:%M:%S}] {message}\n")

def prompt_non_empty(prompt):
    while not (value := input(prompt).strip()): print("Input cannot be empty.")
    return value

def prompt_profession(prompt):
    while (profession := input(prompt).strip().title()) not in PROFESSION_STATS: print("Invalid profession. Please enter 'Warrior' or 'Tanker'.")
    return profession

def prompt_index(prompt, upper_bound):
    while True:
        selection = input(prompt).strip()
        if selection.isdigit() and 0 <= (index := int(selection) - 1) < upper_bound: return index
        print(f"Invalid input. Please enter a number from 1 to {upper_bound}.")

class Character:
    def __init__(self, name, profession):
        profession = profession.title()
        if profession not in PROFESSION_STATS: raise ValueError(f"Invalid profession: {profession}")
        self.name, self.profession, self.max_hp, self.hp, self.exp, self.rank = name, profession, 100, 100, 0, 1
        stats = PROFESSION_STATS[profession]
        self.atk, self.defense = random.randint(*stats["atk"]), random.randint(*stats["defense"])

    def display_info(self): print(f"{self.name} ({self.profession})  HP: {self.hp}, ATK: {self.atk}, DEF: {self.defense}, EXP: {self.exp}, Rank: {self.rank}")
    def short_status(self): return f"{self.name}(HP={self.hp})"
    def is_defeated(self): return self.hp <= 0
    def heal_full(self): self.hp = self.max_hp

    def take_damage(self, damage):
        self.hp = max(0, self.hp - damage)
        print(f"\n{self.name} takes {damage} damage! Remaining HP: {self.hp}")

    def gain_exp(self, amount):
        if amount <= 0: return
        self.exp += amount
        while self.exp >= 100:
            self.exp -= 100
            self.rank += 1
            self.rank_up()

    def rank_up(self):
        self.max_hp += 20
        self.atk += 5
        self.hp = self.max_hp
        print(f"{self.name} leveled up to Rank {self.rank}! HP: {self.max_hp}, ATK: {self.atk}")
        log_event(f"{self.name} leveled up. New rank={self.rank}")

    def attack_target(self, target):
        raw_damage = self.atk - target.defense + random.randint(-5, 10)
        damage = max(raw_damage, 0)
        target.take_damage(damage)
        self.gain_exp(damage)
        target.gain_exp(target.defense)
        if raw_damage > 10: target.gain_exp(int(0.2 * target.defense))
        elif raw_damage <= 0: target.gain_exp(int(0.5 * target.defense))
        return damage

    def to_dict(self): return self.__dict__.copy()

    @staticmethod
    def from_dict(data):
        character = Character(data["name"], data["profession"])
        character.__dict__.update(data)
        return character

class Team:
    def __init__(self):
        self.units, self.coins = [], 100

    def add_unit(self, unit): self.units.append(unit)
    def alive_units(self): return [unit for unit in self.units if not unit.is_defeated()]
    def is_defeated(self): return not self.alive_units()
    def heal_all(self): [unit.heal_full() for unit in self.units]

    def display_team(self):
        for unit in self.units: unit.display_info()
        print(f"Coins: {self.coins}")

    def status_snapshot(self): return ", ".join(unit.short_status() for unit in self.units)

    def recruit_unit(self):
        if self.coins < 50:
            print("You Do Not Have Enough Coins to Recruit a New Unit!")
            log_event(f"Failed to recruit new unit: insufficient coins ({self.coins})")
            return False
        name = prompt_non_empty("\nEnter Name for the New Character: ")
        profession = prompt_profession("Choose a Profession for the New Character (Warrior/Tanker): ")
        unit = Character(name, profession)
        self.add_unit(unit)
        self.coins -= 50
        print(f"{name} Has Been Recruited! Remaining Coins: {self.coins}")
        log_event(f"Recruited {unit.name} ({unit.profession}); HP={unit.max_hp}, ATK={unit.atk}, DEF={unit.defense}; Coins Remaining={self.coins}")
        return True

    def to_dict(self): return {"units": [unit.to_dict() for unit in self.units], "coins": self.coins}

    @staticmethod
    def from_dict(data):
        team = Team()
        team.units = [Character.from_dict(unit) for unit in data.get("units", [])]
        team.coins = data.get("coins", 100)
        return team

def setup_player_team():
    team = Team()
    log_event("Player is forming their team")
    for index in range(3):
        unit = Character(prompt_non_empty(f"\nPlease Enter Character {index + 1}'s Name: "), prompt_profession(f"Choose a Profession for Character {index + 1} (Warrior or Tanker): "))
        team.add_unit(unit)
        log_event(f"Recruited {unit.name} ({unit.profession}); stats=HP{unit.max_hp}/ATK{unit.atk}/DEF{unit.defense}")
    print("\nYour Team is Ready to Start an Exciting Adventure Now!")
    return team

def setup_ai_team():
    team = Team()
    log_event("Initializing AI Team")
    for _ in range(3):
        unit = Character(f"AI{random.randint(10, 99)}", random.choice(list(PROFESSION_STATS)))
        team.add_unit(unit)
        log_event(f"AI Recruited {unit.name} ({unit.profession}); HP={unit.max_hp}, ATK={unit.atk}, DEF={unit.defense}")
    log_event("AI Team Setup Complete")
    return team

def show_team_status(team, label):
    print(f"\n--- {label} Status ---")
    for member in team.units: print(f"{member.name}: DEFEATED" if member.is_defeated() else f"{member.name}: HP: {member.hp}, ATK: {member.atk}, DEF: {member.defense}, Rank: {member.rank}")

def show_matchup(player_team, ai_team):
    print("\n=== Team Status ===")
    for label, team in (("Your Team", player_team), ("Enemy Team", ai_team)):
        print(f"\n--- {label} ---")
        team.display_team()

def log_team_info(team, team_name):
    log_event(f"--- {team_name} Info ---")
    for unit in team.units: log_event(f"{unit.name} ({unit.profession}) - HP: {unit.hp}, ATK: {unit.atk}, DEF: {unit.defense}, EXP: {unit.exp}, Rank: {unit.rank}")
    log_event(f"Coins: {team.coins}")

def announce_victory(player_team):
    print("\nAll enemies defeated! You win!")
    for player in player_team.alive_units(): player.gain_exp(50)
    log_event("PLAYER VICTORY")
    return "victory"

def announce_defeat():
    print("\nAll Your Units are Down. Game Over.")
    log_event("PLAYER DEFEATED")
    return "defeat"

def resolve_attack(attacker, target, attacking_team, team_name):
    damage = attacker.attack_target(target)
    attacking_team.coins += damage
    print(f"{attacker.name} dealt {damage} damage to {target.name} for +{damage} coins! (Total: {attacking_team.coins})")
    log_event(f"{team_name}: {attacker.name} attacked {target.name} for {damage} damage; coins={attacking_team.coins}")

def choose_player_target(player, enemy_team):
    alive = enemy_team.alive_units()
    print(f"\n--- It's {player.name}'s Turn. Choose a Target to Attack ---")
    for index, enemy in enumerate(alive, 1): print(f"  {index}. {enemy.name} (HP: {enemy.hp}, DEF: {enemy.defense})")
    target = alive[prompt_index(f"\nEnter Target Number (1-{len(alive)}): ", len(alive))]
    input(f"\n{player.name} prepares to attack {target.name}. Press [Enter] to confirm attack.")
    return target

def run_player_phase(player_team, enemy_team, auto_mode):
    for player in player_team.alive_units():
        if enemy_team.is_defeated(): return announce_victory(player_team)
        target = random.choice(enemy_team.alive_units()) if auto_mode else choose_player_target(player, enemy_team)
        if auto_mode: print(f"\n{player.name} automatically attacks {target.name}")
        resolve_attack(player, target, player_team, "Player")
    return announce_victory(player_team) if enemy_team.is_defeated() else None

def run_enemy_phase(player_team, enemy_team):
    for enemy in enemy_team.alive_units():
        if player_team.is_defeated(): return announce_defeat()
        target = random.choice(player_team.alive_units())
        print(f"\n--- Enemy {enemy.name}'s Turn. Attacking {target.name} ---")
        resolve_attack(enemy, target, enemy_team, "Enemy")
    return announce_defeat() if player_team.is_defeated() else None

def log_round_summary(round_number, player_team, enemy_team):
    log_event(f"End of Round {round_number} Status -> Player [{player_team.status_snapshot()}] (Coins={player_team.coins}); Enemy [{enemy_team.status_snapshot()}] (Coins={enemy_team.coins})")

def run_battle(player_team, enemy_team, auto_mode=False):
    round_number = 1
    while True:
        if enemy_team.is_defeated(): return announce_victory(player_team)
        if player_team.is_defeated(): return announce_defeat()
        label = "Auto Round" if auto_mode else "Round"
        print(f"\n========== {label} {round_number} ==========")
        log_event(f"{label} {round_number} started")
        show_team_status(player_team, "Player Team")
        show_team_status(enemy_team, "Enemy Team")
        if (result := run_player_phase(player_team, enemy_team, auto_mode)) is not None: return result
        if (result := run_enemy_phase(player_team, enemy_team)) is not None: return result
        log_round_summary(round_number, player_team, enemy_team)
        round_number += 1

def battle_loop(player_team, enemy_team): return run_battle(player_team, enemy_team, False)
def auto_battle_loop(player_team, enemy_team): return run_battle(player_team, enemy_team, True)

def post_defeat_menu(player_team):
    while True:
        print("\n=== You Were Defeated ===\n1. Heal Team & Start Another Battle\n2. Assemble a New Team\n3. Quit")
        choice = input("Choose an option (1-3): ").strip()
        if choice == "1": player_team.heal_all(); return "retry"
        if choice == "2": return "new_team"
        if choice == "3": return "quit"
        print("Invalid choice. Please enter 1, 2, or 3.")

def save_game(player_team, ai_team):
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as file: json.dump({"saved_at": datetime.datetime.now().isoformat(timespec="seconds"), "player_team": player_team.to_dict(), "ai_team": ai_team.to_dict()}, file, indent=4)
    except OSError as error:
        print(f"Failed to save game: {error}")
        log_event(f"Save failed: {error}")
        return False
    print("Game Saved Successfully!")
    log_event("Game Saved")
    return True

def load_game():
    try:
        with open(SAVE_FILE, encoding="utf-8") as file: data = json.load(file)
        player_team, ai_team = Team.from_dict(data["player_team"]), Team.from_dict(data["ai_team"])
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        print("Save file could not be loaded. Starting a new game instead.")
        log_event(f"Load failed: {error}")
        return None, None
    print("Game Loaded Successfully!")
    log_event("Game Loaded")
    return player_team, ai_team

def recruit_units(team):
    recruited_any = False
    while team.coins >= 50:
        if input(f"\nCurrent Coins: {team.coins}\nRecruit a New Teammate For 50 Coins? (Enter Y to Recruit / Any Other Key to Stop): ").strip().lower() != "y": break
        recruited_any = team.recruit_unit() or recruited_any
    if team.coins < 50: print("\nYou Do Not Have Enough Coins (50 Required) to Recruit Another Teammate.")
    if recruited_any:
        print("\n=== Updated Team ===")
        team.display_team()
        log_team_info(team, "Player (Post-recruit)")
    print("Returning to the Adventure Menu...")

def create_new_game(): return setup_player_team(), setup_ai_team()

def prepare_game(start_from_save):
    if not start_from_save: return create_new_game()
    player_team, ai_team = load_game()
    if player_team is not None and ai_team is not None: return player_team, ai_team
    print("No valid save found. Starting New Game.")
    return create_new_game()

def handle_battle_outcome(result, player_team, ai_team):
    if result == "victory":
        print("\nA new enemy team is approaching!")
        return player_team, setup_ai_team(), False
    if result == "defeat":
        action = post_defeat_menu(player_team)
        if action == "retry": return player_team, setup_ai_team(), False
        if action == "new_team":
            player_team, ai_team = create_new_game()
            return player_team, ai_team, False
        print("Returning to title screen...\n")
        return player_team, ai_team, True
    return player_team, ai_team, False

def game_loop(start_from_save=False):
    player_team, ai_team = prepare_game(start_from_save)
    show_matchup(player_team, ai_team)
    while True:
        print("\n=== Adventure Menu ===\n1. Start the Battle\n2. Recruit New Teammate(s) (50 Coins each)\n3. Save Game\n4. Exit\n5. Autobattle")
        choice = input("\nPlease Enter your choice (1 to 5): ").strip()
        if choice in ("1", "5"):
            result = (battle_loop if choice == "1" else auto_battle_loop)(player_team, ai_team)
            player_team, ai_team, should_exit = handle_battle_outcome(result, player_team, ai_team)
            if should_exit: return
            show_matchup(player_team, ai_team)
        elif choice == "2": recruit_units(player_team)
        elif choice == "3": save_game(player_team, ai_team)
        elif choice == "4":
            save_game(player_team, ai_team)
            print("\nGame Auto-Saved. See You Again Soon!")
            return
        else: print("Invalid Choice. Please Enter an Option From 1 to 5.")

def main():
    while True:
        print("\n=== The TRAILBLAZERS ===\n1. New Adventure\n2. Load Adventure from Save File\n3. Exit Game")
        choice = input("\nPlease Enter an Option (1 to 3): ").strip()
        if choice == "1": game_loop(False)
        elif choice == "2": game_loop(True)
        elif choice == "3":
            print("Thanks for Playing! Goodbye.")
            break
        else: print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__": main()
