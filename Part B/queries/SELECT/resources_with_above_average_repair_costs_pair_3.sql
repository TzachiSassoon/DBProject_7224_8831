SELECT 
    r.resource_name, 
    SUM(m.repair_cost) AS total_repair_cost,
    (SELECT AVG(m2.repair_cost) 
     FROM MAINTENANCE_LOG m2 
     JOIN RESOURCES r2 ON m2.resource_id = r2.resource_id 
     WHERE r2.type_id = r.type_id) AS category_avg
FROM RESOURCES r
JOIN MAINTENANCE_LOG m ON r.resource_id = m.resource_id
GROUP BY r.resource_id, r.resource_name, r.type_id
HAVING SUM(m.repair_cost) > (
    SELECT AVG(m3.repair_cost) 
    FROM MAINTENANCE_LOG m3 
    JOIN RESOURCES r3 ON m3.resource_id = r3.resource_id 
    WHERE r3.type_id = r.type_id
);
