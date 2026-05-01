DELETE FROM SYSTEM_EVENTS
WHERE severity = 'Info'
  AND pid IN (
      SELECT p.pid 
      FROM PROCESSES p
      JOIN USERS u ON p.user_id = u.user_id
      WHERE u.account_type = 'Developer'
  );