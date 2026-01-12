# ACE IT OR FACE IT 

Ace it or face it is a simple card guessing game where a player guesses if a randomly drawn card is an ace, face or number card. They're are scored based on how rare the card is. It has been designed to show:
- Clean object-oriented modelling
- Probability-driven game mechanics
- Risk vs reward balancing
- Extensible architecture
The project is deliberately small-scale, readable, and easy to extend to showcase solid engineering fundamentals.
This project includes two implementations of the same core game: a CLI version and GUI version. This is explained later

## Why make this game?

I chose to make this simple probability-based game so that the game mechanics were simplified and I could focus on clean deck modelling. This means that is very buildable to add extensions to make it more complex and build it up over time, making it more viable with given personal time constraints. 

Other options such as Beat the Dealer were more interesting in terms of gamers decision-making and state management. The hand management of beating a given target is very familiar and also feels closer to a real-world game but my focus was the design of the game rather than the game itself.

_Overall, I chose Ace or Face because it highlights probability-based decision-making rather than hand optimization. I'd like to focus on architecture_

The "ace it or face it" game deals with :
- Odds: how likely a card it to appear is really important to how the game works

- Expected Value: the reward for guessing is scaled with difficulty to do so- game balance is itentionaly not just random

- Risk Design: this is at the base of every card game and I wanted to demonstrate that in this very simple game. Risky behaviour can be tempted through rules and rewards. Giving players meaningful choices tempts the risky but rewarding consequences. If every guess gave +1 point regardless of difficulty, there's no risk design, choices are equal and the game becoems trivial

These 3 points are the foundation of Casino games, Strategy games and Economic simulations. The game is intentionally designed around probability and risk, encouraging the player to balance safe, high-probability choices against low-probability, high-reward decisions.

### Why are there 2 versions?
The CLI and GUI Versions serve 2 different purposes:

### `CLI Version`
The command-line version focuses on:
- Clean modelling of cards and decks
- Rule enforcement and probability mechanics
- Statistics tracking and difficulty modes
This version demonstrates precise game logic and architecture.

### `GUI Version (Tkinter)`
The GUI version builds on the same game design but excludes the feature of the joker due to time constraints:
- Interactive buttons for difficulty and prediction modes
- Visual card reveal using card images
- Dynamic probability hints
- Game-over popups and restart flow
This version demonstrates user interface design and event-driven programming.

# Gameplay Rules
## How to Play
1. The deck is shuffled at the start of the game. 

2. The playet selects a difficulty level:
    - Easy: 3 lives
    - Medium: 2 lives
    - Hard: 1 life
3. Before each draw, the player chooses a prediction:
    -  Safe Mode: Predict the card category (Ace, Face, or Number) 
    -  Risk Mode: Predict the exact rank (e.g. Queen, 7, Ace)

3. A card is drawn from the deck.
4. Correct guesses increase the player’s score:
    - Safe Mode scores 10 points
    - Risk Mode scores 30 points
5. An incorrect guess ends the game/ loses a life.
6. The game also ends when the deck is empty (all cards have been guessed)

## Scoring
Safe Mode correct guess: +10 point
Risk Mode correct guess: +30 points
Any incorrect guess: Takes away a life

## Special features
- The are 3 difficulty modes that a player can choose
- There are 2 joker in the deck and can either do nothing or award 5 bonus points.
- Track current score, high score and average score

# Architecture 
This project models many aspects of the game using OOP (object-oriented programming). This organises the different systems into self-contained and reusable objects that can make the project much more scalable. Key features of OOP can be seen here such as encapsulation, polymorphism and inheritance. The classes are:

### `Card`
Represents a single card in the deck.Stores rank, suit, and whether the card is a Joker.Provides a category() helper to classify the card.

### `Deck`
Builds a standard 52-card deck and adds two Jokers.Handles shuffling and dealing cards.Maintains deck state throughout the game.

### `GameStats`
Tracks:
- High score
- Total score
- Games played
- Average score
This logic is separated from gameplay to keep responsibilities clean.

### `AceOrFaceGame`
Implements the full game loop:
- Difficulty selection
- Mode selection
- Guess validation
- Scoring
- Life tracking
- Joker behaviour
- Probability hints

# How to Run
No external dependencies are needed and the main requirement is Python 3.8+
this runs the CLI version: 
```
python mainGame.py
```
this runs the GUI version: 
```
python GUIgame.py
```

# Further Improvements
Here are some ways I could improve the application given more time:
- GUI can be upgraded to a web application form such as Flask so that it is more accessible.
    - in this case extra features can be added such as a database server backend that can hold data from multiple users to create a global scoreboard of multiple users.
- Add the joker functionality to the GUI
- Additional game modes
- Difficulty scaling over time
- User profiles
- Global scoreboard

# License & Credits
Playing card art (for future GUI implementation):
https://opengameart.org/content/playing-cards-pack
