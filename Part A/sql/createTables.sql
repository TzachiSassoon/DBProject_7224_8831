-- 1. USERS (Parent Table)
CREATE TABLE USERS (
  user_id INT NOT NULL,
  username VARCHAR(50) NOT NULL,
  account_type VARCHAR(20) NOT NULL,
  creation_date DATE NOT NULL,
  PRIMARY KEY (user_id)
);

-- 2. EXECUTABLES (Parent Table)
CREATE TABLE EXECUTABLES (
  exe_id INT NOT NULL,
  file_path VARCHAR(255) NOT NULL,
  version VARCHAR(20) NOT NULL,
  file_size_kb INT NOT NULL,
  PRIMARY KEY (exe_id)
);

-- 3. RESOURCE_TYPES (Parent Table)
CREATE TABLE RESOURCE_TYPES (
  type_id INT NOT NULL,
  type_name VARCHAR(50) NOT NULL,
  unit_measure VARCHAR(20) NOT NULL,
  PRIMARY KEY (type_id)
);

-- 4. PROCESSES (The Core - Fixed Circular Dependency)
CREATE TABLE PROCESSES (
  pid INT NOT NULL,
  process_name VARCHAR(100) NOT NULL,
  start_time TIMESTAMP NOT NULL, -- Significant DATE #1
  status VARCHAR(20) NOT NULL,
  user_id INT NOT NULL,
  exe_id INT NOT NULL,
  parent_pid INT, -- Removed NOT NULL to allow 'Root' processes
  PRIMARY KEY (pid),
  CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES USERS(user_id),
  CONSTRAINT fk_exe FOREIGN KEY (exe_id) REFERENCES EXECUTABLES(exe_id),
  CONSTRAINT fk_parent FOREIGN KEY (parent_pid) REFERENCES PROCESSES(pid)
);

-- 5. RESOURCES (Child of Resource_Types)
CREATE TABLE RESOURCES (
  resource_id INT NOT NULL,
  resource_name VARCHAR(100) NOT NULL,
  capacity NUMERIC(12, 2) NOT NULL, -- Fixed comma
  is_operational BOOLEAN NOT NULL, -- Used Boolean for Supabase
  type_id INT NOT NULL,
  PRIMARY KEY (resource_id),
  CONSTRAINT fk_type FOREIGN KEY (type_id) REFERENCES RESOURCE_TYPES(type_id)
);

-- 6. USAGE_LOGS (Child of Processes - 20,000+ Rows)
CREATE TABLE USAGE_LOGS (
  log_id INT NOT NULL,
  snapshot_time TIMESTAMP NOT NULL, -- Significant DATE #2
  cpu_percent NUMERIC(5, 2) NOT NULL, -- Fixed comma
  ram_usage_mb INT NOT NULL,
  pid INT NOT NULL,
  PRIMARY KEY (log_id),
  CONSTRAINT fk_process_usage FOREIGN KEY (pid) REFERENCES PROCESSES(pid)
);

-- 7. SYSTEM_EVENTS (Child of Processes)
CREATE TABLE SYSTEM_EVENTS (
  event_id INT NOT NULL,
  event_type VARCHAR(50) NOT NULL,
  severity VARCHAR(20) NOT NULL,
  description TEXT NOT NULL, -- Used TEXT for longer descriptions
  pid INT NOT NULL,
  PRIMARY KEY (event_id),
  CONSTRAINT fk_process_event FOREIGN KEY (pid) REFERENCES PROCESSES(pid)
);

-- 8. MAINTENANCE_LOG (Child of Resources)
CREATE TABLE MAINTENANCE_LOG (
  maint_id INT NOT NULL,
  repair_date DATE NOT NULL,
  technician_name VARCHAR(100) NOT NULL,
  repair_cost NUMERIC(10, 2) NOT NULL, -- Fixed comma
  resource_id INT NOT NULL,
  PRIMARY KEY (maint_id),
  CONSTRAINT fk_resource_maint FOREIGN KEY (resource_id) REFERENCES RESOURCES(resource_id)
);

-- 9. ALLOCATIONS (Bridge Table between Processes & Resources)
CREATE TABLE ALLOCATIONS (
  alloc_id INT NOT NULL,
  resource_request_id INT NOT NULL,
  amount_requested INT NOT NULL,
  is_active BOOLEAN NOT NULL,
  resource_id INT NOT NULL,
  pid INT NOT NULL,
  PRIMARY KEY (alloc_id),
  CONSTRAINT fk_res_alloc FOREIGN KEY (resource_id) REFERENCES RESOURCES(resource_id),
  CONSTRAINT fk_proc_alloc FOREIGN KEY (pid) REFERENCES PROCESSES(pid)
);

-- 10. NETWORK_SESSIONS (Child of Processes - 20,000+ Rows)
CREATE TABLE NETWORK_SESSIONS (
  session_id INT NOT NULL,
  dest_ip VARCHAR(45) NOT NULL,
  port INT NOT NULL,
  protocol VARCHAR(10) NOT NULL,
  bytes_sent BIGINT NOT NULL,
  pid INT NOT NULL,
  PRIMARY KEY (session_id),
  CONSTRAINT fk_process_net FOREIGN KEY (pid) REFERENCES PROCESSES(pid)
);