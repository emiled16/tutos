"""Data source definitions for the fraud detection feature store."""

from __future__ import annotations

from feast import FileSource

# --- Transaction Data Source ---
# Parquet file containing raw transaction records with columns:
# transaction_id, user_id, amount, merchant_id, is_fraud, timestamp

transaction_source = FileSource(
    # TODO: Implement - set the path to the transactions parquet file
    # Use a relative path like "data/transactions.parquet"
    # Set the timestamp_field to the column containing event timestamps
    # Set created_timestamp_column for the ingestion timestamp
    path="",
    timestamp_field="",
)

# --- User Profile Data Source ---
# Parquet file containing user profile data with columns:
# user_id, account_created_at, email_verified, country, timestamp

user_source = FileSource(
    # TODO: Implement - set the path to the user profiles parquet file
    # Set appropriate timestamp fields
    path="",
    timestamp_field="",
)

# --- Aggregated Transaction Data Source ---
# Parquet file containing pre-computed aggregation features with columns:
# user_id, window_start, window_end, txn_count_1h, txn_amount_sum_1h,
# txn_count_24h, txn_amount_sum_24h, txn_count_7d, txn_amount_sum_7d, timestamp

aggregation_source = FileSource(
    # TODO: Implement - set the path to the aggregations parquet file
    # Set appropriate timestamp fields
    path="",
    timestamp_field="",
)
