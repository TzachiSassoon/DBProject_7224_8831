"""
SysManager – Database Connection Manager
Handles all PostgreSQL communication via psycopg2.
"""

import psycopg2
import psycopg2.extras


class DatabaseManager:
    """Singleton database manager for PostgreSQL connections."""

    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.conn = None
        self.connected = False
        self.host = ""
        self.db_name = ""
        self.user = ""

    # ------------------------------------------------------------------ #
    #  Connection lifecycle                                                #
    # ------------------------------------------------------------------ #

    def connect(self, host, port, dbname, user, password):
        """Establish a connection to the PostgreSQL database."""
        try:
            self.conn = psycopg2.connect(
                host=host,
                port=int(port),
                dbname=dbname,
                user=user,
                password=password,
                sslmode="require",
                connect_timeout=15,
            )
            self.conn.autocommit = True
            self.connected = True
            self.host = host
            self.db_name = dbname
            self.user = user
            return True, "Connection established successfully."
        except psycopg2.OperationalError as exc:
            self.connected = False
            return False, f"Connection failed:\n{exc}"
        except Exception as exc:
            self.connected = False
            return False, f"Unexpected error:\n{exc}"

    def disconnect(self):
        """Close the database connection."""
        if self.conn and not self.conn.closed:
            self.conn.close()
        self.connected = False
        self.host = ""
        self.db_name = ""

    def test_connection(self):
        """Quick connection health-check."""
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT 1")
            cur.close()
            return True
        except Exception:
            return False

    def get_status_text(self):
        if self.connected:
            return f"Connected  ·  {self.user}@{self.host}/{self.db_name}"
        return "Disconnected"

    # ------------------------------------------------------------------ #
    #  Query helpers                                                       #
    # ------------------------------------------------------------------ #

    def fetch_all(self, sql, params=None):
        """Run a SELECT and return (column_names, rows_as_tuples, error)."""
        try:
            cur = self.conn.cursor()
            cur.execute(sql, params or ())
            columns = [desc[0] for desc in cur.description] if cur.description else []
            rows = cur.fetchall()
            cur.close()
            return columns, rows, None
        except Exception as exc:
            try:
                self.conn.rollback()
            except Exception:
                pass
            return [], [], str(exc)

    def fetch_one(self, sql, params=None):
        """Run a SELECT and return a single row (column_names, row, error)."""
        try:
            cur = self.conn.cursor()
            cur.execute(sql, params or ())
            columns = [desc[0] for desc in cur.description] if cur.description else []
            row = cur.fetchone()
            cur.close()
            return columns, row, None
        except Exception as exc:
            try:
                self.conn.rollback()
            except Exception:
                pass
            return [], None, str(exc)

    def execute(self, sql, params=None):
        """Run an INSERT / UPDATE / DELETE. Returns (affected_rows, error)."""
        try:
            cur = self.conn.cursor()
            cur.execute(sql, params or ())
            affected = cur.rowcount
            cur.close()
            return affected, None
        except Exception as exc:
            try:
                self.conn.rollback()
            except Exception:
                pass
            return 0, str(exc)

    def call_procedure(self, sql, params=None):
        """Execute a CALL statement. Returns (success, message)."""
        try:
            cur = self.conn.cursor()
            cur.execute(sql, params or ())
            cur.close()
            return True, "Procedure executed successfully."
        except Exception as exc:
            try:
                self.conn.rollback()
            except Exception:
                pass
            return False, str(exc)

    def fetch_dropdown_options(self, table, pk_col, display_col):
        """Load (pk, display_value) pairs for FK combo-boxes."""
        sql = f'SELECT {pk_col}, {display_col} FROM {table} ORDER BY {pk_col}'
        cols, rows, err = self.fetch_all(sql)
        if err:
            return []
        return [(row[0], row[1]) for row in rows]
