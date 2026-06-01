CREATE OR REPLACE PROCEDURE update_efficiencies()
LANGUAGE plpgsql AS $$
DECLARE
    -- Explicit Cursor 
    c_resources CURSOR FOR SELECT * FROM RESOURCES WHERE is_operational = TRUE;
    v_res RESOURCES%ROWTYPE; 
    v_score NUMERIC;
BEGIN
    OPEN c_resources;
    LOOP
        FETCH c_resources INTO v_res;
        EXIT WHEN NOT FOUND;

        v_score := calc_efficiency(v_res.resource_id);
        
        -- Update the resource
        UPDATE RESOURCES SET efficiency_score = v_score WHERE resource_id = v_res.resource_id;
    END LOOP;
    CLOSE c_resources;
END;
$$;