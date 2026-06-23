"""
SysManager – Dashboard
Main application frame with a sidebar for navigation and a content area
that swaps between CRUD screens and the System Operations panel.
"""

import customtkinter as ctk

from ui.theme import (
    BG_DARKEST, BG_SIDEBAR, BG_CARD, BG_INPUT, BG_HOVER,
    ACCENT, ACCENT_HOVER, ACCENT_DIM, DANGER,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_HEADING, TEXT_ACCENT, BORDER,
    FONT_TITLE, FONT_SUBHEAD, FONT_BODY, FONT_BODY_SM,
    FONT_LABEL, FONT_BUTTON, FONT_SIDEBAR,
    SIDEBAR_WIDTH, CORNER_RADIUS, BUTTON_HEIGHT, PADDING,
    TABLE_ICONS,
)
from ui.table_configs import ALL_TABLES
from ui.crud_screen import CRUDScreen
from ui.operations_screen import OperationsScreen
from db.connection import DatabaseManager


class Dashboard(ctk.CTkFrame):
    """Full-screen dashboard with sidebar navigation and content area."""

    def __init__(self, parent, on_logout):
        super().__init__(parent, fg_color=BG_DARKEST)
        self.on_logout = on_logout
        self.db = DatabaseManager.get_instance()
        self.active_btn = None      # Currently highlighted sidebar button
        self.current_screen = None  # Widget in content area
        self.sidebar_buttons = {}   # key → button widget

        self._build_ui()

        # Auto-select first table
        if ALL_TABLES:
            first_key = ALL_TABLES[0]["table_name"]
            self.after(100, lambda: self._show_table(first_key))

    # ================================================================== #
    #  LAYOUT                                                              #
    # ================================================================== #

    def _build_ui(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self._build_sidebar()
        self._build_content_area()

    # ── Sidebar ─────────────────────────────────────────────────────── #

    def _build_sidebar(self):
        sidebar = ctk.CTkFrame(self, fg_color=BG_SIDEBAR,
                                width=SIDEBAR_WIDTH, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="ns")
        sidebar.grid_propagate(False)
        sidebar.grid_rowconfigure(3, weight=1)
        sidebar.grid_columnconfigure(0, weight=1)

        # ── Brand ──
        brand = ctk.CTkFrame(sidebar, fg_color="transparent", height=70)
        brand.grid(row=0, column=0, sticky="ew")
        brand.grid_propagate(False)
        brand.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(brand, text="⌘  SysManager", font=FONT_SUBHEAD,
                     text_color=ACCENT).grid(row=0, column=0, padx=16, pady=(20, 2),
                                              sticky="w")
        ctk.CTkLabel(brand, text="Database Console",
                     font=(FONT_SIDEBAR[0], 11),
                     text_color=TEXT_SECONDARY).grid(row=1, column=0, padx=18,
                                                      sticky="w")

        # ── Separator ──
        sep = ctk.CTkFrame(sidebar, fg_color=BORDER, height=1)
        sep.grid(row=1, column=0, sticky="ew", padx=12, pady=(12, 8))

        # ── Table section header ──
        ctk.CTkLabel(sidebar, text="TABLES", font=(FONT_SIDEBAR[0], 10, "bold"),
                     text_color=TEXT_SECONDARY).grid(
            row=2, column=0, sticky="w", padx=18, pady=(8, 4))

        # ── Scrollable table list ──
        nav_scroll = ctk.CTkScrollableFrame(
            sidebar, fg_color="transparent",
            scrollbar_button_color=BG_HOVER,
            scrollbar_button_hover_color=ACCENT_DIM,
        )
        nav_scroll.grid(row=3, column=0, sticky="nsew", padx=4)
        nav_scroll.grid_columnconfigure(0, weight=1)

        for i, tbl in enumerate(ALL_TABLES):
            key = tbl["table_name"]
            icon = TABLE_ICONS.get(key, "📋")
            text = f"{icon}  {tbl['display_name']}"

            btn = ctk.CTkButton(
                nav_scroll, text=text, font=FONT_SIDEBAR,
                height=36, corner_radius=8, anchor="w",
                fg_color="transparent", hover_color=BG_HOVER,
                text_color=TEXT_PRIMARY,
                command=lambda k=key: self._show_table(k),
            )
            btn.grid(row=i, column=0, sticky="ew", pady=1, padx=4)
            self.sidebar_buttons[key] = btn

        # ── Operations button ──
        sep2 = ctk.CTkFrame(sidebar, fg_color=BORDER, height=1)
        sep2.grid(row=4, column=0, sticky="ew", padx=12, pady=(8, 4))

        ctk.CTkLabel(sidebar, text="ADVANCED", font=(FONT_SIDEBAR[0], 10, "bold"),
                     text_color=TEXT_SECONDARY).grid(
            row=5, column=0, sticky="w", padx=18, pady=(4, 4))

        ops_btn = ctk.CTkButton(
            sidebar, text="🚀  System Operations", font=FONT_SIDEBAR,
            height=36, corner_radius=8, anchor="w",
            fg_color="transparent", hover_color=BG_HOVER,
            text_color=TEXT_PRIMARY,
            command=self._show_operations,
        )
        ops_btn.grid(row=6, column=0, sticky="ew", padx=8, pady=2)
        self.sidebar_buttons["__operations__"] = ops_btn

        # ── Bottom: status & logout ──
        bottom = ctk.CTkFrame(sidebar, fg_color="transparent")
        bottom.grid(row=7, column=0, sticky="ew", padx=8, pady=(8, 12))
        bottom.grid_columnconfigure(0, weight=1)

        self.status_label = ctk.CTkLabel(
            bottom, text=self.db.get_status_text(),
            font=(FONT_SIDEBAR[0], 10), text_color=TEXT_SECONDARY,
            anchor="w", wraplength=SIDEBAR_WIDTH - 40,
        )
        self.status_label.grid(row=0, column=0, sticky="w", padx=4, pady=(0, 6))

        ctk.CTkButton(
            bottom, text="⏻  Disconnect", font=FONT_SIDEBAR,
            height=32, corner_radius=8,
            fg_color=DANGER, hover_color="#ff6b81",
            text_color="#fff", command=self._on_logout,
        ).grid(row=1, column=0, sticky="ew")

    # ── Content area ────────────────────────────────────────────────── #

    def _build_content_area(self):
        self.content = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=0)
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

    # ================================================================== #
    #  NAVIGATION                                                          #
    # ================================================================== #

    def _show_table(self, table_name):
        tbl_cfg = next((t for t in ALL_TABLES if t["table_name"] == table_name), None)
        if not tbl_cfg:
            return
        self._set_active(table_name)
        self._swap_content(CRUDScreen(self.content, tbl_cfg, self.db))

    def _show_operations(self):
        self._set_active("__operations__")
        self._swap_content(OperationsScreen(self.content, self.db))

    def _swap_content(self, new_widget):
        if self.current_screen:
            self.current_screen.destroy()
        self.current_screen = new_widget
        new_widget.grid(row=0, column=0, sticky="nsew")

    def _set_active(self, key):
        # Reset previous
        if self.active_btn and self.active_btn in [b for b in self.sidebar_buttons.values()]:
            self.active_btn.configure(fg_color="transparent", text_color=TEXT_PRIMARY)
        # Highlight new
        btn = self.sidebar_buttons.get(key)
        if btn:
            btn.configure(fg_color=BG_HOVER, text_color=ACCENT)
            self.active_btn = btn

    def _on_logout(self):
        self.db.disconnect()
        self.on_logout()
