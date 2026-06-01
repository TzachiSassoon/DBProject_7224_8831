SELECT First_Name, Last_Name, COUNT(pid) as active_processes
FROM sysmanager_process_audit_view
GROUP BY First_Name, Last_Name;