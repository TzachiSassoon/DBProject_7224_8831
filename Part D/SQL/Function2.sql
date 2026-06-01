CREATE OR REPLACE FUNCTION calc_efficiency(p_resource_id INT)
RETURNS NUMERIC AS $$
DECLARE
    v_total_cost NUMERIC;
    v_capacity INT;
    v_score NUMERIC;
BEGIN
    SELECT SUM(repair_cost) INTO v_total_cost FROM MAINTENANCE_LOG WHERE resource_id = p_resource_id;
    SELECT capacity INTO v_capacity FROM RESOURCES WHERE resource_id = p_resource_id;

    IF v_total_cost IS NULL OR v_total_cost = 0 THEN
        v_score := 100.00;
    ELSE
        -- Calculate raw score
        v_score := (v_capacity / v_total_cost) * 100;
    END IF;

    -- THE FIX: Cap the score at 100 and round to 2 decimals
    IF v_score > 100.00 THEN
        v_score := 100.00;
    END IF;

    RETURN ROUND(v_score, 2);

EXCEPTION
    WHEN division_by_zero THEN
        RETURN 0;
END;
$$ LANGUAGE plpgsql;