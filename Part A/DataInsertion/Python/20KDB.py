import csv
import random
from datetime import datetime, timedelta

# Settings
TOTAL_ROWS = 20000
PIDS = 500  # Matches your 500 Processes

# 1. GENERATE USAGE_LOGS (20,000 rows)
with open('usage_logs.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['log_id', 'snapshot_time', 'cpu_percent', 'ram_usage_mb', 'pid'])
    
    # Start logs from today's date
    start_time = datetime.now()
    
    for i in range(1, TOTAL_ROWS + 1):
        # Each log is 5 seconds apart to show a timeline
        log_time = start_time + timedelta(seconds=i * 5)
        writer.writerow([
            i, 
            log_time.strftime('%Y-%m-%d %H:%M:%S'), 
            round(random.uniform(0.5, 98.0), 2), 
            random.randint(128, 16384), 
            random.randint(1, PIDS)
        ])

# 2. GENERATE NETWORK_SESSIONS (20,000 rows)
with open('network_sessions.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['session_id', 'dest_ip', 'port', 'protocol', 'bytes_sent', 'pid'])
    
    protocols = ['TCP', 'UDP', 'HTTP', 'HTTPS', 'SSH']
    
    for i in range(1, TOTAL_ROWS + 1):
        ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
        writer.writerow([
            i, 
            ip, 
            random.choice([80, 443, 22, 53, 8080]), 
            random.choice(protocols), 
            random.randint(500, 10000000), # Up to 10MB sent
            random.randint(1, PIDS)
        ])

print("✅ SUCCESS: usage_logs.csv (20,000) and network_sessions.csv (20,000) created!")