CREATE VIEW sysmanager_process_audit_view AS
SELECT 
    p.pid,
    p.process_name,
    u.username,
    e.First_Name,
    e.Last_Name,
    e.Job_Title
FROM PROCESSES p
JOIN USERS u ON p.user_id = u.user_id
JOIN employee e ON u.user_id = e.Employee_ID;