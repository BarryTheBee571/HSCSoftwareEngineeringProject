import customtkinter as ctk
import auth
from styles import BLUE, GREEN, RED, WHITE, CARD, MUTED

class MenuFrame(ctk.CTkFrame):
    """Main menu where player picks mode, time, and difficulty."""

    def __init__(self, app):
        super().__init__(app, fg_color=WHITE, corner_radius=0)  # base frame init
        self.app = app  # app reference for navigation
        self._scalable = []  # widgets that need font scaling
        self.mode = ctk.StringVar()  # selected game mode
        self.difficulty = ctk.StringVar()  # selected difficulty
        self.time_limit = ctk.IntVar()  # selected time limit
        self.mode.trace_add("write", self.on_mode_change)  # react to mode changes

        self.setup_ui()  # build menu widgets

    def scale_value(self, base):
        return self.app.scale_value(base)  # delegate scaling to app

    def get_diff_choices(self):
        """Difficulty toggle options."""
        return [("Easy", "easy"), ("Medium", "medium"), ("Hard", "hard")]

    def on_mode_change(self, *args):
        """Rebuild difficulty row if mode changes."""
        if hasattr(self, '_diff_frame'):
            for widget in self._diff_frame.winfo_children():
                widget.destroy()  # clear old difficulty row
            DIFFS = self.get_diff_choices()
            self.make_toggle_buttons(self._diff_frame, DIFFS, self.difficulty)

    def refresh_scaling(self):
        for widget, family, base_size, weight in self._scalable:
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
        self._scalable.append((lbl, "Comic Sans MS", size, weight))  # track for resize
        return lbl  # return built label

    def make_button(self, parent, text, cmd, fg=BLUE, text_color=WHITE, width=180, height=44):
        btn = ctk.CTkButton(
            parent, text=text, command=cmd,
            fg_color=fg,
            text_color=text_color,
            font=("Comic Sans MS", self.scale_value(15), "bold"),
            corner_radius=10, width=self.scale_value(width), height=self.scale_value(height),
        )
        self._scalable.append((btn, "Comic Sans MS", 15, "bold"))  # track for resize
        return btn  # return built button

    def make_toggle_buttons(self, parent, options, variable):
        """Make a row of selectable toggle-style buttons."""
        buttons = {}

        def select(val):
            """Handle one toggle selection and update styles."""
            variable.set(val)
            for v, b in buttons.items():
                active = (v == val)
                b.configure(
                    fg_color=BLUE if active else WHITE,  # active/inactive bg
                    text_color=WHITE if active else BLUE,  # active/inactive text
                )

        for col, (label, val) in enumerate(options):
            active = variable.get() == val  # pre-select if already chosen
            btn = ctk.CTkButton(
                parent, text=label,
                command=lambda v=val: select(v),
                fg_color=BLUE if active else WHITE,
                text_color=WHITE if active else BLUE,
                font=("Comic Sans MS", self.scale_value(12), "normal"),
                corner_radius=8, height=self.scale_value(36),
                border_width=1, border_color=BLUE,
            )
            btn.grid(row=0, column=col, padx=3, pady=4, sticky="ew")
            parent.grid_columnconfigure(col, weight=1)  # even spacing
            self._scalable.append((btn, "Comic Sans MS", 12, "normal"))
            buttons[val] = btn

        return buttons

    def setup_ui(self):
        """Build the full menu UI."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=0)
        self.grid_rowconfigure(6, weight=0)

        hdr = ctk.CTkFrame(self, fg_color=CARD, corner_radius=0)  # top header bar
        hdr.grid(row=0, column=0, sticky="ew")
        hdr.grid_columnconfigure(0, weight=1)
        hdr.grid_columnconfigure(1, weight=0)

        self.make_label(hdr, "Speedy Maths", size=26, bold=True, color=BLUE).grid(
            row=0, column=0, pady=18, padx=20, sticky="w")

        self.setup_user_info(hdr)  # right-side account controls

        self.make_label(
            self, "Answer as many questions as you can!",
            size=13, color=MUTED,
        ).grid(row=1, column=0, pady=(14, 0))

        mc = ctk.CTkFrame(self, fg_color=CARD, corner_radius=12)  # mode section card
        mc.grid(row=2, column=0, padx=40, pady=(12, 6), sticky="nsew")
        mc.grid_columnconfigure(0, weight=1)
        mc.grid_rowconfigure(1, weight=1)

        self.make_label(mc, "Game Mode", size=14, bold=True, color=BLUE).grid(
            row=0, column=0, padx=20, pady=(12, 4), sticky="w")

        mode_row = ctk.CTkFrame(mc, fg_color="transparent")
        mode_row.grid(row=1, column=0, padx=14, pady=(0, 12), sticky="nsew")

        MODES = [  # available game modes
            ("Addition", "addition"),
            ("Subtraction", "subtraction"),
            ("Multiplication", "multiplication"),
            ("Division", "division"),
            ("Mixed", "mixed"),
        ]
        self.make_toggle_buttons(mode_row, MODES, self.mode)

        mc = ctk.CTkFrame(self, fg_color=CARD, corner_radius=12)  # time section card
        mc.grid(row=3, column=0, padx=40, pady=(6, 12), sticky="nsew")
        mc.grid_columnconfigure(0, weight=1)
        mc.grid_rowconfigure(1, weight=1)

        self.make_label(mc, "Time Limit", size=14, bold=True, color=BLUE).grid(
            row=0, column=0, padx=20, pady=(12, 4), sticky="w")
        
        mode_row = ctk.CTkFrame(mc, fg_color="transparent")
        mode_row.grid(row=1, column=0, padx=14, pady=(0, 12), sticky="nsew")

        TIMES = [  # available time modes
            ("30 seconds", 30),
            ("60 seconds", 60),
            ("90 seconds", 90),
            ("120 seconds", 120),
            ("Unlimited", -1),
        ]
        self.make_toggle_buttons(mode_row, TIMES, self.time_limit)

        dc = ctk.CTkFrame(self, fg_color=CARD, corner_radius=12)  # difficulty section card
        dc.grid(row=4, column=0, padx=40, pady=6, sticky="nsew")
        dc.grid_columnconfigure(0, weight=1)
        dc.grid_rowconfigure(1, weight=1)

        self.make_label(dc, "Difficulty", size=14, bold=True, color=BLUE).grid(
            row=0, column=0, padx=20, pady=(12, 4), sticky="w")

        self._diff_frame = ctk.CTkFrame(dc, fg_color="transparent")  # dynamic diff row holder
        self._diff_frame.grid(row=1, column=0, padx=14, pady=(0, 12), sticky="nsew")

        DIFFS = self.get_diff_choices()
        self.make_toggle_buttons(self._diff_frame, DIFFS, self.difficulty)

        self.error_label = self.make_label(self, "", size=12, color=RED)
        self.error_label.grid(row=5, column=0, pady=(8, 0))

        self.make_button(self, "Start Game", self.start_game, width=220, height=50).grid(row=6, column=0, pady=20)

    def setup_user_info(self, header):
        """Show account buttons/high score area in header."""
        if self.app.current_user:
            user_data = auth.find_user(self.app.current_user)  # load current user data
            high_score = user_data["high_score"] if user_data else 0  # fallback if missing

            info = ctk.CTkFrame(header, fg_color="transparent")
            info.grid(row=0, column=1, padx=16, pady=10, sticky="e")

            profile_btn = ctk.CTkButton(
                info, text=self.app.current_user,
                command=self.app.show_stats,
                fg_color=WHITE, text_color=BLUE,
                font=("Comic Sans MS", self.scale_value(12), "bold"),
                width=self.scale_value(130), height=self.scale_value(26),
                border_width=1, border_color=BLUE,
                corner_radius=6,
            )
            profile_btn.pack(anchor="e")
            self._scalable.append((profile_btn, "Comic Sans MS", 12, "bold"))
            self.make_label(info, f"Best: {high_score} pts",
                        size=11, color=MUTED).pack(anchor="e")

            actions = ctk.CTkFrame(info, fg_color="transparent")
            actions.pack(anchor="e", pady=(2, 0))

            leaderboard_btn = ctk.CTkButton(
                actions, text="Leaderboard",
                command=self.app.show_leaderboard,
                fg_color=WHITE, text_color=BLUE,
                font=("Comic Sans MS", self.scale_value(10), "normal"),
                width=self.scale_value(95), height=self.scale_value(22),
                border_width=1, border_color=BLUE,
                corner_radius=4,
            )
            leaderboard_btn.pack(side="left", padx=(0, 6))
            self._scalable.append((leaderboard_btn, "Comic Sans MS", 10, "normal"))

            logout_btn = ctk.CTkButton(
                actions, text="Log out",
                command=self.log_out,
                fg_color=WHITE, text_color=BLUE,
                font=("Comic Sans MS", self.scale_value(10), "normal"),
                width=self.scale_value(60), height=self.scale_value(22),
                border_width=1, border_color=BLUE,
                corner_radius=4,
            )
            logout_btn.pack(side="left")
            self._scalable.append((logout_btn, "Comic Sans MS", 10, "normal"))
        else:
            
            login_btn = ctk.CTkButton(
                header, text="Log in",
                command=self.app.show_login,
                fg_color=WHITE, text_color=BLUE,
                font=("Comic Sans MS", self.scale_value(12), "bold"),
                width=self.scale_value(70), height=self.scale_value(30),
                border_width=1, border_color=BLUE,
                corner_radius=6,
            )
            login_btn.grid(row=0, column=1, padx=16, pady=10)
            self._scalable.append((login_btn, "Comic Sans MS", 12, "bold"))

    def log_out(self):
        self.app.current_user = None  # clear active user
        self.app.session_token = None  # clear active token
        self.app.show_login()  # send user to login page

    def start_game(self):
        """Validate selections, then open the game screen."""
        mode = self.mode.get()  # read selected mode
        difficulty = self.difficulty.get()  # read selected difficulty
        time_limit = self.time_limit.get()  # read selected time limit
        
        # these checks stop empty selections before starting the game
        if not mode:
            self.error_label.configure(text="Please select a game mode", text_color=RED)
            return
        if not difficulty:
            self.error_label.configure(text="Please select a difficulty", text_color=RED)
            return
        if not time_limit:
            self.error_label.configure(text="Please select a time limit", text_color=RED)
            return
        
        # clear old error once all selections are valid
        self.error_label.configure(text="")  # hide old warning
        self.app.show_game(mode, difficulty, time_limit)  # launch game with selected settings