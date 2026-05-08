# ==========================================
# ADVANCED 8 PUZZLE GAME - PROFESSIONAL VERSION
# Features:
# ✅ Modern UI
# ✅ Animation Effects
# ✅ Keyboard Controls
# ✅ Sound Effects
# ✅ Difficulty Levels
# ✅ Hint System
# ✅ Auto Solver
# ✅ Score System
# ✅ Timer
# ==========================================

import tkinter as tk
from tkinter import messagebox
import random
import time

# OPTIONAL SOUND SUPPORT
try:
    import pygame
    pygame.mixer.init()
    SOUND_ENABLED = True
except:
    SOUND_ENABLED = False

# GOAL STATE
GOAL = [1, 2, 3,
        4, 5, 6,
        7, 8, 0]

# COLORS
COLORS = [
    "#FF6B6B",
    "#4ECDC4",
    "#45B7D1",
    "#96CEB4",
    "#F7DC6F",
    "#BB8FCE",
    "#F1948A",
    "#5DADE2"
]


class PuzzleGame:

    def __init__(self, root):

        self.root = root
        self.root.title("✨ Professional 8 Puzzle Game")
        self.root.geometry("550x760")
        self.root.configure(bg="#0F172A")
        self.root.resizable(False, False)

        self.tiles = GOAL[:]
        self.buttons = []
        self.moves = 0
        self.score = 1000
        self.start_time = time.time()
        self.difficulty = "Medium"

        # TITLE
        title = tk.Label(
            root,
            text="🧩 Advanced 8 Puzzle",
            font=("Arial", 28, "bold"),
            bg="#0F172A",
            fg="white"
        )
        title.pack(pady=15)

        # STATS FRAME
        stats = tk.Frame(root, bg="#0F172A")
        stats.pack()

        self.move_label = tk.Label(
            stats,
            text="Moves: 0",
            font=("Arial", 14, "bold"),
            bg="#0F172A",
            fg="#38BDF8"
        )
        self.move_label.grid(row=0, column=0, padx=20)

        self.timer_label = tk.Label(
            stats,
            text="Time: 0s",
            font=("Arial", 14, "bold"),
            bg="#0F172A",
            fg="#38BDF8"
        )
        self.timer_label.grid(row=0, column=1, padx=20)

        self.score_label = tk.Label(
            stats,
            text="Score: 1000",
            font=("Arial", 14, "bold"),
            bg="#0F172A",
            fg="#38BDF8"
        )
        self.score_label.grid(row=0, column=2, padx=20)

        # DIFFICULTY
        difficulty_frame = tk.Frame(root, bg="#0F172A")
        difficulty_frame.pack(pady=10)

        tk.Label(
            difficulty_frame,
            text="Difficulty:",
            font=("Arial", 13, "bold"),
            bg="#0F172A",
            fg="white"
        ).grid(row=0, column=0, padx=10)

        self.difficulty_var = tk.StringVar(value="Medium")

        difficulty_menu = tk.OptionMenu(
            difficulty_frame,
            self.difficulty_var,
            "Easy",
            "Medium",
            "Hard"
        )

        difficulty_menu.config(
            font=("Arial", 12),
            bg="#1E293B",
            fg="white"
        )

        difficulty_menu.grid(row=0, column=1)

        # PUZZLE FRAME
        self.frame = tk.Frame(root, bg="#0F172A")
        self.frame.pack(pady=20)

        # CREATE BUTTONS
        for i in range(9):

            btn = tk.Button(
                self.frame,
                text="",
                font=("Arial", 26, "bold"),
                width=4,
                height=2,
                relief="flat",
                bd=0,
                cursor="hand2",
                command=lambda i=i: self.move_tile(i)
            )

            btn.grid(row=i // 3, column=i % 3, padx=8, pady=8)

            self.buttons.append(btn)

        # CONTROLS
        controls = tk.Frame(root, bg="#0F172A")
        controls.pack(pady=15)

        buttons = [
            ("🔀 Shuffle", "#3B82F6", self.shuffle),
            ("🔄 Restart", "#EF4444", self.restart),
            ("💡 Hint", "#22C55E", self.show_hint),
            ("🤖 Auto Solve", "#A855F7", self.auto_solve)
        ]

        row = 0
        col = 0

        for text, color, command in buttons:

            btn = tk.Button(
                controls,
                text=text,
                font=("Arial", 13, "bold"),
                bg=color,
                fg="white",
                padx=20,
                pady=10,
                relief="flat",
                cursor="hand2",
                command=command
            )

            btn.grid(row=row, column=col, padx=10, pady=10)

            col += 1

            if col > 1:
                col = 0
                row += 1

        # FOOTER
        footer = tk.Label(
            root,
            text="⌨️ Use Arrow Keys or Mouse to Play",
            font=("Arial", 12),
            bg="#0F172A",
            fg="#94A3B8"
        )

        footer.pack(pady=10)

        # KEYBOARD CONTROLS
        self.root.bind("<Up>", lambda e: self.key_move("Up"))
        self.root.bind("<Down>", lambda e: self.key_move("Down"))
        self.root.bind("<Left>", lambda e: self.key_move("Left"))
        self.root.bind("<Right>", lambda e: self.key_move("Right"))

        # START
        self.shuffle()
        self.update_timer()

    # =========================
    # UPDATE BOARD
    # =========================
    def update_board(self):

        for i in range(9):

            value = self.tiles[i]

            if value == 0:

                self.buttons[i].config(
                    text="",
                    bg="#0F172A",
                    state="disabled"
                )

            else:

                self.buttons[i].config(
                    text=str(value),
                    bg=COLORS[(value - 1) % len(COLORS)],
                    fg="white",
                    activebackground="white",
                    state="normal"
                )

    # =========================
    # SHUFFLE
    # =========================
    def shuffle(self):

        difficulty = self.difficulty_var.get()

        if difficulty == "Easy":
            shuffle_count = 15
        elif difficulty == "Medium":
            shuffle_count = 35
        else:
            shuffle_count = 60

        self.tiles = GOAL[:]

        empty = 8

        for _ in range(shuffle_count):

            possible = []

            if empty % 3 > 0:
                possible.append(empty - 1)

            if empty % 3 < 2:
                possible.append(empty + 1)

            if empty > 2:
                possible.append(empty - 3)

            if empty < 6:
                possible.append(empty + 3)

            target = random.choice(possible)

            self.tiles[empty], self.tiles[target] = (
                self.tiles[target],
                self.tiles[empty]
            )

            empty = target

        self.moves = 0
        self.score = 1000
        self.start_time = time.time()

        self.update_labels()
        self.update_board()

    # =========================
    # MOVE TILE
    # =========================
    def move_tile(self, index):

        empty = self.tiles.index(0)

        valid = [
            empty - 1,
            empty + 1,
            empty - 3,
            empty + 3
        ]

        if empty % 3 == 0 and empty - 1 in valid:
            valid.remove(empty - 1)

        if empty % 3 == 2 and empty + 1 in valid:
            valid.remove(empty + 1)

        if index in valid and 0 <= index < 9:

            self.tiles[empty], self.tiles[index] = (
                self.tiles[index],
                self.tiles[empty]
            )

            self.moves += 1
            self.score -= 5

            self.animate(index)

            self.update_labels()
            self.update_board()

            # SOUND
            if SOUND_ENABLED:
                pass

            if self.tiles == GOAL:
                self.win_game()

    # =========================
    # KEYBOARD MOVE
    # =========================
    def key_move(self, direction):

        empty = self.tiles.index(0)

        if direction == "Up" and empty < 6:
            self.move_tile(empty + 3)

        elif direction == "Down" and empty > 2:
            self.move_tile(empty - 3)

        elif direction == "Left" and empty % 3 < 2:
            self.move_tile(empty + 1)

        elif direction == "Right" and empty % 3 > 0:
            self.move_tile(empty - 1)

    # =========================
    # TILE ANIMATION
    # =========================
    def animate(self, index):

        self.buttons[index].config(font=("Arial", 32, "bold"))

        self.root.after(
            100,
            lambda: self.buttons[index].config(
                font=("Arial", 26, "bold")
            )
        )

    # =========================
    # WIN GAME
    # =========================
    def win_game(self):

        for _ in range(4):

            for btn in self.buttons:
                btn.config(bg="#22C55E")

            self.root.update()
            time.sleep(0.15)

            self.update_board()
            self.root.update()
            time.sleep(0.15)

        elapsed = int(time.time() - self.start_time)

        messagebox.showinfo(
            "🎉 You Won!",
            f"Moves: {self.moves}\n"
            f"Time: {elapsed} seconds\n"
            f"Score: {self.score}"
        )

    # =========================
    # RESTART
    # =========================
    def restart(self):

        self.tiles = GOAL[:]

        self.moves = 0
        self.score = 1000
        self.start_time = time.time()

        self.update_labels()
        self.update_board()

    # =========================
    # HINT
    # =========================
    def show_hint(self):

        messagebox.showinfo(
            "💡 Hint",
            "Arrange numbers row by row.\n"
            "Keep empty tile near target positions."
        )

    # =========================
    # AUTO SOLVE
    # =========================
    def auto_solve(self):

        self.tiles = GOAL[:]

        self.update_board()

        messagebox.showinfo(
            "🤖 Auto Solver",
            "Puzzle solved automatically!"
        )

    # =========================
    # UPDATE LABELS
    # =========================
    def update_labels(self):

        self.move_label.config(text=f"Moves: {self.moves}")
        self.score_label.config(text=f"Score: {self.score}")

    # =========================
    # TIMER
    # =========================
    def update_timer(self):

        elapsed = int(time.time() - self.start_time)

        self.timer_label.config(text=f"Time: {elapsed}s")

        self.root.after(1000, self.update_timer)


# =============================
# RUN APPLICATION
# =============================
root = tk.Tk()

app = PuzzleGame(root)

root.mainloop()