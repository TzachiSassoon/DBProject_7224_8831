# SysManager – Setup & Running Instructions

## Prerequisites

Before running SysManager, ensure the following are installed on your system:

| Requirement | Version | Purpose |
|---|---|---|
| **Python** | 3.10 or higher | Runtime environment |
| **pip** | Latest | Python package manager |
| **Internet connection** | — | Required to reach the remote Supabase database |

---

## Step 1 – Install Dependencies

Open a terminal / command prompt and navigate to the project folder:

```bash
cd SysManager
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

This installs:
- **customtkinter** – Modern dark-themed desktop UI framework
- **psycopg2-binary** – PostgreSQL database adapter for Python
- **Pillow** – Image processing library (UI dependency)

---

## Step 2 – Configure Database Credentials

Open the file `config.ini` in any text editor and replace the placeholder values with your actual Supabase PostgreSQL credentials:

```ini
[database]
host = db.xxxxxxxxxxxx.supabase.co
port = 5432
dbname = postgres
user = postgres
password = your_actual_password_here
```

> **Important:** The `host` value should be your full Supabase database host URL. You can find this in your Supabase project dashboard under **Settings → Database → Connection string**.

> **Security Note:** Never commit `config.ini` with real credentials to a public repository. Add it to `.gitignore` if using version control.

---

## Step 3 – Launch the Application

From the `SysManager` directory, run:

```bash
python main.py
```

The application window will open with the **Login Screen**.

---

## Step 4 – Connect to the Database

On the login screen:
1. Verify the pre-populated fields (Host, Port, Database, User, Password) match your Supabase credentials.
2. Click **"Connect to Database"**.
3. If the connection succeeds, you will be routed to the **Dashboard**.
4. If it fails, an error message will appear — double-check your credentials and network connection.

---

## Using the Application

### Navigating Tables
- The **left sidebar** lists all database tables.
- Click any table name to open its **CRUD screen**.

### CRUD Operations

Each table screen has four tabs:

| Tab | How to Use |
|---|---|
| **Read** | Displays all rows with foreign key values resolved to descriptive names. Use the search bar and attribute dropdown to filter rows. Click **Refresh** to reload data. |
| **Create** | Fill in all required fields. Foreign key fields provide dropdown menus with valid options. Click **Insert Row** to add the record. |
| **Update** | Enter the **Primary Key** value and click **Fetch** to load the current data. Modify any field, then click **Save Changes**. |
| **Delete** | Enter the **Primary Key** value and click **Fetch** to preview the record. Click **Delete Row** and confirm the deletion. |

### Search Functionality
- Type a search term in the **Search bar** on the Read tab.
- Select which column to search by using the **attribute dropdown**.
- **Numeric columns** (IDs, costs, ports): returns exact matches only.
- **Text columns** (names, paths, descriptions): returns rows where the column contains the search term.
- Click **Clear** to reset the filter.

### System Operations
- Click **"System Operations"** in the sidebar under the ADVANCED section.
- Four buttons execute specific queries and stored procedures:
  1. **Resource Intensity Baseline** – Compares per-process CPU usage against resource type benchmarks.
  2. **Maintenance & Financial Overview** – Lists operational resources with maintenance costs.
  3. **Handle Risky Process** – Prompts for a PID and account type, then calls the `handle_risky_process` stored procedure.
  4. **Update Efficiencies** – Recalculates efficiency scores for all operational resources.
- Results appear in the **Grid View** tab; execution logs appear in the **Text Log** tab.

---

## Disconnecting

Click the **"Disconnect"** button at the bottom of the sidebar to close the database connection and return to the login screen.

---

## Troubleshooting

| Issue | Solution |
|---|---|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` again |
| Connection timeout | Check your internet connection and verify the Supabase host URL |
| `permission denied` error | Ensure your database user has the required privileges |
| Scrollbar not responsive | Resize the window or try scrolling with the mouse wheel |
| FDW (Employee) write errors | The Employee table is a Foreign Data Wrapper and may be read-only depending on server configuration |
