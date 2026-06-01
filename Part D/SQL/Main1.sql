DO $$
DECLARE
    v_refcursor refcursor;
    v_record RECORD;
BEGIN
    v_refcursor := get_risky_processes(1);

    LOOP
        FETCH v_refcursor INTO v_record;
        EXIT WHEN NOT FOUND;
        CALL handle_risky_process(v_record.pid, v_record.account_type);
    END LOOP;

    CLOSE v_refcursor;
END;
$$;