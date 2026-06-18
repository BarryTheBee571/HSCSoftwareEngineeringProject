import customtkinter as ctk
import auth
from styles import BLUE, GREEN, RED, WHITE, CARD, MUTED


class MenuFrame(ctk.CTkFrame):

    def __init__(self, app):
        super().__init__(app, fg_color=WHITE, corner_radius=0)
        self.app = app
        self._scalable = []
        self.mode = ctk.StringVar()
        self.difficulty = ctk.StringVar()
        self.time_limit = ctk.IntVar()
        self.mode.trace_add("write", self.handle_mode_change)

        self.build_ui()

    def scale_value(self, base):
        return self.app.scale_value(base)

    def get_difficulty_options(self):
        mode = self.mode.get()
        if mode == "addition":
            return [("Easy (1-20)", "easy"), ("Medium (1-50)", "medium"), ("Hard (1-100)", "hard")]
        elif mode == "subtraction":
            return [("Easy (1-20)", "easy"), ("Medium (1-50)", "medium"), ("Hard (1-100)", "hard")]
        elif mode == "multiplication":
            return [("Easy (1-10)", "easy"), ("Medium (1-20)", "medium"), ("Hard (1-50)", "hard")]
        elif mode == "division":
            return [("Easy (1-10)", "easy"), ("Medium (1-20)", "medium"), ("Hard (1-50)", "hard")]
        else:
            return [("Easy", "easy"), ("Medium", "medium"), ("Hard", "hard")]

    def handle_mode_change(self, *args):
        if hasattr(self, '_diff_frame'):
            for widget in self._diff_frame.winfo_children():
                widget.destroy()
            DIFFS = self.get_difficulty_options()
            self.create_toggle_buttons(self._diff_frame, DIFFS, self.difficulty)

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
            font=("Times New Roman", self.scale_value(size), weight),
            text_color=color, **kw,
        )
        self._scalable.append((lbl, "Times New Roman", size, weight))
        return lbl

    def create_button(self, parent, text, cmd, fg=BLUE, text_color=WHITE, width=180, height=44):
        btn = ctk.CTkButton(
            parent, text=text, command=cmd,
            fg_color=fg, hover_color=self.lighten_color(fg),
            text_color=text_color,
            font=("Times New Roman", self.scale_value(15), "bold"),
            corner_radius=10, width=self.scale_value(width), height=self.scale_value(height),
        )
        self._scalable.append((btn, "Times New Roman", 15, "bold"))
        return btn

    def create_toggle_buttons(self, parent, options, variable):
        buttons = {}

        def select(val):
            variable.set(val)
            for v, b in buttons.items():
                active = (v == val)
                b.configure(
                    fg_color=BLUE if active else WHITE,
                    text_color=WHITE if active else BLUE,
                    hover_color=self.lighten_color(BLUE) if active else self.lighten_color(WHITE),
                )

        for col, (label, val) in enumerate(options):
            active = variable.get() == val
            btn = ctk.CTkButton(
                parent, text=label,
                command=lambda v=val: select(v),
                fg_color=BLUE if active else WHITE,
                text_color=WHITE if active else BLUE,
                hover_color=self.lighten_color(BLUE) if active else self.lighten_color(WHITE),
                font=("Times New Roman", self.scale_value(12), "normal"),
                corner_radius=8, height=self.scale_value(36),
                border_width=1, border_color=BLUE,
            )
            btn.grid(row=0, column=col, padx=3, pady=4, sticky="ew")
            parent.grid_columnconfigure(col, weight=1)
            self._scalable.append((btn, "Times New Roman", 12, "normal"))
            buttons[val] = btn

        return buttons

    def build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=0)
        self.grid_rowconfigure(6, weight=0)

        hdr = ctk.CTkFrame(self, fg_color=CARD, corner_radius=0)
        hdr.grid(row=0, column=0, sticky="ew")
        hdr.grid_columnconfigure(0, weight=1)
        hdr.grid_columnconfigure(1, weight=0)

        self.create_label(hdr, "Speedy Maths", size=26, bold=True, color=BLUE).grid(
            row=0, column=0, pady=18, padx=20, sticky="w")

        self.build_user_info_section(hdr)

        self.create_label(
            self, "Answer as many questions as you can!",
            size=13, color=MUTED,
        ).grid(row=1, column=0, pady=(14, 0))

        mc = ctk.CTkFrame(self, fg_color=CARD, corner_radius=12)
        mc.grid(row=2, column=0, padx=40, pady=(12, 6), sticky="nsew")
        mc.grid_columnconfigure(0, weight=1)
        mc.grid_rowconfigure(1, weight=1)

        self.create_label(mc, "Game Mode", size=14, bold=True, color=BLUE).grid(
            row=0, column=0, padx=20, pady=(12, 4), sticky="w")

        mode_row = ctk.CTkFrame(mc, fg_color="transparent")
        mode_row.grid(row=1, column=0, padx=14, pady=(0, 12), sticky="nsew")

        MODES = [
            ("Addition", "addition"),
            ("Subtraction", "subtraction"),
            ("Multiplication", "multiplication"),
            ("Division", "division"),
            ("Mixed", "mixed"),
        ]
        self.create_toggle_buttons(mode_row, MODES, self.mode)

        mc = ctk.CTkFrame(self, fg_color=CARD, corner_radius=12)
        mc.grid(row=3, column=0, padx=40, pady=(6, 12), sticky="nsew")
        mc.grid_columnconfigure(0, weight=1)
        mc.grid_rowconfigure(1, weight=1)

        self.create_label(mc, "Time Limit", size=14, bold=True, color=BLUE).grid(
            row=0, column=0, padx=20, pady=(12, 4), sticky="w")
        
        mode_row = ctk.CTkFrame(mc, fg_color="transparent")
        mode_row.grid(row=1, column=0, padx=14, pady=(0, 12), sticky="nsew")

        TIMES = [
            ("30 seconds", 30),
            ("60 seconds", 60),
            ("90 seconds", 90),
            ("120 seconds", 120),
            (Unlimited := "Unlimited", -1),
        ]
        self.create_toggle_buttons(mode_row, TIMES, self.time_limit)

        dc = ctk.CTkFrame(self, fg_color=CARD, corner_radius=12)
        dc.grid(row=4, column=0, padx=40, pady=6, sticky="nsew")
        dc.grid_columnconfigure(0, weight=1)
        dc.grid_rowconfigure(1, weight=1)

        self.create_label(dc, "Difficulty", size=14, bold=True, color=BLUE).grid(
            row=0, column=0, padx=20, pady=(12, 4), sticky="w")

        self._diff_frame = ctk.CTkFrame(dc, fg_color="transparent")
        self._diff_frame.grid(row=1, column=0, padx=14, pady=(0, 12), sticky="nsew")

        DIFFS = self.get_difficulty_options()
        self.create_toggle_buttons(self._diff_frame, DIFFS, self.difficulty)

        self.error_label = self.create_label(self, "", size=12, color=RED)
        self.error_label.grid(row=5, column=0, pady=(8, 0))

        self.create_button(self, "Start Game", self.launch_game, width=220, height=50).grid(row=6, column=0, pady=20)

    def build_user_info_section(self, header):
        if self.app.current_user:
            user_data = auth.get_user(self.app.current_user)
            high_score = user_data["high_score"] if user_data else 0

            info = ctk.CTkFrame(header, fg_color="transparent")
            info.grid(row=0, column=1, padx=16, pady=10, sticky="e")

            self.create_label(info, f"{self.app.current_user}",
                        size=12, bold=True, color=BLUE).pack(anchor="e")
            self.create_label(info, f"Best: {high_score} pts",
                        size=11, color=MUTED).pack(anchor="e")

            logout_btn = ctk.CTkButton(
                info, text="Log out",
                command=self.logout_user,
                fg_color=WHITE, text_color=BLUE,
                hover_color=self.lighten_color(WHITE),
                font=("Times New Roman", self.scale_value(10), "normal"),
                width=self.scale_value(60), height=self.scale_value(22),
                border_width=1, border_color=BLUE,
                corner_radius=4,
            )
            logout_btn.pack(anchor="e", pady=(2, 0))
            self._scalable.append((logout_btn, "Times New Roman", 10, "normal"))
        else:
            
            login_btn = ctk.CTkButton(
                header, text="Log in",
                command=self.app.show_login,
                fg_color=WHITE, text_color=BLUE,
                hover_color=self.lighten_color(WHITE),
                font=("Times New Roman", self.scale_value(12), "bold"),
                width=self.scale_value(70), height=self.scale_value(30),
                border_width=1, border_color=BLUE,
                corner_radius=6,
            )
            login_btn.grid(row=0, column=1, padx=16, pady=10)
            self._scalable.append((login_btn, "Times New Roman", 12, "bold"))

    def logout_user(self):
        self.app.current_user = None
        self.app.session_token = None
        self.app.show_login()

    def launch_game(self):
        mode = self.mode.get()
        difficulty = self.difficulty.get()
        time_limit = self.time_limit.get()
        
        if not mode:
            self.error_label.configure(text="Please select a game mode", text_color=RED)
            return
        if not difficulty:
            self.error_label.configure(text="Please select a difficulty", text_color=RED)
            return
        if not time_limit:
            self.error_label.configure(text="Please select a time limit", text_color=RED)
            return
        
        self.error_label.configure(text="")
        self.app.show_game(mode, difficulty, time_limit)
