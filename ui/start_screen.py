import customtkinter as ctk
from ui.theme import *
from ui.widgets import AnimatedButton, GlassCard


class SplashScreen(ctk.CTkFrame):
    """Modern splash/landing screen with concise product messaging."""

    def __init__(self, master, on_start_callback, on_exit_callback):
        super().__init__(master, fg_color=COLOR_BG_DARK)
        self.on_start_callback = on_start_callback
        self.on_exit_callback = on_exit_callback

        outer = ctk.CTkFrame(self, fg_color="transparent")
        outer.pack(fill="both", expand=True, padx=42, pady=42)
        outer.grid_columnconfigure(0, weight=1)
        outer.grid_rowconfigure(0, weight=1)

        hero = GlassCard(outer, width=980, height=560)
        hero.grid(row=0, column=0, sticky="nsew")
        hero.grid_propagate(True)
        hero.grid_columnconfigure((0, 1), weight=1)
        hero.grid_rowconfigure(0, weight=1)

        left = ctk.CTkFrame(hero, fg_color="transparent")
        left.grid(row=0, column=0, sticky="nsew", padx=(36, 18), pady=36)

        right = ctk.CTkFrame(hero, fg_color=COLOR_CARD_ALT_BG, corner_radius=14)
        right.grid(row=0, column=1, sticky="nsew", padx=(18, 36), pady=36)

        ctk.CTkLabel(
            left,
            text="Real-Time Human Detection",
            font=FONT_TITLE,
            text_color=COLOR_TEXT_PRIMARY,
            anchor="w"
        ).pack(anchor="w", pady=(6, 8))

        ctk.CTkLabel(
            left,
            text="Computer vision dashboard for image, video, and live camera crowd analytics.",
            font=FONT_BODY,
            text_color=COLOR_TEXT_SECONDARY,
            justify="left",
            wraplength=420
        ).pack(anchor="w", pady=(0, 20))

        for text in [
            "• Faster R-CNN inference with live human count overlays",
            "• Real-time session metrics and crowd-density classification",
            "• Automatic analytics plots and PDF report generation",
        ]:
            ctk.CTkLabel(left, text=text, font=FONT_BODY, text_color=COLOR_TEXT_SECONDARY, anchor="w").pack(anchor="w", pady=4)

        ctk.CTkLabel(
            left,
            text="Ready to start a new detection session?",
            font=(FONT_FAMILY, 12, "bold"),
            text_color=COLOR_TEXT_MUTED
        ).pack(anchor="w", pady=(28, 14))

        button_row = ctk.CTkFrame(left, fg_color="transparent")
        button_row.pack(anchor="w", fill="x")

        self.start_btn = AnimatedButton(
            button_row,
            text="Launch Dashboard",
            command=self.on_start_callback,
            primary=True,
            width=200
        )
        self.start_btn.pack(side="left")

        self.exit_btn = AnimatedButton(
            button_row,
            text="Exit",
            command=self.on_exit_callback,
            primary=False,
            width=130
        )
        self.exit_btn.pack(side="left", padx=(12, 0))

        ctk.CTkLabel(
            right,
            text="Session Overview",
            font=FONT_SUBTITLE,
            text_color=COLOR_TEXT_PRIMARY
        ).pack(anchor="w", padx=20, pady=(20, 10))

        for heading, body in [
            ("Input sources", "Choose image, video file, or webcam capture."),
            ("Detection workflow", "Preview source, start/stop threaded detection, monitor status live."),
            ("Post-run outputs", "Open analytics screen with plots and generated Crowd_Report.pdf."),
        ]:
            block = ctk.CTkFrame(right, fg_color=COLOR_BG_SURFACE, corner_radius=10)
            block.pack(fill="x", padx=18, pady=8)
            ctk.CTkLabel(block, text=heading, font=(FONT_FAMILY, 12, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w", padx=12, pady=(10, 2))
            ctk.CTkLabel(block, text=body, font=FONT_CAPTION, text_color=COLOR_TEXT_SECONDARY, justify="left", wraplength=320).pack(anchor="w", padx=12, pady=(0, 10))

        ctk.CTkLabel(
            right,
            text="Team 23 | IIIT Kottayam",
            font=FONT_CAPTION,
            text_color=COLOR_TEXT_MUTED
        ).pack(side="bottom", anchor="w", padx=20, pady=20)
