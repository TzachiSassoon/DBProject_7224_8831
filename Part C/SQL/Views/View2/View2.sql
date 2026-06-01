CREATE VIEW gymops_staff_access_view AS
SELECT 
    e.Employee_ID,
    e.First_Name,
    e.Last_Name,
    u.account_type,
    u.creation_date
FROM EMPLOYEE e
JOIN USERS u ON e.Employee_ID = u.user_id;