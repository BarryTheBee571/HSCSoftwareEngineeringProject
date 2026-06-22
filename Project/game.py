import customtkinter as ctk
import time
from questions import make_question
from styles import BLUE, GREEN, RED, WHITE, CARD, MUTED

class GameFrame(ctk.CTkFrame):
    """Main gameplay screen where questions are asked and scored."""
    def __init__(self, app, mode, difficulty, time_limit=30):
        super().__init__(app, fg_color=WHITE, corner_radius=0)  # base frame setup
        self.app = app  # app reference for navigation
        self.mode = mode  # math mode selection
        self.difficulty = difficulty  # selected difficulty
        self.time_limit = time_limit  # timer length in seconds
        self.unlimited = time_limit < 0  # -1 means endless mode
        self.scalable = []  # widgets that need font scaling
        self.timer_id = None  # after() id for timer callback
        self.score = 0  # points in current run
        self.questions_answered = 0  # total answered in this run
        self.correct_answers = 0  # correct answers in this run
        self.current_streak = 0  # current correct streak
        self.best_streak = 0  # best streak this run
        self.start_time = time.time()  # run start timestamp
        self.current_answer = None  # expected answer for current question

        self.setup_ui()  # build screen widgets
        self.next_question()  # load first question
        self.tick_timer()  # start timer updates

    def scale_value(self, base):
        return self.app.scale_value(base)  # delegate scaling to app

    def refresh_scaling(self):
        for widget, family, base_size, weight in self.scalable:
            try:
                widget.configure(font=(family, max(8, self.scale_value(base_size)), weight))  # resize font
            except Exception:
                pass  # skip widgets that cannot be reconfigured

    def make_label(self, parent, text, size=14, bold=False, color=WHITE, **kw):
        weight = "bold" if bold else "normal"  # map bool to tk weight
        lbl = ctk.CTkLabel(
            parent, text=text,
            font=("Comic Sans MS", self.scale_value(size), weight),
            text_color=color, **kw,
        )
        self.scalable.append((lbl, "Comic Sans MS", size, weight))  # track for resizing
        return lbl  # hand label back to caller

    def make_button(self, parent, text, cmd, fg=BLUE, text_color=WHITE, width=180, height=44):
        btn = ctk.CTkButton(
            parent, text=text, command=cmd,
            fg_color=fg,
            text_color=text_color,
            font=("Comic Sans MS", self.scale_value(15), "bold"),
            corner_radius=10, width=self.scale_value(width), height=self.scale_value(height),
        )
        self.scalable.append((btn, "Comic Sans MS", 15, "bold"))  # track for resizing
        return btn  # hand button back

    def setup_ui(self):
        """Build all widgets for the game screen."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=2)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)
        self.grid_rowconfigure(4, weight=1)

        sb = ctk.CTkFrame(self, fg_color=CARD, corner_radius=0)  # top status bar
        sb.grid(row=0, column=0, sticky="ew")
        sb.grid_columnconfigure(0, weight=0)
        sb.grid_columnconfigure(1, weight=1)
        sb.grid_columnconfigure(2, weight=1)

        back_btn = ctk.CTkButton(
            sb, text="Menu", command=self.back_to_menu,
            fg_color=WHITE, text_color=BLUE,
            font=("Comic Sans MS", self.scale_value(11), "normal"),
            border_width=1, border_color=BLUE,
            corner_radius=6, width=self.scale_value(60), height=self.scale_value(32),)
        back_btn.grid(row=0, column=0, padx=8, pady=8)
        self.scalable.append((back_btn, "Comic Sans MS", 11, "normal"))

        left = ctk.CTkFrame(sb, fg_color="transparent")  # timer column
        left.grid(row=0, column=1, padx=20, pady=10)
        self.make_label(left, "TIME", size=11, color=MUTED).pack()
        self.timer_label = self.make_label(left, "30", size=28, bold=True, color=RED)
        self.timer_label.pack()

        right = ctk.CTkFrame(sb, fg_color="transparent")  # score column
        right.grid(row=0, column=2, padx=20, pady=10)
        self.make_label(right, "SCORE", size=11, color=MUTED).pack()
        self.score_label = self.make_label(right, "0", size=28, bold=True, color=BLUE)
        self.score_label.pack()

        qc = ctk.CTkFrame(self, fg_color=CARD, corner_radius=16)  # question card
        qc.grid(row=1, column=0, padx=50, pady=(24, 0), sticky="nsew")
        qc.grid_columnconfigure(0, weight=1)
        qc.grid_rowconfigure(0, weight=1)
        qc.grid_rowconfigure(1, weight=1)

        self.make_label(qc, "What is", size=13, color=MUTED).grid(
            row=0, column=0, pady=(14, 0))
        self.question_label = self.make_label(qc, "", size=46, bold=True, color=BLUE)
        self.question_label.grid(row=1, column=0, pady=(0, 14))

        self.answer_entry = ctk.CTkEntry(  # answer input box
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
        self.scalable.append((self.answer_entry, "Comic Sans MS", 28, "bold"))

        controls = ctk.CTkFrame(self, fg_color="transparent")  # submit/end row
        controls.grid(row=3, column=0)
        controls.grid_columnconfigure(0, weight=1)
        controls.grid_columnconfigure(1, weight=1)

        self.make_button(controls, "Submit", self.submit_answer,
                  width=160, height=44).grid(row=0, column=0, padx=(0, 8))

        if self.unlimited:  # only show in endless mode
            self.make_button(controls, "End Game", self.end_game,
                      fg=RED, width=160, height=44).grid(row=0, column=1)

        self.feedback_label = self.make_label(self, "", size=15, bold=True, color=WHITE)
        self.feedback_label.grid(row=4, column=0, pady=(8, 0))

    def tick_timer(self):
        """Update timer display and end game when time runs out."""
        elapsed = time.time() - self.start_time  # seconds since run start
        if self.unlimited:
            secs = int(elapsed)  # count up in endless mode
            self.timer_label.configure(text=str(secs), text_color=GREEN)
            self.timer_id = self.after(200, self.tick_timer)  # schedule next tick
            return

        # Timed modes count down from selected time.
        remaining = self.time_limit - elapsed
        if remaining <= 0:
            self.timer_label.configure(text="0")  # clamp display to zero
            self.end_game()  # stop and go to results
            return
        secs = int(remaining)  # whole seconds left
        colour = RED if secs <= 10 else (MUTED if secs <= 20 else GREEN)  # color urgency
        self.timer_label.configure(text=str(secs), text_color=colour)
        self.timer_id = self.after(200, self.tick_timer)  # continue ticking

    def next_question(self):
        """Load and show the next generated question."""
        question, self.current_answer = make_question(self.mode, self.difficulty)  # new question + answer
        self.question_label.configure(text=f"{question} =")
        self.answer_entry.delete(0, "end")
        self.answer_entry.focus()

    def submit_answer(self, event=None):
        """Check typed answer, update stats, then move to next question."""
        if not self.unlimited and time.time() - self.start_time >= self.time_limit:
            return  # ignore late submits after timer end

        raw = self.answer_entry.get().strip()  # read input text

        # Keep input simple: whole numbers only.
        if not raw.lstrip("-").isdigit():
            self.feedback_label.configure(
                text="Enter a whole number!", text_color=BLUE)
            return

        self.questions_answered += 1  # every valid numeric input counts
        if int(raw) == self.current_answer:
            self.correct_answers += 1  # increment correct count
            self.score += 10  # add points for correct answer
            self.current_streak += 1  # grow streak
            if self.current_streak > self.best_streak:
                self.best_streak = self.current_streak  # update personal run best
            self.feedback_label.configure(text="Correct!", text_color=GREEN)
        else:
            self.current_streak = 0  # reset streak on wrong answer
            self.feedback_label.configure(
                text=f"Wrong, answer was {self.current_answer}", text_color=RED)

        self.score_label.configure(text=str(self.score))  # refresh score display
        self.next_question()  # move to next question immediately

    def back_to_menu(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)  # stop timer callback
            self.timer_id = None  # clear stored callback id
        self.app.show_menu()  # navigate away

    def end_game(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)  # stop timer callback
            self.timer_id = None  # clear stored callback id

        elapsed_seconds = time.time() - self.start_time  # final run duration

        self.app.show_results(  # pass run summary to results page
            self.score,
            self.correct_answers,
            self.questions_answered,
            self.mode,
            self.difficulty,
            self.time_limit,
            elapsed_seconds,
            self.best_streak,
        )
