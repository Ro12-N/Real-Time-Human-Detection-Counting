import customtkinter as ctk
from ui.theme import *

class GlassCard(ctk.CTkFrame):
    """Reusable card frame with sleek borders and dark background."""
    def __init__(self, master, width=200, height=200, **kwargs):
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

class AnimatedButton(ctk.CTkButton):
    """Modern CTkButton with clean typography and hover color transitions."""
    def __init__(self, master, text="", command=None, primary=True, **kwargs):
        fg_col = COLOR_ACCENT_PURPLE if primary else COLOR_CARD_BORDER
        hover_col = COLOR_ACCENT_BLUE if primary else COLOR_CARD_BG
        
        super().__init__(
            master,
            text=text,
            command=command,
            font=(FONT_FAMILY, 13, "bold"),
            fg_color=fg_col,
            hover_color=hover_col,
            corner_radius=10,
            height=40,
            **kwargs
        )

class MetricBadge(ctk.CTkFrame):
    """Badge widget for live stats like Humans Detected & FPS."""
    def __init__(self, master, title="TITLE", value="0", value_color=COLOR_SUCCESS, **kwargs):
        super().__init__(
            master,
            fg_color=COLOR_CARD_BG,
            border_color=COLOR_CARD_BORDER,
            border_width=1,
            corner_radius=12,
            **kwargs
        )
        self.title_label = ctk.CTkLabel(
            self,
            text=title.upper(),
            font=(FONT_FAMILY, 10, "bold"),
            text_color=COLOR_TEXT_SECONDARY
        )
        self.title_label.pack(anchor="w", padx=12, pady=(8, 2))
        
        self.value_label = ctk.CTkLabel(
            self,
            text=value,
            font=(FONT_FAMILY, 20, "bold"),
            text_color=value_color
        )
        self.value_label.pack(anchor="w", padx=12, pady=(0, 8))

    def update_value(self, new_val, color=None):
        self.value_label.configure(text=str(new_val))
        if color:
            self.value_label.configure(text_color=color)
