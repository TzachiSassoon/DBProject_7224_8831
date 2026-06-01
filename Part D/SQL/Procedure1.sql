CREATE OR REPLACE PROCEDURE handle_risky_process(p_pid INT, p_account_type VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE
    v_process_name VARCHAR;
    v_next_event_id INT;
BEGIN
    SELECT process_name INTO v_process_name FROM PROCESSES WHERE pid = p_pid;

    -- Update logic
    IF LOWER(p_account_type) = 'administrator' THEN
        UPDATE PROCESSES SET risk_level = 'High - Admin Review Needed' WHERE pid = p_pid;
    ELSIF LOWER(p_account_type) = 'user' THEN
        UPDATE PROCESSES SET risk_level = 'Medium', status = 'Suspended' WHERE pid = p_pid;
    ELSE
        UPDATE PROCESSES SET risk_level = 'Low' WHERE pid = p_pid;
    END IF;

    -- Calculate the next available event_id
    SELECT COALESCE(MAX(event_id), 0) + 1 INTO v_next_event_id FROM SYSTEM_EVENTS;

    -- Insert with the calculated event_id
    INSERT INTO SYSTEM_EVENTS (event_id, event_type, severity, description, pid)
    VALUES (v_next_event_id, 'Audit Action', 'Warning', 'Risk level updated for ' || v_process_name, p_pid);

END;
$$;