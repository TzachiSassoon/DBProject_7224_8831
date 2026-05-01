SELECT 
    p.process_name, 
    u.username, 
    COUNT(s.event_id) AS total_critical_events
FROM PROCESSES p
JOIN USERS u ON p.user_id = u.user_id
JOIN SYSTEM_EVENTS s ON p.pid = s.pid
WHERE s.severity = 'Critical'
  AND p.pid IN (SELECT pid FROM USAGE_LOGS)
GROUP BY p.process_name, u.username
HAVING COUNT(s.event_id) > 2;
