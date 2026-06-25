
Big Data Input Files

This folder stores the simplified CSV files used in the big data part of this project.

The original cleaned files are kept in the outputs folder. For Hive, Pig and Spark, 
I created smaller and cleaner versions here so that the tools can read the data more easily.

Files in this folder:
1. tool_core_long_2015_2024.csv
Core indicator data in long format, with header.

2. tool_core_long_2015_2024_noheader.csv
Same as above, but without header. This version is mainly used for Hive and Pig.

3. tool_index_2015_2024.csv
Country-year EVI, DRI and risk gap results, with header.

4. tool_index_2015_2024_noheader.csv
Same as above, but without header. This version is mainly used for Hive.

5. tool_cluster_2019_2024.csv
SEA-only K-means clustering result, with header.

6. tool_cluster_2019_2024_noheader.csv
Same as above, but without header.

Why these files are simplified:
Some text fields in the original dataset, such as indicator_name, contain commas. 
This may cause parsing problems when Hive or Pig reads the file using comma as the separator. 
Therefore, these big data input files keep only the fields needed for Hive, Pig, 
Spark and optional HBase tasks.
