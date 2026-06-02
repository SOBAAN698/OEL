# Styles and visual themes for School Management System

# Palette colors (Modern slate design)
PRIMARY_COLOR = "#2563eb"     # Royal Blue
SECONDARY_COLOR = "#4f46e5"   # Indigo
BG_COLOR = "#f8fafc"          # Off-white / light slate
CARD_BG = "#ffffff"           # White for frames/cards
TEXT_COLOR = "#1e293b"        # Dark slate text
TEXT_MUTED = "#64748b"        # Slate gray
SUCCESS_COLOR = "#16a34a"     # Green
DANGER_COLOR = "#dc2626"      # Red
BORDER_COLOR = "#e2e8f0"      # Light gray borders

# Fonts
FONT_TITLE = ("Segoe UI", 20, "bold")
FONT_SUBTITLE = ("Segoe UI", 14, "bold")
FONT_HEADER = ("Segoe UI", 11, "bold")
FONT_BODY = ("Segoe UI", 11)
FONT_SMALL = ("Segoe UI", 9)

# Common styling configurations
def apply_card_style(widget):
    """Applies a clean white card border style to a frame."""
    widget.configure(bg=CARD_BG, highlightbackground=BORDER_COLOR, highlightthickness=1, bd=0)

def apply_button_style(widget, bg_color=PRIMARY_COLOR, fg_color="#ffffff"):
    """Applies clean button styling to standard buttons."""
    widget.configure(
        bg=bg_color,
        fg=fg_color,
        font=FONT_HEADER,
        relief="flat",
        borderwidth=0,
        activebackground=SECONDARY_COLOR,
        activeforeground="#ffffff",
        cursor="hand2",
        padx=12,
        pady=6
    )

def apply_danger_button_style(widget):
    """Applies styled alert button designs."""
    apply_button_style(widget, bg_color=DANGER_COLOR)

def apply_success_button_style(widget):
    """Applies styled success button designs."""
    apply_button_style(widget, bg_color=SUCCESS_COLOR)

def apply_entry_style(widget):
    """Applies styles to Text/Entry fields."""
    widget.configure(
        font=FONT_BODY,
        bg="#ffffff",
        fg=TEXT_COLOR,
        relief="solid",
        borderwidth=1,
        highlightcolor=PRIMARY_COLOR,
        highlightthickness=1,
        insertbackground=TEXT_COLOR
    )
