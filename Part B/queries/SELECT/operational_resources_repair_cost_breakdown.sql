SELECT 
    r.resource_name,
    rt.type_name,
    m.technician_name,
    m.repair_cost
FROM RESOURCES r
JOIN MAINTENANCE_LOG m ON r.resource_id = m.resource_id
JOIN RESOURCE_TYPES rt ON r.type_id = rt.type_id
WHERE r.is_operational = TRUE
ORDER BY m.repair_cost DESC;
