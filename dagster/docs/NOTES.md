# Dagster & Software-Defined Assets — Theory Notes

## Core Concepts

### Software-Defined Assets vs Task-Based Orchestration

Traditional orchestrators (Airflow) define **tasks**: units of computation arranged in a DAG. The focus is on *what runs and when*.

Dagster flips this by defining **assets**: data artifacts that exist and have dependencies. The focus is on *what data exists and how it was produced*. The execution DAG is derived from the dependency graph automatically.

| Aspect | Task-Based (Airflow) | Asset-Based (Dagster) |
|--------|---------------------|----------------------|
| Primary unit | Task (operator) | Asset (data artifact) |
| DAG represents | Execution order | Data dependencies |
| Question answered | "What runs next?" | "What data exists?" |
| Reprocessing | Re-run tasks | Re-materialize assets |
| Observability | Task logs | Data lineage + logs |
| Testing | Mock operators | Test asset functions |

### Asset Materialization

An asset is "materialized" when Dagster executes the function that produces it, and the result is persisted via an IO manager. Materialization is tracked, so you can see:
- When each asset was last computed
- What code produced it
- How long it took
- What upstream assets it depended on

### The Definitions Object

`Definitions` is Dagster's entry point — it registers all assets, resources, sensors, schedules, and jobs in one place:

```python
defs = Definitions(
    assets=[raw_data, cleaned_data, ...],
    resources={"io_manager": ParquetIOManager(), "database": DatabaseResource()},
    sensors=[new_data_sensor],
    schedules=[daily_schedule],
)
```

This is loaded by `dagster dev` to discover and serve the full pipeline.

## IO Managers

IO managers handle the *persistence* of asset outputs. They decouple asset logic from storage concerns.

### How IO Managers Work

1. Asset function returns a Python object (DataFrame, model, etc.)
2. Dagster calls `io_manager.handle_output()` to serialize and store it
3. When a downstream asset needs this data, Dagster calls `io_manager.load_input()` to deserialize and return it

### Why Custom IO Managers?

The default IO manager pickles everything to the filesystem. This works for prototyping but not production:

- **ParquetIOManager**: efficient columnar storage for DataFrames, queryable by tools like DuckDB
- **ModelIOManager**: serialize ML models with joblib/pickle, track metadata like model version

### IO Manager Contract

```python
class MyIOManager(IOManager):
    def handle_output(self, context: OutputContext, obj: Any) -> None:
        """Persist the asset output."""
        ...

    def load_input(self, context: InputContext) -> Any:
        """Load a previously persisted asset for use as input."""
        ...
```

The `context` object contains metadata: asset key, partition key, run ID, etc.

## Resources

Resources are shared, configurable objects injected into assets and IO managers. Examples:
- Database connections
- API clients
- Configuration objects

Resources enable testability: in tests, inject a mock database; in production, inject the real one.

```python
class DatabaseResource(ConfigurableResource):
    connection_string: str

    def query(self, sql: str) -> pd.DataFrame:
        ...
```

## Partitions

Partitions divide an asset's data into non-overlapping subsets, typically by time.

### Daily Partitions

```python
daily_partitions = DailyPartitionsDefinition(start_date="2024-01-01")
```

Each partition key is a date string ("2024-01-15"). When materialized:
- Only the data for that day is processed
- IO managers store/load per-partition
- Enables incremental processing instead of full recomputation

### Static Partitions

For non-time-based divisions (by region, model type, etc.):

```python
region_partitions = StaticPartitionsDefinition(["us-east", "us-west", "eu-west"])
```

### Partition-to-Partition Dependencies

When a partitioned asset depends on another partitioned asset, Dagster maps partition keys. By default, a daily asset depends on the same day's partition of its upstream asset.

## Sensors vs Schedules

### Sensors

Sensors poll for external conditions and trigger runs when conditions are met:

```python
@sensor(job=my_job)
def new_data_sensor(context):
    new_files = check_for_new_files()
    for f in new_files:
        yield RunRequest(run_key=f.name, ...)
```

- Run on a configurable interval (default: 30 seconds)
- Use `run_key` to prevent duplicate runs for the same trigger
- Can include `run_config` to parameterize the triggered run
- Use cursors to track state between evaluations

### Schedules

Schedules trigger runs at fixed intervals using cron expressions:

```python
@schedule(cron_schedule="0 6 * * *", job=my_job)
def daily_training_schedule(context):
    partition_key = context.scheduled_execution_time.strftime("%Y-%m-%d")
    return RunRequest(partition_key=partition_key)
```

### When to Use Which

- **Sensor**: event-driven — "run when new data arrives"
- **Schedule**: time-driven — "run every day at 6 AM"
- Both can be used together: schedule for regular runs, sensor for ad-hoc triggers

## Asset Groups and Code Locations

### Asset Groups

Organize related assets into groups for the UI:

```python
@asset(group_name="ingestion")
def raw_data(): ...

@asset(group_name="features")
def feature_table(): ...
```

Groups appear as sections in the Dagster UI asset graph.

### Code Locations

A code location is a Python module/package that contains Dagster definitions. In production, you might have multiple code locations (one per team or domain) loaded by a single Dagster instance.

## Dagster Type System

Dagster has an optional type system for runtime type checking:

```python
@asset
def my_asset() -> pd.DataFrame:
    ...
```

When type annotations are present, Dagster can:
- Validate that asset functions return the expected type
- Display type information in the UI
- IO managers can use type info to choose serialization strategy

## Testing Strategies

### Unit Testing Assets

Assets are just Python functions — test them directly:

```python
def test_cleaned_data():
    raw = pd.DataFrame({"a": [1, None, 3], "b": [4, 5, 6]})
    result = cleaned_data(raw)
    assert result.isna().sum().sum() == 0
```

### Testing with Dagster Utilities

```python
from dagster import materialize

def test_asset_materialization():
    result = materialize(
        [raw_data, cleaned_data],
        resources={"database": MockDatabase()},
    )
    assert result.success
```

### Testing IO Managers

```python
def test_parquet_io_manager(tmp_path):
    manager = ParquetIOManager(base_path=str(tmp_path))
    # Test handle_output writes a file
    # Test load_input reads it back correctly
```

### Testing Sensors

```python
from dagster import build_sensor_context

def test_new_data_sensor():
    context = build_sensor_context()
    result = new_data_sensor(context)
    # Assert RunRequests are generated correctly
```

## Dagster vs Airflow Comparison

| Feature | Dagster | Airflow |
|---------|---------|---------|
| Paradigm | Asset-centric | Task-centric |
| Local dev | `dagster dev` (fast) | Docker compose (heavy) |
| Testing | First-class, unit-testable | Limited, often integration-only |
| Type safety | Optional typing | No typing support |
| IO management | Built-in IO managers | Manual (XCom, limited) |
| Partitions | Native, per-asset | External (via templating) |
| Data lineage | Automatic from asset deps | Manual tracking |
| Learning curve | Moderate | Low (but grows with complexity) |

## Asset Observation

Besides materialization, assets can be **observed** — Dagster checks metadata about an asset without recomputing it:

```python
@observable_source_asset
def external_data(context):
    last_modified = check_external_system()
    return DataVersion(str(last_modified))
```

Observations are useful for external assets that Dagster doesn't produce but depends on.

## Freshness Policies

Freshness policies declare SLAs on how recently an asset should have been materialized:

```python
@asset(freshness_policy=FreshnessPolicy(maximum_lag_minutes=60))
def feature_table(): ...
```

If `feature_table` hasn't been materialized in the last 60 minutes, Dagster flags it as stale. Combined with auto-materialization policies, this can trigger automatic re-computation.

## Best Practices

1. **Think in assets, not tasks**: focus on what data you're producing, not what steps to run
2. **Use IO managers**: decouple computation from storage — your asset code shouldn't care whether it writes to S3, local disk, or a database
3. **Leverage partitions for incremental processing**: don't reprocess all history when only today's data changed
4. **Test assets as pure functions**: pass DataFrames in, assert DataFrames out
5. **Use resources for external dependencies**: database connections, API clients — inject them for testability
6. **Start with `dagster dev`**: iterate locally before deploying to production
7. **Group related assets**: use `group_name` for organizational clarity in the UI

## Common Pitfalls

- **Putting IO logic in asset functions**: assets should compute, IO managers should persist. Mixing them reduces testability.
- **Ignoring partition mapping**: when partitioned assets depend on each other, ensure partition keys align or define explicit mappings.
- **Not using `run_key` in sensors**: without a run key, sensors may trigger duplicate runs for the same event.
- **Over-partitioning**: too many partitions create management overhead. Use daily partitions for daily data, not hourly partitions for annual data.
- **Testing only in integration**: unit test asset functions as plain Python functions first — faster feedback, easier debugging.

## Key Terminology

- **Asset**: a persistent data artifact described by a function and its dependencies
- **Materialization**: the act of computing and persisting an asset
- **IO Manager**: handles serialization and deserialization of asset outputs
- **Resource**: a configurable, injectable dependency (database, API client)
- **Partition**: a subset of an asset's data (e.g., one day's worth)
- **Sensor**: polls for external conditions and triggers pipeline runs
- **Schedule**: triggers pipeline runs on a cron-like interval
- **Definitions**: the root object that registers all Dagster components
- **Code Location**: a Python package containing Dagster definitions
- **Freshness Policy**: an SLA on how recently an asset should be materialized
- **Asset Observation**: checking an asset's state without recomputing it
