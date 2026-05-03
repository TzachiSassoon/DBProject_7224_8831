BEGIN; -- Starts the transaction

-- 1. Show state before (Check a specific resource status)
SELECT resource_id, resource_name, is_operational FROM RESOURCES WHERE resource_id = 1;

-- 2. Perform the update (Simulate a system failure)
UPDATE RESOURCES SET is_operational = FALSE WHERE resource_id = 1;

-- 3. Show state after update (It will show FALSE within this block)
SELECT resource_id, resource_name, is_operational FROM RESOURCES WHERE resource_id = 1;

ROLLBACK; -- Undo everything

-- 4. Verify it returned to original state
SELECT resource_id, resource_name, is_operational FROM RESOURCES WHERE resource_id = 1;