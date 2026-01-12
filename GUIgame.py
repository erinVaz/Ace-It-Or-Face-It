# Ace It or Face It (Tkinter GUI)
from tkinter import *
from tkinter import messagebox
import random
from PIL import Image, ImageTk
import os

# ----------------------------
# Config
# ----------------------------
WINDOW_W, WINDOW_H = 900, 520
BG = "green"
CARDS_DIR = "cards"
CARD_BACK_PATH = os.path.join(CARDS_DIR, "card_back.png")

SAFE_POINTS = 10
RISK_POINTS = 30

DIFFICULTY_LIVES = {
    "Easy": 3,
    "Medium": 2,
    "Hard": 1,
}

SUITS = ["diamonds", "clubs", "hearts", "spades"]
VALUES = list(range(2, 15))  # 11=J,12=Q,13=K,14=Ace


def value_to_rank(value: int) -> str:
    if value == 14:
        return "Ace"
    if value == 13:
        return "King"
    if value == 12:
        return "Queen"
    if value == 11:
        return "Jack"
    return str(value)


def category_from_value(value: int) -> str:
    if value == 14:
        return "Ace"
    if value in (11, 12, 13):
        return "Face"
    return "Number"


def resize_image(path: str, target_height: int = 230) -> ImageTk.PhotoImage:
    img = Image.open(path)
    w, h = img.size
    scale = target_height / h
    new_w = int(w * scale)
    img = img.resize((new_w, target_height), Image.LANCZOS)
    return ImageTk.PhotoImage(img)



class Deck:
    """Deck of cards"""
    def __init__(self):
        self.cards = []
        self.reset()

    def reset(self):
        self.cards = [("card", suit, value) for suit in SUITS for value in VALUES]
        random.shuffle(self.cards)

    def draw(self):
        if not self.cards:
            return None
        return self.cards.pop()

    def remaining(self):
        return len(self.cards)

    def counts_for_hint(self):
        """Dynamic probabilities based on remaining deck; excludes jokers from category counts."""
        total = len(self.cards)
        if total == 0:
            return (0, 0, 0, 0)

        aces = 0
        faces = 0
        numbers = 0
       
        for _, _, v in self.cards:
            cat = category_from_value(v)
            if cat == "Ace":
                aces += 1
            elif cat == "Face":
                faces += 1
            else:
                numbers += 1

        return (aces, faces, numbers)


# the APPLICATION CLASS
class AceOrFaceApp:
    def __init__(self, root: Tk):
        self.root = root
        self.root.title("Ace it or Face it - Card Game")
        self.root.geometry(f"{WINDOW_W}x{WINDOW_H}")
        self.root.configure(background=BG)

        # Game state
        self.deck = Deck()
        self.difficulty = None
        self.lives = 0
        self.score = 0
        self.high_score = 0
        self.games_played = 0
        self.total_score = 0

        self.current_mode = None   # "safe" or "risk"
        self.pending_guess = None  # category string OR rank string

        # Image cache
        self.img_cache = {}
        self.card_back_img = None
        self.current_card_img = None  # keep reference

        self._load_static_images()

        # Frames
        self.start_frame = Frame(self.root, bg=BG)
        self.game_frame = Frame(self.root, bg=BG)

        self._build_start_screen()
        self._build_game_screen()

        self.show_start_screen()

    # ---------- Screens ----------
    def show_start_screen(self):
        self.game_frame.pack_forget()
        self.start_frame.pack(fill="both", expand=True)

    def show_game_screen(self):
        self.start_frame.pack_forget()
        self.game_frame.pack(fill="both", expand=True)

    # ---------- UI Build ----------
    def _build_start_screen(self):
        Label(
            self.start_frame,
            text="Select Difficulty",
            bg=BG,
            fg="white",
            font=("Helvetica", 20, "bold"),
        ).pack(pady=25)

        btn_row = Frame(self.start_frame, bg=BG)
        btn_row.pack(pady=10)

        for name in ["Easy", "Medium", "Hard"]:
            Button(
                btn_row,
                text=f"{name} ({DIFFICULTY_LIVES[name]} lives)",
                font=("Helvetica", 14),
                width=18,
                command=lambda n=name: self.start_game(n)
            ).pack(side=LEFT, padx=10)

        Label(
            self.start_frame,
            text="Tip: Safe Mode is easier (+10). Risk Mode pays more (+30).",
            bg=BG,
            fg="white",
            font=("Helvetica", 12),
        ).pack(pady=20)

    def _build_game_screen(self):
        # Top status bar
        top = Frame(self.game_frame, bg=BG)
        top.pack(fill="x", pady=(10, 0))

        self.difficulty_label = Label(top, text="", bg=BG, fg="white", font=("Helvetica", 12, "bold"))
        self.difficulty_label.pack(side=LEFT, padx=10)

        self.score_label = Label(top, text="Score: 0", bg=BG, fg="white", font=("Helvetica", 12, "bold"))
        self.score_label.pack(side=LEFT, padx=10)

        self.lives_label = Label(top, text="Lives: 0", bg=BG, fg="white", font=("Helvetica", 12, "bold"))
        self.lives_label.pack(side=LEFT, padx=10)

        self.deck_label = Label(top, text="Cards left: 0", bg=BG, fg="white", font=("Helvetica", 12, "bold"))
        self.deck_label.pack(side=LEFT, padx=10)

        self.stats_label = Label(top, text="High: 0 | Avg: 0.00", bg=BG, fg="white", font=("Helvetica", 12))
        self.stats_label.pack(side=RIGHT, padx=10)

        # Main content
        main = Frame(self.game_frame, bg=BG)
        main.pack(fill="both", expand=True, pady=10)

        # Card pile (single pile)
        pile = Frame(main, bg=BG)
        pile.pack(pady=10)

        self.card_label = Label(pile, image=self.card_back_img, bg=BG)
        self.card_label.pack()

        self.reveal_text = Label(main, text="", bg=BG, fg="white", font=("Helvetica", 14, "bold"))
        self.reveal_text.pack(pady=(10, 0))

        self.hint_label = Label(main, text="", bg=BG, fg="white", font=("Helvetica", 11))
        self.hint_label.pack(pady=(6, 10))

        # Interaction area
        self.controls = Frame(main, bg=BG)
        self.controls.pack(pady=10)

        self.mode_frame = Frame(self.controls, bg=BG)
        self.choice_frame = Frame(self.controls, bg=BG)
        self.risk_frame = Frame(self.controls, bg=BG)

        # Mode buttons (Safe/Risk)
        self.safe_btn = Button(
            self.mode_frame, text="Safe Mode", font=("Helvetica", 14),
            width=14, command=self.choose_safe_mode
        )
        self.risk_btn = Button(
            self.mode_frame, text="Risk Mode", font=("Helvetica", 14),
            width=14, command=self.choose_risk_mode
        )
        self.safe_btn.pack(side=LEFT, padx=10)
        self.risk_btn.pack(side=LEFT, padx=10)

        # Safe choices
        self.ace_btn = Button(self.choice_frame, text="Ace", font=("Helvetica", 14), width=10,
                              command=lambda: self.submit_safe_guess("Ace"))
        self.face_btn = Button(self.choice_frame, text="Face", font=("Helvetica", 14), width=10,
                               command=lambda: self.submit_safe_guess("Face"))
        self.num_btn = Button(self.choice_frame, text="Number", font=("Helvetica", 14), width=10,
                              command=lambda: self.submit_safe_guess("Number"))

        # Risk input
        self.risk_entry = Entry(self.risk_frame, font=("Helvetica", 14), width=18)
        self.risk_submit_btn = Button(self.risk_frame, text="Submit", font=("Helvetica", 14),
                                      command=self.submit_risk_guess)

        # Start in mode selection state
        self.mode_frame.pack(pady=10)

    # ---------- Image Loading ----------
    def _load_static_images(self):
        if not os.path.exists(CARD_BACK_PATH):
            messagebox.showerror("Missing Asset", f"Could not find {CARD_BACK_PATH}")
            self.root.destroy()
            return

        self.card_back_img = resize_image(CARD_BACK_PATH, target_height=230)

        # if os.path.exists(JOKER_IMAGE_PATH):
        #     self.img_cache["joker"] = resize_image(JOKER_IMAGE_PATH, target_height=230)

    def _get_card_face_image(self, suit: str, value: int):
        key = f"{suit}_{value}"
        if key in self.img_cache:
            return self.img_cache[key]

        path = os.path.join(CARDS_DIR, f"card_{suit}_{value}.png")
        if not os.path.exists(path):
            return None

        self.img_cache[key] = resize_image(path, target_height=230)
        return self.img_cache[key]

    # ---------- Game Flow ----------
    def start_game(self, difficulty_name: str):
        # Initialize game state
        self.difficulty = difficulty_name
        self.lives = DIFFICULTY_LIVES[difficulty_name]
        self.score = 0
        self.current_mode = None
        self.pending_guess = None

        self.deck.reset()

        # Update UI
        self.difficulty_label.config(text=f"Difficulty: {self.difficulty}")
        self._update_status_labels()
        self._update_probability_hint()

        self._reset_round_ui()

        self.show_game_screen()

    def _reset_round_ui(self):
        """Prepare for next prediction: show facedown card + mode buttons; hide other inputs."""
        self.card_label.config(image=self.card_back_img)
        self.current_card_img = self.card_back_img  # keep ref
        self.reveal_text.config(text="")

        # Clear/hide frames
        self.choice_frame.pack_forget()
        self.risk_frame.pack_forget()

        # Reset mode frame
        self.safe_btn.config(state=NORMAL)
        self.risk_btn.config(state=NORMAL)
        self.mode_frame.pack_forget()
        self.mode_frame.pack(pady=10)

        self.current_mode = None
        self.pending_guess = None

        self.risk_entry.delete(0, END)

    def choose_safe_mode(self):
        self.current_mode = "safe"
        # Hide mode frame (disappears) and show 3 choice buttons
        self.mode_frame.pack_forget()

        # Ensure buttons are packed once
        for w in self.choice_frame.winfo_children():
            w.pack_forget()

        self.ace_btn.pack(side=LEFT, padx=8)
        self.face_btn.pack(side=LEFT, padx=8)
        self.num_btn.pack(side=LEFT, padx=8)
        self.choice_frame.pack(pady=10)

    def choose_risk_mode(self):
        self.current_mode = "risk"
        # Hide mode frame (disappears) and show entry + submit
        self.mode_frame.pack_forget()

        self.risk_entry.pack(side=LEFT, padx=8)
        self.risk_submit_btn.pack(side=LEFT, padx=8)
        self.risk_frame.pack(pady=10)
        self.risk_entry.focus_set()

    def submit_safe_guess(self, category: str):
        # Hide choice buttons after selection
        self.choice_frame.pack_forget()
        self.pending_guess = category
        self._resolve_draw_and_score()

    def submit_risk_guess(self):
        guess = self.risk_entry.get().strip()
        if not guess:
            messagebox.showwarning("Missing Guess", "Enter a rank (e.g., Ace, 7, Queen).")
            return

        # Normalize guess
        guess_norm = guess.capitalize()
        self.pending_guess = guess_norm

        # Hide entry + submit after submission
        self.risk_frame.pack_forget()
        self._resolve_draw_and_score()

    def _resolve_draw_and_score(self):
        """Draw a card, reveal it, apply scoring/life rules, then either continue or game over."""
        card = self.deck.draw()
        if card is None:
            self._game_over(reason="Deck is empty!")
            return

        ctype, suit, value = card

        img = self._get_card_face_image(suit, value)
        if img:
            self.card_label.config(image=img)
            self.current_card_img = img
        else:
            # If image missing, at least show text
            self.card_label.config(image=self.card_back_img)
            self.current_card_img = self.card_back_img

        rank = value_to_rank(value)
        category = category_from_value(value)
        self.reveal_text.config(text=f"Revealed: {rank} of {suit.capitalize()} ({category})")

        # Score / lives based on mode and guess
        correct = False
        if self.current_mode == "safe":
            correct = (self.pending_guess == category)
            if correct:
                self.score += SAFE_POINTS
        elif self.current_mode == "risk":
            correct = (self.pending_guess == rank)
            if correct:
                self.score += RISK_POINTS

        if correct:
            # Continue
            pass
        else:
            self.lives -= 1

        self._update_status_labels()
        self._update_probability_hint()

        self._after_turn_check_end(correct=correct)

    def _after_turn_check_end(self, correct=True):
        if self.lives <= 0:
            self._game_over(reason="No lives left!")
            return
        if self.deck.remaining() <= 0:
            self._game_over(reason="Deck is empty!")
            return

        # Prepare next round after a short beat (optional) — but keep it instant for reliability
        self.root.after(1500, self._reset_round_ui)

    def _game_over(self, reason: str):
        # Update session stats
        self.games_played += 1
        self.total_score += self.score
        if self.score > self.high_score:
            self.high_score = self.score

        self._update_status_labels()

        avg = self.total_score / self.games_played if self.games_played else 0
        msg = f"{reason}\n\nFinal Score: {self.score}\nHigh Score: {self.high_score}\nAverage Score: {avg:.2f}\n\nPlay again?"
        play_again = messagebox.askyesno("Game Over", msg)

        if play_again:
            # Go back to difficulty selection
            self.show_start_screen()
        else:
            self.root.destroy()

    def _update_status_labels(self):
        self.score_label.config(text=f"Score: {self.score}")
        self.lives_label.config(text=f"Lives: {self.lives}")
        self.deck_label.config(text=f"Cards left: {self.deck.remaining()}")

        avg = self.total_score / self.games_played if self.games_played else 0
        self.stats_label.config(text=f"High: {self.high_score} | Avg: {avg:.2f}")

    def _update_probability_hint(self):
        total = self.deck.remaining()
        if total <= 0:
            self.hint_label.config(text="")
            return

        aces, faces, numbers = self.deck.counts_for_hint()
        # Show hints for gameplay categories; also mention jokers briefly
        hint = (
            f"Probability hint (remaining deck): "
            f"Ace {aces/total:.0%} | Face {faces/total:.0%} | Number {numbers/total:.0%} "
        )
        self.hint_label.config(text=hint)

if __name__ == "__main__":
    root = Tk()
    app = AceOrFaceApp(root)
    root.mainloop()
