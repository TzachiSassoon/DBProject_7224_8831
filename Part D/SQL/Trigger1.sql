CREATE OR REPLACE FUNCTION log_resource_downtime()
RETURNS TRIGGER AS $$
DECLARE
    v_next_event_id INT;
    v_fallback_pid INT;
BEGIN
    IF OLD.is_operational = TRUE AND NEW.is_operational = FALSE THEN
        -- Calculate the next available event_id
        SELECT COALESCE(MAX(event_id), 0) + 1 INTO v_next_event_id FROM SYSTEM_EVENTS;

        -- Grab any valid PID to satisfy the NOT NULL constraint
        SELECT pid INTO v_fallback_pid FROM PROCESSES LIMIT 1;

        -- Insert the critical alert with the new ID and the valid PID
        INSERT INTO SYSTEM_EVENTS (event_id, event_type, severity, description, pid)
        VALUES (v_next_event_id, 'Hardware Alert', 'Critical', 'Resource ' || NEW.resource_name || ' unexpectedly went offline.', v_fallback_pid);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;