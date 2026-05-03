-- STEP 1: The Reset
-- Explain: "I am dropping the index to establish our baseline performance for network queries."
DROP INDEX IF EXISTS idx_net_ip;

-- STEP 2: The "Before" Benchmark (Sequential Scan)
-- Explain: "Here I am searching 20,000+ network sessions for traffic heading to a specific IP address. Without an index, the engine performs a full Seq Scan."
EXPLAIN ANALYZE 
SELECT * FROM NETWORK_SESSIONS 
WHERE dest_ip = '161.49.55.123';
-- NOTE for you: Point out the higher "Execution Time" and the "Seq Scan" label to the professor.

-- STEP 3: The Optimization
-- Explain: "To optimize our Security Audit dashboard, I am creating a B-Tree index specifically on the destination IP column."
CREATE INDEX idx_net_ip ON NETWORK_SESSIONS(dest_ip);

-- STEP 4: The "After" Benchmark (Index Scan/Bitmap Heap Scan)
-- Explain: "Running the exact same query again. The query planner now utilizes the index to map directly to the relevant rows, bypassing thousands of irrelevant logs."
EXPLAIN ANALYZE 
SELECT * FROM NETWORK_SESSIONS 
WHERE dest_ip = '161.49.55.123';
-- NOTE for you: Point out the steep drop in "Execution Time" and the "Index Scan" (or "Bitmap Heap Scan") label.