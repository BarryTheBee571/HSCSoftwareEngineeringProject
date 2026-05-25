import customtkinter as ctk
import random
import time

BASE_W, BASE_H = 620, 540
MIN_W,  MIN_H  = 480, 400

def generate_question(mode, difficulty):
    ranges = {"easy": (1, 10), "medium": (1, 20), "hard": (1, 50)}
    lo, hi = ranges[difficulty]

    if mode == "mixed":
        mode = random.choice(["addition", "subtraction", "multiplication", "division"])

    if mode == "addition":
        answer = random.randint(lo * 2, hi * 2)
        a      = random.randint(lo, answer - lo)
        b      = answer - a
        return f"{a}  +  {b}", answer

    elif mode == "subtraction":
        answer = random.randint(lo, hi)
        b      = random.randint(lo, hi)
        a      = answer + b
        return f"{a}  −  {b}", answer

    elif mode == "multiplication":
        answer  = random.randint(lo, hi)
        factors = [i for i in range(lo, min(hi, 12) + 1) if answer % i == 0]
        if factors:
            a = random.choice(factors)
            b = answer // a
        else:
            a      = random.randint(lo, min(hi, 12))
            b      = random.randint(lo, min(hi, 12))
            answer = a * b
        return f"{a}  ×  {b}", answer

    elif mode == "division":
        answer = random.randint(lo, hi)
        b      = random.randint(max(1, lo), min(hi, 12))
        a      = answer * b
        return f"{a}  ÷  {b}", answer

BLUE  = "#0c2752"
GREEN = "#33813c"
RED   = "#e05353"
WHITE = "#F7F9FC"
CARD  = "#a7bbdb"
MUTED = "#3A3A3A"

class MathsSpeedGame(ctk.CTk):
    TIME_LIMIT = 30

    def __init__(self):
        super().__init__()
        self.title("Speedy Maths")
        self.geometry(f"{BASE_W}x{BASE_H}")
        self.minsize(MIN_W, MIN_H)
        self.resizable(True, True)
        self.configure(fg_color=WHITE)
        ctk.set_appearance_mode("light")

        self.mode       = ctk.StringVar(value="mixed")
        self.difficulty = ctk.StringVar(value="easy")
        self._timer_id  = None
        self._scalable  = []
        self._resize_id = None

        self.bind("<Configure>", self._on_resize)
        self._show_menu()

    def _sf(self):
        w, h = self.winfo_width(), self.winfo_height()
        if w < 10 or h < 10:
            return 1.0
        return min(w / BASE_W, h / BASE_H)

    def _s(self, base):
        return max(1, int(base * self._sf()))

    def _on_resize(self, event):
        if event.widget is not self:
            return
        if self._resize_id:
            self.after_cancel(self._resize_id)
        self._resize_id = self.after(50, self._apply_scale)

    def _apply_scale(self):
        sf = self._sf()
        for widget, family, base_size, weight in self._scalable:
            try:
                widget.configure(font=(family, max(8, int(base_size * sf)), weight))
            except Exception:
                pass

    def _label(self, parent, text, size=14, bold=False, color=WHITE, **kw):
        weight = "bold" if bold else "normal"
        lbl = ctk.CTkLabel(
            parent, text=text,
            font=("Trebuchet MS", self._s(size), weight),
            text_color=color, **kw,
        )
        self._scalable.append((lbl, "Trebuchet MS", size, weight))
        return lbl

    def _btn(self, parent, text, cmd, fg=BLUE, text_color=WHITE, width=180, height=44):
        btn = ctk.CTkButton(
            parent, text=text, command=cmd,
            fg_color=fg, hover_color=self._lighten(fg),
            text_color=text_color,
            font=("Trebuchet MS", self._s(15), "bold"),
            corner_radius=10, width=self._s(width), height=self._s(height),
        )
        self._scalable.append((btn, "Trebuchet MS", 15, "bold"))
        return btn

    def _toggle_row(self, parent, options, variable):
        buttons = {}

        def select(val):
            variable.set(val)
            for v, b in buttons.items():
                active = (v == val)
                b.configure(
                    fg_color=BLUE    if active else WHITE,
                    text_color=WHITE if active else BLUE,
                    hover_color=self._lighten(BLUE) if active else self._lighten(WHITE),
                )

        for col, (label, val) in enumerate(options):
            active = variable.get() == val
            btn = ctk.CTkButton(
                parent, text=label,
                command=lambda v=val: select(v),
                fg_color=BLUE    if active else WHITE,
                text_color=WHITE if active else BLUE,
                hover_color=self._lighten(BLUE) if active else self._lighten(WHITE),
                font=("Trebuchet MS", self._s(12), "normal"),
                corner_radius=8, height=self._s(36),
                border_width=1, border_color=BLUE,
            )
            btn.grid(row=0, column=col, padx=3, pady=4, sticky="ew")
            parent.grid_columnconfigure(col, weight=1)
            self._scalable.append((btn, "Trebuchet MS", 12, "normal"))
            buttons[val] = btn

        return buttons

    @staticmethod
    def _lighten(hex_color):
        r = min(255, int(hex_color[1:3], 16) + 30)
        g = min(255, int(hex_color[3:5], 16) + 30)
        b = min(255, int(hex_color[5:7], 16) + 30)
        return f"#{r:02x}{g:02x}{b:02x}"

    def _clear(self):
        if self._timer_id:
            self.after_cancel(self._timer_id)
            self._timer_id = None
        self._scalable.clear()
        for w in self.winfo_children():
            w.destroy()
        for i in range(10):
            self.grid_rowconfigure(i, weight=0, minsize=0)
        self.grid_columnconfigure(0, weight=0)

    def _show_menu(self):
        self._clear()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=0)

        hdr = ctk.CTkFrame(self, fg_color=CARD, corner_radius=0)
        hdr.grid(row=0, column=0, sticky="ew")
        self._label(hdr, "Speedy Maths", size=26, bold=True, color=BLUE).pack(pady=18, padx=20)

        self._label(
            self, "Answer as many questions as you can in 30 seconds!",
            size=13, color=MUTED,
        ).grid(row=1, column=0, pady=(14, 0))

        mc = ctk.CTkFrame(self, fg_color=CARD, corner_radius=12)
        mc.grid(row=2, column=0, padx=40, pady=(12, 6), sticky="nsew")
        mc.grid_columnconfigure(0, weight=1)
        mc.grid_rowconfigure(1, weight=1)

        self._label(mc, "Game Mode", size=14, bold=True, color=BLUE).grid(
            row=0, column=0, padx=20, pady=(12, 4), sticky="w")

        mode_row = ctk.CTkFrame(mc, fg_color="transparent")
        mode_row.grid(row=1, column=0, padx=14, pady=(0, 12), sticky="nsew")

        MODES = [
            ("Addition",    "addition"),
            ("Subtraction", "subtraction"),
            ("Multiply",    "multiplication"),
            ("Division",    "division"),
            ("Mixed",       "mixed"),
        ]
        self._toggle_row(mode_row, MODES, self.mode)

        dc = ctk.CTkFrame(self, fg_color=CARD, corner_radius=12)
        dc.grid(row=3, column=0, padx=40, pady=6, sticky="nsew")
        dc.grid_columnconfigure(0, weight=1)
        dc.grid_rowconfigure(1, weight=1)

        self._label(dc, "Difficulty", size=14, bold=True, color=BLUE).grid(
            row=0, column=0, padx=20, pady=(12, 4), sticky="w")

        diff_row = ctk.CTkFrame(dc, fg_color="transparent")
        diff_row.grid(row=1, column=0, padx=14, pady=(0, 12), sticky="nsew")

        DIFFS = [
            ("Easy  (1–10)",   "easy"),
            ("Medium  (1–20)", "medium"),
            ("Hard  (1–50)",   "hard"),
        ]
        self._toggle_row(diff_row, DIFFS, self.difficulty)

        self._btn(self, "Start Game", self._start_game,
                  width=220, height=50).grid(row=4, column=0, pady=20)

    def _start_game(self):
        self._clear()
        self.score              = 0
        self.questions_answered = 0
        self.correct_answers    = 0
        self.start_time         = time.time()
        self.current_answer     = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=2)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)
        self.grid_rowconfigure(4, weight=1)

        sb = ctk.CTkFrame(self, fg_color=CARD, corner_radius=0)
        sb.grid(row=0, column=0, sticky="ew")
        sb.grid_columnconfigure(0, weight=0)
        sb.grid_columnconfigure(1, weight=1)
        sb.grid_columnconfigure(2, weight=1)

        back_btn = ctk.CTkButton(
            sb, text="← Back", command=self._show_menu,
            fg_color="transparent", text_color=BLUE,
            hover_color=self._lighten(WHITE),
            font=("Trebuchet MS", self._s(11), "normal"),
            corner_radius=6, width=self._s(60), height=self._s(32),
        )
        back_btn.grid(row=0, column=0, padx=8, pady=8)
        self._scalable.append((back_btn, "Trebuchet MS", 11, "normal"))

        left = ctk.CTkFrame(sb, fg_color="transparent")
        left.grid(row=0, column=1, padx=20, pady=10)
        self._label(left, "⏱  TIME", size=11, color=MUTED).pack()
        self.timer_label = self._label(left, "30", size=28, bold=True, color=RED)
        self.timer_label.pack()

        right = ctk.CTkFrame(sb, fg_color="transparent")
        right.grid(row=0, column=2, padx=20, pady=10)
        self._label(right, "SCORE", size=11, color=MUTED).pack()
        self.score_label = self._label(right, "0", size=28, bold=True, color=BLUE)
        self.score_label.pack()

        qc = ctk.CTkFrame(self, fg_color=CARD, corner_radius=16)
        qc.grid(row=1, column=0, padx=50, pady=(24, 0), sticky="nsew")
        qc.grid_columnconfigure(0, weight=1)
        qc.grid_rowconfigure(0, weight=1)
        qc.grid_rowconfigure(1, weight=1)

        self._label(qc, "What is…", size=13, color=MUTED).grid(
            row=0, column=0, pady=(14, 0))
        self.question_label = self._label(qc, "", size=46, bold=True, color=BLUE)
        self.question_label.grid(row=1, column=0, pady=(0, 14))

        self.answer_entry = ctk.CTkEntry(
            self,
            font=("Trebuchet MS", self._s(28), "bold"),
            width=self._s(200), height=self._s(55),
            justify="center",
            fg_color=CARD, border_color=BLUE, border_width=2,
            text_color=BLUE, placeholder_text="?",
            placeholder_text_color=MUTED,
        )
        self.answer_entry.grid(row=2, column=0, pady=16)
        self.answer_entry.bind("<Return>", self._submit)
        self.answer_entry.focus()
        self._scalable.append((self.answer_entry, "Trebuchet MS", 28, "bold"))

        self._btn(self, "Submit  ↵", self._submit,
                  width=160, height=44).grid(row=3, column=0)

        self.feedback_label = self._label(self, "", size=15, bold=True, color=WHITE)
        self.feedback_label.grid(row=4, column=0, pady=(8, 0))

        self._next_question()
        self._tick()

    def _tick(self):
        elapsed   = time.time() - self.start_time
        remaining = self.TIME_LIMIT - elapsed
        if remaining <= 0:
            self.timer_label.configure(text="0")
            self._end_game()
            return
        secs   = int(remaining)
        colour = RED if secs <= 10 else (MUTED if secs <= 20 else GREEN)
        self.timer_label.configure(text=str(secs), text_color=colour)
        self._timer_id = self.after(200, self._tick)

    def _next_question(self):
        question, self.current_answer = generate_question(
            self.mode.get(), self.difficulty.get()
        )
        self.question_label.configure(text=f"{question}  =")
        self.answer_entry.delete(0, "end")
        self.answer_entry.focus()

    def _submit(self, event=None):
        if time.time() - self.start_time >= self.TIME_LIMIT:
            return
        raw = self.answer_entry.get().strip()
        if not raw.lstrip("-").isdigit():
            self.feedback_label.configure(
                text="⚠  Enter a whole number!", text_color=BLUE)
            return
        self.questions_answered += 1
        if int(raw) == self.current_answer:
            self.correct_answers += 1
            self.score           += 10
            self.feedback_label.configure(text="✓  Correct!", text_color=GREEN)
        else:
            self.feedback_label.configure(
                text=f"✗  Wrong — answer was {self.current_answer}", text_color=RED)
        self.score_label.configure(text=str(self.score))
        self._next_question()

    def _end_game(self):
        if self._timer_id:
            self.after_cancel(self._timer_id)
            self._timer_id = None

        accuracy = (self.correct_answers / self.questions_answered * 100) \
                   if self.questions_answered else 0
        self._clear()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)

        hdr = ctk.CTkFrame(self, fg_color=CARD, corner_radius=0)
        hdr.grid(row=0, column=0, sticky="ew")
        self._label(hdr, "Round Over!", size=26, bold=True, color=BLUE).pack(pady=18)

        sc = ctk.CTkFrame(self, fg_color=CARD, corner_radius=14)
        sc.grid(row=1, column=0, padx=60, pady=24, sticky="nsew")
        sc.grid_columnconfigure(0, weight=1)

        stats = [
            ("Score",             f"{self.score} pts",          BLUE),
            ("Questions Answered", str(self.questions_answered),  BLUE),
            ("Correct Answers",    str(self.correct_answers),     GREEN),
            ("Accuracy",           f"{accuracy:.1f}%",
             GREEN if accuracy >= 70 else RED),
        ]

        for i, (lbl, val, val_color) in enumerate(stats):
            row = ctk.CTkFrame(sc, fg_color="transparent")
            row.grid(row=i * 2, column=0, padx=30, pady=8, sticky="ew")
            self._label(row, lbl, size=15, color=MUTED).pack(side="left")
            self._label(row, val, size=16, bold=True, color=val_color).pack(side="right")
            if i < len(stats) - 1:
                ctk.CTkFrame(sc, fg_color=WHITE, height=1).grid(
                    row=i * 2 + 1, column=0, padx=30, sticky="ew")

        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.grid(row=2, column=0, pady=20)

        self._btn(btn_row, "▶  Play Again", self._start_game,
                  width=165, height=46).pack(side="left", padx=10)
        self._btn(btn_row, "☰  Main Menu", self._show_menu,
                  fg=CARD, text_color=BLUE, width=165, height=46).pack(side="left", padx=10)

MathsSpeedGame().mainloop()