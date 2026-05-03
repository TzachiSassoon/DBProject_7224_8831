-- STEP 1: The Reset
-- Explain: "I am dropping the index to establish our baseline for detecting critical hardware stress."
DROP INDEX IF EXISTS idx_cpu_spike;

-- STEP 2: The "Before" Benchmark (Sequential Scan)
-- Explain: "I am querying the USAGE_LOGS table for extreme CPU spikes (98% or higher). Without an index, the database must perform a full Seq Scan across all 20,000+ telemetry rows to find these few critical events."
EXPLAIN ANALYZE 
SELECT * FROM USAGE_LOGS 
WHERE cpu_percent >= 98.00;
-- NOTE for you: Point out the higher Execution Time and the "Seq Scan" label.

-- STEP 3: The Optimization
-- Explain: "To allow the Dashboard to instantly trigger warnings during a system overload, I am creating a B-Tree index on the cpu_percent column."
CREATE INDEX idx_cpu_spike ON USAGE_LOGS(cpu_percent);

-- STEP 4: The "After" Benchmark (Index Scan)
-- Explain: "Running the exact same query again. Because extreme CPU values are highly selective, the query planner utilizes the new index to instantly isolate those specific logs."
EXPLAIN ANALYZE 
SELECT * FROM USAGE_LOGS 
WHERE cpu_percent >= 98.00;
-- NOTE for you: Point out the steep drop in Execution Time and the "Index Scan" (or "Bitmap Heap Scan") label.