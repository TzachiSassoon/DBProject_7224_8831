BEGIN;

-- 1. Show state before
SELECT * FROM USERS WHERE user_id = 1;

-- 2. Update username
UPDATE USERS SET username = 'admin_v2' WHERE user_id = 1;

COMMIT; -- Save permanently

-- 3. Show state remains updated
SELECT * FROM USERS WHERE user_id = 1;