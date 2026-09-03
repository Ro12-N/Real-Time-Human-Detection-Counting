import customtkinter as ctk
from ui.theme import *

class SplashScreen(ctk.CTkFrame):
    """Modern Dark Splash Screen with title, animated buttons, and team credentials."""
    def __init__(self, master, on_start_callback, on_exit_callback):
        super().__init__(master, fg_color=COLOR_BG_DARK)
        self.on_start_callback = on_start_callback
        self.on_exit_callback = on_exit_callback

        # Main Center Container
        self.center_card = ctk.CTkFrame(
            self,
            fg_color=COLOR_CARD_BG,
            border_color=COLOR_CARD_BORDER,
            border_width=1,
            corner_radius=20,
            width=700,
            height=480
        )
        self.center_card.place(relx=0.5, rely=0.48, anchor="center")

        # Header Title
        self.title_label = ctk.CTkLabel(
            self.center_card,
            text="REAL-TIME HUMAN DETECTION\n& COUNTING SYSTEM",
            font=(FONT_FAMILY, 26, "bold"),
            text_color=COLOR_TEXT_PRIMARY,
            justify="center"
        )
        self.title_label.pack(pady=(45, 10))

        # Subtitle
        self.subtitle_label = ctk.CTkLabel(
            self.center_card,
            text="Powered by Faster R-CNN Inception v2 Deep Neural Network",
            font=(FONT_FAMILY, 13),
            text_color=COLOR_ACCENT_BLUE
        )
        self.subtitle_label.pack(pady=(0, 35))

        # Action Buttons Container
        self.btn_frame = ctk.CTkFrame(self.center_card, fg_color="transparent")
        self.btn_frame.pack(pady=20)

        self.start_btn = ctk.CTkButton(
            self.btn_frame,
            text="▶  START DASHBOARD",
            font=(FONT_FAMILY, 15, "bold"),
            fg_color=COLOR_SUCCESS,
            hover_color="#059669",
            corner_radius=12,
            width=220,
            height=50,
            command=self.on_start_callback
        )
        self.start_btn.pack(side="left", padx=15)

        self.exit_btn = ctk.CTkButton(
            self.btn_frame,
            text="❌  EXIT APPLICATION",
            font=(FONT_FAMILY, 15, "bold"),
            fg_color=COLOR_DANGER,
            hover_color="#DC2626",
            corner_radius=12,
            width=220,
            height=50,
            command=self.on_exit_callback
        )
        self.exit_btn.pack(side="left", padx=15)

        # Team Footer Card
        self.footer_label = ctk.CTkLabel(
            self.center_card,
            text="Team 23 | IIIT Kottayam\nM ROHAN NAIDU (2023BCS0148)  |  VARSHITH KILLARI (2023BCS0157)\nDEBAM DIAN (2023BCS0154)  |  GOPICHAND (2023BCS145)",
            font=(FONT_FAMILY, 11),
            text_color=COLOR_TEXT_SECONDARY,
            justify="center"
        )
        self.footer_label.pack(side="bottom", pady=25)
