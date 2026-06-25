USE labour_shock;

-- Query 1: Row count validation
SELECT 'country_year_index' AS table_name, COUNT(*) AS row_count FROM country_year_index
UNION ALL
SELECT 'core_long' AS table_name, COUNT(*) AS row_count FROM core_long
UNION ALL
SELECT 'sea_cluster' AS table_name, COUNT(*) AS row_count FROM sea_cluster;

-- Query 2: 2024 risk gap ranking
SELECT
country_code,
country_name,
ROUND(evi_main,3) AS evi_main,
ROUND(dri,3) AS dri,
ROUND(risk_gap,3) AS risk_gap
FROM country_year_index
WHERE year=2024
ORDER BY risk_gap DESC;

-- Query 3: China benchmark trend, 2015-2024
SELECT
year,
ROUND(evi_main,3) AS evi_main,
ROUND(dri,3) AS dri,
ROUND(risk_gap,3) AS risk_gap
FROM country_year_index
WHERE country_code='CHN'
ORDER BY year;

-- Query 4: Indicator group audit
SELECT
indicator_group,
COUNT(*) AS row_count
FROM core_long
GROUP BY indicator_group
ORDER BY indicator_group;

-- Query 5: K-means cluster baseline table
SELECT
country_code,
country_name,
ROUND(evi_main_avg,3) AS evi_main_avg,
ROUND(dri_avg,3) AS dri_avg,
ROUND(risk_gap_avg,3) AS risk_gap_avg,
cluster,
cluster_label
FROM sea_cluster
ORDER BY cluster, country_code;