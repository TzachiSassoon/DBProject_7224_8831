"""
SysManager – Login Screen
Secure connection card that reads config.ini and connects to the Supabase DB.
"""

import configparser
import os
import customtkinter as ctk

from ui.theme import (
    BG_DARKEST, BG_CARD, BG_INPUT, ACCENT, ACCENT_HOVER, ACCENT_DIM,
    DANGER, TEXT_PRIMARY, TEXT_SECONDARY, TEXT_HEADING, BORDER,
    FONT_TITLE, FONT_BODY, FONT_LABEL, FONT_BUTTON, FONT_BODY_SM,
    CORNER_RADIUS, ENTRY_HEIGHT, BUTTON_HEIGHT, PADDING,
)
from db.connection import DatabaseManager


class LoginScreen(ctk.CTkFrame):
    """Full-screen login card for database credentials."""

    def __init__(self, parent, on_login_success):
        super().__init__(parent, fg_color=BG_DARKEST)
        self.on_login_success = on_login_success
        self.db = DatabaseManager.get_instance()

        # Load defaults from config.ini
        self.defaults = self._load_config()

        self._build_ui()

    # ------------------------------------------------------------------ #
    #  Config loader                                                       #
    # ------------------------------------------------------------------ #

    def _load_config(self):
        config = configparser.ConfigParser()
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.ini")
        defaults = {
            "host": "", "port": "5432", "dbname": "postgres",
            "user": "postgres", "password": "",
        }
        if os.path.exists(config_path):
            config.read(config_path)
            if "database" in config:
                for key in defaults:
                    if key in config["database"]:
                        defaults[key] = config["database"][key]
        return defaults

    # ------------------------------------------------------------------ #
    #  UI                                                                  #
    # ------------------------------------------------------------------ #

    def _build_ui(self):
        # Centre container
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        card = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=18, width=480)
        card.grid(row=0, column=0)
        card.grid_propagate(False)
        card.configure(width=480, height=620)
        card.grid_columnconfigure(0, weight=1)

        row = 0

        # ── Logo / Title ──
        accent_bar = ctk.CTkFrame(card, fg_color=ACCENT, height=4, corner_radius=2)
        accent_bar.grid(row=row, column=0, sticky="ew", padx=40, pady=(32, 0))
        row += 1

        title = ctk.CTkLabel(card, text="SysManager", font=FONT_TITLE,
                              text_color=TEXT_HEADING)
        title.grid(row=row, column=0, pady=(12, 2))
        row += 1

        subtitle = ctk.CTkLabel(card, text="Database Management Console",
                                 font=FONT_BODY_SM, text_color=TEXT_SECONDARY)
        subtitle.grid(row=row, column=0, pady=(0, 24))
        row += 1

        # ── Fields ──
        fields_frame = ctk.CTkFrame(card, fg_color="transparent")
        fields_frame.grid(row=row, column=0, padx=36, sticky="ew")
        fields_frame.grid_columnconfigure(0, weight=1)
        row += 1

        self.entries = {}
        field_defs = [
            ("host",     "Host",     False),
            ("port",     "Port",     False),
            ("dbname",   "Database", False),
            ("user",     "User",     False),
            ("password", "Password", True),
        ]

        for i, (key, label, is_pass) in enumerate(field_defs):
            lbl = ctk.CTkLabel(fields_frame, text=label, font=FONT_LABEL,
                               text_color=TEXT_SECONDARY, anchor="w")
            lbl.grid(row=i * 2, column=0, sticky="w", pady=(8, 2))

            entry = ctk.CTkEntry(
                fields_frame,
                height=ENTRY_HEIGHT,
                font=FONT_BODY,
                fg_color=BG_INPUT,
                border_color=BORDER,
                border_width=1,
                corner_radius=8,
                text_color=TEXT_PRIMARY,
                placeholder_text=f"Enter {label.lower()}",
                show="•" if is_pass else "",
            )
            entry.grid(row=i * 2 + 1, column=0, sticky="ew")
            if self.defaults.get(key):
                entry.insert(0, self.defaults[key])
            self.entries[key] = entry

        # ── Status label ──
        self.status_label = ctk.CTkLabel(card, text="", font=FONT_BODY_SM,
                                          text_color=DANGER, wraplength=380)
        self.status_label.grid(row=row, column=0, pady=(12, 0))
        row += 1

        # ── Connect button ──
        self.connect_btn = ctk.CTkButton(
            card,
            text="Connect to Database",
            font=FONT_BUTTON,
            height=BUTTON_HEIGHT + 4,
            corner_radius=10,
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            text_color="#000000",
            command=self._on_connect,
        )
        self.connect_btn.grid(row=row, column=0, padx=36, pady=(16, 32), sticky="ew")

    # ------------------------------------------------------------------ #
    #  Connection logic                                                    #
    # ------------------------------------------------------------------ #

    def _on_connect(self):
        self.connect_btn.configure(state="disabled", text="Connecting…")
        self.status_label.configure(text="", text_color=DANGER)
        self.update_idletasks()

        vals = {k: e.get().strip() for k, e in self.entries.items()}

        # Basic validation
        for key, val in vals.items():
            if not val:
                self.status_label.configure(text=f"Please fill in the {key} field.")
                self.connect_btn.configure(state="normal", text="Connect to Database")
                return

        success, msg = self.db.connect(
            host=vals["host"],
            port=vals["port"],
            dbname=vals["dbname"],
            user=vals["user"],
            password=vals["password"],
        )

        if success:
            self.status_label.configure(text="✓  Connected!", text_color=ACCENT)
            self.update_idletasks()
            self.after(400, self.on_login_success)
        else:
            self.status_label.configure(text=msg, text_color=DANGER)
            self.connect_btn.configure(state="normal", text="Connect to Database")
