import customtkinter as ctk
import auth
from styles import BASE_W, BASE_H, MIN_W, MIN_H, WHITE

class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Speedy Maths")
        self.geometry(f"{BASE_W}x{BASE_H}")
        self.minsize(MIN_W, MIN_H)
        self.resizable(True, True)
        self.configure(fg_color=WHITE)
        ctk.set_appearance_mode("light")

        self.current_user = None
        self.session_token = None

        self._current_frame = None
        self._resize_id = None

        self.bind("<Configure>", self.handle_window_resize)

        self.after(100, self.maximize_window)

    def maximize_window(self):
        try:
            self.state("zoomed")
        except Exception:
            pass
        if self._current_frame is None:
            self.show_login()

    def calculate_scale_factor(self):
        w, h = self.winfo_width(), self.winfo_height()
        if w < 10 or h < 10:
            return 1.0
        return min(w / BASE_W, h / BASE_H)

    def scale_value(self, base):
        return max(1, int(base * self.calculate_scale_factor()))

    def handle_window_resize(self, event):
        if event.widget is not self:
            return
        if self._resize_id:
            self.after_cancel(self._resize_id)
        self._resize_id = self.after(50, self.apply_scaling)

    def apply_scaling(self):
        if self._current_frame and hasattr(self._current_frame, "apply_scaling"):
            self._current_frame.apply_scaling()

    def switch_frame(self, frame):
        if self._current_frame:
            self._current_frame.destroy()
        self._current_frame = frame
        frame.pack(fill="both", expand=True)

    def show_login(self):
        from login import LoginFrame
        self.switch_frame(LoginFrame(self))

    def show_menu(self):
        from menu import MenuFrame
        self.switch_frame(MenuFrame(self))

    def show_stats(self):
        if not self.current_user:
            self.show_menu()
            return
        from stats import StatsFrame
        self.switch_frame(StatsFrame(self))

    def show_game(self, mode, difficulty, time_limit):
        from game import GameFrame
        if self.current_user:
            auth.record_test_started(self.current_user, mode)
        self.switch_frame(GameFrame(self, mode, difficulty, time_limit))

    def show_results(self, score, correct, total, mode, difficulty, time_limit, time_spent_seconds, longest_streak_in_test):
        from results import ResultsFrame
        self.switch_frame(ResultsFrame(
            self, score, correct, total, mode, difficulty, time_limit, time_spent_seconds, longest_streak_in_test,
        ))

App().mainloop()