CREATE OR REPLACE FUNCTION get_risky_processes(p_threshold INT)
RETURNS refcursor AS $$
DECLARE
    risky_cursor refcursor;
BEGIN
    -- Open Ref Cursor with a complex JOIN query
    OPEN risky_cursor FOR
        SELECT p.pid, p.process_name, u.account_type, COUNT(e.event_id) as event_count
        FROM PROCESSES p
        JOIN USERS u ON p.user_id = u.user_id
        JOIN SYSTEM_EVENTS e ON p.pid = e.pid
        GROUP BY p.pid, p.process_name, u.account_type
        HAVING COUNT(e.event_id) >= p_threshold;

    RETURN risky_cursor;
EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Error generating ref cursor: %', SQLERRM;
        RETURN NULL;
END;
$$ LANGUAGE plpgsql;