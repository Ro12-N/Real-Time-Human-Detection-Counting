import customtkinter as ctk
from ui.theme import *


class GlassCard(ctk.CTkFrame):
    """Reusable elevated card surface."""

    def __init__(self, master, width=200, height=200, padding=0, **kwargs):
        super().__init__(
            master,
            width=width,
            height=height,
            fg_color=COLOR_CARD_BG,
            border_color=COLOR_CARD_BORDER,
            border_width=1,
            corner_radius=14,
            **kwargs
        )
        self.grid_propagate(False)
        self.pack_propagate(False)
        self.inner_padding = padding


class AnimatedButton(ctk.CTkButton):
    """Consistent CTA/secondary buttons."""

    def __init__(self, master, text="", command=None, primary=True, compact=False, **kwargs):
        fg_col = COLOR_ACCENT_PURPLE if primary else COLOR_CARD_ALT_BG
        hover_col = COLOR_ACCENT_BLUE if primary else "#223454"

        super().__init__(
            master,
            text=text,
            command=command,
            font=(FONT_FAMILY, 12 if compact else 13, "bold"),
            text_color=COLOR_TEXT_PRIMARY,
            fg_color=fg_col,
            hover_color=hover_col,
            border_color=COLOR_CARD_BORDER,
            border_width=0 if primary else 1,
            corner_radius=10,
            height=34 if compact else 42,
            **kwargs
        )


class MetricBadge(ctk.CTkFrame):
    """Metric tile widget for live stats and summary values."""

    def __init__(self, master, title="TITLE", value="0", value_color=COLOR_SUCCESS, **kwargs):
        super().__init__(
            master,
            fg_color=COLOR_CARD_ALT_BG,
            border_color=COLOR_CARD_BORDER,
            border_width=1,
            corner_radius=12,
            **kwargs
        )

        self.title_label = ctk.CTkLabel(
            self,
            text=title.upper(),
            font=(FONT_FAMILY, 10, "bold"),
            text_color=COLOR_TEXT_MUTED
        )
        self.title_label.pack(anchor="w", padx=12, pady=(10, 2))

        self.value_label = ctk.CTkLabel(
            self,
            text=value,
            font=(FONT_FAMILY, 20, "bold"),
            text_color=value_color
        )
        self.value_label.pack(anchor="w", padx=12, pady=(0, 10))

    def update_value(self, new_val, color=None):
        self.value_label.configure(text=str(new_val))
        if color is not None:
            self.value_label.configure(text_color=color)


class StatusPill(ctk.CTkFrame):
    """Compact status indicator badge."""

    def __init__(self, master, label="Idle", color=COLOR_TEXT_SECONDARY, **kwargs):
        super().__init__(
            master,
            fg_color=COLOR_BG_SURFACE,
            border_color=COLOR_CARD_BORDER,
            border_width=1,
            corner_radius=999,
            **kwargs
        )
        self.dot = ctk.CTkLabel(self, text="●", text_color=color, font=(FONT_FAMILY, 11, "bold"))
        self.dot.pack(side="left", padx=(10, 4), pady=5)
        self.text_label = ctk.CTkLabel(self, text=label, text_color=COLOR_TEXT_SECONDARY, font=(FONT_FAMILY, 11, "bold"))
        self.text_label.pack(side="left", padx=(0, 10), pady=5)

    def update_status(self, label, color):
        self.dot.configure(text_color=color)
        self.text_label.configure(text=label)
