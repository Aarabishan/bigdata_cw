## 📌 Task 1 — Graph In-Degree Distribution with Hadoop (Streaming) & Spark

### 📖 Overview

This task computes in-degree per node and the in-degree distribution for several public graph datasets, using two engines:
  - Hadoop Streaming (MapReduce) with Python mappers/reducers
  - Apache Spark (PySpark) in a Jupyter Notebook

Both approaches generate comparable outputs and simple plots for analysis.

### 📂 What’s in this folder

docker-hadoop/

  - mapper_indegree.py — Stage 1 mapper (edge → (dst, 1))
  - reducer_indegree.py — Stage 1 reducer (sum counts → (dst, in_deg))
  - mapper_degree_dist.py — Stage 2 mapper ((in_deg, 1))
  - reducer_degree_dist.py — Stage 2 reducer (sum → (in_deg, n_nodes))
  - Notebook for hadoop indegree analysis

spark-work/

  - Spark_Indegree_Analysis.ipynb — PySpark notebook to load data, compute in-degree & distribution, plot, and capture basic metrics

### 📁 Datasets

  - Email-EuAll — email communication network
  - web-BerkStan — Web graph (Berkely/Stanford)
  - cit-Patents — Patent citation network
  - soc-LiveJournal1 — Social network (for scalability tests)

### 🛠️ Technologies Used

  - Hadoop (Dockerized, YARN + HDFS)
  - Spark (Dockerized, PySpark via Jupyter)
  - Python MapReduce (Hadoop Streaming)
  - HDFS (data storage for Hadoop jobs)
  - Docker & Docker Compose (orchestration)
  - Jupyter Notebook (plots, Spark code, metrics)

> 🔴 Note: Java is present in the images but Python is used for Hadoop Streaming and PySpark is used for Spark.

### 🔁 Workflow Summary

### 🐘 Hadoop (Streaming)

1. Cluster setup (Docker Compose).
A multi-container Hadoop stack (NameNode, DataNode, ResourceManager, NodeManager, HistoryServer) is launched. Volumes are mounted so code/results persist on the host.

2. Dataset ingestion to HDFS.
Raw text edge lists (e.g., src<tab>dst) are uploaded to HDFS under /input/<dataset> using hdfs dfs -put. This ensures parallel, distributed reads during MapReduce.

3. Python mappers/reducers (no Java).

    - Stage 1 — In-degree per node:
      mapper_indegree.py emits (dst, 1) per edge; reducer_indegree.py sums to (dst, in_deg).

    - Stage 2 — In-degree distribution:
      mapper_degree_dist.py emits (in_deg, 1); reducer_degree_dist.py aggregates to (in_deg, n_nodes).

4. Run MapReduce jobs on YARN.
Each stage is submitted with hadoop-streaming.jar, bundling the Python scripts via -file. Outputs are written to HDFS under /output/<dataset>_*. Jobs log counters and timings in YARN/HistoryServer.

5. Collect & visualize results.
Final part files are copied from HDFS to the mounted results/ folder. A Jupyter notebook loads these text outputs to produce log-log plots and simple tables for analysis. (Optionally, job logs/metrics are saved alongside for reporting.)

### ⚡ Spark (PySpark) 

1. Notebook environment (Docker).
A single jupyter/pyspark-notebook container is started with a bind mount to spark-work/. JupyterLab runs on localhost:8888 and the Spark UI on :4040.

2. Load datasets from the host mount.
PySpark reads the tab-separated edge lists from /home/jovyan/work/data/*.txt[.gz], skipping comment lines. Data are parsed into a DataFrame with columns src, dst.

3. In-degree & distribution in PySpark.

    - In-degree: df.groupBy("dst").count() → (dst, in_deg)

    - Distribution: groupBy("in_deg").count() → (in_deg, n_nodes)
      Results are collected to Pandas for quick inspection and plotting.

4. Plot & basic metrics.
The notebook renders log-log plots of (in_deg, n_nodes). In local single-container mode, Spark REST metrics for CPU/IO/shuffle may be sparse (often 0), so wall-clock execution time is captured for consistent comparisons. (Optional) a cached variant (.cache() then reuse) is run to demonstrate iterative speed-ups.

5. Persist outputs for comparison.
Summary rows (dataset, wall time, and available counters) are appended to spark_metrics.csv. These are later joined with Hadoop results in the report’s comparison section.

### ℹ️ Notes on Stages & Comparability

- Hadoop runs two explicit stages (two MapReduce jobs) to move from edges → in-degree → distribution.
- Spark computes both steps within one pipeline (two groupBy aggregations), with an optional cached reuse for iterative queries.
- For fair comparison, the analysis uses:

    - Correctness: Same final (in_deg, n_nodes) tables/plots across systems.
    - Performance: Hadoop per-stage times + Spark wall time (and any available counters).
    - Design: Batch (Hadoop) vs in-memory iterative analytics (Spark).

### ⚠️ Notes
- Full Hadoop Docker images are not included due to storage constraints
- Only configuration changes and custom code are provided

## 🎓 Academic
