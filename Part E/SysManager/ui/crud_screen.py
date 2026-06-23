"""
SysManager – Generic CRUD Screen
A data-driven widget that provides Read / Create / Update / Delete tabs
for any table defined in table_configs.py.
"""

import calendar
import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
from tkinter import messagebox

from ui.theme import (
    BG_CARD, BG_INPUT, BG_SIDEBAR, BG_HOVER, BG_ROW_ALT,
    ACCENT, ACCENT_HOVER, ACCENT_DIM, DANGER, DANGER_HOVER, SUCCESS, WARNING,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_HEADING, BORDER,
    SCROLLBAR_BG, SCROLLBAR_FG,
    FONT_SUBHEAD, FONT_BODY, FONT_BODY_SM, FONT_LABEL, FONT_BUTTON,
    FONT_MONO, FONT_HEADING,
    CORNER_RADIUS, ENTRY_HEIGHT, BUTTON_HEIGHT, PADDING, ROW_HEIGHT,
)
from ui.table_configs import BOOL, TEXT, DATE


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Date Picker Widget  (Year list → Month grid → Day grid)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

_MONTH_ABBR = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
_DAY_HEADERS = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]

_CELL_FONT       = ("Segoe UI", 11)
_CELL_FONT_BOLD  = ("Segoe UI", 11, "bold")
_HEADER_FONT     = ("Segoe UI", 12, "bold")


class DatePickerWidget(ctk.CTkFrame):
    """Three-step date selector: year → month → day.

    Public interface matches CTkEntry so existing form helpers work:
        .get()               → 'YYYY-MM-DD' or ''
        .set(value)          → parse and display
        .delete(0, 'end')    → clear
        .configure(state=..) → enable / disable
    """

    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color=BG_INPUT, corner_radius=8,
                         border_color=BORDER, border_width=1, **kwargs)

        self._year = None
        self._month = None
        self._day = None
        self._disabled = False

        self.grid_columnconfigure(0, weight=1)

        # ── Row 0: display label showing current value ──
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.grid(row=0, column=0, sticky="ew", padx=6, pady=(6, 2))
        top.grid_columnconfigure(0, weight=1)

        self._display_label = ctk.CTkLabel(
            top, text="Select a date…", font=FONT_BODY,
            text_color=TEXT_SECONDARY, anchor="w")
        self._display_label.grid(row=0, column=0, sticky="w")

        self._clear_btn = ctk.CTkButton(
            top, text="✕", width=28, height=24, corner_radius=6,
            font=("Segoe UI", 11, "bold"),
            fg_color="transparent", hover_color=BG_HOVER,
            text_color=TEXT_SECONDARY, command=self._on_clear)
        self._clear_btn.grid(row=0, column=1, padx=(4, 0))

        # ── Row 1: step area (swapped between year / month / day) ──
        self._step_frame = ctk.CTkFrame(self, fg_color="transparent")
        self._step_frame.grid(row=1, column=0, sticky="nsew", padx=4, pady=(2, 6))
        self._step_frame.grid_columnconfigure(0, weight=1)

        self._show_year_step()

    # ────────────────────── YEAR STEP ──────────────────────

    def _show_year_step(self):
        self._clear_step_frame()
        self._year = None
        self._month = None
        self._day = None
        self._update_display()

        container = ctk.CTkFrame(self._step_frame, fg_color="transparent")
        container.grid(row=0, column=0, sticky="ew")
        container.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(container, text="Year", font=_HEADER_FONT,
                     text_color=ACCENT).grid(row=0, column=0, sticky="w",
                                             padx=4, pady=(2, 4))

        # Scrollable list of years
        scroll = ctk.CTkScrollableFrame(
            container, fg_color="transparent", height=110,
            scrollbar_button_color=BG_HOVER,
            scrollbar_button_hover_color=ACCENT_DIM)
        scroll.grid(row=1, column=0, sticky="ew")
        scroll.grid_columnconfigure(tuple(range(5)), weight=1)

        import datetime
        current_year = datetime.date.today().year
        years = list(range(current_year - 30, current_year + 11))

        for idx, yr in enumerate(years):
            r, c = divmod(idx, 5)
            is_current = (yr == current_year)
            btn = ctk.CTkButton(
                scroll, text=str(yr), width=56, height=28,
                corner_radius=6, font=_CELL_FONT_BOLD if is_current else _CELL_FONT,
                fg_color=ACCENT_DIM if is_current else "transparent",
                hover_color=BG_HOVER, text_color=TEXT_PRIMARY,
                command=lambda y=yr: self._pick_year(y))
            btn.grid(row=r, column=c, padx=2, pady=2, sticky="ew")

    def _pick_year(self, year):
        if self._disabled:
            return
        self._year = year
        self._show_month_step()

    # ────────────────────── MONTH STEP ──────────────────────

    def _show_month_step(self):
        self._clear_step_frame()
        self._month = None
        self._day = None
        self._update_display()

        container = ctk.CTkFrame(self._step_frame, fg_color="transparent")
        container.grid(row=0, column=0, sticky="ew")
        container.grid_columnconfigure(0, weight=1)

        # Sub-header with back button
        hdr = ctk.CTkFrame(container, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", padx=4, pady=(2, 4))
        hdr.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(hdr, text="◀", width=28, height=24, corner_radius=6,
                       fg_color="transparent", hover_color=BG_HOVER,
                       text_color=TEXT_SECONDARY, font=_CELL_FONT,
                       command=self._show_year_step).grid(row=0, column=0)

        ctk.CTkLabel(hdr, text=f"Month  ·  {self._year}", font=_HEADER_FONT,
                     text_color=ACCENT).grid(row=0, column=1, sticky="w", padx=6)

        # 4×3 month grid
        grid = ctk.CTkFrame(container, fg_color="transparent")
        grid.grid(row=1, column=0, sticky="ew")
        for c in range(4):
            grid.grid_columnconfigure(c, weight=1)

        for idx, abbr in enumerate(_MONTH_ABBR):
            r, c = divmod(idx, 4)
            btn = ctk.CTkButton(
                grid, text=abbr, width=52, height=30, corner_radius=6,
                font=_CELL_FONT, fg_color="transparent", hover_color=BG_HOVER,
                text_color=TEXT_PRIMARY,
                command=lambda m=idx + 1: self._pick_month(m))
            btn.grid(row=r, column=c, padx=2, pady=2, sticky="ew")

    def _pick_month(self, month):
        if self._disabled:
            return
        self._month = month
        self._show_day_step()

    # ────────────────────── DAY STEP ──────────────────────

    def _show_day_step(self):
        self._clear_step_frame()
        self._day = None
        self._update_display()

        container = ctk.CTkFrame(self._step_frame, fg_color="transparent")
        container.grid(row=0, column=0, sticky="ew")
        container.grid_columnconfigure(0, weight=1)

        # Sub-header with back button
        hdr = ctk.CTkFrame(container, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", padx=4, pady=(2, 4))
        hdr.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(hdr, text="◀", width=28, height=24, corner_radius=6,
                       fg_color="transparent", hover_color=BG_HOVER,
                       text_color=TEXT_SECONDARY, font=_CELL_FONT,
                       command=self._show_month_step).grid(row=0, column=0)

        month_name = _MONTH_ABBR[self._month - 1]
        ctk.CTkLabel(hdr, text=f"Day  ·  {month_name} {self._year}",
                     font=_HEADER_FONT,
                     text_color=ACCENT).grid(row=0, column=1, sticky="w", padx=6)

        # Day-of-week header row
        grid = ctk.CTkFrame(container, fg_color="transparent")
        grid.grid(row=1, column=0, sticky="ew")
        for c in range(7):
            grid.grid_columnconfigure(c, weight=1)

        for c, dh in enumerate(_DAY_HEADERS):
            ctk.CTkLabel(grid, text=dh, font=_CELL_FONT_BOLD,
                         text_color=ACCENT_DIM, width=34).grid(
                row=0, column=c, padx=1, pady=(0, 2))

        # Calendar days
        cal = calendar.Calendar(firstweekday=0)  # Monday start
        weeks = cal.monthdayscalendar(self._year, self._month)
        for w_idx, week in enumerate(weeks):
            for d_idx, day in enumerate(week):
                if day == 0:
                    # Empty cell
                    ctk.CTkLabel(grid, text="", width=34, height=28).grid(
                        row=w_idx + 1, column=d_idx, padx=1, pady=1)
                else:
                    btn = ctk.CTkButton(
                        grid, text=str(day), width=34, height=28,
                        corner_radius=6, font=_CELL_FONT,
                        fg_color="transparent", hover_color=BG_HOVER,
                        text_color=TEXT_PRIMARY,
                        command=lambda d=day: self._pick_day(d))
                    btn.grid(row=w_idx + 1, column=d_idx, padx=1, pady=1,
                             sticky="ew")

    def _pick_day(self, day):
        if self._disabled:
            return
        self._day = day
        self._update_display()

    # ────────────────────── HELPERS ──────────────────────

    def _clear_step_frame(self):
        for w in self._step_frame.winfo_children():
            w.destroy()

    def _update_display(self):
        val = self.get()
        if val:
            self._display_label.configure(text=val, text_color=TEXT_PRIMARY)
        else:
            parts = []
            if self._year is not None:
                parts.append(str(self._year))
            if self._month is not None:
                parts.append(_MONTH_ABBR[self._month - 1])
            if parts:
                self._display_label.configure(
                    text=" · ".join(parts) + " · …",
                    text_color=TEXT_SECONDARY)
            else:
                self._display_label.configure(
                    text="Select a date…", text_color=TEXT_SECONDARY)

    def _on_clear(self):
        if self._disabled:
            return
        self._show_year_step()

    # ── Public API (CTkEntry-compatible) ──

    def get(self):
        """Return 'YYYY-MM-DD' or '' if incomplete."""
        if self._year and self._month and self._day:
            return f"{self._year:04d}-{self._month:02d}-{self._day:02d}"
        return ""

    def set(self, value):
        """Parse 'YYYY-MM-DD' and display. Accepts str or datetime.date."""
        import datetime
        if isinstance(value, datetime.date):
            self._year = value.year
            self._month = value.month
            self._day = value.day
            self._update_display()
            # Show day step so user can re-pick if desired
            self._show_day_step()
            self._day = value.day          # restore after rebuild
            self._update_display()
            return
        s = str(value).strip() if value else ""
        if not s:
            self._show_year_step()
            return
        try:
            parts = s.split("-")
            self._year = int(parts[0])
            self._month = int(parts[1])
            self._day = int(parts[2])
            self._show_day_step()
            self._day = int(parts[2])      # restore after rebuild
            self._update_display()
        except (IndexError, ValueError):
            self._show_year_step()

    def delete(self, *_args):
        """Clear the date selection (CTkEntry compat)."""
        self._show_year_step()

    def configure(self, **kwargs):
        state = kwargs.pop("state", None)
        if state is not None:
            self._disabled = (state == "disabled")
        super().configure(**kwargs)


class CRUDScreen(ctk.CTkFrame):
    """Reusable CRUD widget driven by a table_config dict."""

    def __init__(self, parent, table_config, db_manager):
        super().__init__(parent, fg_color=BG_CARD, corner_radius=0)
        self.cfg = table_config
        self.db = db_manager
        self.fk_cache = {}        # column_name → [(id, display), ...]
        self.update_fields = {}   # column_name → widget  (Update tab)
        self.create_fields = {}   # column_name → widget  (Create tab)
        self._all_rows = []       # cached rows for search filtering
        self._all_cols = []       # cached column names

        self._build_ui()

    # ================================================================== #
    #  TOP-LEVEL LAYOUT                                                    #
    # ================================================================== #

    def _build_ui(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # ── Header ──
        header = ctk.CTkFrame(self, fg_color="transparent", height=56)
        header.grid(row=0, column=0, sticky="ew", padx=24, pady=(18, 0))
        header.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(header, text=self.cfg["display_name"],
                     font=FONT_HEADING, text_color=TEXT_HEADING).grid(
            row=0, column=0, sticky="w")

        pk_badge = ctk.CTkLabel(header,
                                text=f"PK: {self.cfg['primary_key']}",
                                font=FONT_BODY_SM, text_color=ACCENT,
                                fg_color=BG_INPUT, corner_radius=6,
                                padx=10, pady=4)
        pk_badge.grid(row=0, column=1, sticky="w", padx=16)

        # ── Tabview ──
        self.tabview = ctk.CTkTabview(
            self, fg_color=BG_CARD,
            segmented_button_fg_color=BG_SIDEBAR,
            segmented_button_selected_color=ACCENT,
            segmented_button_selected_hover_color=ACCENT_HOVER,
            segmented_button_unselected_color=BG_SIDEBAR,
            segmented_button_unselected_hover_color=BG_HOVER,
            text_color=TEXT_PRIMARY,
            corner_radius=12,
        )
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=16, pady=(8, 16))

        tab_read   = self.tabview.add("  Read  ")
        tab_create = self.tabview.add("  Create  ")
        tab_update = self.tabview.add("  Update  ")
        tab_delete = self.tabview.add("  Delete  ")

        self._build_read_tab(tab_read)
        self._build_create_tab(tab_create)
        self._build_update_tab(tab_update)
        self._build_delete_tab(tab_delete)

    # ================================================================== #
    #  READ TAB                                                            #
    # ================================================================== #

    def _build_read_tab(self, parent):
        parent.grid_rowconfigure(1, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        # Toolbar
        toolbar = ctk.CTkFrame(parent, fg_color="transparent", height=42)
        toolbar.grid(row=0, column=0, sticky="ew", pady=(4, 8))

        ctk.CTkButton(toolbar, text="Refresh", font=FONT_BUTTON,
                       width=100, height=34, corner_radius=8,
                       fg_color=ACCENT, hover_color=ACCENT_HOVER,
                       text_color="#000", command=self._load_read_data
                       ).pack(side="left", padx=(0, 12))

        # Search bar
        self.search_entry = ctk.CTkEntry(
            toolbar, height=34, width=260, font=FONT_BODY,
            fg_color=BG_INPUT, border_color=BORDER, border_width=1,
            corner_radius=8, text_color=TEXT_PRIMARY,
            placeholder_text="Search...",
        )
        self.search_entry.pack(side="left", padx=(0, 4))
        self.search_entry.bind("<Return>", lambda e: self._on_search())

        # Attribute selector dropdown
        display_cols = self.cfg["read_display_columns"]
        col_labels = [c.replace("_", " ").title() for c in display_cols]
        self.search_attr_combo = ctk.CTkComboBox(
            toolbar, values=col_labels, font=FONT_BODY_SM,
            width=170, height=34, corner_radius=8,
            fg_color=BG_INPUT, border_color=BORDER, border_width=1,
            text_color=TEXT_PRIMARY,
            button_color=ACCENT_DIM, button_hover_color=ACCENT,
            dropdown_fg_color=BG_INPUT, dropdown_hover_color=BG_HOVER,
            dropdown_text_color=TEXT_PRIMARY,
            state="readonly",
        )
        self.search_attr_combo.set(col_labels[0])
        self.search_attr_combo.pack(side="left", padx=(0, 4))

        ctk.CTkButton(toolbar, text="Search", font=FONT_BUTTON,
                       width=90, height=34, corner_radius=8,
                       fg_color=ACCENT_DIM, hover_color=ACCENT,
                       text_color="#000", command=self._on_search
                       ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(toolbar, text="Clear", font=FONT_BODY_SM,
                       width=70, height=34, corner_radius=8,
                       fg_color=BG_INPUT, hover_color=BG_HOVER,
                       text_color=TEXT_SECONDARY, command=self._clear_search
                       ).pack(side="left", padx=(0, 12))

        self.row_count_label = ctk.CTkLabel(toolbar, text="",
                                             font=FONT_BODY_SM,
                                             text_color=TEXT_SECONDARY)
        self.row_count_label.pack(side="right", padx=8)

        # Treeview frame
        tree_frame = ctk.CTkFrame(parent, fg_color=BG_CARD, corner_radius=0)
        tree_frame.grid(row=1, column=0, sticky="nsew")
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(tree_frame, columns=display_cols,
                                  show="headings", style="Dark.Treeview",
                                  selectmode="browse")
        for col in display_cols:
            nice = col.replace("_", " ").title()
            self.tree.heading(col, text=nice, anchor="w")
            self.tree.column(col, anchor="w", minwidth=80, width=140)

        vsb = tk.Scrollbar(tree_frame, orient="vertical",
                            command=self.tree.yview,
                            bg=SCROLLBAR_FG, troughcolor=SCROLLBAR_BG,
                            activebackground=ACCENT_DIM,
                            highlightthickness=0, bd=0, width=12)
        hsb = tk.Scrollbar(tree_frame, orient="horizontal",
                            command=self.tree.xview,
                            bg=SCROLLBAR_FG, troughcolor=SCROLLBAR_BG,
                            activebackground=ACCENT_DIM,
                            highlightthickness=0, bd=0, width=12)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        # Alternate row colours via tags
        self.tree.tag_configure("odd",  background=BG_CARD)
        self.tree.tag_configure("even", background=BG_ROW_ALT)

        # ── Mouse-wheel scrolling (Windows needs explicit binding) ──
        def _on_mousewheel(event):
            self.tree.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.tree.bind("<MouseWheel>", _on_mousewheel)
        # Also capture wheel when hovering the scrollbar or frame
        tree_frame.bind("<MouseWheel>", _on_mousewheel)
        vsb.bind("<MouseWheel>", _on_mousewheel)

        # Bind/unbind global mousewheel so scrolling works even when
        # the cursor is anywhere over the tree area.
        def _bind_wheel(event):
            self.tree.winfo_toplevel().bind_all("<MouseWheel>", _on_mousewheel)

        def _unbind_wheel(event):
            self.tree.winfo_toplevel().unbind_all("<MouseWheel>")

        self.tree.bind("<Enter>", _bind_wheel)
        self.tree.bind("<Leave>", _unbind_wheel)

        # Initial load
        self.after(100, self._load_read_data)

    def _load_read_data(self):
        """Fetch all rows from the DB, cache them, and display."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        cols, rows, err = self.db.fetch_all(self.cfg["read_query"])
        if err:
            messagebox.showerror("Query Error", err)
            return

        # Cache for search filtering
        self._all_cols = cols
        self._all_rows = [[self._format_cell(v) for v in row] for row in rows]

        self._populate_tree(self._all_rows)

    def _populate_tree(self, rows):
        """Fill the treeview with the given (already-formatted) rows."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        for i, values in enumerate(rows):
            tag = "even" if i % 2 == 0 else "odd"
            self.tree.insert("", "end", values=values, tags=(tag,))
        self.row_count_label.configure(text=f"{len(rows)} rows")

    def _get_display_col_type(self, display_col_name):
        """Determine the data type for a read-display column.

        Direct columns use their defined type from the config.
        FK-masked columns (e.g. username, resource_name) are always strings.
        """
        # Build a lookup from the direct column definitions
        col_types = {c["name"]: c["type"] for c in self.cfg["columns"]}
        if display_col_name in col_types:
            return col_types[display_col_name]
        # Not a direct column → it's a FK display value, always a string
        return "str"

    def _on_search(self):
        """Filter cached rows by the selected attribute and search text.

        Matching strategy per column type:
          - int / bigint / decimal / bool / date / timestamp → exact match
          - str / text (names, paths, descriptions) → case-insensitive substring
        """
        query = self.search_entry.get().strip()
        if not query:
            self._populate_tree(self._all_rows)
            return

        # Resolve selected column index and its type
        display_cols = self.cfg["read_display_columns"]
        selected_label = self.search_attr_combo.get()
        col_idx = 0
        col_name = display_cols[0]
        for i, c in enumerate(display_cols):
            if c.replace("_", " ").title() == selected_label:
                col_idx = i
                col_name = c
                break

        col_type = self._get_display_col_type(col_name)

        # String-like types → case-insensitive substring (contains)
        if col_type in ("str", "text"):
            query_lower = query.lower()
            filtered = [row for row in self._all_rows
                        if query_lower in str(row[col_idx]).lower()]
        else:
            # Numeric / bool / date / timestamp → exact match
            query_lower = query.lower()
            filtered = [row for row in self._all_rows
                        if str(row[col_idx]).lower() == query_lower]

        self._populate_tree(filtered)

    def _clear_search(self):
        """Reset the search bar and show all rows."""
        self.search_entry.delete(0, "end")
        self._populate_tree(self._all_rows)

    @staticmethod
    def _format_cell(value):
        if value is None:
            return ""
        if isinstance(value, bool):
            return "Yes" if value else "No"
        return str(value)

    # ================================================================== #
    #  CREATE TAB                                                          #
    # ================================================================== #

    def _build_create_tab(self, parent):
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        scroll = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        scroll.grid(row=0, column=0, sticky="nsew")
        scroll.grid_columnconfigure(1, weight=1)

        self.create_fields = {}
        r = 0
        for col_def in self.cfg["columns"]:
            name = col_def["name"]
            lbl = ctk.CTkLabel(scroll, text=col_def["label"],
                               font=FONT_LABEL, text_color=TEXT_SECONDARY, anchor="w")
            lbl.grid(row=r, column=0, sticky="w", padx=(8, 16), pady=(10, 2))

            widget = self._make_input_widget(scroll, col_def, self.create_fields, name)
            widget.grid(row=r, column=1, sticky="ew", padx=(0, 8), pady=(10, 2))
            r += 1

        # Status + button
        self.create_status = ctk.CTkLabel(scroll, text="", font=FONT_BODY_SM,
                                           text_color=DANGER, anchor="w")
        self.create_status.grid(row=r, column=0, columnspan=2, sticky="w",
                                 padx=8, pady=(12, 2))
        r += 1

        btn_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        btn_frame.grid(row=r, column=0, columnspan=2, sticky="ew", pady=(4, 16))

        ctk.CTkButton(btn_frame, text="Insert Row", font=FONT_BUTTON,
                       height=BUTTON_HEIGHT, corner_radius=8,
                       fg_color=ACCENT, hover_color=ACCENT_HOVER,
                       text_color="#000", command=self._on_create
                       ).pack(side="left", padx=8)

        ctk.CTkButton(btn_frame, text="Clear", font=FONT_BUTTON,
                       height=BUTTON_HEIGHT, corner_radius=8,
                       fg_color=BG_INPUT, hover_color=BG_HOVER,
                       text_color=TEXT_PRIMARY,
                       command=lambda: self._clear_fields(self.create_fields)
                       ).pack(side="left", padx=4)

    def _on_create(self):
        values, err = self._collect_form_values(self.create_fields)
        if err:
            self.create_status.configure(text=err, text_color=DANGER)
            return

        col_names = list(values.keys())
        placeholders = ", ".join(["%s"] * len(col_names))
        col_list = ", ".join(col_names)
        sql = f'INSERT INTO {self.cfg["table_name"]} ({col_list}) VALUES ({placeholders})'

        affected, db_err = self.db.execute(sql, list(values.values()))
        if db_err:
            self.create_status.configure(text=f"Error: {db_err}", text_color=DANGER)
        else:
            self.create_status.configure(text="✓  Row inserted successfully.",
                                          text_color=SUCCESS)
            self._clear_fields(self.create_fields)
            self._load_read_data()

    # ================================================================== #
    #  UPDATE TAB  (fetch-before-update)                                   #
    # ================================================================== #

    def _build_update_tab(self, parent):
        parent.grid_rowconfigure(1, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        # ── PK fetch bar ──
        fetch_bar = ctk.CTkFrame(parent, fg_color=BG_INPUT, corner_radius=10)
        fetch_bar.grid(row=0, column=0, sticky="ew", padx=4, pady=(8, 4))
        fetch_bar.grid_columnconfigure(1, weight=1)

        pk = self.cfg["primary_key"]
        ctk.CTkLabel(fetch_bar,
                     text=f"Enter {pk.replace('_',' ').title()}:",
                     font=FONT_LABEL, text_color=TEXT_SECONDARY
                     ).grid(row=0, column=0, padx=(12, 8), pady=10)

        self.update_pk_entry = ctk.CTkEntry(
            fetch_bar, height=ENTRY_HEIGHT, font=FONT_BODY,
            fg_color=BG_CARD, border_color=BORDER, border_width=1,
            corner_radius=8, text_color=TEXT_PRIMARY, width=180,
            placeholder_text=f"{pk}",
        )
        self.update_pk_entry.grid(row=0, column=1, sticky="w", pady=10)

        ctk.CTkButton(fetch_bar, text="Fetch", font=FONT_BUTTON,
                       width=100, height=34, corner_radius=8,
                       fg_color=ACCENT, hover_color=ACCENT_HOVER,
                       text_color="#000", command=self._on_fetch_for_update
                       ).grid(row=0, column=2, padx=12, pady=10)

        # ── Scrollable form ──
        scroll = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        scroll.grid(row=1, column=0, sticky="nsew")
        scroll.grid_columnconfigure(1, weight=1)

        self.update_fields = {}
        r = 0
        for col_def in self.cfg["columns"]:
            name = col_def["name"]
            if col_def.get("pk"):
                continue  # PK is in the fetch bar
            lbl = ctk.CTkLabel(scroll, text=col_def["label"],
                               font=FONT_LABEL, text_color=TEXT_SECONDARY, anchor="w")
            lbl.grid(row=r, column=0, sticky="w", padx=(8, 16), pady=(10, 2))

            widget = self._make_input_widget(scroll, col_def, self.update_fields, name)
            widget.grid(row=r, column=1, sticky="ew", padx=(0, 8), pady=(10, 2))
            widget.configure(state="disabled")
            r += 1

        self.update_status = ctk.CTkLabel(scroll, text="", font=FONT_BODY_SM,
                                           text_color=DANGER, anchor="w")
        self.update_status.grid(row=r, column=0, columnspan=2, sticky="w",
                                 padx=8, pady=(12, 2))
        r += 1

        btn_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        btn_frame.grid(row=r, column=0, columnspan=2, sticky="ew", pady=(4, 16))

        self.update_save_btn = ctk.CTkButton(
            btn_frame, text="Save Changes", font=FONT_BUTTON,
            height=BUTTON_HEIGHT, corner_radius=8,
            fg_color=WARNING, hover_color="#d4940a",
            text_color="#000", command=self._on_update, state="disabled",
        )
        self.update_save_btn.pack(side="left", padx=8)

    def _on_fetch_for_update(self):
        pk_val = self.update_pk_entry.get().strip()
        if not pk_val:
            self.update_status.configure(text="Please enter the primary key value.",
                                          text_color=DANGER)
            return

        pk = self.cfg["primary_key"]
        sql = f'SELECT * FROM {self.cfg["table_name"]} WHERE {pk} = %s'
        cols, row, err = self.db.fetch_one(sql, (pk_val,))

        if err:
            self.update_status.configure(text=f"Error: {err}", text_color=DANGER)
            return
        if row is None:
            self.update_status.configure(
                text=f"No record found with {pk} = {pk_val}.", text_color=WARNING)
            return

        # Map column names to values
        row_dict = dict(zip(cols, row))

        # Populate fields
        for col_def in self.cfg["columns"]:
            name = col_def["name"]
            if col_def.get("pk"):
                continue
            if name not in self.update_fields:
                continue
            widget = self.update_fields[name]
            val = row_dict.get(name, "")
            self._set_widget_value(widget, col_def, val)
            try:
                widget.configure(state="normal")
            except Exception:
                pass

        self.update_save_btn.configure(state="normal")
        self.update_status.configure(
            text=f"✓  Record fetched. Modify fields and click Save.",
            text_color=ACCENT)

    def _on_update(self):
        pk_val = self.update_pk_entry.get().strip()
        if not pk_val:
            return

        values, err = self._collect_form_values(self.update_fields)
        if err:
            self.update_status.configure(text=err, text_color=DANGER)
            return

        set_clauses = ", ".join([f"{k} = %s" for k in values.keys()])
        pk = self.cfg["primary_key"]
        sql = f'UPDATE {self.cfg["table_name"]} SET {set_clauses} WHERE {pk} = %s'
        params = list(values.values()) + [pk_val]

        affected, db_err = self.db.execute(sql, params)
        if db_err:
            self.update_status.configure(text=f"Error: {db_err}", text_color=DANGER)
        elif affected == 0:
            self.update_status.configure(text="No rows updated.", text_color=WARNING)
        else:
            self.update_status.configure(text="✓  Record updated successfully.",
                                          text_color=SUCCESS)
            self._load_read_data()

    # ================================================================== #
    #  DELETE TAB                                                          #
    # ================================================================== #

    def _build_delete_tab(self, parent):
        parent.grid_rowconfigure(2, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        # ── PK fetch bar ──
        fetch_bar = ctk.CTkFrame(parent, fg_color=BG_INPUT, corner_radius=10)
        fetch_bar.grid(row=0, column=0, sticky="ew", padx=4, pady=(8, 4))
        fetch_bar.grid_columnconfigure(1, weight=1)

        pk = self.cfg["primary_key"]
        ctk.CTkLabel(fetch_bar,
                     text=f"Enter {pk.replace('_',' ').title()}:",
                     font=FONT_LABEL, text_color=TEXT_SECONDARY
                     ).grid(row=0, column=0, padx=(12, 8), pady=10)

        self.delete_pk_entry = ctk.CTkEntry(
            fetch_bar, height=ENTRY_HEIGHT, font=FONT_BODY,
            fg_color=BG_CARD, border_color=BORDER, border_width=1,
            corner_radius=8, text_color=TEXT_PRIMARY, width=180,
            placeholder_text=f"{pk}",
        )
        self.delete_pk_entry.grid(row=0, column=1, sticky="w", pady=10)

        ctk.CTkButton(fetch_bar, text="Fetch", font=FONT_BUTTON,
                       width=100, height=34, corner_radius=8,
                       fg_color=ACCENT, hover_color=ACCENT_HOVER,
                       text_color="#000", command=self._on_fetch_for_delete
                       ).grid(row=0, column=2, padx=12, pady=10)

        # ── Preview area ──
        self.delete_preview = ctk.CTkTextbox(
            parent, font=FONT_MONO, height=200,
            fg_color=BG_INPUT, text_color=TEXT_PRIMARY,
            border_color=BORDER, border_width=1, corner_radius=8,
            state="disabled",
        )
        self.delete_preview.grid(row=1, column=0, sticky="ew", padx=8, pady=8)

        # ── Status + button ──
        bottom = ctk.CTkFrame(parent, fg_color="transparent")
        bottom.grid(row=2, column=0, sticky="ew", padx=8, pady=(0, 16))

        self.delete_status = ctk.CTkLabel(bottom, text="", font=FONT_BODY_SM,
                                           text_color=DANGER, anchor="w")
        self.delete_status.pack(side="left", padx=8)

        self.delete_btn = ctk.CTkButton(
            bottom, text="Delete Row", font=FONT_BUTTON,
            height=BUTTON_HEIGHT, corner_radius=8,
            fg_color=DANGER, hover_color=DANGER_HOVER,
            text_color="#fff", command=self._on_delete, state="disabled",
        )
        self.delete_btn.pack(side="right", padx=8)

    def _on_fetch_for_delete(self):
        pk_val = self.delete_pk_entry.get().strip()
        if not pk_val:
            self.delete_status.configure(text="Enter the primary key.", text_color=DANGER)
            return

        pk = self.cfg["primary_key"]
        sql = f'SELECT * FROM {self.cfg["table_name"]} WHERE {pk} = %s'
        cols, row, err = self.db.fetch_one(sql, (pk_val,))

        if err:
            self.delete_status.configure(text=f"Error: {err}", text_color=DANGER)
            return
        if row is None:
            self.delete_status.configure(
                text=f"No record found with {pk} = {pk_val}.", text_color=WARNING)
            self._set_textbox(self.delete_preview, "")
            self.delete_btn.configure(state="disabled")
            return

        # Show preview
        lines = []
        for c, v in zip(cols, row):
            lines.append(f"  {c:25s}  │  {self._format_cell(v)}")
        preview_text = "\n".join(lines)
        self._set_textbox(self.delete_preview, preview_text)
        self.delete_btn.configure(state="normal")
        self.delete_status.configure(text="Review the record above, then confirm delete.",
                                      text_color=WARNING)

    def _on_delete(self):
        pk_val = self.delete_pk_entry.get().strip()
        if not pk_val:
            return

        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete the record with "
            f"{self.cfg['primary_key']} = {pk_val}?\n\n"
            f"This action cannot be undone.",
        )
        if not confirm:
            return

        pk = self.cfg["primary_key"]
        sql = f'DELETE FROM {self.cfg["table_name"]} WHERE {pk} = %s'
        affected, db_err = self.db.execute(sql, (pk_val,))

        if db_err:
            self.delete_status.configure(text=f"Error: {db_err}", text_color=DANGER)
        elif affected == 0:
            self.delete_status.configure(text="No rows deleted.", text_color=WARNING)
        else:
            self.delete_status.configure(text="✓  Record deleted.", text_color=SUCCESS)
            self._set_textbox(self.delete_preview, "")
            self.delete_btn.configure(state="disabled")
            self.delete_pk_entry.delete(0, "end")
            self._load_read_data()

    # ================================================================== #
    #  FORM HELPERS                                                        #
    # ================================================================== #

    def _make_input_widget(self, parent, col_def, field_dict, name):
        """Create the appropriate input widget for a column."""
        fk_info = self.cfg["foreign_keys"].get(name)

        if fk_info:
            # FK → ComboBox with options from referenced table
            options = self._get_fk_options(name, fk_info)
            display_list = [f"{pk}  ·  {disp}" for pk, disp in options]
            widget = ctk.CTkComboBox(
                parent, values=display_list, font=FONT_BODY,
                fg_color=BG_INPUT, border_color=BORDER, border_width=1,
                corner_radius=8, text_color=TEXT_PRIMARY,
                button_color=ACCENT_DIM, button_hover_color=ACCENT,
                dropdown_fg_color=BG_INPUT, dropdown_hover_color=BG_HOVER,
                dropdown_text_color=TEXT_PRIMARY,
                height=ENTRY_HEIGHT, state="normal",
            )
            widget.set("")
            field_dict[name] = widget
            return widget

        if col_def["type"] == BOOL:
            widget = ctk.CTkComboBox(
                parent, values=["True", "False"], font=FONT_BODY,
                fg_color=BG_INPUT, border_color=BORDER, border_width=1,
                corner_radius=8, text_color=TEXT_PRIMARY,
                button_color=ACCENT_DIM, button_hover_color=ACCENT,
                dropdown_fg_color=BG_INPUT, dropdown_hover_color=BG_HOVER,
                dropdown_text_color=TEXT_PRIMARY,
                height=ENTRY_HEIGHT,
            )
            widget.set("True")
            field_dict[name] = widget
            return widget

        if col_def["type"] == TEXT:
            widget = ctk.CTkTextbox(
                parent, font=FONT_BODY, height=80,
                fg_color=BG_INPUT, text_color=TEXT_PRIMARY,
                border_color=BORDER, border_width=1, corner_radius=8,
            )
            field_dict[name] = widget
            return widget

        # Date columns → custom date picker (year → month → day)
        if col_def["type"] == DATE:
            widget = DatePickerWidget(parent)
            field_dict[name] = widget
            return widget

        # Default: entry
        placeholder = ""
        if col_def["type"] == "timestamp":
            placeholder = "YYYY-MM-DD HH:MM:SS"

        widget = ctk.CTkEntry(
            parent, height=ENTRY_HEIGHT, font=FONT_BODY,
            fg_color=BG_INPUT, border_color=BORDER, border_width=1,
            corner_radius=8, text_color=TEXT_PRIMARY,
            placeholder_text=placeholder,
        )
        field_dict[name] = widget
        return widget

    def _get_fk_options(self, col_name, fk_info):
        """Load FK options, with caching."""
        if col_name in self.fk_cache:
            return self.fk_cache[col_name]
        options = self.db.fetch_dropdown_options(
            fk_info["ref_table"], fk_info["ref_pk"], fk_info["display_col"]
        )
        nullable = fk_info.get("nullable", False)
        if nullable:
            options = [("", "(None)")] + options
        self.fk_cache[col_name] = options
        return options

    def _set_widget_value(self, widget, col_def, value):
        """Set a form widget's value from a DB row."""
        if isinstance(widget, DatePickerWidget):
            widget.configure(state="normal")
            widget.set(value if value is not None else "")
            return

        if isinstance(widget, ctk.CTkTextbox):
            widget.configure(state="normal")
            widget.delete("1.0", "end")
            if value is not None:
                widget.insert("1.0", str(value))
            return

        if isinstance(widget, ctk.CTkComboBox):
            fk_info = self.cfg["foreign_keys"].get(col_def["name"])
            if fk_info:
                # Find matching option
                options = self._get_fk_options(col_def["name"], fk_info)
                for pk, disp in options:
                    if str(pk) == str(value) or pk == value:
                        widget.set(f"{pk}  ·  {disp}")
                        return
                widget.set(str(value) if value is not None else "")
            elif col_def["type"] == BOOL:
                widget.set("True" if value else "False")
            return

        # CTkEntry
        try:
            widget.configure(state="normal")
        except Exception:
            pass
        widget.delete(0, "end")
        if value is not None:
            widget.insert(0, str(value))

    def _collect_form_values(self, field_dict):
        """Read all form fields and return (dict_of_values, error_string|None)."""
        values = {}
        for col_def in self.cfg["columns"]:
            name = col_def["name"]
            if col_def.get("pk") and field_dict is self.update_fields:
                continue  # PK handled separately in update
            if name not in field_dict:
                continue

            widget = field_dict[name]
            raw = self._get_widget_value(widget)

            # Nullable check
            if raw == "" or raw is None:
                if col_def.get("nullable") or col_def.get("pk"):
                    values[name] = None
                    continue
                # Check if it's a FK that's nullable
                fk = self.cfg["foreign_keys"].get(name, {})
                if fk.get("nullable"):
                    values[name] = None
                    continue
                if not col_def.get("pk"):
                    return None, f"Field '{col_def['label']}' is required."

            # FK: extract the ID portion
            fk_info = self.cfg["foreign_keys"].get(name)
            if fk_info and raw:
                raw = raw.split("·")[0].strip() if "·" in str(raw) else raw
                if raw == "" or raw == "(None)":
                    values[name] = None
                    continue

            # Type coercion
            try:
                if col_def["type"] in ("int", "bigint"):
                    values[name] = int(raw) if raw else None
                elif col_def["type"] == "decimal":
                    values[name] = float(raw) if raw else None
                elif col_def["type"] == "bool":
                    values[name] = str(raw).lower() in ("true", "yes", "1")
                else:
                    values[name] = raw if raw else None
            except (ValueError, TypeError) as exc:
                return None, f"Invalid value for '{col_def['label']}': {exc}"

        return values, None

    @staticmethod
    def _get_widget_value(widget):
        if isinstance(widget, DatePickerWidget):
            return widget.get()
        if isinstance(widget, ctk.CTkTextbox):
            return widget.get("1.0", "end").strip()
        if isinstance(widget, ctk.CTkComboBox):
            return widget.get()
        return widget.get()

    def _clear_fields(self, field_dict):
        for name, widget in field_dict.items():
            if isinstance(widget, DatePickerWidget):
                widget.configure(state="normal")
                widget.delete()
            elif isinstance(widget, ctk.CTkTextbox):
                widget.configure(state="normal")
                widget.delete("1.0", "end")
            elif isinstance(widget, ctk.CTkComboBox):
                widget.set("")
            else:
                try:
                    widget.configure(state="normal")
                except Exception:
                    pass
                widget.delete(0, "end")

    @staticmethod
    def _set_textbox(textbox, text):
        textbox.configure(state="normal")
        textbox.delete("1.0", "end")
        textbox.insert("1.0", text)
        textbox.configure(state="disabled")
