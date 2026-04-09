import csv
import random

# Base categories to keep the data somewhat logical
categories = [
    ("Compute", "GHz"), ("Memory", "GB"), ("Storage", "TB"), 
    ("Network", "Gbps"), ("Accelerator", "TFLOPS"), ("Cache", "MB"), 
    ("IO_Controller", "Ops/s"), ("Buffer", "KB"), ("Bus", "MT/s"), ("Virtual_Unit", "vCore")
]

# --- 1. GENERATE RESOURCE_TYPES.CSV (500 Rows) ---
with open('resource_types.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['type_id', 'type_name', 'unit_measure'])
    
    for i in range(1, 501):
        cat_name, unit = random.choice(categories)
        # Create a unique type name like "Compute_Type_042"
        type_name = f"{cat_name}_Type_{str(i).zfill(3)}"
        writer.writerow([i, type_name, unit])

# --- 2. GENERATE RESOURCES.CSV (500 Rows) ---
with open('resources.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['resource_id', 'resource_name', 'capacity', 'is_operational', 'type_id'])
    
    brand_names = ["Intel", "AMD", "NVIDIA", "Samsung", "Cisco", "Dell", "HP", "Apple", "AWS", "Azure"]
    
    for i in range(1, 501):
        # Link resource_id 'i' to type_id 'i' (1-to-1 mapping for simplicity)
        tid = i 
        res_name = f"{random.choice(brand_names)}_Asset_{str(i).zfill(3)}"
        capacity = round(random.uniform(10.0, 5000.0), 2)
        
        writer.writerow([i, res_name, capacity, True, tid])

print("Created resource_types.csv (500 rows) and resources.csv (500 rows).")