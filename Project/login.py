import customtkinter as ctk
import auth
from styles import BLUE, GREEN, RED, WHITE, CARD, MUTED


class LoginFrame(ctk.CTkFrame):

    def __init__(self, app):
        super().__init__(app, fg_color=WHITE, corner_radius=0)
        self.app = app
        self._scalable = []
        self._mode = "login"

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
            font=("Time New Roman", self.scale_value(14), "bold"),
            corner_radius=10, width=self.scale_value(width), height=self.scale_value(height),
        )
        self._scalable.append((btn, "Time New Roman", 14, "bold"))
        return btn

    def create_entry(self, parent, placeholder, show=""):
        entry = ctk.CTkEntry(
            parent,
            font=("Time New Roman", self.scale_value(13), "normal"),
            width=self.scale_value(260), height=self.scale_value(42),
            fg_color=WHITE, border_color=BLUE, border_width=2,
            text_color=BLUE, placeholder_text=placeholder,
            placeholder_text_color=MUTED,
            show=show,
            corner_radius=8,
        )
        self._scalable.append((entry, "Time New Roman", 13, "normal"))
        return entry

    def build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=0)

        hdr = ctk.CTkFrame(self, fg_color=CARD, corner_radius=0)
        hdr.grid(row=0, column=0, sticky="ew")
        hdr.grid_columnconfigure(0, weight=1)
        self.create_label(hdr, "Speedy Maths", size=26, bold=True, color=BLUE).grid(
            row=0, column=0, pady=18)
        self.create_label(hdr, "Login or create an account to save your scores",
                    size=11, color=MUTED).grid(row=1, column=0, pady=(0, 12))

        tab_row = ctk.CTkFrame(self, fg_color="transparent")
        tab_row.grid(row=1, column=0, pady=(18, 0))

        self._login_tab_btn = ctk.CTkButton(
            tab_row, text="Login",
            command=lambda: self.switch_authentication_mode("login"),
            fg_color=BLUE, text_color=WHITE,
            hover_color=self.lighten_color(BLUE),
            font=("Time New Roman", self.scale_value(13), "bold"),
            corner_radius=8, width=self.scale_value(120), height=self.scale_value(36),
            border_width=1, border_color=BLUE,
        )
        self._login_tab_btn.pack(side="left", padx=4)
        self._scalable.append((self._login_tab_btn, "Time New Roman", 13, "bold"))

        self._reg_tab_btn = ctk.CTkButton(
            tab_row, text="Sign Up",
            command=lambda: self.switch_authentication_mode("register"),
            fg_color=WHITE, text_color=BLUE,
            hover_color=self.lighten_color(WHITE),
            font=("Time New Roman", self.scale_value(13), "bold"),
            corner_radius=8, width=self.scale_value(120), height=self.scale_value(36),
            border_width=1, border_color=BLUE,
        )
        self._reg_tab_btn.pack(side="left", padx=4)
        self._scalable.append((self._reg_tab_btn, "Time New Roman", 13, "bold"))

        card = ctk.CTkFrame(self, fg_color=CARD, corner_radius=14)
        card.grid(row=2, column=0, padx=60, pady=16, sticky="nsew")
        card.grid_columnconfigure(0, weight=1)
        self._form_card = card

        self.build_login_form()

        self.create_button(
            self, "Continue as Guest", self.login_as_guest,
            fg=WHITE, text_color=MUTED, width=180, height=36,
        ).grid(row=3, column=0, pady=(0, 18))

    def build_login_form(self):
        for w in self._form_card.winfo_children():
            w.destroy()

        card = self._form_card
        card.grid_columnconfigure(0, weight=1)

        if self._mode == "login":
            title_text = "Welcome back!"
            btn_text = "Log In"
            btn_cmd = self.perform_login
        else:
            title_text = "Create account"
            btn_text = "Sign Up"
            btn_cmd = self.perform_registration

        self.create_label(card, title_text, size=16, bold=True, color=BLUE).grid(
            row=0, column=0, pady=(18, 8))

        self.create_label(card, "Username", size=12, color=MUTED).grid(
            row=1, column=0, padx=30, pady=(4, 2), sticky="w")
        self.username_entry = self.create_entry(card, "Enter username")
        self.username_entry.grid(row=2, column=0, padx=30, pady=(0, 8))
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus())

        self.create_label(card, "Password", size=12, color=MUTED).grid(
            row=3, column=0, padx=30, pady=(4, 2), sticky="w")
        self.password_entry = self.create_entry(card, "Enter password", show="*")
        self.password_entry.grid(row=4, column=0, padx=30, pady=(0, 8))
        self.password_entry.bind("<Return>", lambda e: btn_cmd())

        self._show_pw = False
        self._pw_toggle = ctk.CTkButton(
            card, text="Show password",
            command=self.toggle_password_visibility,
            fg_color=WHITE, text_color=BLUE,
            hover_color=self.lighten_color(WHITE),
            font=("Time New Roman", self.scale_value(11), "normal"),
            width=self.scale_value(140), height=self.scale_value(24),
            border_width=1, border_color=BLUE,
            corner_radius=4,
        )
        self._pw_toggle.grid(row=5, column=0, padx=30, pady=(0, 4), sticky="w")
        self._scalable.append((self._pw_toggle, "Time New Roman", 11, "normal"))

        self.msg_label = self.create_label(card, "", size=12, color=RED)
        self.msg_label.grid(row=6, column=0, pady=(2, 4))

        self.create_button(card, btn_text, btn_cmd, width=200, height=44).grid(
            row=7, column=0, pady=(4, 18))

    def toggle_password_visibility(self):
        self._show_pw = not self._show_pw
        if self._show_pw:
            self.password_entry.configure(show="")
            self._pw_toggle.configure(text="Hide password")
        else:
            self.password_entry.configure(show="*")
            self._pw_toggle.configure(text="Show password")

    def switch_authentication_mode(self, mode):
        self._mode = mode
        if mode == "login":
            self._login_tab_btn.configure(fg_color=BLUE, text_color=WHITE)
            self._reg_tab_btn.configure(fg_color=WHITE, text_color=BLUE)
        else:
            self._login_tab_btn.configure(fg_color=WHITE, text_color=BLUE)
            self._reg_tab_btn.configure(fg_color=BLUE, text_color=WHITE)
        self.build_login_form()

    def perform_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            self.msg_label.configure(text="Please fill in both fields", text_color=RED)
            return

        success, result = auth.login(username, password)
        if success:
            self.app.current_user = username
            self.app.session_token = result
            self.app.show_menu()
        else:
            self.msg_label.configure(text=f"{result}", text_color=RED)

    def perform_registration(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            self.msg_label.configure(text="Please fill in both fields", text_color=RED)
            return

        success, result = auth.register(username, password)
        if success:
            self.app.current_user = username
            self.app.session_token = result
            self.msg_label.configure(text="Account created!", text_color=GREEN)
            self.after(800, self.app.show_menu)
        else:
            self.msg_label.configure(text=f"{result}", text_color=RED)

    def login_as_guest(self):
        self.app.current_user = None
        self.app.session_token = None
        self.app.show_menu()
