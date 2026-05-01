UPDATE PROCESSES
SET status = 'Terminated'
WHERE parent_pid IS NOT NULL 
  AND parent_pid IN (
      SELECT pid 
      FROM PROCESSES 
      WHERE status = 'Terminated'
  );