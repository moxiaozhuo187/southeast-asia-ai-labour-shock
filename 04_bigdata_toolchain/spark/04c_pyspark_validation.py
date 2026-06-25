# %pyspark
from pyspark.sql import functions as F
from pyspark.sql.types import DoubleType
from pyspark.ml.feature import VectorAssembler, MinMaxScaler

core_path="hdfs:///user/maria_dev/labour_shock/input/tool_core_long_2015_2024.csv"
index_path="hdfs:///user/maria_dev/labour_shock/input/tool_index_2015_2024.csv"
cluster_path="hdfs:///user/maria_dev/labour_shock/input/tool_cluster_2019_2024.csv"

core=spark.read.format("csv").option("header","true").option("inferSchema","true").load(core_path)
py_index=spark.read.format("csv").option("header","true").option("inferSchema","true").load(index_path)
py_cluster=spark.read.format("csv").option("header","true").option("inferSchema","true").load(cluster_path)

print("core rows:",core.count())
print("python index rows:",py_index.count())
print("python cluster rows:",py_cluster.count())

core.printSchema()

# %pyspark
core2=core.withColumn(
    "var",
    F.when(F.col("indicator_code")=="SL.IND.EMPL.ZS","ind_emp")
     .when(F.col("indicator_code")=="SL.AGR.EMPL.ZS","agr_emp")
     .when(F.col("indicator_code")=="SL.SRV.EMPL.ZS","srv_emp")
     .when(F.col("indicator_code")=="SL.UEM.TOTL.ZS","unemp")
     .when(F.col("indicator_code")=="SL.UEM.1524.ZS","youth_unemp")
     .when(F.col("indicator_code")=="IT.NET.USER.ZS","net_user")
     .when(F.col("indicator_code")=="IT.CEL.SETS.P2","mobile_sub")
     .when(F.col("indicator_code")=="IT.NET.BBND.P2","broadband")
)

core2.select("indicator_code","var").distinct().orderBy("var").show(20,False)

# %pyspark
var_order=["ind_emp","agr_emp","srv_emp","unemp","youth_unemp","net_user","mobile_sub","broadband"]

wide=core2.groupBy("country_code","country_name","is_benchmark","year") \
          .pivot("var",var_order) \
          .agg(F.first("value")) \
          .orderBy("country_code","year")

print("wide rows:",wide.count())

wide.show(10,False)

# %pyspark
raw_cols=["ind_emp","agr_emp","srv_emp","unemp","youth_unemp","net_user","mobile_sub","broadband"]

assembler=VectorAssembler(inputCols=raw_cols,outputCol="raw_features")
wide_vec=assembler.transform(wide)

scaler=MinMaxScaler(inputCol="raw_features",outputCol="norm_features")
scaler_model=scaler.fit(wide_vec)
scaled=scaler_model.transform(wide_vec)

def get_vec_item(i):
    return F.udf(lambda v: float(v[i]),DoubleType())

norm_cols=["ind_emp_n","agr_emp_n","srv_emp_n","unemp_n","youth_unemp_n","net_user_n","mobile_sub_n","broadband_n"]

spark_norm=scaled
for i in range(len(norm_cols)):
    spark_norm=spark_norm.withColumn(norm_cols[i],get_vec_item(i)(F.col("norm_features")))

spark_norm.select(
    "country_code","year",
    F.round("ind_emp_n",3).alias("ind_emp_n"),
    F.round("agr_emp_n",3).alias("agr_emp_n"),
    F.round("net_user_n",3).alias("net_user_n"),
    F.round("broadband_n",3).alias("broadband_n")
).show(10,False)

# %pyspark
spark_index=spark_norm.withColumn(
    "evi_main",
    0.30*F.col("ind_emp_n")+
    0.20*F.col("agr_emp_n")+
    0.25*F.col("unemp_n")+
    0.25*F.col("youth_unemp_n")
).withColumn(
    "dri",
    (F.col("net_user_n")+F.col("mobile_sub_n")+F.col("broadband_n"))/3.0
).withColumn(
    "risk_gap",
    F.col("evi_main")-F.col("dri")
)

spark_index.select(
    "country_code",
    "country_name",
    "year",
    F.round("evi_main",3).alias("evi"),
    F.round("dri",3).alias("dri"),
    F.round("risk_gap",3).alias("risk_gap")
).filter(F.col("year")==2024).orderBy(F.desc("risk_gap")).show(20,False)

# %pyspark
spark_compare=spark_index.select(
    "country_code",
    "year",
    F.col("evi_main").alias("spark_evi"),
    F.col("dri").alias("spark_dri"),
    F.col("risk_gap").alias("spark_risk_gap")
).join(
    py_index.select(
        "country_code",
        "year",
        F.col("evi_main").alias("python_evi"),
        F.col("dri").alias("python_dri"),
        F.col("risk_gap").alias("python_risk_gap")
    ),
    ["country_code","year"],
    "inner"
)

spark_compare=spark_compare.withColumn("evi_diff",F.abs(F.col("spark_evi")-F.col("python_evi"))) \
                           .withColumn("dri_diff",F.abs(F.col("spark_dri")-F.col("python_dri"))) \
                           .withColumn("risk_gap_diff",F.abs(F.col("spark_risk_gap")-F.col("python_risk_gap")))

spark_compare.agg(
    F.round(F.max("evi_diff"),10).alias("max_evi_diff"),
    F.round(F.max("dri_diff"),10).alias("max_dri_diff"),
    F.round(F.max("risk_gap_diff"),10).alias("max_risk_gap_diff")
).show()

spark_compare.select(
    "country_code",
    "year",
    F.round("spark_risk_gap",6).alias("spark_risk_gap"),
    F.round("python_risk_gap",6).alias("python_risk_gap"),
    F.round("risk_gap_diff",10).alias("diff")
).filter(F.col("year")==2024).orderBy(F.desc("spark_risk_gap")).show(20,False)

# %pyspark
sea_avg=spark_index.filter(
    (F.col("country_code")!="CHN") &
    (F.col("year")>=2019) &
    (F.col("year")<=2024)
).groupBy("country_code","country_name").agg(
    F.avg("evi_main").alias("evi_main_avg"),
    F.avg("dri").alias("dri_avg"),
    F.avg("risk_gap").alias("risk_gap_avg")
).orderBy("country_code")

sea_avg.select(
    "country_code",
    "country_name",
    F.round("evi_main_avg",3).alias("evi_avg"),
    F.round("dri_avg",3).alias("dri_avg"),
    F.round("risk_gap_avg",3).alias("risk_gap_avg")
).show(20,False)

# %pyspark
from pyspark.ml.clustering import KMeans

cluster_assembler=VectorAssembler(
    inputCols=["evi_main_avg","dri_avg"],
    outputCol="features"
)

sea_vec=cluster_assembler.transform(sea_avg)

best_model=None
best_seed=None
best_cost=None

for s in [1,2,3,4,5,6,7,8,9,10,20,30,40,42,50,60,70,80,90,100]:
    km=KMeans() \
        .setK(3) \
        .setSeed(s) \
        .setFeaturesCol("features") \
        .setPredictionCol("spark_cluster") \
        .setMaxIter(50)
    model=km.fit(sea_vec)
    cost=model.computeCost(sea_vec)
    print("seed:",s,"cost:",cost)
    if best_cost is None or cost<best_cost:
        best_cost=cost
        best_seed=s
        best_model=model

print("best seed:",best_seed)
print("best cost:",best_cost)

spark_cluster=best_model.transform(sea_vec)

spark_cluster.select(
    "country_code",
    "country_name",
    F.round("evi_main_avg",3).alias("evi_avg"),
    F.round("dri_avg",3).alias("dri_avg"),
    F.round("risk_gap_avg",3).alias("risk_gap_avg"),
    "spark_cluster"
).orderBy("spark_cluster","country_code").show(20,False)

# %pyspark
evi_values=[r["evi_main_avg"] for r in sea_avg.select("evi_main_avg").collect()]
dri_values=[r["dri_avg"] for r in sea_avg.select("dri_avg").collect()]

evi_values.sort()
dri_values.sort()

def median(vals):
    n=len(vals)
    if n%2==0:
        return (vals[n//2-1]+vals[n//2])/2.0
    else:
        return vals[n//2]

evi_cut=median(evi_values)
dri_cut=median(dri_values)

print("SEA median evi:",evi_cut)
print("SEA median dri:",dri_cut)

spark_cluster_summary=spark_cluster.groupBy("spark_cluster").agg(
    F.avg("evi_main_avg").alias("cluster_evi_avg"),
    F.avg("dri_avg").alias("cluster_dri_avg"),
    F.count("*").alias("country_count")
)

spark_cluster_summary=spark_cluster_summary.withColumn(
    "vulnerability_label",
    F.when(F.col("cluster_evi_avg")>=F.lit(evi_cut),"High vulnerability")
     .otherwise("Low vulnerability")
).withColumn(
    "readiness_label",
    F.when(F.col("cluster_dri_avg")>=F.lit(dri_cut),"High readiness")
     .otherwise("Low readiness")
).withColumn(
    "spark_cluster_label",
    F.concat(F.col("vulnerability_label"),F.lit(" - "),F.col("readiness_label"))
)

spark_cluster_labeled=spark_cluster.join(
    spark_cluster_summary.select("spark_cluster","spark_cluster_label"),
    "spark_cluster",
    "left"
)

spark_cluster_labeled.select(
    "country_code",
    "country_name",
    F.round("evi_main_avg",3).alias("evi_avg"),
    F.round("dri_avg",3).alias("dri_avg"),
    "spark_cluster",
    "spark_cluster_label"
).orderBy("spark_cluster","country_code").show(20,False)

# %pyspark
cluster_compare=spark_cluster_labeled.select(
    "country_code",
    "country_name",
    F.col("spark_cluster"),
    F.col("spark_cluster_label")
).join(
    py_cluster.select(
        "country_code",
        F.col("cluster").alias("python_cluster"),
        F.col("cluster_label").alias("python_cluster_label")
    ),
    "country_code",
    "inner"
)

cluster_compare=cluster_compare.withColumn(
    "label_agreement",
    F.when(F.col("spark_cluster_label")==F.col("python_cluster_label"),"Same")
     .otherwise("Different")
)

cluster_compare.select(
    "country_code",
    "country_name",
    "spark_cluster",
    "spark_cluster_label",
    "python_cluster",
    "python_cluster_label",
    "label_agreement"
).orderBy("country_code").show(20,False)

cluster_compare.groupBy("label_agreement").count().show()

