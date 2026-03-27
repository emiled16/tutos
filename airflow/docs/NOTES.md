# Apache Airflow — Theory & Notes

## Core Concepts

### DAG (Directed Acyclic Graph)

A DAG is a collection of tasks organized with dependencies that define execution order. Key properties:

- **Directed:** Tasks have a defined order (upstream → downstream)
- **Acyclic:** No circular dependencies allowed
- Every DAG has a `dag_id`, `schedule`, `start_date`, and `catchup` setting

### Tasks and Task Instances

- A **task** is a unit of work defined in a DAG (an operator instance)
- A **task instance** is a specific run of a task for a given execution date
- Task states: `queued`, `running`, `success`, `failed`, `skipped`, `up_for_retry`

### Execution Date vs Logical Date

The execution date (now called "logical date" in Airflow 2.x) represents the start of the **data interval**, not when the task actually runs. A daily DAG scheduled for `2024-01-15` runs **after** that date's data is available (i.e., runs on `2024-01-16`).

## Operators, Sensors, and Hooks

### Operators

Operators define a single unit of work. Types:

- **Action operators:** Perform an action (BashOperator, PythonOperator)
- **Transfer operators:** Move data between systems
- **Sensor operators:** Wait for a condition to be met

Custom operators inherit from `BaseOperator` and implement `execute(self, context)`.

```python
from airflow.models.baseoperator import BaseOperator

class MyOperator(BaseOperator):
    def __init__(self, my_param: str, **kwargs):
        super().__init__(**kwargs)
        self.my_param = my_param

    def execute(self, context):
        # Task logic here
        return result  # returned value is pushed to XCom
```

### Sensors

Sensors are a special type of operator that waits for an external condition:

- Inherit from `BaseSensorOperator`
- Implement `poke(self, context) -> bool` — returns True when condition is met
- Configurable `poke_interval`, `timeout`, and `mode` (poke vs reschedule)
- **Poke mode:** Holds a worker slot while waiting
- **Reschedule mode:** Frees the worker slot between pokes (preferred for long waits)

### Hooks

Hooks provide a reusable interface to external systems:

- Inherit from `BaseHook`
- Manage connections via `self.get_connection(conn_id)`
- Used by operators to interact with external services
- Examples: `HttpHook`, `S3Hook`, `PostgresHook`

## XComs (Cross-Communications)

XComs allow tasks to exchange small pieces of data:

- Pushed automatically from `execute()` return value, or manually via `xcom_push`
- Pulled via `xcom_pull(task_ids='task_id', key='key')`
- **Best practice:** Only pass small metadata (IDs, paths, counts). Never pass DataFrames or large objects.
- Stored in the Airflow metadata database (default) — not for large data

### TaskFlow API (Airflow 2.x)

```python
@task
def extract() -> dict:
    return {"data": [1, 2, 3]}

@task
def transform(data: dict) -> dict:
    return {"processed": data}

# Dependencies inferred automatically:
result = transform(extract())
```

## Scheduling

### Cron Expressions

- `@daily` = `0 0 * * *` (midnight UTC)
- `@hourly` = `0 * * * *`
- `None` = manually triggered only
- Custom: `0 6 * * 1-5` (6 AM UTC, weekdays)

### Timetables (Airflow 2.x)

For complex schedules (e.g., business days only), use custom Timetable classes instead of cron.

### Catchup and Backfilling

- **catchup=True:** Airflow creates DAG runs for all intervals since `start_date`
- **catchup=False:** Only the most recent interval is run
- **Backfilling:** `airflow dags backfill -s START -e END dag_id` to retroactively run for past dates
- Tasks **must be idempotent** for backfilling to be safe

## Executor Types

| Executor | Description | Use Case |
|---|---|---|
| **SequentialExecutor** | Single process, one task at a time | Development/testing only |
| **LocalExecutor** | Multiple processes on one machine | Small-medium workloads |
| **CeleryExecutor** | Distributed workers via Celery + broker | Large-scale production |
| **KubernetesExecutor** | Each task runs in its own K8s pod | Cloud-native, isolation |

## DAG Design Patterns

### Fan-in / Fan-out

```
extract_api ─┐
              ├──> transform ──> train_model
extract_db  ─┘
```

### Branching

Use `BranchPythonOperator` to conditionally execute different paths based on runtime logic.

### Task Groups

Group related tasks visually and logically:

```python
with TaskGroup("data_validation") as validation:
    check_schema = PythonOperator(...)
    check_nulls = PythonOperator(...)
    check_ranges = PythonOperator(...)
```

### Dynamic Task Mapping (Airflow 2.3+)

Dynamically generate parallel tasks at runtime:

```python
@task
def get_partitions() -> list[str]:
    return ["2024-01", "2024-02", "2024-03"]

@task
def process(partition: str):
    ...

process.expand(partition=get_partitions())
```

## Connection and Variable Management

- **Connections:** Store external system credentials (database URIs, API keys)
  - Configured via UI, CLI, or environment variables (`AIRFLOW_CONN_MY_CONN`)
- **Variables:** Store arbitrary key-value config
  - Access via `Variable.get("key")` or Jinja template `{{ var.value.key }}`
  - Avoid calling `Variable.get()` at module level (causes DB hit on every DAG parse)

## Best Practices for Production

1. **Idempotency:** Tasks should produce the same result when run multiple times for the same date
2. **Atomicity:** Tasks should either fully succeed or fully fail (no partial writes)
3. **Top-level code:** Minimize imports and logic at the top level of DAG files (they are parsed frequently)
4. **Small XComs:** Pass references (file paths, IDs), not data
5. **Retries:** Configure `retries` and `retry_delay` for transient failures
6. **SLAs:** Set SLA timers to alert when tasks take too long
7. **Testing:** Validate DAGs load without errors in CI/CD
8. **Monitoring:** Set up alerting on task failures and SLA misses
9. **Separation of concerns:** Keep business logic out of DAG files; call external modules

## Common Pitfalls

1. **Heavy top-level code** — Importing heavy libraries (pandas, sklearn) at the module level slows down the scheduler's DAG parsing
2. **Large XComs** — Passing DataFrames through XCom overwhelms the metadata database
3. **Not setting catchup=False** — Can trigger hundreds of backfill runs on first deployment
4. **Non-idempotent tasks** — Appending instead of upserting causes duplicates on retry
5. **Hardcoded connections** — Use Airflow Connections/Variables instead of hardcoded credentials
6. **Missing timeouts** — Tasks without `execution_timeout` can run indefinitely

## Key Terminology

- **DAG Run:** A single execution of a DAG for a specific logical date
- **Logical Date:** The start of the data interval (formerly execution_date)
- **Data Interval:** The time range of data a DAG run is responsible for
- **Upstream/Downstream:** Task dependency direction
- **Trigger Rule:** When a task should run relative to upstream status (all_success, one_failed, etc.)
- **Pool:** Limits the number of concurrent task instances (e.g., limit DB connections)
- **Priority Weight:** Determines task execution order when resources are limited
