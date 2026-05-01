SELECT 
    p.process_name,
    rt.type_name,
    AVG(u.cpu_percent) AS process_avg_cpu,
    (SELECT AVG(u2.cpu_percent) 
     FROM USAGE_LOGS u2
     JOIN PROCESSES p2 ON u2.pid = p2.pid
     JOIN ALLOCATIONS a2 ON p2.pid = a2.pid
     JOIN RESOURCES r2 ON a2.resource_id = r2.resource_id
     WHERE r2.type_id = rt.type_id) AS type_benchmark_avg
FROM PROCESSES p
JOIN USAGE_LOGS u ON p.pid = u.pid
JOIN ALLOCATIONS a ON p.pid = a.pid
JOIN RESOURCES r ON a.resource_id = r.resource_id
JOIN RESOURCE_TYPES rt ON r.type_id = rt.type_id
GROUP BY p.process_name, rt.type_name, rt.type_id
HAVING AVG(u.cpu_percent) > (
    SELECT AVG(u2.cpu_percent) 
    FROM USAGE_LOGS u2
    JOIN PROCESSES p2 ON u2.pid = p2.pid
    JOIN ALLOCATIONS a2 ON p2.pid = a2.pid
    JOIN RESOURCES r2 ON a2.resource_id = r2.resource_id
    WHERE r2.type_id = rt.type_id
);
