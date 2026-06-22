import customtkinter as ctk
import auth
from styles import BLUE, GREEN, RED, WHITE, CARD, MUTED

class LoginFrame(ctk.CTkFrame):
    """Login/register page with optional guest mode."""

    def __init__(self, app):
        super().__init__(app, fg_color=WHITE, corner_radius=0)  # base frame init
        self.app = app  # app reference for navigation
        self._scalable = []  # widgets that need font scaling
        self._mode = "login"  # current tab: login/register

        self.setup_ui()  # build page widgets

    def scale_value(self, base):
        return self.app.scale_value(base)  # delegate scaling to app

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
            font=("Comic Sans MS", self.scale_value(14), "bold"),
            corner_radius=10, width=self.scale_value(width), height=self.scale_value(height),
        )
        self._scalable.append((btn, "Comic Sans MS", 14, "bold"))  # track for resize
        return btn  # return built button

    def make_entry(self, parent, placeholder, show=""):
        entry = ctk.CTkEntry(
            parent,
            font=("Comic Sans MS", self.scale_value(13), "normal"),
            width=self.scale_value(260), height=self.scale_value(42),
            fg_color=WHITE, border_color=BLUE, border_width=2,
            text_color=BLUE, placeholder_text=placeholder,
            placeholder_text_color=MUTED,
            show=show,
            corner_radius=8,
        )
        self._scalable.append((entry, "Comic Sans MS", 13, "normal"))  # track for resize
        return entry  # return built entry

    def setup_ui(self):
        """Build static parts of the login page."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=0)

        hdr = ctk.CTkFrame(self, fg_color=CARD, corner_radius=0)  # top banner
        hdr.grid(row=0, column=0, sticky="ew")
        hdr.grid_columnconfigure(0, weight=1)
        self.make_label(hdr, "Speedy Maths", size=26, bold=True, color=BLUE).grid(
            row=0, column=0, pady=18)
        self.make_label(hdr, "Login or create an account to save your scores",
                    size=11, color=MUTED).grid(row=1, column=0, pady=(0, 12))

        tab_row = ctk.CTkFrame(self, fg_color="transparent")  # login/register tabs row
        tab_row.grid(row=1, column=0, pady=(18, 0))

        self._login_tab_btn = ctk.CTkButton(
            tab_row, text="Login",
            command=lambda: self.switch_mode("login"),
            fg_color=BLUE, text_color=WHITE,
            font=("Comic Sans MS", self.scale_value(13), "bold"),
            corner_radius=8, width=self.scale_value(120), height=self.scale_value(36),
            border_width=1, border_color=BLUE,
        )
        self._login_tab_btn.pack(side="left", padx=4)
        self._scalable.append((self._login_tab_btn, "Comic Sans MS", 13, "bold"))

        self._reg_tab_btn = ctk.CTkButton(
            tab_row, text="Sign Up",
            command=lambda: self.switch_mode("register"),
            fg_color=WHITE, text_color=BLUE,
            font=("Comic Sans MS", self.scale_value(13), "bold"),
            corner_radius=8, width=self.scale_value(120), height=self.scale_value(36),
            border_width=1, border_color=BLUE,
        )
        self._reg_tab_btn.pack(side="left", padx=4)
        self._scalable.append((self._reg_tab_btn, "Comic Sans MS", 13, "bold"))

        card = ctk.CTkFrame(self, fg_color=CARD, corner_radius=14)  # form card
        card.grid(row=2, column=0, padx=60, pady=16, sticky="nsew")
        card.grid_columnconfigure(0, weight=1)
        self._form_card = card  # store to rebuild later

        self.setup_login_form()  # create current tab form

        self.make_button(
            self, "Continue as Guest", self.use_guest_mode,
            fg=WHITE, text_color=MUTED, width=180, height=36,
        ).grid(row=3, column=0, pady=(0, 18))

    def setup_login_form(self):
        """Rebuild the card form when switching between login/register."""
        for w in self._form_card.winfo_children():
            w.destroy()  # clear old form widgets

        card = self._form_card  # local alias
        card.grid_columnconfigure(0, weight=1)

        if self._mode == "login":
            title_text = "Welcome back!"  # login heading
            btn_text = "Log In"  # login button label
            btn_cmd = self.try_login  # login callback
        else:
            title_text = "Create account"  # register heading
            btn_text = "Sign Up"  # register button label
            btn_cmd = self.try_register  # register callback

        self.make_label(card, title_text, size=16, bold=True, color=BLUE).grid(
            row=0, column=0, pady=(18, 8))

        self.make_label(card, "Username", size=12, color=MUTED).grid(
            row=1, column=0, padx=30, pady=(4, 2), sticky="w")
        self.username_entry = self.make_entry(card, "Enter username")
        self.username_entry.grid(row=2, column=0, padx=30, pady=(0, 8))
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus())

        self.make_label(card, "Password", size=12, color=MUTED).grid(
            row=3, column=0, padx=30, pady=(4, 2), sticky="w")
        self.password_entry = self.make_entry(card, "Enter password", show="*")
        self.password_entry.grid(row=4, column=0, padx=30, pady=(0, 8))
        self.password_entry.bind("<Return>", lambda e: btn_cmd())

        self._show_pw = False  # password hidden by default
        self._pw_toggle = ctk.CTkButton(
            card, text="Show password",
            command=self.toggle_password,
            fg_color=WHITE, text_color=BLUE,
            font=("Comic Sans MS", self.scale_value(11), "normal"),
            width=self.scale_value(140), height=self.scale_value(24),
            border_width=1, border_color=BLUE,
            corner_radius=4,
        )
        self._pw_toggle.grid(row=5, column=0, padx=30, pady=(0, 4), sticky="w")
        self._scalable.append((self._pw_toggle, "Comic Sans MS", 11, "normal"))

        self.msg_label = self.make_label(card, "", size=12, color=RED)
        self.msg_label.grid(row=6, column=0, pady=(2, 4))

        self.make_button(card, btn_text, btn_cmd, width=200, height=44).grid(
            row=7, column=0, pady=(4, 18))

    def toggle_password(self):
        """Show or hide password text in the entry box."""
        self._show_pw = not self._show_pw  # flip visibility flag
        if self._show_pw:
            self.password_entry.configure(show="")  # show real text
            self._pw_toggle.configure(text="Hide password")  # update button label
        else:
            self.password_entry.configure(show="*")  # mask text again
            self._pw_toggle.configure(text="Show password")  # update button label

    def switch_mode(self, mode):
        """Switch between login and register tabs."""
        self._mode = mode  # save selected tab
        if mode == "login":
            self._login_tab_btn.configure(fg_color=BLUE, text_color=WHITE)  # active style
            self._reg_tab_btn.configure(fg_color=WHITE, text_color=BLUE)  # inactive style
        else:
            self._login_tab_btn.configure(fg_color=WHITE, text_color=BLUE)  # inactive style
            self._reg_tab_btn.configure(fg_color=BLUE, text_color=WHITE)  # active style
        self.setup_login_form()  # rebuild fields + button callback

    def try_login(self):
        """Attempt login and open menu on success."""
        username = self.username_entry.get().strip()  # read username input
        password = self.password_entry.get()  # read password input

        if not username or not password:
            self.msg_label.configure(text="Please fill in both fields", text_color=RED)  # validation msg
            return

        success, result = auth.login(username, password)  # auth check
        if success:
            self.app.current_user = username  # store active user
            self.app.session_token = result  # store session token
            self.app.show_menu()  # go to menu on success
        else:
            self.msg_label.configure(text=f"{result}", text_color=RED)  # show auth error

    def try_register(self):
        """Attempt account creation and continue to menu on success."""
        username = self.username_entry.get().strip()  # read username input
        password = self.password_entry.get()  # read password input

        if not username or not password:
            self.msg_label.configure(text="Please fill in both fields", text_color=RED)  # validation msg
            return

        success, result = auth.register(username, password)  # attempt account create
        if success:
            self.app.current_user = username  # store active user
            self.app.session_token = result  # store session token
            self.msg_label.configure(text="Account created!", text_color=GREEN)  # success msg
            self.after(800, self.app.show_menu)  # short delay then continue
        else:
            self.msg_label.configure(text=f"{result}", text_color=RED)  # show register error

    def use_guest_mode(self):
        """Skip auth and continue as a guest session."""
        self.app.current_user = None  # guest has no account id
        self.app.session_token = None  # guest has no token
        self.app.show_menu()  # continue straight to menu