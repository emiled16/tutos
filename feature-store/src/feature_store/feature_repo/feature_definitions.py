"""Feast feature views, entities, and feature services for fraud detection."""

from __future__ import annotations

from datetime import timedelta

from feast import Entity, FeatureService, FeatureView, Field
from feast.types import Float64, Int64, String, UnixTimestamp

from feature_store.feature_repo.data_sources import (
    aggregation_source,
    transaction_source,
    user_source,
)

# ---------------------------------------------------------------------------
# Entities
# ---------------------------------------------------------------------------

user_entity = Entity(
    # TODO: Implement - define the user entity
    # - name: "user"
    # - join_keys: ["user_id"]
    # - description: describe what this entity represents
    name="user",
    join_keys=["user_id"],
)

merchant_entity = Entity(
    # TODO: Implement - define the merchant entity
    # - name: "merchant"
    # - join_keys: ["merchant_id"]
    name="merchant",
    join_keys=["merchant_id"],
)

# ---------------------------------------------------------------------------
# Feature Views
# ---------------------------------------------------------------------------

transaction_features_view = FeatureView(
    # TODO: Implement - define the transaction feature view
    # - name: "transaction_features"
    # - entities: [user_entity]
    # - schema: define Fields for amount_mean, amount_std, amount_max,
    #           transaction_count, avg_time_between_transactions (all Float64)
    # - source: transaction_source
    # - ttl: timedelta(days=1)
    # - online: True
    name="transaction_features",
    entities=[user_entity],
    schema=[],
    source=transaction_source,
    ttl=timedelta(days=1),
    online=True,
)

user_features_view = FeatureView(
    # TODO: Implement - define the user feature view
    # - name: "user_features"
    # - entities: [user_entity]
    # - schema: define Fields for account_age_days (Int64),
    #           email_verified (Int64), avg_daily_spend (Float64),
    #           days_since_last_transaction (Int64), country (String)
    # - source: user_source
    # - ttl: timedelta(days=1)
    # - online: True
    name="user_features",
    entities=[user_entity],
    schema=[],
    source=user_source,
    ttl=timedelta(days=1),
    online=True,
)

aggregation_features_view = FeatureView(
    # TODO: Implement - define the aggregation feature view
    # - name: "aggregation_features"
    # - entities: [user_entity]
    # - schema: define Fields for txn_count_1h, txn_amount_sum_1h,
    #           txn_count_24h, txn_amount_sum_24h, txn_count_7d,
    #           txn_amount_sum_7d (all Float64)
    # - source: aggregation_source
    # - ttl: timedelta(hours=1)
    # - online: True
    name="aggregation_features",
    entities=[user_entity],
    schema=[],
    source=aggregation_source,
    ttl=timedelta(hours=1),
    online=True,
)

# ---------------------------------------------------------------------------
# Feature Service
# ---------------------------------------------------------------------------

fraud_detection_service = FeatureService(
    # TODO: Implement - combine all feature views into a single service
    # - name: "fraud_detection"
    # - features: [transaction_features_view, user_features_view, aggregation_features_view]
    name="fraud_detection",
    features=[],
)
