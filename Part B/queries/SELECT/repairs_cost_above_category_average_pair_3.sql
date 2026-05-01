SELECT 
    resource_name, 
    total_repair_cost, 
    category_avg
FROM (
    SELECT 
        r.resource_name,
        r.type_id,
        SUM(m.repair_cost) as total_repair_cost,
        -- Matches the logic of Implementation B by averaging individual repairs
        AVG(m.repair_cost) OVER(PARTITION BY r.type_id) as category_avg
    FROM RESOURCES r
    JOIN MAINTENANCE_LOG m ON r.resource_id = m.resource_id
    GROUP BY r.resource_id, r.resource_name, r.type_id, m.repair_cost
) AS AggregatedStats
WHERE total_repair_cost > category_avg;
