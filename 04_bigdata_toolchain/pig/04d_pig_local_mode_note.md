Pig was used as a lightweight ETL audit tool for the long-format core indicator dataset.



In the HDP sandbox environment, TEZ/YARN execution was unstable during Pig execution, so Pig was run in local mode. This was an environment adaptation and did not change the audit logic. 



The input CSV was first copied from HDFS to the local working directory. Pig then loaded the no-header long-format indicator file, filtered the formal analysis period from 2015 to 2024, and validated row counts by indicator group and country.



The Pig audit confirmed:



total records = 720

EVI records = 450

DRI records = 270

each country contained 50 EVI records and 30 DRI records

