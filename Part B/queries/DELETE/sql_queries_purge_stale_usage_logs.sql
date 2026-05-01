DELETE FROM USAGE_LOGS
WHERE snapshot_time < CURRENT_DATE - INTERVAL '30 days'
  AND pid IN (
      SELECT pid 
      FROM PROCESSES 
      WHERE status = 'Terminated' OR status = 'Completed'
  );