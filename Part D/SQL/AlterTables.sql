-- Add a risk level column to track suspicious processes
ALTER TABLE PROCESSES ADD COLUMN risk_level VARCHAR(50);

-- Add an efficiency score column to evaluate hardware ROI
ALTER TABLE RESOURCES ADD COLUMN efficiency_score NUMERIC(5,2);