# SysManager – Development Workflow & Tools

## Overview

SysManager is a custom desktop database management application built as a frontend client for a live PostgreSQL database hosted on Supabase. The application was developed using a modern Python stack, following a clean architecture pattern that separates data access logic from the user interface layer.

---

## Development Tools & Technologies

### Language: Python 3.11

Python was chosen for its rapid development cycle, rich ecosystem of database and GUI libraries, and cross-platform compatibility. The entire application is written in pure Python with no compilation step required.

### UI Framework: CustomTkinter

CustomTkinter is a modern UI library built on top of Python's native Tkinter. It was selected for its:

- **Built-in dark mode** support that provides a sleek, professional appearance out of the box.
- **Modern widget set** including rounded buttons, segmented tab views, scrollable frames, and combo boxes.
- **No external runtime dependencies** — unlike Electron or Qt-based solutions, CustomTkinter runs natively without a browser engine or heavy runtime.

For the data grid (table rows display), the standard `ttk.Treeview` widget was used with custom dark-mode styling applied through the ttk Style engine, since CustomTkinter does not include a native table/grid widget.

### Database Adapter: psycopg2

psycopg2 is the most widely used PostgreSQL adapter for Python. It was used because:

- It supports **parameterized queries** to prevent SQL injection.
- It provides reliable connectivity to **remote PostgreSQL instances** over SSL (required by Supabase).
- It handles PostgreSQL-specific types (NUMERIC, BOOLEAN, TIMESTAMP) natively.
- It supports **stored procedure execution** via standard `CALL` statements.

### Database: PostgreSQL 17 on Supabase

The backend database is a fully managed PostgreSQL 17 instance hosted on Supabase. The schema includes 10 local tables, 1 Foreign Data Wrapper (FDW) table connecting to an external database, 2 views, 2 stored procedures, a trigger, and a custom function.

### Version Control: Git

Standard Git version control was used throughout development for tracking changes and maintaining code history.

---

## Architecture & Design Decisions

### Clean Separation of Concerns

The codebase follows a **layered architecture** with two distinct packages:

```
db/              → Data Access Layer
  connection.py  → Singleton DatabaseManager handling all SQL communication

ui/              → Presentation Layer
  theme.py       → Centralized design tokens (colors, fonts, dimensions)
  table_configs  → Declarative table metadata driving all CRUD screens
  login_screen   → Authentication UI
  crud_screen    → Generic, reusable CRUD widget
  operations     → Advanced query execution panel
  dashboard      → Navigation shell and content routing
```

This separation ensures that:
- Database queries never live inside UI widget code.
- The UI layer communicates with the database exclusively through the `DatabaseManager` API.
- Table definitions are **data-driven**: adding a new table requires only a new config dict — no new UI code.

### Data-Driven CRUD via Table Configurations

Rather than writing a separate screen for each of the 11 tables, a **single generic `CRUDScreen` widget** was built. Each table is described by a configuration dictionary in `table_configs.py` that specifies:

- Table name, display name, and primary key
- Column definitions with types, labels, and nullability
- Foreign key mappings (referenced table, display column)
- A pre-written `SELECT` query with `JOIN`s for FK masking

The CRUD widget reads this configuration and dynamically generates forms, dropdowns, and grid columns at runtime. This approach eliminated code duplication and made the application trivially extensible.

### Foreign Key Masking

A key usability requirement was to never show raw foreign key IDs in the data grid. This was achieved by:

1. Writing `SELECT` queries with `JOIN` clauses that pull descriptive columns (e.g., `username` instead of `user_id`).
2. Using `LEFT JOIN` for nullable foreign keys (e.g., `parent_pid` in processes) to avoid dropping rows.
3. Populating create/update forms with **ComboBox dropdowns** loaded from referenced tables, displaying both the ID and the descriptive name.

### Fetch-Before-Update Pattern

To prevent accidental overwrites, the Update tab enforces a **fetch-first workflow**:

1. The user enters only the Primary Key.
2. The application runs a `SELECT` to retrieve the current row.
3. All fields are populated with existing values.
4. The user modifies only the fields they want to change.
5. The `UPDATE` query is built from the modified form values.

This ensures users always see the current state of a record before making changes.

### Smart Search

The search bar on each table's Read tab uses **type-aware matching**:

- **String/text columns** (usernames, file paths, descriptions) use case-insensitive substring matching — typing part of a name finds all containing matches.
- **Numeric/date/boolean columns** (IDs, costs, dates) use exact matching — searching for "7" returns only exact matches, not "17" or "71".

The column type is resolved at search time by cross-referencing the display column against the table's schema definition.

---

## Development Workflow

### Phase 1: Schema Analysis

The development process began with a thorough analysis of the PostgreSQL backup file (`backup4.sql`) to extract:

- All public-schema table definitions (columns, data types, constraints)
- Primary key constraints
- Foreign key relationships between tables
- Stored procedure signatures and logic
- Views and triggers

This analysis produced the table configuration data model that drives the entire application.

### Phase 2: Foundation Layer

The database connection module (`DatabaseManager`) was built first as a **singleton class** providing:

- Connection lifecycle management (connect, disconnect, health check)
- Parameterized query execution (SELECT, INSERT, UPDATE, DELETE)
- Stored procedure invocation (CALL)
- FK dropdown option loading

### Phase 3: Design System

A centralized theme module was created to define all visual constants — colors, fonts, dimensions, and ttk Treeview dark-mode styling — ensuring visual consistency across every screen.

### Phase 4: UI Components

Components were built bottom-up:

1. **Login Screen** — credential entry card with config.ini pre-population
2. **CRUD Screen** — the generic four-tab widget (Read, Create, Update, Delete)
3. **Operations Screen** — four action buttons with grid/text result display
4. **Dashboard** — sidebar navigation shell with content area routing

### Phase 5: Integration & Polish

All components were assembled into the main application window with screen transition logic (login → dashboard → logout cycle). Search functionality, smart type-aware matching, and input validation were added as final polish steps.

---

## Key Libraries & Versions

| Library | Version | Role |
|---|---|---|
| `customtkinter` | 5.2.2 | Modern dark-themed desktop UI |
| `psycopg2-binary` | 2.9.12 | PostgreSQL database adapter |
| `Pillow` | 10+ | Image processing (CustomTkinter dependency) |
| `darkdetect` | 0.8.0 | OS dark mode detection (CustomTkinter dependency) |
