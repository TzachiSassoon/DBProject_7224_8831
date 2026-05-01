UPDATE SYSTEM_EVENTS
SET severity = 'Critical'
WHERE pid IN (
    SELECT pid 
    FROM NETWORK_SESSIONS 
    WHERE bytes_sent > 1073741824 -- 1GB in bytes
);