# PySpark Feature Engineering — Theory & Notes

## 1. Spark Architecture

### Components
- **Driver** — the process running your `main()` function. Creates the SparkSession, builds the execution plan, and coordinates executors.
- **Executors** — JVM processes on worker nodes that execute tasks and store cached data.
- **Tasks** — the smallest unit of work, one task per partition per stage.
- **Cluster Manager** — allocates resources (YARN, Kubernetes, Mesos, or Standalone).

### Execution Flow
```
User Code → Logical Plan → Optimized Plan (Catalyst) → Physical Plan → Tasks → Executors
```

The Catalyst optimizer rewrites your transformations before execution. This is why you should prefer Spark-native functions over Python UDFs — Catalyst can optimize the former but not the latter.

## 2. Lazy Evaluation and DAG Execution

Spark builds a **Directed Acyclic Graph** of transformations but doesn't execute anything until an **action** is triggered.

### Why Lazy?
- Catalyst can optimize the entire pipeline holistically
- Operations can be fused (e.g., filter before join rather than after)
- Only computes what's actually needed

### Key Implication
Calling `df.filter(...)` returns instantly — it just adds a node to the DAG. The computation happens when you call `.show()`, `.collect()`, `.write()`, or `.count()`.

## 3. Transformations vs Actions

| Transformations (lazy) | Actions (trigger execution) |
|------------------------|-----------------------------|
| `select`, `filter`, `groupBy` | `show`, `collect`, `count` |
| `join`, `withColumn`, `drop` | `write`, `save`, `take` |
| `orderBy`, `distinct` | `first`, `foreach` |

**Rule of thumb:** If it returns a DataFrame, it's a transformation. If it returns a value or writes data, it's an action.

## 4. Shuffle Operations and Their Cost

A **shuffle** occurs when data must be redistributed across partitions — the most expensive Spark operation.

### Operations That Cause Shuffles
- `groupBy().agg()` — data with the same key must land on the same partition
- `join()` — both sides need matching keys on the same partition
- `repartition()` — explicit data redistribution
- `distinct()` — needs to compare all records
- `orderBy()` — global sorting requires data movement

### Minimizing Shuffle Cost
- Use broadcast joins for small tables (< 10MB default)
- Pre-partition data by join/group keys
- Use `coalesce()` instead of `repartition()` when reducing partitions
- Avoid unnecessary `orderBy()` in intermediate steps

## 5. Partitioning Strategies

### Hash Partitioning
Default. Applies hash function to partition key(s). Good for joins and groupBy on the same columns.

```python
df.repartition(200, "user_id")  # 200 partitions by user_id hash
```

### Range Partitioning
Divides data into ranges. Good for ordered data and range queries.

```python
df.repartitionByRange(200, "timestamp")
```

### Write-Time Partitioning
Organizes output files on disk by column values:

```python
df.write.partitionBy("year", "month").parquet("output/")
```

**Choose partition columns wisely:** High cardinality (user_id) = too many small files. Low cardinality (year/month) = good partition sizes.

## 6. Broadcast Joins vs Sort-Merge Joins

### Sort-Merge Join (Default)
Both sides shuffled by join key, sorted, then merged. Expensive but works for any size.

### Broadcast Join
Small table copied to every executor. No shuffle needed for the small side.

```python
from pyspark.sql.functions import broadcast

result = large_df.join(broadcast(small_df), "key")
```

**When to use broadcast:**
- One side is small (< `spark.sql.autoBroadcastJoinThreshold`, default 10MB)
- Can force with `broadcast()` hint
- Dramatically reduces shuffle for fact-dimension joins

## 7. Window Functions

Window functions compute values across a "window" of rows related to the current row.

### Components
```python
from pyspark.sql.window import Window

window_spec = Window.partitionBy("user_id").orderBy("timestamp")
```

### Row-Based Windows
```python
Window.partitionBy("user_id").orderBy("timestamp").rowsBetween(-2, 0)
# Current row and 2 preceding rows
```

### Range-Based Windows
```python
Window.partitionBy("user_id").orderBy("timestamp").rangeBetween(-86400, 0)
# All rows within 86400 seconds (1 day) before current row
```

### Common Window Functions
| Function | Use Case |
|----------|----------|
| `row_number()` | Assign sequential numbers per partition |
| `rank()` | Rank with gaps for ties |
| `dense_rank()` | Rank without gaps |
| `lag(col, n)` | Value n rows before |
| `lead(col, n)` | Value n rows after |
| `sum().over(w)` | Running/rolling sum |
| `avg().over(w)` | Rolling average |

## 8. UDF Performance

### Python UDFs (Avoid)
```python
@udf(returnType=DoubleType())
def my_udf(x):
    return x * 2.0
```
- Data serialized from JVM to Python and back
- Breaks Catalyst optimization
- 10-100x slower than native functions

### Pandas UDFs (Better)
```python
@pandas_udf(DoubleType())
def my_pandas_udf(s: pd.Series) -> pd.Series:
    return s * 2.0
```
- Uses Apache Arrow for efficient serialization
- Operates on batches (vectorized), not row by row
- 3-10x faster than Python UDFs

### Native Functions (Best)
```python
from pyspark.sql import functions as F
df.withColumn("doubled", F.col("x") * 2.0)
```
- Runs entirely in the JVM
- Catalyst can optimize
- Always prefer when possible

## 9. Caching and Persistence

### When to Cache
- DataFrame used multiple times in the same job
- After an expensive transformation (large join, complex aggregation)

### When NOT to Cache
- DataFrame used only once
- Data doesn't fit in memory (spills to disk, slower than recomputing)
- Near the start of a pipeline (blocks memory early)

### Persistence Levels
| Level | Storage | Serialized? | Use Case |
|-------|---------|-------------|----------|
| `MEMORY_ONLY` | RAM | No | Default, fastest |
| `MEMORY_AND_DISK` | RAM + spillover | No | Large datasets |
| `DISK_ONLY` | Disk | Yes | Very large datasets |
| `MEMORY_ONLY_SER` | RAM | Yes | Memory-constrained |

```python
df.cache()  # same as persist(StorageLevel.MEMORY_AND_DISK)
df.unpersist()  # release cached data
```

## 10. Delta Lake

### What It Adds to Parquet
- **ACID transactions** — concurrent reads/writes are safe
- **Time travel** — query historical versions of data
- **Schema enforcement** — rejects writes that don't match schema
- **Schema evolution** — can add/merge new columns
- **Z-Ordering** — optimizes file layout for specific query patterns

### Time Travel
```python
# Read a specific version
df = spark.read.format("delta").option("versionAsOf", 5).load("path")

# Read as of a timestamp
df = spark.read.format("delta").option("timestampAsOf", "2024-01-01").load("path")
```

### Z-Ordering
Colocates related data in the same files for faster filtering:
```python
from delta.tables import DeltaTable
dt = DeltaTable.forPath(spark, "path")
dt.optimize().executeZOrderBy("user_id", "timestamp")
```

## 11. Spark UI for Debugging

### Key Tabs
- **Jobs** — see which actions triggered which jobs
- **Stages** — see shuffle reads/writes, task distribution
- **Storage** — see what's cached and memory usage
- **SQL** — see logical and physical query plans

### What to Look For
- **Skewed tasks** — one task taking 100x longer than others → data skew
- **Large shuffles** — high shuffle read/write bytes → consider broadcast joins
- **Spill to disk** — not enough memory, consider increasing executor memory

## 12. Common Performance Anti-Patterns

### `collect()` on Large Data
```python
all_data = df.collect()  # DON'T — pulls entire dataset to driver
```

### Too Many Small Files
Writing with high-cardinality `partitionBy` creates millions of tiny files. Use `coalesce()` before writing or run `OPTIMIZE` on Delta tables.

### Data Skew
When one key has disproportionately many rows, tasks become unbalanced. Mitigations:
- Salting: add random prefix to skewed key
- Broadcast join the smaller side
- Adaptive Query Execution (AQE) in Spark 3.x

### Python UDFs in Hot Paths
Replace with Spark-native functions or Pandas UDFs wherever possible.

### Caching Everything
More caching ≠ better performance. Each cache consumes executor memory that could be used for computation.

## Key Terminology

| Term | Definition |
|------|-----------|
| **Partition** | A chunk of data processed by a single task |
| **Shuffle** | Redistribution of data across partitions (expensive) |
| **Stage** | A group of tasks separated by shuffle boundaries |
| **Catalyst** | Spark's query optimizer |
| **Tungsten** | Spark's memory management and code generation engine |
| **AQE** | Adaptive Query Execution — runtime optimization in Spark 3.x |
| **Delta Lake** | Storage layer adding ACID, versioning, and optimization to Parquet |
| **Broadcast** | Sending a small dataset to all executors to avoid shuffle |
