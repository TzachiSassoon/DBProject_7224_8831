ALTER TABLE USAGE_LOGS 
ADD CONSTRAINT check_cpu_range CHECK (cpu_percent >= 0 AND cpu_percent <= 100);

ALTER TABLE MAINTENANCE_LOG 
ADD CONSTRAINT unique_repair UNIQUE (repair_date, resource_id, technician_name);

ALTER TABLE PROCESSES 
ADD CONSTRAINT check_start_time CHECK (start_time <= CURRENT_TIMESTAMP);