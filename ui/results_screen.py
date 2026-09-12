import os
import cv2
from PIL import Image, ImageTk
import customtkinter as ctk
from ui.theme import *
from ui.widgets import GlassCard, MetricBadge

class ResultsScreen(ctk.CTkFrame):
    """Analytics & PDF Preview Screen."""
    def __init__(self, master, on_back_callback):
        super().__init__(master, fg_color=COLOR_BG_DARK)
        self.on_back_callback = on_back_callback

        # Top Bar
        self.top_bar = ctk.CTkFrame(self, fg_color=COLOR_CARD_BG, height=60, corner_radius=0)
        self.top_bar.pack(fill="x", side="top")

        self.back_btn = ctk.CTkButton(
            self.top_bar,
            text="← BACK TO DASHBOARD",
            font=(FONT_FAMILY, 12, "bold"),
            fg_color=COLOR_CARD_BORDER,
            hover_color=COLOR_ACCENT_PURPLE,
            width=180,
            command=self.on_back_callback
        )
        self.back_btn.pack(side="left", padx=20, pady=10)

        self.title_label = ctk.CTkLabel(
            self.top_bar,
            text="ANALYTICS & EXECUTIVE REPORT SUMMARY",
            font=(FONT_FAMILY, 16, "bold"),
            text_color=COLOR_TEXT_PRIMARY
        )
        self.title_label.pack(side="left", padx=20)

        # Content Split Frame
        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.pack(fill="both", expand=True, padx=20, pady=20)

        # Left Column: Plots
        self.left_col = ctk.CTkFrame(self.content, fg_color="transparent")
        self.left_col.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.enum_card = GlassCard(self.left_col, height=260)
        self.enum_card.pack(fill="x", pady=(0, 10))
        self.enum_label = ctk.CTkLabel(self.enum_card, text="ENUMERATION PLOT PREVIEW", font=FONT_CAPTION, text_color=COLOR_TEXT_SECONDARY)
        self.enum_label.pack(pady=5)
        self.enum_img_label = ctk.CTkLabel(self.enum_card, text="[ Plot image will appear after detection run ]")
        self.enum_img_label.pack(fill="both", expand=True, padx=10, pady=10)

        self.acc_card = GlassCard(self.left_col, height=260)
        self.acc_card.pack(fill="x")
        self.acc_label = ctk.CTkLabel(self.acc_card, text="ACCURACY PLOT PREVIEW", font=FONT_CAPTION, text_color=COLOR_TEXT_SECONDARY)
        self.acc_label.pack(pady=5)
        self.acc_img_label = ctk.CTkLabel(self.acc_card, text="[ Plot image will appear after detection run ]")
        self.acc_img_label.pack(fill="both", expand=True, padx=10, pady=10)

        # Right Column: Report & Stats Summary
        self.right_col = GlassCard(self.content, width=320)
        self.right_col.pack(side="right", fill="both", padx=(10, 0))

        self.summary_header = ctk.CTkLabel(self.right_col, text="CROWD REPORT SUMMARY", font=FONT_SUBTITLE, text_color=COLOR_ACCENT_PURPLE)
        self.summary_header.pack(pady=15)

        self.badge_max = MetricBadge(self.right_col, title="Max Humans Detected", value="0", value_color=COLOR_ACCENT_BLUE)
        self.badge_max.pack(fill="x", padx=15, pady=6)

        self.badge_avg = MetricBadge(self.right_col, title="Average Humans / Frame", value="0.0", value_color=COLOR_TEXT_PRIMARY)
        self.badge_avg.pack(fill="x", padx=15, pady=6)

        self.badge_accuracy = MetricBadge(self.right_col, title="Average Detection Accuracy", value="0.0%", value_color=COLOR_SUCCESS)
        self.badge_accuracy.pack(fill="x", padx=15, pady=6)

        self.badge_status = MetricBadge(self.right_col, title="Crowd Density Classification", value="Not Evaluated", value_color=COLOR_WARNING)
        self.badge_status.pack(fill="x", padx=15, pady=6)

        self.report_info = ctk.CTkLabel(
            self.right_col,
            text="Executive Crowd Report has been automatically outputted to project root as Crowd_Report.pdf.",
            font=FONT_CAPTION,
            text_color=COLOR_TEXT_SECONDARY,
            wraplength=280
        )
        self.report_info.pack(pady=20)

    def load_plots_and_summary(self, enum_path, acc_path, max_c, avg_c, avg_a, status, status_color):
        """Update preview widgets with newly generated plots & stats."""
        self.badge_max.update_value(max_c)
        self.badge_avg.update_value(f"{avg_c:.2f}")
        self.badge_accuracy.update_value(f"{avg_a * 100:.1f}%")
        self.badge_status.update_value(status, color=status_color)

        if os.path.exists(enum_path):
            img = Image.open(enum_path).resize((480, 220), Image.Resampling.LANCZOS)
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(480, 220))
            self.enum_img_label.configure(image=ctk_img, text="")

        if os.path.exists(acc_path):
            img = Image.open(acc_path).resize((480, 220), Image.Resampling.LANCZOS)
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(480, 220))
            self.acc_img_label.configure(image=ctk_img, text="")
