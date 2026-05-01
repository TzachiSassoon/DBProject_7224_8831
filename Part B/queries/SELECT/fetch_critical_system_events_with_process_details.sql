SELECT 
    s.event_type,
    p.process_name,
    s.description,
    p.start_time
FROM SYSTEM_EVENTS s
JOIN PROCESSES p ON s.pid = p.pid
WHERE s.severity = 'Critical'
ORDER BY p.start_time DESC;
