UPDATE MAINTENANCE_LOG
SET repair_cost = repair_cost * 1.15
WHERE technician_name = 'Maria Garcia'
  AND EXTRACT(YEAR FROM repair_date) = 2026
  AND resource_id IN (
      SELECT r.resource_id 
      FROM RESOURCES r
      JOIN RESOURCE_TYPES rt ON r.type_id = rt.type_id
      WHERE rt.type_name = 'System_RAM'
  );