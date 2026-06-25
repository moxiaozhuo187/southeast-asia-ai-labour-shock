core = LOAD 'tool_core_long_2015_2024_noheader.csv'
USING PigStorage(',')
AS (
country_code,
country_name,
is_benchmark,
indicator_code,
indicator_group,
year,
value
);

formal = FILTER core BY year >= 2015 AND year <= 2024;

all_group = GROUP formal ALL;
total_count = FOREACH all_group GENERATE COUNT(formal) AS total_rows;
DUMP total_count;

group_by_indicator = GROUP formal BY indicator_group;
indicator_count = FOREACH group_by_indicator GENERATE
group AS indicator_group,
COUNT(formal) AS row_count;
DUMP indicator_count;

group_by_country_indicator = GROUP formal BY (country_code, indicator_group);
country_indicator_count = FOREACH group_by_country_indicator GENERATE
group.country_code AS country_code,
group.indicator_group AS indicator_group,
COUNT(formal) AS row_count;
DUMP country_indicator_count;