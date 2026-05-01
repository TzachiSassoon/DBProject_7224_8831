WITH CleanUserActivity AS (
    SELECT DISTINCT u.username, p.pid, e.file_size_kb
    FROM USERS u
    JOIN PROCESSES p ON u.user_id = p.user_id
    JOIN EXECUTABLES e ON p.exe_id = e.exe_id
    WHERE p.status = 'Running'
)
SELECT 
    username, 
    COUNT(pid) AS running_processes, 
    AVG(file_size_kb) AS avg_exe_size
FROM CleanUserActivity
GROUP BY username;
