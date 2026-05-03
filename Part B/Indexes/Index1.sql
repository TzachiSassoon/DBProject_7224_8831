-- STEP 1: The Reset
-- Explain: "First, I am ensuring the index does not exist to establish a baseline."
DROP INDEX IF EXISTS idx_usage_time;

-- STEP 2: The "Before" Benchmark (Sequential Scan)
-- Explain: "I am querying for a specific 5-minute window. Without an index, the database must scan all 20,000+ rows to find these specific logs."
EXPLAIN ANALYZE 
SELECT * FROM USAGE_LOGS 
WHERE snapshot_time BETWEEN '2026-04-09 17:00:00' AND '2026-04-09 17:05:00'; 
-- NOTE for you: Point out the higher "Execution Time" and the words "Seq Scan" in the output to the professor.

-- STEP 3: The Optimization
-- Explain: "To optimize this heavily queried telemetry table, I will now create a B-Tree index on the timestamp column."
CREATE INDEX idx_usage_time ON USAGE_LOGS(snapshot_time);

-- STEP 4: The "After" Benchmark (Index Scan)
-- Explain: "I will now run the exact same query. Because the index exists, the query planner uses an Index Scan to jump directly to the relevant rows."
EXPLAIN ANALYZE 
SELECT * FROM USAGE_LOGS 
WHERE snapshot_time BETWEEN '2026-04-09 17:00:00' AND '2026-04-09 17:05:00';
-- NOTE for you: Point out the massive drop in "Execution Time" and the words "Index Scan" to secure full marks.