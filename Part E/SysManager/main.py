"""
SysManager – Entry Point
Launches the CustomTkinter desktop application.
"""

import customtkinter as ctk
from ui.theme import BG_DARKEST, configure_treeview_style
from ui.login_screen import LoginScreen
from ui.dashboard import Dashboard


class SysManagerApp(ctk.CTk):
    """Root application window."""

    def __init__(self):
        super().__init__()

        # ── Window setup ──
        self.title("SysManager  ·  Database Management Console")
        self.geometry("1360x820")
        self.minsize(1100, 700)
        self.configure(fg_color=BG_DARKEST)

        # Centre on screen
        self.update_idletasks()
        w, h = 1360, 820
        x = (self.winfo_screenwidth() - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

        # ── Apply dark Treeview style ──
        configure_treeview_style()

        # ── Layout ──
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Start with login
        self._show_login()

    # ------------------------------------------------------------------ #
    #  Screen transitions                                                  #
    # ------------------------------------------------------------------ #

    def _show_login(self):
        self._clear()
        login = LoginScreen(self, on_login_success=self._show_dashboard)
        login.grid(row=0, column=0, sticky="nsew")

    def _show_dashboard(self):
        self._clear()
        dash = Dashboard(self, on_logout=self._show_login)
        dash.grid(row=0, column=0, sticky="nsew")

    def _clear(self):
        for child in self.winfo_children():
            child.destroy()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Launch
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    app = SysManagerApp()
    app.mainloop()
