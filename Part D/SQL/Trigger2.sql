CREATE OR REPLACE FUNCTION verify_maintenance_cost()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.repair_cost > 10000 THEN
        RAISE EXCEPTION 'Repair cost % exceeds maximum allowed budget ($10,000).', NEW.repair_cost;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_check_repair_cost
BEFORE INSERT OR UPDATE ON MAINTENANCE_LOG
FOR EACH ROW
EXECUTE FUNCTION verify_maintenance_cost();