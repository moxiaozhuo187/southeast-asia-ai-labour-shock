# Southeast Asia and the AI Labour Shock
### A Comparative Big Data Analysis with China as a Benchmark

**Course:** STQD6324 Data Management  
**Dataset:** World Bank Open Data API  
**Analysis period:** 2015–2024  
**Countries:** Malaysia, Singapore, Thailand, Indonesia, Vietnam, Philippines, Cambodia, Laos + China (benchmark)



## Why I Did This


I am studying in Malaysia and I have been curious about Southeast Asia for a while — not just in terms of which countries are richer or faster-growing, but in terms of how differently their labour markets are structured. When AI started becoming a real topic rather than a future speculation, I kept wondering whether the countries here were actually in very different positions when it came to handling that kind of disruption.

Most of what I read on AI and labour markets focuses on the US or Europe. Southeast Asia gets mentioned as a region that will be affected, but rarely broken down country by country. I wanted to do that with actual data instead of general statements.

I added China as an external benchmark because it felt like a useful reference point — a country that has gone through rapid industrialisation, has a very large labour force, and has been investing heavily in digital infrastructure. What I did not expect was that China would end up with one of the highest employment vulnerability scores in the dataset. After checking the numbers it made sense, but it was a good reminder that high digital readiness does not mean low vulnerability — it just means the two things can coexist.



## Research Question

Which Southeast Asian countries are more exposed to AI-related labour market vulnerability, and which ones have the digital readiness to absorb that pressure?

I built two indices:

- **EVI** (Employment Vulnerability Index) — based on employment structure and unemployment rates
- **DRI** (Digital Readiness Index) — based on internet access, mobile subscriptions, and broadband

The difference between them is the risk gap:

```text
risk_gap = EVI - DRI
```

Positive = vulnerability is outpacing readiness.  
Negative = readiness may offset some of the pressure.



## Key Findings

Indonesia has the highest positive risk gap in 2024.

Singapore and Thailand ended up in the same K-means cluster. Thailand's strong mobile connectivity pushed its DRI up enough to group it with Singapore, even though the two countries are quite different overall. K-means works on indicator distance, not general development level.

In the K-means result, Laos, Cambodia, and the Philippines cluster as low EVI and low DRI. That is not a safe position — low vulnerability here mostly reflects that these economies have not yet reached the stage where AI displacement pressure is fully showing up, not that they are prepared.

The quadrant analysis and K-means agree on 6 out of 8 countries. Indonesia and the Philippines are the two that diverge. Quadrant puts them in the higher-risk category. K-means places them differently because it works on distance rather than fixed thresholds. The divergence is discussed in the report.

Regionally, the average risk gap turned negative around 2018–2019, meaning digital readiness has been gradually catching up. But the regional average covers a lot of variation.



## Data Source

World Bank Open Data API ([https://data.worldbank.org](https://data.worldbank.org)) 

```text
9 countries × 8 indicators × 2015–2025 downloaded (72 API requests)
Formal analysis period: 2015–2024
```

2025 was downloaded but excluded after the coverage audit showed only 63.89% completeness, with most missing values in DRI indicators. The exclusion came from the audit, not a decision made upfront. 

China was used only as an external benchmark. It was not included in the Southeast Asian average or the K-means clustering sample.



## Tools Used

| Tool | Purpose |
|------|---------|
| Python / Google Colab | main analysis — data cleaning, index construction, clustering, visualisation |
| Apache Hive | SQL validation of row counts, rankings, and trends |
| Apache Spark / Zeppelin | independent recalculation of EVI, DRI, risk gap, and K-means |
| Apache Pig | lightweight ETL audit of the long-format indicator dataset |
| HBase | NoSQL country-year profile lookup |
| World Bank API | data source |

The Hadoop tools were used as a validation layer for the Python analysis. Hive for SQL checks, Spark to recalculate everything from scratch and confirm zero numerical difference from the Python results, Pig to audit the data structure, HBase to store and query selected country-year profiles.



## Repository Structure

```text
southeast-asia-ai-labour-shock/
├── README.md
├── report/
│   └── final_report.md
├── 01_data_availability_audit/
│   ├── 01_data_availability_audit.ipynb
│   └── outputs/
├── 02_index_calculation/
│   ├── 02_index_calculation.ipynb
│   └── outputs/
├── 03_visualization/
│   ├── 03_visualization.ipynb
│   └── figures/
└── 04_bigdata_toolchain/
    ├── 04a_bigdata_toolchain.ipynb
    ├── bigdata_input/
    ├── hive/
    │   ├── 04b_create_hive_tables.sql
    │   ├── 04b_hive_queries_readable.sql
    │   └── 04b_zeppelin_hive_query_validation.json
    ├── spark/
    │   ├── 04c_pyspark_validation.py
    │   └── 04c_Zeppelin_Pyspark_Validation.json
    ├── pig/
    │   ├── 04d_pig_etl_audit.pig
    │   └── 04d_pig_local_mode_note.md
    ├── hbase/
    │   ├── 04e_generate_hbase_puts.py
    │   └── 04e_hbase_commands.txt
    └── screenshots/
```



## How to Reproduce

**Python analysis (01–03):**
Open in Google Colab and run in order: 01 → 02 → 03. Each notebook reads from the previous stage's outputs.

**Big data input preparation (04a):**
Run `04_bigdata_toolchain/04a_bigdata_toolchain.ipynb` to generate the simplified CSV files for the Hadoop toolchain.

**Hadoop toolchain validation (04b–04e):**
Requires Hortonworks Sandbox VM.

1. Upload files from `04_bigdata_toolchain/bigdata_input/` to HDFS at `/user/maria_dev/labour_shock/input/`

2. Run `04_bigdata_toolchain/hive/04b_create_hive_tables.sql` in Hive CLI to create the external tables.

3. Use `04_bigdata_toolchain/hive/04b_hive_queries_readable.sql` or the exported Zeppelin note `04_bigdata_toolchain/hive/04b_zeppelin_hive_query_validation.json` to reproduce the Hive validation queries.

4. Run `04_bigdata_toolchain/spark/04c_pyspark_validation.py` in Zeppelin `%pyspark`, or check the exported Zeppelin note `04_bigdata_toolchain/spark/04c_Zeppelin_Pyspark_Validation.json`.

5. Run `04_bigdata_toolchain/pig/04d_pig_etl_audit.pig` in Pig local mode. The no-header core CSV should be copied to the Pig working directory before running the script. TEZ/YARN was unstable in the sandbox, so local mode was used while the audit logic stayed the same.

6. Run `04_bigdata_toolchain/hbase/04e_generate_hbase_puts.py` after placing `tool_index_2015_2024.csv` in the same working directory, or adjust the input path in the script. Then use `04_bigdata_toolchain/hbase/04e_hbase_commands.txt` in HBase shell.

Screenshots of the Hadoop toolchain outputs are stored in `04_bigdata_toolchain/screenshots/`.



## Full Report

The full report is available here:

[Open final report](report/final_report.md)



## Main Figures and Toolchain Screenshots

Figures generated from the Python analysis are stored here:

[Open visualisation figures](03_visualization/figures)

Screenshots from the Hadoop toolchain validation are stored here:

[Open Hadoop toolchain screenshots](04_bigdata_toolchain/screenshots)
