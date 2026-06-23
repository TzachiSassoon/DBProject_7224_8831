"""
SysManager – System Operations Screen
Four dedicated buttons that run specific SQL queries and stored procedures.
"""

import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
from tkinter import messagebox

from ui.theme import (
    BG_CARD, BG_INPUT, BG_SIDEBAR, BG_HOVER, BG_ROW_ALT,
    ACCENT, ACCENT_HOVER, ACCENT_DIM, DANGER, DANGER_HOVER,
    SUCCESS, WARNING,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_HEADING, BORDER,
    SCROLLBAR_BG, SCROLLBAR_FG,
    FONT_HEADING, FONT_SUBHEAD, FONT_BODY, FONT_BODY_SM,
    FONT_LABEL, FONT_BUTTON, FONT_MONO,
    CORNER_RADIUS, ENTRY_HEIGHT, BUTTON_HEIGHT, PADDING, ROW_HEIGHT,
)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Exact SQL queries (as specified in requirements)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SQL_RESOURCE_INTENSITY = """
SELECT p.process_name,
       rt.type_name,
       AVG(u.cpu_percent) AS process_avg_cpu,
       (SELECT AVG(u2.cpu_percent)
          FROM USAGE_LOGS u2
          JOIN PROCESSES p2    ON u2.pid = p2.pid
          JOIN ALLOCATIONS a2  ON p2.pid = a2.pid
          JOIN RESOURCES r2    ON a2.resource_id = r2.resource_id
         WHERE r2.type_id = rt.type_id) AS type_benchmark_avg
  FROM PROCESSES p
  JOIN USAGE_LOGS u    ON p.pid = u.pid
  JOIN ALLOCATIONS a   ON p.pid = a.pid
  JOIN RESOURCES r     ON a.resource_id = r.resource_id
  JOIN RESOURCE_TYPES rt ON r.type_id = rt.type_id
 GROUP BY p.process_name, rt.type_name, rt.type_id
HAVING AVG(u.cpu_percent) >
       (SELECT AVG(u2.cpu_percent)
          FROM USAGE_LOGS u2
          JOIN PROCESSES p2    ON u2.pid = p2.pid
          JOIN ALLOCATIONS a2  ON p2.pid = a2.pid
          JOIN RESOURCES r2    ON a2.resource_id = r2.resource_id
         WHERE r2.type_id = rt.type_id)
"""

SQL_MAINTENANCE_FINANCIAL = """
SELECT r.resource_name,
       rt.type_name,
       m.technician_name,
       m.repair_cost
  FROM RESOURCES r
  JOIN MAINTENANCE_LOG m   ON r.resource_id = m.resource_id
  JOIN RESOURCE_TYPES rt   ON r.type_id = rt.type_id
 WHERE r.is_operational = TRUE
 ORDER BY m.repair_cost DESC
"""


class OperationsScreen(ctk.CTkFrame):
    """System Operations dashboard with four action buttons."""

    def __init__(self, parent, db_manager):
        super().__init__(parent, fg_color=BG_CARD, corner_radius=0)
        self.db = db_manager
        self._build_ui()

    # ================================================================== #
    #  LAYOUT                                                              #
    # ================================================================== #

    def _build_ui(self):
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # ── Header ──
        ctk.CTkLabel(self, text="System Operations",
                     font=FONT_HEADING, text_color=TEXT_HEADING
                     ).grid(row=0, column=0, sticky="w", padx=24, pady=(18, 4))

        ctk.CTkLabel(self, text="Execute advanced queries and stored procedures",
                     font=FONT_BODY_SM, text_color=TEXT_SECONDARY
                     ).grid(row=1, column=0, sticky="w", padx=24, pady=(0, 12))

        # ── Main content ──
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.grid(row=2, column=0, sticky="nsew", padx=16, pady=(0, 16))
        content.grid_rowconfigure(1, weight=1)
        content.grid_columnconfigure(0, weight=1)

        # Button bar
        btn_bar = ctk.CTkFrame(content, fg_color="transparent")
        btn_bar.grid(row=0, column=0, sticky="ew", pady=(0, 12))

        buttons = [
            ("📊  Resource Intensity\n     Baseline",   ACCENT,  self._run_resource_intensity),
            ("🔧  Maintenance &\n     Financial Overview", "#6c63ff", self._run_maintenance),
            ("⚡  Handle Risky\n     Process",        WARNING, self._run_handle_risky),
            ("🔄  Update\n     Efficiencies",         "#e94560", self._run_update_efficiencies),
        ]

        for i, (text, color, cmd) in enumerate(buttons):
            btn = ctk.CTkButton(
                btn_bar, text=text, font=FONT_BUTTON,
                width=200, height=72, corner_radius=12,
                fg_color=color,
                hover_color=self._lighten(color),
                text_color="#000" if color in (ACCENT, WARNING) else "#fff",
                command=cmd,
                anchor="center",
            )
            btn.pack(side="left", padx=(0, 12))

        # ── Results area (tabview: Grid | Text) ──
        self.result_tabs = ctk.CTkTabview(
            content, fg_color=BG_CARD,
            segmented_button_fg_color=BG_SIDEBAR,
            segmented_button_selected_color=ACCENT,
            segmented_button_selected_hover_color=ACCENT_HOVER,
            segmented_button_unselected_color=BG_SIDEBAR,
            segmented_button_unselected_hover_color=BG_HOVER,
            text_color=TEXT_PRIMARY,
            corner_radius=10,
        )
        self.result_tabs.grid(row=1, column=0, sticky="nsew")

        tab_grid = self.result_tabs.add("  Grid View  ")
        tab_text = self.result_tabs.add("  Text Log  ")

        # Grid tab
        tab_grid.grid_rowconfigure(0, weight=1)
        tab_grid.grid_columnconfigure(0, weight=1)

        self.result_tree_frame = ctk.CTkFrame(tab_grid, fg_color=BG_CARD)
        self.result_tree_frame.grid(row=0, column=0, sticky="nsew")
        self.result_tree_frame.grid_rowconfigure(0, weight=1)
        self.result_tree_frame.grid_columnconfigure(0, weight=1)

        self.result_tree = None  # Created dynamically per query

        # Text tab
        tab_text.grid_rowconfigure(0, weight=1)
        tab_text.grid_columnconfigure(0, weight=1)

        self.result_text = ctk.CTkTextbox(
            tab_text, font=FONT_MONO,
            fg_color=BG_INPUT, text_color=TEXT_PRIMARY,
            border_color=BORDER, border_width=1, corner_radius=8,
            state="disabled",
        )
        self.result_text.grid(row=0, column=0, sticky="nsew", padx=4, pady=4)

    # ================================================================== #
    #  BUTTON HANDLERS                                                     #
    # ================================================================== #

    def _run_resource_intensity(self):
        self._append_log("▸ Executing: Resource Intensity Baseline …")
        cols, rows, err = self.db.fetch_all(SQL_RESOURCE_INTENSITY)
        if err:
            self._append_log(f"  ✗ Error: {err}\n")
            messagebox.showerror("Query Error", err)
            return
        self._display_grid(cols, rows)
        self._append_log(f"  ✓ Returned {len(rows)} rows.\n")

    def _run_maintenance(self):
        self._append_log("▸ Executing: Maintenance & Financial Overview …")
        cols, rows, err = self.db.fetch_all(SQL_MAINTENANCE_FINANCIAL)
        if err:
            self._append_log(f"  ✗ Error: {err}\n")
            messagebox.showerror("Query Error", err)
            return
        self._display_grid(cols, rows)
        self._append_log(f"  ✓ Returned {len(rows)} rows.\n")

    def _run_handle_risky(self):
        """Prompt user for pid and account_type, then CALL handle_risky_process."""
        dialog = _ProcedureInputDialog(
            self,
            title="Handle Risky Process",
            fields=[
                ("pid", "Process ID (INT)", "int"),
                ("account_type", "Account Type (VARCHAR)", "str"),
            ],
        )
        self.wait_window(dialog)

        if not dialog.result:
            self._append_log("▸ Handle Risky Process – cancelled by user.\n")
            return

        pid_val = dialog.result["pid"]
        acct_val = dialog.result["account_type"]

        self._append_log(
            f"▸ Executing: CALL handle_risky_process({pid_val}, '{acct_val}') …")

        ok, msg = self.db.call_procedure(
            "CALL handle_risky_process(%s, %s)", (pid_val, acct_val)
        )
        if ok:
            self._append_log(f"  ✓ {msg}\n")
            self._display_message("Procedure executed successfully.\n\n"
                                  f"PID: {pid_val}\nAccount Type: {acct_val}")
        else:
            self._append_log(f"  ✗ Error: {msg}\n")
            messagebox.showerror("Procedure Error", msg)

    def _run_update_efficiencies(self):
        self._append_log("▸ Executing: CALL update_efficiencies() …")
        ok, msg = self.db.call_procedure("CALL update_efficiencies()")
        if ok:
            self._append_log(f"  ✓ {msg}\n")
            self._display_message("update_efficiencies() completed successfully.\n\n"
                                  "Resource efficiency scores have been recalculated.")
        else:
            self._append_log(f"  ✗ Error: {msg}\n")
            messagebox.showerror("Procedure Error", msg)

    # ================================================================== #
    #  RESULT DISPLAY                                                      #
    # ================================================================== #

    def _display_grid(self, columns, rows):
        """Recreate the Treeview with the query's result set."""
        # Destroy old tree
        for child in self.result_tree_frame.winfo_children():
            child.destroy()

        self.result_tree_frame.grid_rowconfigure(0, weight=1)
        self.result_tree_frame.grid_columnconfigure(0, weight=1)

        tree = ttk.Treeview(self.result_tree_frame, columns=columns,
                            show="headings", style="Dark.Treeview",
                            selectmode="browse")
        for col in columns:
            nice = col.replace("_", " ").title()
            tree.heading(col, text=nice, anchor="w")
            tree.column(col, anchor="w", minwidth=80, width=160)

        vsb = tk.Scrollbar(self.result_tree_frame, orient="vertical",
                            command=tree.yview,
                            bg=SCROLLBAR_FG, troughcolor=SCROLLBAR_BG,
                            activebackground=ACCENT_DIM,
                            highlightthickness=0, bd=0, width=12)
        hsb = tk.Scrollbar(self.result_tree_frame, orient="horizontal",
                            command=tree.xview,
                            bg=SCROLLBAR_FG, troughcolor=SCROLLBAR_BG,
                            activebackground=ACCENT_DIM,
                            highlightthickness=0, bd=0, width=12)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        tree.tag_configure("odd",  background=BG_CARD)
        tree.tag_configure("even", background=BG_ROW_ALT)

        for i, row in enumerate(rows):
            tag = "even" if i % 2 == 0 else "odd"
            vals = [self._fmt(v) for v in row]
            tree.insert("", "end", values=vals, tags=(tag,))

        # Mouse-wheel scrolling
        def _on_mousewheel(event):
            tree.yview_scroll(int(-1 * (event.delta / 120)), "units")

        tree.bind("<MouseWheel>", _on_mousewheel)
        self.result_tree_frame.bind("<MouseWheel>", _on_mousewheel)
        vsb.bind("<MouseWheel>", _on_mousewheel)

        def _bind_wheel(event):
            tree.winfo_toplevel().bind_all("<MouseWheel>", _on_mousewheel)

        def _unbind_wheel(event):
            tree.winfo_toplevel().unbind_all("<MouseWheel>")

        tree.bind("<Enter>", _bind_wheel)
        tree.bind("<Leave>", _unbind_wheel)

        self.result_tree = tree
        self.result_tabs.set("  Grid View  ")

    def _display_message(self, msg):
        """Show a text message in the grid area."""
        for child in self.result_tree_frame.winfo_children():
            child.destroy()

        lbl = ctk.CTkLabel(self.result_tree_frame, text=msg,
                            font=FONT_BODY, text_color=SUCCESS,
                            justify="left", anchor="nw")
        lbl.grid(row=0, column=0, sticky="nw", padx=24, pady=24)

    def _append_log(self, text):
        self.result_text.configure(state="normal")
        self.result_text.insert("end", text + "\n")
        self.result_text.see("end")
        self.result_text.configure(state="disabled")

    @staticmethod
    def _fmt(val):
        if val is None:
            return ""
        if isinstance(val, bool):
            return "Yes" if val else "No"
        if isinstance(val, float):
            return f"{val:.2f}"
        return str(val)

    @staticmethod
    def _lighten(hex_color):
        """Naïve hex lighten for hover states."""
        try:
            hex_color = hex_color.lstrip("#")
            r, g, b = int(hex_color[:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
            r = min(255, r + 30)
            g = min(255, g + 30)
            b = min(255, b + 30)
            return f"#{r:02x}{g:02x}{b:02x}"
        except Exception:
            return hex_color


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Input dialog for stored procedure parameters
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class _ProcedureInputDialog(ctk.CTkToplevel):
    """Modal dialog that prompts for procedure parameters."""

    def __init__(self, parent, title, fields):
        super().__init__(parent)
        self.title(title)
        self.geometry("420x320")
        self.resizable(False, False)
        self.configure(fg_color=BG_CARD)
        self.result = None
        self.fields_meta = fields
        self.entries = {}

        self.transient(parent)
        self.grab_set()

        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self._on_cancel)

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self, text=self.title(), font=FONT_SUBHEAD,
                     text_color=TEXT_HEADING).grid(
            row=0, column=0, pady=(20, 16), padx=24, sticky="w")

        form = ctk.CTkFrame(self, fg_color="transparent")
        form.grid(row=1, column=0, sticky="ew", padx=24)
        form.grid_columnconfigure(1, weight=1)

        for i, (key, label, _) in enumerate(self.fields_meta):
            ctk.CTkLabel(form, text=label, font=FONT_LABEL,
                         text_color=TEXT_SECONDARY, anchor="w").grid(
                row=i, column=0, sticky="w", padx=(0, 12), pady=8)

            entry = ctk.CTkEntry(form, height=ENTRY_HEIGHT, font=FONT_BODY,
                                  fg_color=BG_INPUT, border_color=BORDER,
                                  border_width=1, corner_radius=8,
                                  text_color=TEXT_PRIMARY)
            entry.grid(row=i, column=1, sticky="ew", pady=8)
            self.entries[key] = entry

        self.error_label = ctk.CTkLabel(self, text="", font=FONT_BODY_SM,
                                         text_color=DANGER)
        self.error_label.grid(row=2, column=0, pady=(8, 0), padx=24, sticky="w")

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=3, column=0, pady=(12, 20), padx=24, sticky="ew")

        ctk.CTkButton(btn_frame, text="Execute", font=FONT_BUTTON,
                       height=BUTTON_HEIGHT, corner_radius=8,
                       fg_color=ACCENT, hover_color=ACCENT_HOVER,
                       text_color="#000", command=self._on_submit
                       ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(btn_frame, text="Cancel", font=FONT_BUTTON,
                       height=BUTTON_HEIGHT, corner_radius=8,
                       fg_color=BG_INPUT, hover_color=BG_HOVER,
                       text_color=TEXT_PRIMARY, command=self._on_cancel
                       ).pack(side="left")

    def _on_submit(self):
        result = {}
        for key, label, ftype in self.fields_meta:
            val = self.entries[key].get().strip()
            if not val:
                self.error_label.configure(text=f"'{label}' is required.")
                return
            try:
                if ftype == "int":
                    result[key] = int(val)
                else:
                    result[key] = val
            except ValueError:
                self.error_label.configure(text=f"'{label}' must be a valid {ftype}.")
                return

        self.result = result
        self.destroy()

    def _on_cancel(self):
        self.result = None
        self.destroy()
