import customtkinter as ctk
import auth
from styles import BLUE, GREEN, RED, WHITE, CARD, MUTED

class ResultsFrame(ctk.CTkFrame):
    """Results page shown right after a game ends."""

    def __init__(self, app, score, correct, total, mode, difficulty, time_limit, time_spent_seconds, longest_streak_in_test):
        super().__init__(app, fg_color=WHITE, corner_radius=0)  # base frame init
        self.app = app  # app reference for navigation
        self.score = score  # points from finished run
        self.correct = correct  # correct count from run
        self.total = total  # answered count from run
        self.mode = mode  # mode used in run
        self.difficulty = difficulty  # difficulty used in run
        self.time_limit = time_limit  # timer setting used
        self.time_spent_seconds = time_spent_seconds  # actual time spent
        self.longest_streak_in_test = longest_streak_in_test  # best streak in this run
        self.scalable = []  # widgets that need font scaling

        # Guard divide-by-zero if player ran out of time early.
        self.accuracy = (correct / total * 100) if total > 0 else 0  # computed accuracy percent

        if self.app.current_user:
            auth.save_game_stats(
                self.app.current_user,
                score,
                correct,
                total,
                mode,
                difficulty,
                time_limit,
                time_spent_seconds,
                longest_streak_in_test,
            )  # persist stats for logged-in users only

        self.setup_ui()  # build page widgets

    def scale_value(self, base):
        return self.app.scale_value(base)  # delegate scaling to app

    def refresh_scaling(self):
        for widget, family, base_size, weight in self.scalable:
            try:
                widget.configure(font=(family, max(8, self.scale_value(base_size)), weight))
            except Exception:
                pass  # ignore widgets that cannot be reconfigured

    def make_label(self, parent, text, size=14, bold=False, color=WHITE, **kw):
        weight = "bold" if bold else "normal"
        lbl = ctk.CTkLabel(
            parent, text=text,
            font=("Comic Sans MS", self.scale_value(size), weight),
            text_color=color, **kw,
        )
        self.scalable.append((lbl, "Comic Sans MS", size, weight))  # track for resize
        return lbl  # return built label

    def make_button(self, parent, text, cmd, fg=BLUE, text_color=WHITE, width=180, height=44):
        btn = ctk.CTkButton(
            parent, text=text, command=cmd,
            fg_color=fg,
            text_color=text_color,
            font=("Comic Sans MS", self.scale_value(15), "bold"),
            corner_radius=10, width=self.scale_value(width), height=self.scale_value(height),
        )
        self.scalable.append((btn, "Comic Sans MS", 15, "bold"))  # track for resize
        return btn  # return built button

    def setup_ui(self):
        """Build results layout and action buttons."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=0)

        hdr = ctk.CTkFrame(self, fg_color=CARD, corner_radius=0)  # top header bar
        hdr.grid(row=0, column=0, sticky="ew")
        hdr.grid_columnconfigure(0, weight=1)

        self.make_label(hdr, "Results", size=26, bold=True, color=BLUE).grid(
            row=0, column=0, pady=18)

        if self.app.current_user:  # guests have no personal high score
            self.show_highscore_banner()  # maybe show high score banner

        sc = ctk.CTkFrame(self, fg_color=CARD, corner_radius=14)  # stats card
        sc.grid(row=2, column=0, padx=60, pady=16, sticky="nsew")
        sc.grid_columnconfigure(0, weight=1)

        stats = [  # base rows shown for every user
            ("Score", f"{self.score} pts", BLUE),
            ("Questions Answered", str(self.total), BLUE),
            ("Correct Answers", str(self.correct), GREEN),
            ("Accuracy", f"{self.accuracy:.1f}%", GREEN if self.accuracy >= 70 else RED),
        ]

        if self.app.current_user:
            user_data = auth.find_user(self.app.current_user)  # fetch latest saved stats
            if user_data:
                stats.append(("Your High Score", f"{user_data['high_score']} pts", BLUE))  # add personal pb row

        for i, (lbl, val, val_color) in enumerate(stats):
            row = ctk.CTkFrame(sc, fg_color="transparent")
            row.grid(row=i * 2, column=0, padx=30, pady=8, sticky="ew")
            self.make_label(row, lbl, size=15, color=MUTED).pack(side="left")
            self.make_label(row, val, size=16, bold=True, color=val_color).pack(side="right")
            if i < len(stats) - 1:  # divider after each row except last
                ctk.CTkFrame(sc, fg_color=WHITE, height=1).grid(
                    row=i * 2 + 1, column=0, padx=30, sticky="ew")

        btn_row = ctk.CTkFrame(self, fg_color="transparent")  # action buttons row
        btn_row.grid(row=3, column=0, pady=20)

        self.make_button(
            btn_row, "Play Again",
            # reuse same settings the player just used
            lambda: self.app.show_game(self.mode, self.difficulty, self.time_limit),
            width=165, height=46,
        ).pack(side="left", padx=10)

        self.make_button(
            # return without starting another game
            btn_row, "Main Menu", self.app.show_menu,
            fg=CARD, text_color=BLUE, width=165, height=46,
        ).pack(side="left", padx=10)

    def show_highscore_banner(self):
        """Show a small banner if this run matched a new high score."""
        if not self.app.current_user:
            return  # guests do not have account highscores
        user_data = auth.find_user(self.app.current_user)  # load user data
        if not user_data:
            return  # account missing/corrupt edge case
        if self.score > 0 and user_data["high_score"] == self.score and self.score >= 10:
            banner = ctk.CTkFrame(self, fg_color=GREEN, corner_radius=8)  # success banner box
            banner.grid(row=1, column=0, padx=80, pady=(8, 0), sticky="ew")
            self.make_label(
                banner, "New High Score!", size=13, bold=True, color=WHITE,
            ).pack(pady=8)