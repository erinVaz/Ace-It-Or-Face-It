import random

# ------------------ Card ------------------

class Card:
    def __init__(self, rank=None, suit=None, is_joker=False):
        self.rank = rank
        self.suit = suit
        self.is_joker = is_joker

    def category(self):
        if self.is_joker:
            return "JOKER"
        if self.rank == "Ace":
            return "Ace"
        if self.rank in ["Jack", "Queen", "King"]:
            return "Face"
        return "Number"

    def __str__(self):
        if self.is_joker:
            return "JOKER"
        return f"{self.rank} of {self.suit}"


# ------------------ Deck ------------------

class Deck:
    def __init__(self):
        self.cards = []
        self._build()
        self.shuffle()

    def _build(self):
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        ranks = ["Ace"] + [str(n) for n in range(2, 11)] + ["Jack", "Queen", "King"]

        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(rank, suit))

        # Add 2 Jokers
        self.cards.append(Card(is_joker=True))
        self.cards.append(Card(is_joker=True))

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        if self.cards:
            return self.cards.pop()
        return None

    def remaining(self):
        return len(self.cards)


# ------------------ Game Stats ------------------

class GameStats:
    def __init__(self):
        self.high_score = 0
        self.total_score = 0
        self.games_played = 0

    def record_game(self, score):
        self.games_played += 1
        self.total_score += score
        self.high_score = max(self.high_score, score)

    def average_score(self):
        if self.games_played == 0:
            return 0
        return self.total_score / self.games_played


# ------------------ Game ------------------

class AceOrFaceGame:
    SAFE_POINTS = 10
    RISK_POINTS = 30
    JOKER_BONUS = 5

    def __init__(self, stats):
        self.deck = Deck()
        self.score = 0
        self.stats = stats
        self.lives = self.choose_difficulty()

    def choose_difficulty(self):
        chosen= True

        mode_map={
            "1": 3,
            "2": 2,
            "3": 1
        } 
        #dictionary used here to map user input to lives. better than a bunch of if statements.
        while chosen:
            print("1 - Easy (3 lives)")
            print("2 - Normal (2 lives)")
            print("3 - Hard (1 life)")
            choice = input(" Choose difficulty: > ")
            if choice in mode_map:
                chosen = False
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
                continue

        return mode_map[choice]



    def probability_hint(self):
        total = self.deck.remaining()
        if total == 0:
            return

        aces = sum(1 for c in self.deck.cards if c.rank == "Ace")
        faces = sum(1 for c in self.deck.cards if c.rank in ["Jack", "Queen", "King"])
        numbers = sum(1 for c in self.deck.cards if c.rank and c.rank.isdigit())

        print(f"Probability hint -> Ace: {aces/total:.0%}, "
              f"Face: {faces/total:.0%}, Number: {numbers/total:.0%}")

    def play_round(self):
        print("\n")
        chose_mode = True
        while chose_mode == True:
            print("1 - Safe Mode (Ace / Face / Number)")
            print("2 - Risk Mode (Exact rank)")
            mode = input("Choose mode: > ")

            if mode == "1":
                guess = input("Predict category (Ace / Face / Number): ").capitalize()
                chose_mode = False
            elif mode == "2":
                guess = input("Predict exact rank (e.g. Ace, 7, Queen): ").capitalize()
                chose_mode = False
            else:
                print("Invalid mode selected. Try again.")
            
        card = self.deck.draw()

        if not card:
            return False

        print(f"Drawn card: {card}")

        # Joker logic
        if card.is_joker:
            if random.choice([True, False]):
                self.score += self.JOKER_BONUS
                print(f"Joker bonus! +{self.JOKER_BONUS} points")
            else:
                print("Joker did nothing.")
            return True

        # Check guess
        correct = False
        if mode == "1":
            correct = guess == card.category()
            if correct:
                self.score += self.SAFE_POINTS
        else:
            correct = guess == card.rank
            if correct:
                self.score += self.RISK_POINTS

        if correct:
            print("Correct guess!")
        else:
            self.lives -= 1
            print("Wrong guess! Lost 1 life.")

        return correct or self.lives > 0

    def play(self):
        print("\n=== Ace or Face ===")

        while self.lives > 0 and self.deck.remaining() > 0:
            print(f"\nScore: {self.score} | Lives: {self.lives} | Cards left: {self.deck.remaining()}")
            self.probability_hint()

            if not self.play_round():
                break

        print("\n=== Game Over ===")
        print(f"Final Score: {self.score}")

        self.stats.record_game(self.score)
        print(f"High Score: {self.stats.high_score}")
        print(f"Average Score: {self.stats.average_score():.2f}")


# ------------------ Main ------------------

def main():
    stats = GameStats()

    while True:
        game = AceOrFaceGame(stats)
        game.play()
        correct= True

        while correct:
            again = input("\nPlay again? (y/n): ").lower()
            
            if again == "y":
                correct= False
            elif again == "n":
                print("Thanks for playing!")
                return  # exit program completely

            else:
                print("Invalid input. Please enter 'y' or 'n'.")
                
         


if __name__ == "__main__":
    main()
