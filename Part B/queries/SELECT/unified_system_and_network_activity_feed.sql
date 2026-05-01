SELECT * FROM (
    SELECT 
        'System Event' AS category,
        p.process_name AS target,
        s.severity AS status_or_type,
        s.description AS details,
        p.start_time AS activity_time,
        CASE WHEN s.severity = 'Critical' THEN 3 WHEN s.severity = 'Warning' THEN 2 ELSE 1 END AS priority_level
    FROM SYSTEM_EVENTS s
    JOIN PROCESSES p ON s.pid = p.pid

    UNION ALL

    SELECT 
        'Network Activity' AS category,
        p.process_name AS target,
        n.protocol AS status_or_type,
        ('Dest: ' || n.dest_ip || ' | Data: ' || ROUND(n.bytes_sent/1024, 2) || ' KB') AS details,
        p.start_time AS activity_time,
        1 AS priority_level
    FROM NETWORK_SESSIONS n
    JOIN PROCESSES p ON n.pid = p.pid
) AS UnifiedLog
ORDER BY activity_time DESC
LIMIT 50;
