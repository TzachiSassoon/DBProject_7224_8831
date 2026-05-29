-- 1. Enable the Foreign Data Wrapper extension
CREATE EXTENSION IF NOT EXISTS postgres_fdw;

-- 2. Define the GymOps server using their pooler host and port
CREATE SERVER gymops_server
FOREIGN DATA WRAPPER postgres_fdw
OPTIONS (host 'aws-0-eu-west-1.pooler.supabase.com', port '5432', dbname 'postgres');

-- 3. Set up your authentication bridge using their specific project user
-- MAKE SURE TO REPLACE [YOUR-PASSWORD] WITH THE ACTUAL PASSWORD
CREATE USER MAPPING FOR current_user
SERVER gymops_server
OPTIONS (user 'postgres.dtmlqdvdqvxopncnifmr', password 'D1J2Y3B430!');

-- 4. Import the Employee table securely
IMPORT FOREIGN SCHEMA public LIMIT TO ("EMPLOYEE")
FROM SERVER gymops_server
INTO public;