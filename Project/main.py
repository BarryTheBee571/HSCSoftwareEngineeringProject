import customtkinter as ctk
import auth
from styles import BASE_W, BASE_H, MIN_W, MIN_H, WHITE

class App(ctk.CTk):
    """Main app window. Handles page switching and shared app state."""

    def __init__(self):
        super().__init__()  # init CTk root window
        self.title("Speedy Maths")  # window title bar text
        self.geometry(f"{BASE_W}x{BASE_H}")  # startup size
        self.minsize(MIN_W, MIN_H)  # stop super tiny window
        self.resizable(True, True)  # allow resize drag
        self.configure(fg_color=WHITE)  # app background color
        ctk.set_appearance_mode("light")  # always use light mode

        self.current_user = None  # username string if logged in
        self.session_token = None  # auth token from login/register

        self._current_frame = None  # currently visible page frame
        self._resize_id = None  # id for resize debounce timer

        self.bind("<Configure>", self.on_window_resize)  # resize/move callback

        self.after(100, self.go_fullscreen)  # wait a tick before zooming

    def go_fullscreen(self):
        """Try to open the window maximized, then show login page."""
        try:
            self.state("zoomed")  # Windows maximized state
        except Exception:
            pass  # ignore platform-specific failures
        if self._current_frame is None:
            self.show_login()  # initial page

    def get_scale_factor(self):
        """Get a simple scale factor based on current window size."""
        w, h = self.winfo_width(), self.winfo_height()  # current px size
        if w < 10 or h < 10:
            return 1.0  # avoid weird values during init
        return min(w / BASE_W, h / BASE_H)  # keep proportions stable

    def scale_value(self, base):
        return max(1, int(base * self.get_scale_factor()))  # scaled int >= 1

    def on_window_resize(self, event):
        """Debounce resize events so it does not rescale every single pixel step."""
        if event.widget is not self:
            return  # ignore child widget configure events
        if self._resize_id:
            self.after_cancel(self._resize_id)  # cancel previous pending refresh
        self._resize_id = self.after(50, self.refresh_scaling)  # delay to debounce

    def refresh_scaling(self):
        """Tell the current frame to update its fonts/sizing."""
        if not self._current_frame:
            return  # nothing mounted yet
        if hasattr(self._current_frame, "refresh_scaling"):
            self._current_frame.refresh_scaling()  # new method name
        elif hasattr(self._current_frame, "apply_scaling"):
            self._current_frame.apply_scaling()  # compatibility fallback

    def swap_frame(self, frame):
        """Destroy previous frame and show the new one."""
        # one frame visible at a time keeps navigation simple
        if self._current_frame:
            self._current_frame.destroy()  # remove old page widgets
        self._current_frame = frame  # save new page reference
        frame.pack(fill="both", expand=True)  # show new page full window

    def show_login(self):
        from login import LoginFrame  # local import avoids circulars
        self.swap_frame(LoginFrame(self))  # mount login page

    def show_menu(self):
        from menu import MenuFrame  # local import avoids circulars
        self.swap_frame(MenuFrame(self))  # mount menu page

    def show_stats(self):
        if not self.current_user:
            self.show_menu()  # guests should not open stats
            return  # stop here for guests
        from stats import StatsFrame  # import page class
        self.swap_frame(StatsFrame(self))  # mount stats page

    def show_leaderboard(self):
        if not self.current_user:
            self.show_menu()  # guests should not open leaderboard
            return  # stop here for guests
        from leaderboard import LeaderboardFrame  # import page class
        self.swap_frame(LeaderboardFrame(self))  # mount leaderboard page

    def show_game(self, mode, difficulty, time_limit):
        """Open game page and mark test as started for logged in users."""
        from game import GameFrame  # import page class
        if self.current_user:
            auth.mark_test_started(self.current_user, mode)  # track game start
        self.swap_frame(GameFrame(self, mode, difficulty, time_limit))  # mount gameplay page

    def show_results(self, score, correct, total, mode, difficulty, time_limit, time_spent_seconds, longest_streak_in_test):
        from results import ResultsFrame  # import page class
        self.swap_frame(ResultsFrame(
            self, score, correct, total, mode, difficulty, time_limit, time_spent_seconds, longest_streak_in_test,
        ))  # mount results page

App().mainloop()  # start Tk event loop