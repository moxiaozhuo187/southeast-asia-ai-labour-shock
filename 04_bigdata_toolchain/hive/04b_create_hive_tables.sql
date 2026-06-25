-- Before running this script, the no-header CSV files were copied from:
-- /user/maria_dev/labour_shock/input/
-- to the following Hive external table locations:
-- /user/maria_dev/labour_shock/hive/index
-- /user/maria_dev/labour_shock/hive/core
-- /user/maria_dev/labour_shock/hive/cluster
CREATE DATABASE IF NOT EXISTS labour_shock;
USE labour_shock;

DROP TABLE IF EXISTS country_year_index;
DROP TABLE IF EXISTS core_long;
DROP TABLE IF EXISTS sea_cluster;

CREATE EXTERNAL TABLE country_year_index (
    country_code STRING,
    country_name STRING,
    is_benchmark STRING,
    year INT,
    evi_main DOUBLE,
    evi_robust_010 DOUBLE,
    evi_robust_020 DOUBLE,
    dri DOUBLE,
    risk_gap DOUBLE,
    risk_gap_robust_010 DOUBLE,
    risk_gap_robust_020 DOUBLE
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/user/maria_dev/labour_shock/hive/index';

CREATE EXTERNAL TABLE core_long (
    country_code STRING,
    country_name STRING,
    is_benchmark STRING,
    indicator_code STRING,
    indicator_group STRING,
    year INT,
    value DOUBLE
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/user/maria_dev/labour_shock/hive/core';

CREATE EXTERNAL TABLE sea_cluster (
    country_code STRING,
    country_name STRING,
    evi_main_avg DOUBLE,
    dri_avg DOUBLE,
    risk_gap_avg DOUBLE,
    cluster INT,
    cluster_label STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/user/maria_dev/labour_shock/hive/cluster';

SHOW TABLES;