import sys
import customtkinter as ctk
from ui.theme import COLOR_BG_DARK
from ui.start_screen import SplashScreen
from ui.dashboard import MainDashboard
from ui.results_screen import ResultsScreen

# Configure CustomTkinter Appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Real-Time Human Detection & Counting System")
        self.geometry("1180x760")
        self.minsize(1000, 680)
        self.configure(fg_color=COLOR_BG_DARK)

        # Main Navigation Container
        self.container = ctk.CTkFrame(self, fg_color=COLOR_BG_DARK)
        self.container.pack(fill="both", expand=True)

        # Initialize Views
        self.splash_screen = SplashScreen(self.container, self.show_dashboard, self.quit_app)
        self.dashboard = MainDashboard(self.container, self.show_results, self.show_splash)
        self.results_screen = ResultsScreen(self.container, self.show_dashboard)

        # Start at Splash Screen
        self.show_splash()

    def show_splash(self):
        self.dashboard.pack_forget()
        self.results_screen.pack_forget()
        self.splash_screen.pack(fill="both", expand=True)

    def show_dashboard(self):
        self.splash_screen.pack_forget()
        self.results_screen.pack_forget()
        self.dashboard.pack(fill="both", expand=True)

    def show_results(self, enum_path, acc_path, max_c, avg_c, avg_a, status, status_color):
        self.splash_screen.pack_forget()
        self.dashboard.pack_forget()
        self.results_screen.load_plots_and_summary(enum_path, acc_path, max_c, avg_c, avg_a, status, status_color)
        self.results_screen.pack(fill="both", expand=True)

    def quit_app(self):
        if self.dashboard and self.dashboard.is_detecting:
            self.dashboard.stop_detection()
        self.destroy()
        sys.exit(0)

if __name__ == "__main__":
    app = App()
    app.mainloop()
