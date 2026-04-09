-- ======================================================
-- METHOD 1: MANUAL SQL INSERTIONS (Proof of Concept)
-- ======================================================

-- 1. USERS
INSERT INTO USERS (user_id, username, account_type, creation_date) 
VALUES (1, 'system_admin', 'Administrator', '2026-01-01');
INSERT INTO USERS (user_id, username, account_type, creation_date) 
VALUES (2, 'developer_01', 'Developer', '2026-02-15');

-- 2. EXECUTABLES
INSERT INTO EXECUTABLES (exe_id, file_path, version, file_size_kb) 
VALUES (1, '/usr/bin/python3', '3.12.1', 4500);
INSERT INTO EXECUTABLES (exe_id, file_path, version, file_size_kb) 
VALUES (2, '/usr/local/bin/nginx', '1.25.3', 1200);

-- 3. RESOURCE_TYPES
INSERT INTO RESOURCE_TYPES (type_id, type_name, unit_measure) 
VALUES (1, 'CPU_Core', 'GHz');
INSERT INTO RESOURCE_TYPES (type_id, type_name, unit_measure) 
VALUES (2, 'System_RAM', 'GB');

-- 4. PROCESSES
INSERT INTO PROCESSES (pid, process_name, start_time, status, user_id, exe_id, parent_pid) 
VALUES (1, 'python3_main', '2026-04-09 10:00:00', 'Running', 1, 1, NULL);
INSERT INTO PROCESSES (pid, process_name, start_time, status, user_id, exe_id, parent_pid) 
VALUES (2, 'nginx_worker', '2026-04-09 10:05:00', 'Active', 2, 2, 1);

-- 5. RESOURCES
INSERT INTO RESOURCES (resource_id, resource_name, capacity, is_operational, type_id) 
VALUES (1, 'Intel_Node_001', 5.20, TRUE, 1);
INSERT INTO RESOURCES (resource_id, resource_name, capacity, is_operational, type_id) 
VALUES (2, 'Samsung_RAM_001', 64.00, TRUE, 2);

-- 6. USAGE_LOGS
INSERT INTO USAGE_LOGS (log_id, snapshot_time, cpu_percent, ram_usage_mb, pid) 
VALUES (1, '2026-04-09 11:00:00', 15.50, 512, 1);
INSERT INTO USAGE_LOGS (log_id, snapshot_time, cpu_percent, ram_usage_mb, pid) 
VALUES (2, '2026-04-09 11:01:00', 45.20, 1024, 2);

-- 7. SYSTEM_EVENTS
INSERT INTO SYSTEM_EVENTS (event_id, event_type, severity, description, pid) 
VALUES (1, 'Startup', 'Info', 'System initialized successfully', 1);
INSERT INTO SYSTEM_EVENTS (event_id, event_type, severity, description, pid) 
VALUES (2, 'High_Load', 'Warning', 'CPU threshold exceeded', 2);

-- 8. MAINTENANCE_LOG
INSERT INTO MAINTENANCE_LOG (maint_id, repair_date, technician_name, repair_cost, resource_id) 
VALUES (1, '2026-03-20', 'James Miller', 0.00, 1);
INSERT INTO MAINTENANCE_LOG (maint_id, repair_date, technician_name, repair_cost, resource_id) 
VALUES (2, '2026-04-01', 'Maria Garcia', 120.50, 2);

-- 9. ALLOCATIONS
INSERT INTO ALLOCATIONS (alloc_id, resource_request_id, amount_requested, is_active, resource_id, pid) 
VALUES (1, 1001, 2, TRUE, 1, 1);
INSERT INTO ALLOCATIONS (alloc_id, resource_request_id, amount_requested, is_active, resource_id, pid) 
VALUES (2, 1002, 16, TRUE, 2, 2);

-- 10. NETWORK_SESSIONS
INSERT INTO NETWORK_SESSIONS (session_id, dest_ip, port, protocol, bytes_sent, pid) 
VALUES (1, '192.168.1.1', 443, 'HTTPS', 50000, 1);
INSERT INTO NETWORK_SESSIONS (session_id, dest_ip, port, protocol, bytes_sent, pid) 
VALUES (2, '8.8.8.8', 53, 'UDP', 128, 2);

-- ======================================================
-- METHOD 2: MOCKAROO / EXTERNAL DATASETS
-- ======================================================
/*
   The following tables were populated with 500 rows each using Mockaroo.com:
   - USERS, EXECUTABLES, PROCESSES, SYSTEM_EVENTS, 
     MAINTENANCE_LOG, ALLOCATIONS.
*/

-- ======================================================
-- METHOD 3: PYTHON SCRIPT GENERATION (Big Data & Logic)
-- ======================================================
/*
   Python scripts were used for two specific purposes:
   1. Logic Consistency (500 rows each): RESOURCE_TYPES and RESOURCES 
      were generated together to ensure hardware names matched their units.
   2. High Volume (20,000 rows each): USAGE_LOGS and NETWORK_SESSIONS 
      to simulate real-time system monitoring.
*/