SELECT 
    EXTRACT(YEAR FROM p.start_time) AS event_year,
    EXTRACT(MONTH FROM p.start_time) AS event_month,
    COUNT(s.event_id) AS total_events
FROM SYSTEM_EVENTS s
JOIN PROCESSES p ON s.pid = p.pid
WHERE s.severity = 'Critical'
GROUP BY event_year, event_month
ORDER BY event_year DESC, event_month DESC;
