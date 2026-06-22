import customtkinter as ctk
import auth
from styles import BLUE, RED, WHITE, CARD, MUTED

class StatsFrame(ctk.CTkFrame):
    """Scrollable stats page for the current user."""
    def __init__(self, app):
        super().__init__(app, fg_color=WHITE, corner_radius=0)  # base frame init
        self.app = app  # app reference for navigation
        self.scalable = []  # widgets that need font scaling
        self.user = auth.find_user(self.app.current_user)  # load active user's stats

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

    def make_button(self, parent, text, cmd, fg=BLUE, text_color=WHITE, width=150, height=36):
        btn = ctk.CTkButton(
            parent, text=text, command=cmd,
            fg_color=fg,
            text_color=text_color,
            font=("Comic Sans MS", self.scale_value(13), "bold"),
            corner_radius=8, width=self.scale_value(width), height=self.scale_value(height),
        )
        self.scalable.append((btn, "Comic Sans MS", 13, "bold"))  # track for resize
        return btn  # return built button

    def calc_percent(self, correct, answered):
        """Return percentage safely when answered could be zero."""
        if answered <= 0:
            return 0.0
        return (correct / answered) * 100

    def format_time(self, total_seconds):
        secs = int(max(0, total_seconds))  # clamp to non-negative int
        h = secs // 3600
        m = (secs % 3600) // 60
        s = secs % 60
        if h > 0:
            return f"{h}h {m}m {s}s"
        if m > 0:
            return f"{m}m {s}s"
        return f"{s}s"

    def section_title(self, parent, title):
        """Add a section heading label."""
        self.make_label(parent, title, size=18, bold=True, color=BLUE).pack(anchor="w", padx=14, pady=(10, 6))

    def stat_row(self, parent, key, value, pady=3):
        """Add one key/value stat row."""
        row = ctk.CTkFrame(parent, fg_color="transparent")  # one stat line container
        row.pack(fill="x", padx=14, pady=pady)
        self.make_label(row, key, size=13, color=MUTED).pack(side="left")
        self.make_label(row, str(value), size=13, bold=True, color=BLUE).pack(side="right")

    def bucket_rows(self, parent, title, buckets):
        """Render grouped bucket stats (tests/correct/answered/accuracy)."""
        self.section_title(parent, title)
        items = list(buckets.items())  # convert dict to ordered list
        for index, (name, bucket) in enumerate(items):
            card = ctk.CTkFrame(parent, fg_color=WHITE, corner_radius=8)
            is_last = index == (len(items) - 1)  # add extra bottom space on last
            card.pack(fill="x", padx=14, pady=(4, 12 if is_last else 4))
            self.make_label(card, name.title(), size=14, bold=True, color=BLUE).pack(anchor="w", padx=10, pady=(8, 4))
            self.stat_row(card, "Tests", bucket.get("tests", 0))
            self.stat_row(card, "Correct", bucket.get("correct", 0))
            self.stat_row(card, "Answered", bucket.get("answered", 0))
            avg = bucket.get("average_accuracy", 0.0)
            self.stat_row(card, "Average Accuracy", f"{avg:.1f}%", pady=(3, 10 if is_last else 3))

    def setup_ui(self):
        """Build the full stats page with all sections."""
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        header = ctk.CTkFrame(self, fg_color=CARD, corner_radius=0)  # top header bar
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(1, weight=1)

        self.make_button(header, "⬅️Menu", self.app.show_menu, fg=WHITE, text_color=BLUE, width=80, height=32).grid(
            row=0, column=0, padx=10, pady=10, sticky="w"
        )

        username = self.app.current_user or "Guest"
        self.make_label(header, f"Stats - {username}", size=24, bold=True, color=BLUE).grid(
            row=0, column=1, padx=8, pady=10, sticky="w"
        )

        body = ctk.CTkScrollableFrame(self, fg_color=WHITE)  # scrolling content area
        body.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        if not self.user:
            self.make_label(body, "No user data found.", size=16, color=RED).pack(anchor="w", padx=10, pady=10)  # empty state
            return

        overview = ctk.CTkFrame(body, fg_color=CARD, corner_radius=12)
        overview.pack(fill="x", padx=8, pady=(8, 20))
        # summary card with totals across every game played
        self.section_title(overview, "Overview")

        total_correct = self.user.get("total_correct", 0)  # all-time correct answers
        total_answered = self.user.get("total_answered", 0)  # all-time attempts
        overall_accuracy = self.calc_percent(total_correct, total_answered)  # derived % value
        games_played = self.user.get("games_played", 0)  # completed game count

        self.stat_row(overview, "High Score", self.user.get("high_score", 0))
        self.stat_row(overview, "Games Played", games_played)
        self.stat_row(overview, "Tests Started", self.user.get("tests_started", 0))
        self.stat_row(overview, "Total Correct", total_correct)
        self.stat_row(overview, "Total Answered", total_answered)
        self.stat_row(overview, "Overall Accuracy", f"{overall_accuracy:.1f}%")
        self.stat_row(overview, "Total Time in Tests", self.format_time(self.user.get("total_time_spent_seconds", 0)))
        self.stat_row(overview, "Most Played Mode", self.user.get("most_played_game_mode", "none"))
        self.stat_row(overview, "Longest Unlimited Streak", self.user.get("longest_unlimited_streak", 0), pady=(3, 12))

        mode_count_card = ctk.CTkFrame(body, fg_color=CARD, corner_radius=12)
        mode_count_card.pack(fill="x", padx=8, pady=(8, 20))
        # shows which game modes the player chooses most often
        self.section_title(mode_count_card, "Mode Counts")
        mode_items = list(self.user.get("mode_counts", {}).items())
        for index, (mode, count) in enumerate(mode_items):
            is_last = index == (len(mode_items) - 1)
            self.stat_row(mode_count_card, mode.title(), count, pady=(3, 12 if is_last else 3))

        difficulty_card = ctk.CTkFrame(body, fg_color=CARD, corner_radius=12)
        difficulty_card.pack(fill="x", padx=8, pady=(8, 20))
        self.bucket_rows(difficulty_card, "Difficulty Stats", self.user.get("difficulty_stats", {}))

        time_mode_card = ctk.CTkFrame(body, fg_color=CARD, corner_radius=12)
        time_mode_card.pack(fill="x", padx=8, pady=(8, 20))
        self.bucket_rows(time_mode_card, "Time Mode Stats", self.user.get("time_mode_stats", {}))

        game_mode_card = ctk.CTkFrame(body, fg_color=CARD, corner_radius=12)
        game_mode_card.pack(fill="x", padx=8, pady=(8, 24))
        self.bucket_rows(game_mode_card, "Game Mode Stats", self.user.get("game_mode_stats", {}))