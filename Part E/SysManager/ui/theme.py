"""
SysManager – Theme & Design Tokens
Centralised colour palette, fonts, and ttk Treeview dark-mode styling.
"""

import tkinter.ttk as ttk

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Colour palette
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BG_DARKEST   = "#0b0b1a"      # Window / root background
BG_SIDEBAR   = "#111128"      # Sidebar panel
BG_CARD      = "#161637"      # Cards, panels, content area
BG_INPUT     = "#1c1c45"      # Entry / input backgrounds
BG_HOVER     = "#22224f"      # Hover state
BG_ROW_ALT   = "#13132e"      # Treeview alternate row

ACCENT       = "#00d4aa"      # Primary accent – teal
ACCENT_HOVER = "#00f0c0"      # Accent hover
ACCENT_DIM   = "#00a88a"      # Accent pressed / muted
DANGER       = "#e94560"      # Destructive actions
DANGER_HOVER = "#ff6b81"
WARNING      = "#f0a500"      # Warnings
SUCCESS      = "#00e676"      # Success messages

TEXT_PRIMARY   = "#eaeaea"    # Main text
TEXT_SECONDARY = "#8892b0"    # Muted / labels
TEXT_HEADING   = "#ffffff"    # Headings
TEXT_ACCENT    = ACCENT       # Accent-coloured text

BORDER         = "#2a2a5a"    # Subtle borders
SCROLLBAR_BG   = "#1a1a3e"
SCROLLBAR_FG   = "#3a3a6e"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Typography
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FONT_FAMILY   = "Segoe UI"
FONT_BODY     = (FONT_FAMILY, 13)
FONT_BODY_SM  = (FONT_FAMILY, 12)
FONT_HEADING  = (FONT_FAMILY, 20, "bold")
FONT_SUBHEAD  = (FONT_FAMILY, 15, "bold")
FONT_LABEL    = (FONT_FAMILY, 12)
FONT_BUTTON   = (FONT_FAMILY, 13, "bold")
FONT_MONO     = ("Consolas", 12)
FONT_TREE     = (FONT_FAMILY, 12)
FONT_TREE_HD  = (FONT_FAMILY, 12, "bold")
FONT_TITLE    = (FONT_FAMILY, 28, "bold")
FONT_SIDEBAR  = (FONT_FAMILY, 13)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Widget dimensions
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SIDEBAR_WIDTH      = 240
CORNER_RADIUS      = 10
BUTTON_HEIGHT      = 38
ENTRY_HEIGHT       = 38
PADDING            = 16
ROW_HEIGHT         = 32

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Treeview dark-mode styling
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def configure_treeview_style():
    """Apply a dark theme to ttk.Treeview widgets (call once at startup)."""
    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Dark.Treeview",
        background=BG_CARD,
        foreground=TEXT_PRIMARY,
        fieldbackground=BG_CARD,
        borderwidth=0,
        rowheight=ROW_HEIGHT,
        font=FONT_TREE,
    )
    style.configure(
        "Dark.Treeview.Heading",
        background=BG_SIDEBAR,
        foreground=ACCENT,
        font=FONT_TREE_HD,
        borderwidth=0,
        relief="flat",
        padding=(8, 6),
    )
    style.map(
        "Dark.Treeview",
        background=[("selected", "#1e3a5f")],
        foreground=[("selected", "#ffffff")],
    )
    style.map(
        "Dark.Treeview.Heading",
        background=[("active", BG_HOVER)],
    )
    # Remove treeview borders
    style.layout("Dark.Treeview", [
        ("Dark.Treeview.treearea", {"sticky": "nswe"})
    ])

    # Scrollbar styling (uses default clam layout which has a working thumb)
    style.configure(
        "Dark.Vertical.TScrollbar",
        background=SCROLLBAR_FG,
        troughcolor=SCROLLBAR_BG,
        borderwidth=0,
        arrowsize=14,
        arrowcolor=SCROLLBAR_FG,
        width=12,
    )
    style.map(
        "Dark.Vertical.TScrollbar",
        background=[
            ("pressed", ACCENT),
            ("active", ACCENT_DIM),
        ],
        arrowcolor=[
            ("pressed", ACCENT),
            ("active", ACCENT_DIM),
        ],
    )

    style.configure(
        "Dark.Horizontal.TScrollbar",
        background=SCROLLBAR_FG,
        troughcolor=SCROLLBAR_BG,
        borderwidth=0,
        arrowsize=14,
        arrowcolor=SCROLLBAR_FG,
        width=12,
    )
    style.map(
        "Dark.Horizontal.TScrollbar",
        background=[
            ("pressed", ACCENT),
            ("active", ACCENT_DIM),
        ],
        arrowcolor=[
            ("pressed", ACCENT),
            ("active", ACCENT_DIM),
        ],
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Sidebar table icons (unicode glyphs)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TABLE_ICONS = {
    "users":            "👤",
    "executables":      "⚙️",
    "resource_types":   "📂",
    "resources":        "🖥",
    "processes":        "🔄",
    "allocations":      "📊",
    "usage_logs":       "📈",
    "network_sessions": "🌐",
    "system_events":    "⚡",
    "maintenance_log":  "🔧",
    "employee":         "🏢",
}
