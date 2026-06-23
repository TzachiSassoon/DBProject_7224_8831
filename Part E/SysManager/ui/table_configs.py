"""
SysManager – Table Configurations
Data-driven definitions for every public-schema table.
Each config drives the generic CRUDScreen widget.
"""

# Column type hints used by the CRUD form builder
INT       = "int"
STR       = "str"
DATE      = "date"
TIMESTAMP = "timestamp"
DECIMAL   = "decimal"
BOOL      = "bool"
BIGINT    = "bigint"
TEXT      = "text"


def _col(name, ctype, label=None, nullable=False, editable=True, pk=False):
    """Shorthand to build a column descriptor dict."""
    return {
        "name": name,
        "type": ctype,
        "label": label or name.replace("_", " ").title(),
        "nullable": nullable,
        "editable": editable,
        "pk": pk,
    }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Individual table configs
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

USERS = {
    "table_name": "users",
    "display_name": "Users",
    "primary_key": "user_id",
    "columns": [
        _col("user_id",       INT,  "User ID", pk=True),
        _col("username",      STR,  "Username"),
        _col("account_type",  STR,  "Account Type"),
        _col("creation_date", DATE, "Creation Date"),
    ],
    "foreign_keys": {},
    "read_query": "SELECT user_id, username, account_type, creation_date FROM users ORDER BY user_id",
    "read_display_columns": ["user_id", "username", "account_type", "creation_date"],
}

EXECUTABLES = {
    "table_name": "executables",
    "display_name": "Executables",
    "primary_key": "exe_id",
    "columns": [
        _col("exe_id",       INT, "Exe ID", pk=True),
        _col("file_path",    STR, "File Path"),
        _col("version",      STR, "Version"),
        _col("file_size_kb", INT, "File Size (KB)"),
    ],
    "foreign_keys": {},
    "read_query": "SELECT exe_id, file_path, version, file_size_kb FROM executables ORDER BY exe_id",
    "read_display_columns": ["exe_id", "file_path", "version", "file_size_kb"],
}

RESOURCE_TYPES = {
    "table_name": "resource_types",
    "display_name": "Resource Types",
    "primary_key": "type_id",
    "columns": [
        _col("type_id",      INT, "Type ID", pk=True),
        _col("type_name",    STR, "Type Name"),
        _col("unit_measure", STR, "Unit of Measure"),
    ],
    "foreign_keys": {},
    "read_query": "SELECT type_id, type_name, unit_measure FROM resource_types ORDER BY type_id",
    "read_display_columns": ["type_id", "type_name", "unit_measure"],
}

RESOURCES = {
    "table_name": "resources",
    "display_name": "Resources",
    "primary_key": "resource_id",
    "columns": [
        _col("resource_id",      INT,     "Resource ID", pk=True),
        _col("resource_name",    STR,     "Resource Name"),
        _col("capacity",         DECIMAL, "Capacity"),
        _col("is_operational",   BOOL,    "Operational?"),
        _col("type_id",          INT,     "Resource Type"),
        _col("efficiency_score", DECIMAL, "Efficiency Score", nullable=True),
    ],
    "foreign_keys": {
        "type_id": {
            "ref_table":   "resource_types",
            "ref_pk":      "type_id",
            "display_col": "type_name",
        },
    },
    "read_query": (
        "SELECT r.resource_id, r.resource_name, r.capacity, r.is_operational, "
        "       rt.type_name, r.efficiency_score "
        "FROM resources r "
        "JOIN resource_types rt ON r.type_id = rt.type_id "
        "ORDER BY r.resource_id"
    ),
    "read_display_columns": [
        "resource_id", "resource_name", "capacity",
        "is_operational", "type_name", "efficiency_score",
    ],
}

PROCESSES = {
    "table_name": "processes",
    "display_name": "Processes",
    "primary_key": "pid",
    "columns": [
        _col("pid",          INT,       "PID", pk=True),
        _col("process_name", STR,       "Process Name"),
        _col("start_time",   TIMESTAMP, "Start Time"),
        _col("status",       STR,       "Status"),
        _col("user_id",      INT,       "User"),
        _col("exe_id",       INT,       "Executable"),
        _col("parent_pid",   INT,       "Parent Process", nullable=True),
        _col("risk_level",   STR,       "Risk Level",     nullable=True),
    ],
    "foreign_keys": {
        "user_id": {
            "ref_table":   "users",
            "ref_pk":      "user_id",
            "display_col": "username",
        },
        "exe_id": {
            "ref_table":   "executables",
            "ref_pk":      "exe_id",
            "display_col": "file_path",
        },
        "parent_pid": {
            "ref_table":   "processes",
            "ref_pk":      "pid",
            "display_col": "process_name",
            "nullable":    True,
        },
    },
    "read_query": (
        "SELECT p.pid, p.process_name, p.start_time, p.status, "
        "       u.username, e.file_path, pp.process_name AS parent_process, p.risk_level "
        "FROM processes p "
        "JOIN users u ON p.user_id = u.user_id "
        "JOIN executables e ON p.exe_id = e.exe_id "
        "LEFT JOIN processes pp ON p.parent_pid = pp.pid "
        "ORDER BY p.pid"
    ),
    "read_display_columns": [
        "pid", "process_name", "start_time", "status",
        "username", "file_path", "parent_process", "risk_level",
    ],
}

ALLOCATIONS = {
    "table_name": "allocations",
    "display_name": "Allocations",
    "primary_key": "alloc_id",
    "columns": [
        _col("alloc_id",            INT,  "Alloc ID", pk=True),
        _col("resource_request_id", INT,  "Request ID"),
        _col("amount_requested",    INT,  "Amount Requested"),
        _col("is_active",           BOOL, "Active?"),
        _col("resource_id",         INT,  "Resource"),
        _col("pid",                 INT,  "Process"),
    ],
    "foreign_keys": {
        "resource_id": {
            "ref_table":   "resources",
            "ref_pk":      "resource_id",
            "display_col": "resource_name",
        },
        "pid": {
            "ref_table":   "processes",
            "ref_pk":      "pid",
            "display_col": "process_name",
        },
    },
    "read_query": (
        "SELECT a.alloc_id, a.resource_request_id, a.amount_requested, a.is_active, "
        "       r.resource_name, p.process_name "
        "FROM allocations a "
        "JOIN resources r ON a.resource_id = r.resource_id "
        "JOIN processes p ON a.pid = p.pid "
        "ORDER BY a.alloc_id"
    ),
    "read_display_columns": [
        "alloc_id", "resource_request_id", "amount_requested",
        "is_active", "resource_name", "process_name",
    ],
}

USAGE_LOGS = {
    "table_name": "usage_logs",
    "display_name": "Usage Logs",
    "primary_key": "log_id",
    "columns": [
        _col("log_id",        INT,       "Log ID", pk=True),
        _col("snapshot_time", TIMESTAMP, "Snapshot Time"),
        _col("cpu_percent",   DECIMAL,   "CPU %"),
        _col("ram_usage_mb",  INT,       "RAM (MB)"),
        _col("pid",           INT,       "Process"),
    ],
    "foreign_keys": {
        "pid": {
            "ref_table":   "processes",
            "ref_pk":      "pid",
            "display_col": "process_name",
        },
    },
    "read_query": (
        "SELECT ul.log_id, ul.snapshot_time, ul.cpu_percent, ul.ram_usage_mb, "
        "       p.process_name "
        "FROM usage_logs ul "
        "JOIN processes p ON ul.pid = p.pid "
        "ORDER BY ul.log_id"
    ),
    "read_display_columns": [
        "log_id", "snapshot_time", "cpu_percent", "ram_usage_mb", "process_name",
    ],
}

NETWORK_SESSIONS = {
    "table_name": "network_sessions",
    "display_name": "Network Sessions",
    "primary_key": "session_id",
    "columns": [
        _col("session_id", INT,    "Session ID", pk=True),
        _col("dest_ip",    STR,    "Destination IP"),
        _col("port",       INT,    "Port"),
        _col("protocol",   STR,    "Protocol"),
        _col("bytes_sent", BIGINT, "Bytes Sent"),
        _col("pid",        INT,    "Process"),
    ],
    "foreign_keys": {
        "pid": {
            "ref_table":   "processes",
            "ref_pk":      "pid",
            "display_col": "process_name",
        },
    },
    "read_query": (
        "SELECT ns.session_id, ns.dest_ip, ns.port, ns.protocol, ns.bytes_sent, "
        "       p.process_name "
        "FROM network_sessions ns "
        "JOIN processes p ON ns.pid = p.pid "
        "ORDER BY ns.session_id"
    ),
    "read_display_columns": [
        "session_id", "dest_ip", "port", "protocol", "bytes_sent", "process_name",
    ],
}

SYSTEM_EVENTS = {
    "table_name": "system_events",
    "display_name": "System Events",
    "primary_key": "event_id",
    "columns": [
        _col("event_id",    INT,  "Event ID", pk=True),
        _col("event_type",  STR,  "Event Type"),
        _col("severity",    STR,  "Severity"),
        _col("description", TEXT, "Description", nullable=True),
        _col("pid",         INT,  "Process"),
    ],
    "foreign_keys": {
        "pid": {
            "ref_table":   "processes",
            "ref_pk":      "pid",
            "display_col": "process_name",
        },
    },
    "read_query": (
        "SELECT se.event_id, se.event_type, se.severity, se.description, "
        "       p.process_name "
        "FROM system_events se "
        "JOIN processes p ON se.pid = p.pid "
        "ORDER BY se.event_id"
    ),
    "read_display_columns": [
        "event_id", "event_type", "severity", "description", "process_name",
    ],
}

MAINTENANCE_LOG = {
    "table_name": "maintenance_log",
    "display_name": "Maintenance Log",
    "primary_key": "maint_id",
    "columns": [
        _col("maint_id",         INT,     "Maint ID", pk=True),
        _col("repair_date",      DATE,    "Repair Date"),
        _col("technician_name",  STR,     "Technician"),
        _col("repair_cost",      DECIMAL, "Repair Cost"),
        _col("resource_id",      INT,     "Resource"),
    ],
    "foreign_keys": {
        "resource_id": {
            "ref_table":   "resources",
            "ref_pk":      "resource_id",
            "display_col": "resource_name",
        },
    },
    "read_query": (
        "SELECT m.maint_id, m.repair_date, m.technician_name, m.repair_cost, "
        "       r.resource_name "
        "FROM maintenance_log m "
        "JOIN resources r ON m.resource_id = r.resource_id "
        "ORDER BY m.maint_id"
    ),
    "read_display_columns": [
        "maint_id", "repair_date", "technician_name", "repair_cost", "resource_name",
    ],
}

EMPLOYEE = {
    "table_name": "employee",
    "display_name": "Employee (FDW)",
    "primary_key": "employee_id",
    "columns": [
        _col("employee_id", INT,  "Employee ID", pk=True),
        _col("first_name",  STR,  "First Name"),
        _col("last_name",   STR,  "Last Name"),
        _col("job_title",   STR,  "Job Title"),
        _col("hire_date",   DATE, "Hire Date"),
    ],
    "foreign_keys": {},
    "read_query": (
        "SELECT employee_id, first_name, last_name, job_title, hire_date "
        "FROM employee ORDER BY employee_id"
    ),
    "read_display_columns": [
        "employee_id", "first_name", "last_name", "job_title", "hire_date",
    ],
    "is_fdw": True,   # Foreign Data Wrapper – writes may be restricted
}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Ordered list consumed by the dashboard sidebar
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ALL_TABLES = [
    USERS,
    EXECUTABLES,
    RESOURCE_TYPES,
    RESOURCES,
    PROCESSES,
    ALLOCATIONS,
    USAGE_LOGS,
    NETWORK_SESSIONS,
    SYSTEM_EVENTS,
    MAINTENANCE_LOG,
    EMPLOYEE,
]
