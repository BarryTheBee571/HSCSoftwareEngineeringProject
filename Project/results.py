import customtkinter as ctk
import auth
from styles import BLUE, GREEN, RED, WHITE, CARD, MUTED


class ResultsFrame(ctk.CTkFrame):

    def __init__(self, app, score, correct, total, mode, difficulty, time_limit, time_spent_seconds, longest_streak_in_test):
        super().__init__(app, fg_color=WHITE, corner_radius=0)
        self.app = app
        self.score = score
        self.correct = correct
        self.total = total
        self.mode = mode
        self.difficulty = difficulty
        self.time_limit = time_limit
        self.time_spent_seconds = time_spent_seconds
        self.longest_streak_in_test = longest_streak_in_test
        self._scalable = []

        self.accuracy = (correct / total * 100) if total > 0 else 0

        if self.app.current_user:
            auth.update_stats(
                self.app.current_user,
                score,
                correct,
                total,
                mode,
                difficulty,
                time_limit,
                time_spent_seconds,
                longest_streak_in_test,
            )

        self.build_ui()

    def scale_value(self, base):
        return self.app.scale_value(base)

    def lighten_color(self, hex_color):
        r = min(255, int(hex_color[1:3], 16) + 30)
        g = min(255, int(hex_color[3:5], 16) + 30)
        b = min(255, int(hex_color[5:7], 16) + 30)
        return f"#{r:02x}{g:02x}{b:02x}"

    def apply_scaling(self):
        for widget, family, base_size, weight in self._scalable:
            try:
                widget.configure(font=(family, max(8, self.scale_value(base_size)), weight))
            except Exception:
                pass

    def create_label(self, parent, text, size=14, bold=False, color=WHITE, **kw):
        weight = "bold" if bold else "normal"
        lbl = ctk.CTkLabel(
            parent, text=text,
            font=("Time New Roman", self.scale_value(size), weight),
            text_color=color, **kw,
        )
        self._scalable.append((lbl, "Time New Roman", size, weight))
        return lbl

    def create_button(self, parent, text, cmd, fg=BLUE, text_color=WHITE, width=180, height=44):
        btn = ctk.CTkButton(
            parent, text=text, command=cmd,
            fg_color=fg, hover_color=self.lighten_color(fg),
            text_color=text_color,
            font=("Time New Roman", self.scale_value(15), "bold"),
            corner_radius=10, width=self.scale_value(width), height=self.scale_value(height),
        )
        self._scalable.append((btn, "Time New Roman", 15, "bold"))
        return btn

    def build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=0)

        hdr = ctk.CTkFrame(self, fg_color=CARD, corner_radius=0)
        hdr.grid(row=0, column=0, sticky="ew")
        hdr.grid_columnconfigure(0, weight=1)

        heading, sub = self.generate_result_message()
        self.create_label(hdr, heading, size=26, bold=True, color=BLUE).grid(
            row=0, column=0, pady=(18, 4))
        self.create_label(hdr, sub, size=12, color=MUTED).grid(
            row=1, column=0, pady=(0, 14))

        if self.app.current_user:
            self.show_new_highscore_if_applicable()

        sc = ctk.CTkFrame(self, fg_color=CARD, corner_radius=14)
        sc.grid(row=2, column=0, padx=60, pady=16, sticky="nsew")
        sc.grid_columnconfigure(0, weight=1)

        stats = [
            ("Score", f"{self.score} pts", BLUE),
            ("Questions Answered", str(self.total), BLUE),
            ("Correct Answers", str(self.correct), GREEN),
            ("Accuracy", f"{self.accuracy:.1f}%", GREEN if self.accuracy >= 70 else RED),
        ]

        if self.app.current_user:
            user_data = auth.get_user(self.app.current_user)
            if user_data:
                stats.append(("Your High Score", f"{user_data['high_score']} pts", BLUE))

        for i, (lbl, val, val_color) in enumerate(stats):
            row = ctk.CTkFrame(sc, fg_color="transparent")
            row.grid(row=i * 2, column=0, padx=30, pady=8, sticky="ew")
            self.create_label(row, lbl, size=15, color=MUTED).pack(side="left")
            self.create_label(row, val, size=16, bold=True, color=val_color).pack(side="right")
            if i < len(stats) - 1:
                ctk.CTkFrame(sc, fg_color=WHITE, height=1).grid(
                    row=i * 2 + 1, column=0, padx=30, sticky="ew")

        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.grid(row=3, column=0, pady=20)

        self.create_button(
            btn_row, "Play Again",
            lambda: self.app.show_game(self.mode, self.difficulty, self.time_limit),
            width=165, height=46,
        ).pack(side="left", padx=10)

        self.create_button(
            btn_row, "Main Menu", self.app.show_menu,
            fg=CARD, text_color=BLUE, width=165, height=46,
        ).pack(side="left", padx=10)

    def generate_result_message(self):
        if self.total == 0:
            return "Round Over!", "No questions answered"
        if self.accuracy >= 90:
            return "Amazing!", f"{self.score} points — nearly perfect!"
        elif self.accuracy >= 70:
            return "Great Work!", f"{self.score} points — keep it up!"
        elif self.accuracy >= 50:
            return "Not Bad!", f"{self.score} points — keep practising!"
        else:
            return "Round Over!", f"{self.score} points — try again!"

    def show_new_highscore_if_applicable(self):
        if not self.app.current_user:
            return
        user_data = auth.get_user(self.app.current_user)
        if not user_data:
            return
        if self.score > 0 and user_data["high_score"] == self.score and self.score >= 10:
            banner = ctk.CTkFrame(self, fg_color=GREEN, corner_radius=8)
            banner.grid(row=1, column=0, padx=80, pady=(8, 0), sticky="ew")
            self.create_label(
                banner, "New High Score!", size=13, bold=True, color=WHITE,
            ).pack(pady=8)