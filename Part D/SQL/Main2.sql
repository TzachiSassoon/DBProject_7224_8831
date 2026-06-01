DO $$
BEGIN
    CALL update_efficiencies();
    RAISE NOTICE 'Resource efficiencies recalculated successfully.';
END;
$$;