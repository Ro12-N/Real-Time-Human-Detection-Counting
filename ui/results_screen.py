import os
from PIL import Image
import customtkinter as ctk
from ui.theme import *
from ui.widgets import GlassCard, MetricBadge, AnimatedButton, StatusPill


class ResultsScreen(ctk.CTkFrame):
    """Modern analytics and report summary screen."""

    def __init__(self, master, on_back_callback):
        super().__init__(master, fg_color=COLOR_BG_DARK)
        self.on_back_callback = on_back_callback
        self.enum_plot_image = None
        self.acc_plot_image = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(self, fg_color=COLOR_BG_SURFACE, height=58, corner_radius=0)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(1, weight=1)

        self.back_btn = AnimatedButton(
            header,
            text="← Dashboard",
            command=self.on_back_callback,
            primary=False,
            compact=True,
            width=120
        )
        self.back_btn.grid(row=0, column=0, padx=16, pady=10)

        ctk.CTkLabel(
            header,
            text="Analytics & Report",
            font=(FONT_FAMILY, 16, "bold"),
            text_color=COLOR_TEXT_PRIMARY
        ).grid(row=0, column=1, sticky="w")

        content = ctk.CTkFrame(self, fg_color="transparent")
        content.grid(row=1, column=0, sticky="nsew", padx=18, pady=18)
        content.grid_columnconfigure(0, weight=3)
        content.grid_columnconfigure(1, weight=2)
        content.grid_rowconfigure(0, weight=1)

        plot_col = ctk.CTkFrame(content, fg_color="transparent")
        plot_col.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        plot_col.grid_rowconfigure((0, 1), weight=1)
        plot_col.grid_columnconfigure(0, weight=1)

        self.enum_card = GlassCard(plot_col)
        self.enum_card.grid(row=0, column=0, sticky="nsew", pady=(0, 8))
        ctk.CTkLabel(self.enum_card, text="Enumeration Trend", font=FONT_CAPTION, text_color=COLOR_TEXT_MUTED).pack(anchor="w", padx=14, pady=(12, 6))
        self.enum_img_label = ctk.CTkLabel(self.enum_card, text="Run detection to generate enumeration analytics.", text_color=COLOR_TEXT_SECONDARY)
        self.enum_img_label.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        self.acc_card = GlassCard(plot_col)
        self.acc_card.grid(row=1, column=0, sticky="nsew", pady=(8, 0))
        ctk.CTkLabel(self.acc_card, text="Detection Accuracy Trend", font=FONT_CAPTION, text_color=COLOR_TEXT_MUTED).pack(anchor="w", padx=14, pady=(12, 6))
        self.acc_img_label = ctk.CTkLabel(self.acc_card, text="Run detection to generate accuracy analytics.", text_color=COLOR_TEXT_SECONDARY)
        self.acc_img_label.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        side_col = GlassCard(content)
        side_col.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        side_col.grid_propagate(True)

        ctk.CTkLabel(side_col, text="Session Summary", font=FONT_SUBTITLE, text_color=COLOR_TEXT_PRIMARY).pack(anchor="w", padx=14, pady=(14, 10))

        self.badge_max = MetricBadge(side_col, title="Max Humans Detected", value="0", value_color=COLOR_ACCENT_BLUE)
        self.badge_max.pack(fill="x", padx=14, pady=5)

        self.badge_avg = MetricBadge(side_col, title="Average Humans / Frame", value="0.0", value_color=COLOR_TEXT_PRIMARY)
        self.badge_avg.pack(fill="x", padx=14, pady=5)

        self.badge_accuracy = MetricBadge(side_col, title="Average Detection Accuracy", value="0.0%", value_color=COLOR_SUCCESS)
        self.badge_accuracy.pack(fill="x", padx=14, pady=5)

        status_row = ctk.CTkFrame(side_col, fg_color="transparent")
        status_row.pack(fill="x", padx=14, pady=(8, 10))
        ctk.CTkLabel(status_row, text="Crowd Density", font=FONT_CAPTION, text_color=COLOR_TEXT_MUTED).pack(anchor="w")
        self.status_pill = StatusPill(status_row, label="Not Evaluated", color=COLOR_WARNING)
        self.status_pill.pack(anchor="w", pady=(6, 0))

        self.badge_status = MetricBadge(side_col, title="Status Detail", value="Not Evaluated", value_color=COLOR_WARNING)
        self.badge_status.pack(fill="x", padx=14, pady=(0, 8))

        ctk.CTkLabel(
            side_col,
            text="CROWD_REPORT.PDF is generated automatically in the project root after analytics open.",
            font=FONT_CAPTION,
            text_color=COLOR_TEXT_SECONDARY,
            justify="left",
            wraplength=290
        ).pack(anchor="w", padx=14, pady=(8, 16))

    def _load_plot(self, path, label, target_size):
        if not os.path.exists(path):
            return
        img = Image.open(path).resize(target_size, Image.Resampling.LANCZOS)
        ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=target_size)
        label.configure(image=ctk_img, text="")
        return ctk_img

    def load_plots_and_summary(self, enum_path, acc_path, max_c, avg_c, avg_a, status, status_color):
        """Update preview widgets with generated plots and summary metrics."""
        self.badge_max.update_value(max_c)
        self.badge_avg.update_value(f"{avg_c:.2f}")
        self.badge_accuracy.update_value(f"{avg_a * 100:.1f}%")
        self.badge_status.update_value(status, color=status_color)
        self.status_pill.update_status(status, status_color)

        self.enum_plot_image = self._load_plot(enum_path, self.enum_img_label, (560, 240))
        self.acc_plot_image = self._load_plot(acc_path, self.acc_img_label, (560, 240))
