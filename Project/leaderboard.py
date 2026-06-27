import customtkinter as ctk
import auth
from styles import BLUE, WHITE, CARD, MUTED


class LeaderboardFrame(ctk.CTkFrame):
    """Leaderboard page sorted by each user's high score."""
    def __init__(self, app):
        super().__init__(app, fg_color=WHITE, corner_radius=0)  # base frame init
        self.app = app  # app reference for navigation
        self.scalable = []  # widgets that need font scaling
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
            parent,
            text=text,
            font=("Comic Sans MS", self.scale_value(size), weight),
            text_color=color,
            **kw,
        )
        self.scalable.append((lbl, "Comic Sans MS", size, weight))  # track for resize
        return lbl  # return built label

    def make_button(self, parent, text, cmd, fg=BLUE, text_color=WHITE, width=150, height=36):
        btn = ctk.CTkButton(
            parent,
            text=text,
            command=cmd,
            fg_color=fg,
            text_color=text_color,
            font=("Comic Sans MS", self.scale_value(13), "bold"),
            corner_radius=8,
            width=self.scale_value(width),
            height=self.scale_value(height),
        )
        self.scalable.append((btn, "Comic Sans MS", 13, "bold"))  # track for resize
        return btn  # return built button

    def format_time(self, total_seconds):
        """Turn raw seconds into a readable h/m/s string."""
        secs = int(max(0, total_seconds))
        h = secs // 3600
        m = (secs % 3600) // 60
        s = secs % 60
        if h > 0:
            return f"{h}h {m}m {s}s"
        if m > 0:
            return f"{m}m {s}s"
        return f"{s}s"

    def calc_accuracy(self, user):
        """Calculate overall accuracy for one user."""
        answered = user.get("total_answered", 0)
        if answered <= 0:
            return 0.0
        return (user.get("total_correct", 0) / answered) * 100

    def setup_ui(self):
        """Build leaderboard cards and sort users by high score."""
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        header = ctk.CTkFrame(self, fg_color=CARD, corner_radius=0)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(1, weight=1)

        self.make_button(header, "⬅️ Menu", self.app.show_menu, fg=WHITE, text_color=BLUE, width=90, height=32).grid(
            row=0, column=0, padx=10, pady=10, sticky="w"
        )
        self.make_label(header, "Leaderboard", size=24, bold=True, color=BLUE).grid(
            row=0, column=1, padx=8, pady=10, sticky="w"
        )

        body = ctk.CTkScrollableFrame(self, fg_color=WHITE)
        body.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        users = auth.load_users()  # load all accounts
        rows = []  # table rows for sorting/rendering
        for username, user in users.items():
            # each row stores: name, score, accuracy, total time
            rows.append(
                (
                    username,
                    user.get("high_score", 0),
                    self.calc_accuracy(user),
                    self.format_time(user.get("total_time_spent_seconds", 0)),
                )
            )

        # Highest score first.
        rows.sort(key=lambda item: item[1], reverse=True)

        if not rows:
            self.make_label(body, "No leaderboard data available.", size=16, color=MUTED).pack(anchor="w", padx=10, pady=10)  # empty state
            return

        for index, (username, high_score, accuracy, total_time) in enumerate(rows, start=1):
            card = ctk.CTkFrame(body, fg_color=CARD, corner_radius=12)  # one user row card
            card.pack(fill="x", padx=8, pady=(8, 0))
            card.grid_columnconfigure(1, weight=1)

            self.make_label(card, f"#{index}", size=16, bold=True, color=BLUE).grid(
                row=0, column=0, padx=(12, 8), pady=(10, 2), sticky="w"
            )
            self.make_label(card, username, size=16, bold=True, color=BLUE).grid(
                row=0, column=1, padx=2, pady=(10, 2), sticky="w"
            )
            self.make_label(card, f"High Score: {high_score}", size=12, color=MUTED).grid(
                row=1, column=1, padx=2, pady=(0, 8), sticky="w"
            )
            self.make_label(card, f"Accuracy: {accuracy:.1f}%", size=12, color=MUTED).grid(
                row=1, column=2, padx=8, pady=(0, 8), sticky="e"
            )
            self.make_label(card, f"Time Spent: {total_time}", size=12, color=MUTED).grid(
                row=1, column=3, padx=(8, 12), pady=(0, 8), sticky="e"
            )