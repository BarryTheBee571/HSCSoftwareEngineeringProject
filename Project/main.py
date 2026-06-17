import customtkinter as ctk
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

        self.current_user  = None
        self.session_token = None

        self._current_frame = None
        self._resize_id     = None

        self.bind("<Configure>", self._on_resize)

        self.after(100, self._maximize)

        self.show_login()

    def _maximize(self):
        try:
            self.state("zoomed")
        except Exception:
            pass

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
        if self._current_frame and hasattr(self._current_frame, "apply_scale"):
            self._current_frame.apply_scale()

    def _switch(self, frame):
        if self._current_frame:
            self._current_frame.destroy()
        self._current_frame = frame
        frame.pack(fill="both", expand=True)

    def show_login(self):
        from login import LoginFrame
        self._switch(LoginFrame(self))

    def show_menu(self):
        from menu import MenuFrame
        self._switch(MenuFrame(self))

    def show_game(self, mode, difficulty, time_limit):
        from game import GameFrame
        self._switch(GameFrame(self, mode, difficulty, time_limit))

    def show_results(self, score, correct, total, mode, difficulty):
        from results import ResultsFrame
        self._switch(ResultsFrame(self, score, correct, total, mode, difficulty))


App().mainloop()