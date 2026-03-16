# The Trailblazers

The Trailblazers is a terminal-based, turn-based battle game written in Python. You build a three-character team, fight against an AI squad, earn coins from combat, recruit new teammates, and keep progressing through new enemy teams.

The game runs entirely in the console and uses only Python's standard library, so there are no external dependencies to install.

## Features

- Create a custom starting team with three characters.
- Choose between two classes: `Warrior` and `Tanker`.
- Fight AI-controlled enemy teams in manual or auto-battle mode.
- Earn coins based on damage dealt.
- Recruit additional teammates for `50` coins each.
- Gain EXP, level up, and increase your stats over time.
- Save and load progress with a JSON save file.
- Track events in a timestamped game log.

## Requirements

- Python 3

## How to Run

From the project folder, run:

```bash
python3 TheTrialblazersLauncher.py
```

## Main Menu

When the game starts, you can choose to:

1. Start a new adventure
2. Load from a save file
3. Exit the game

If you start a new adventure, you will create three characters by entering:

- A name
- A profession: `Warrior` or `Tanker`

## Classes

Each class has different stat ranges when a character is created:

- `Warrior`: higher attack, lower defense
- `Tanker`: lower attack, higher defense

All characters start with:

- `100` HP
- `0` EXP
- `Rank 1`

## Adventure Menu

During the game, the adventure menu lets you:

1. Start a battle
2. Recruit new teammate(s)
3. Save the game
4. Exit
5. Start auto-battle

Choosing `Exit` from the adventure menu saves the game before closing.

## Gameplay

- Battles are turn-based.
- Your living characters act first each round.
- The AI team attacks after your team.
- In manual mode, you choose which enemy each character attacks.
- In auto-battle mode, targets are selected automatically.
- Damage depends on attack, defense, and a small random modifier.
- Winning a battle rewards surviving player characters with bonus EXP.

## Progression

- Characters gain EXP when they participate in combat.
- Every `100` EXP increases a character's rank.
- Ranking up restores the character to full health and increases stats.
- Each rank-up gives `+20` max HP and `+5` attack.

## Recruiting

- New teammates cost `50` coins each.
- Coins are earned from damage dealt in battle.
- Recruited teammates are added to your team immediately.

## Save and Log Files

The game creates these files in the project directory:

- `save_game.json`: stores the current player team and enemy team
- `game_log.txt`: records major game events with timestamps

If loading fails because the save file is missing or invalid, the game automatically starts a new adventure.

## Project File

The main launcher for the game is:

- `TheTrialblazersLauncher.py`

## Notes

- This project is designed for the command line and expects keyboard input.
- The game uses random stat generation, so each run will feel a little different.
