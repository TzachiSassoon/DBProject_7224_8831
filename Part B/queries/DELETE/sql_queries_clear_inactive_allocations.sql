DELETE FROM ALLOCATIONS
WHERE resource_id IN (
    SELECT resource_id 
    FROM RESOURCES 
    WHERE is_operational = FALSE
);