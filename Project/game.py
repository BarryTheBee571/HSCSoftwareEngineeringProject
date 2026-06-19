import customtkinter as ctk
import time
from questions import generate_question
from styles import BLUE, GREEN, RED, WHITE, CARD, MUTED

class GameFrame(ctk.CTkFrame):
    def __init__(self, app, mode, difficulty, time_limit=30):
        super().__init__(app, fg_color=WHITE, corner_radius=0)
        self.app = app
        self.mode = mode
        self.difficulty = difficulty
        self.time_limit = time_limit
        self.unlimited = time_limit < 0
        self._scalable = []
        self._timer_id = None
        self.score = 0
        self.questions_answered = 0
        self.correct_answers = 0
        self.current_streak = 0
        self.best_streak = 0
        self.start_time = time.time()
        self.current_answer = None

        self.build_ui()
        self.load_next_question()
        self.update_timer()

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
            font=("Comic Sans MS", self.scale_value(size), weight),
            text_color=color, **kw,
        )
        self._scalable.append((lbl, "Comic Sans MS", size, weight))
        return lbl

    def create_button(self, parent, text, cmd, fg=BLUE, text_color=WHITE, width=180, height=44):
        btn = ctk.CTkButton(
            parent, text=text, command=cmd,
            fg_color=fg, hover_color=self.lighten_color(fg),
            text_color=text_color,
            font=("Comic Sans MS", self.scale_value(15), "bold"),
            corner_radius=10, width=self.scale_value(width), height=self.scale_value(height),
        )
        self._scalable.append((btn, "Comic Sans MS", 15, "bold"))
        return btn

    def build_ui(self):
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
            sb, text="Menu", command=self.go_back_to_menu,
            fg_color=WHITE, text_color=BLUE,
            hover_color=self.lighten_color(WHITE),
            font=("Comic Sans MS", self.scale_value(11), "normal"),
            border_width=1, border_color=BLUE,
            corner_radius=6, width=self.scale_value(60), height=self.scale_value(32),
        )
        back_btn.grid(row=0, column=0, padx=8, pady=8)
        self._scalable.append((back_btn, "Comic Sans MS", 11, "normal"))

        left = ctk.CTkFrame(sb, fg_color="transparent")
        left.grid(row=0, column=1, padx=20, pady=10)
        self.create_label(left, "TIME", size=11, color=MUTED).pack()
        self.timer_label = self.create_label(left, "30", size=28, bold=True, color=RED)
        self.timer_label.pack()

        right = ctk.CTkFrame(sb, fg_color="transparent")
        right.grid(row=0, column=2, padx=20, pady=10)
        self.create_label(right, "SCORE", size=11, color=MUTED).pack()
        self.score_label = self.create_label(right, "0", size=28, bold=True, color=BLUE)
        self.score_label.pack()

        qc = ctk.CTkFrame(self, fg_color=CARD, corner_radius=16)
        qc.grid(row=1, column=0, padx=50, pady=(24, 0), sticky="nsew")
        qc.grid_columnconfigure(0, weight=1)
        qc.grid_rowconfigure(0, weight=1)
        qc.grid_rowconfigure(1, weight=1)

        self.create_label(qc, "What is", size=13, color=MUTED).grid(
            row=0, column=0, pady=(14, 0))
        self.question_label = self.create_label(qc, "", size=46, bold=True, color=BLUE)
        self.question_label.grid(row=1, column=0, pady=(0, 14))

        self.answer_entry = ctk.CTkEntry(
            self,
            font=("Comic Sans MS", self.scale_value(28), "bold"),
            width=self.scale_value(200), height=self.scale_value(55),
            justify="center",
            fg_color=CARD, border_color=BLUE, border_width=2,
            text_color=BLUE, placeholder_text="?",
            placeholder_text_color=MUTED,
        )
        self.answer_entry.grid(row=2, column=0, pady=16)
        self.answer_entry.bind("<Return>", self.submit_answer)
        self.answer_entry.focus()
        self._scalable.append((self.answer_entry, "Comic Sans MS", 28, "bold"))

        controls = ctk.CTkFrame(self, fg_color="transparent")
        controls.grid(row=3, column=0)
        controls.grid_columnconfigure(0, weight=1)
        controls.grid_columnconfigure(1, weight=1)

        self.create_button(controls, "Submit", self.submit_answer,
                  width=160, height=44).grid(row=0, column=0, padx=(0, 8))

        if self.unlimited:
            self.create_button(controls, "End Game", self.end_game,
                      fg=RED, width=160, height=44).grid(row=0, column=1)

        self.feedback_label = self.create_label(self, "", size=15, bold=True, color=WHITE)
        self.feedback_label.grid(row=4, column=0, pady=(8, 0))

    def update_timer(self):
        elapsed = time.time() - self.start_time
        if self.unlimited:
            secs = int(elapsed)
            self.timer_label.configure(text=str(secs), text_color=GREEN)
            self._timer_id = self.after(200, self.update_timer)
            return

        remaining = self.time_limit - elapsed
        if remaining <= 0:
            self.timer_label.configure(text="0")
            self.end_game()
            return
        secs = int(remaining)
        colour = RED if secs <= 10 else (MUTED if secs <= 20 else GREEN)
        self.timer_label.configure(text=str(secs), text_color=colour)
        self._timer_id = self.after(200, self.update_timer)

    def load_next_question(self):
        question, self.current_answer = generate_question(self.mode, self.difficulty)
        self.question_label.configure(text=f"{question} =")
        self.answer_entry.delete(0, "end")
        self.answer_entry.focus()

    def submit_answer(self, event=None):
        if not self.unlimited and time.time() - self.start_time >= self.time_limit:
            return

        raw = self.answer_entry.get().strip()

        if not raw.lstrip("-").isdigit():
            self.feedback_label.configure(
                text="Enter a whole number!", text_color=BLUE)
            return

        self.questions_answered += 1
        if int(raw) == self.current_answer:
            self.correct_answers += 1
            self.score += 10
            self.current_streak += 1
            if self.current_streak > self.best_streak:
                self.best_streak = self.current_streak
            self.feedback_label.configure(text="Correct!", text_color=GREEN)
        else:
            self.current_streak = 0
            self.feedback_label.configure(
                text=f"Wrong, answer was {self.current_answer}", text_color=RED)

        self.score_label.configure(text=str(self.score))
        self.load_next_question()

    def go_back_to_menu(self):
        if self._timer_id:
            self.after_cancel(self._timer_id)
            self._timer_id = None
        self.app.show_menu()

    def end_game(self):
        if self._timer_id:
            self.after_cancel(self._timer_id)
            self._timer_id = None

        elapsed_seconds = time.time() - self.start_time

        self.app.show_results(
            self.score,
            self.correct_answers,
            self.questions_answered,
            self.mode,
            self.difficulty,
            self.time_limit,
            elapsed_seconds,
            self.best_streak,
        )
