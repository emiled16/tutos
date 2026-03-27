"""Tests for Feast feature definitions."""

from __future__ import annotations

from datetime import timedelta

import pytest

from feature_store.feature_repo.feature_definitions import (
    aggregation_features_view,
    fraud_detection_service,
    merchant_entity,
    transaction_features_view,
    user_entity,
    user_features_view,
)


class TestEntities:
    """Tests for entity definitions."""

    def test_user_entity_has_correct_join_key(self) -> None:
        """User entity should join on user_id."""
        # TODO: Implement
        # Assert user_entity.join_keys == ["user_id"]
        raise NotImplementedError

    def test_merchant_entity_has_correct_join_key(self) -> None:
        """Merchant entity should join on merchant_id."""
        # TODO: Implement
        raise NotImplementedError


class TestFeatureViews:
    """Tests for feature view definitions."""

    def test_transaction_view_has_required_features(self) -> None:
        """Transaction feature view should include amount stats and count."""
        # TODO: Implement
        # Get feature names from transaction_features_view.schema
        # Assert expected features are present: amount_mean, amount_std, etc.
        raise NotImplementedError

    def test_transaction_view_uses_correct_entity(self) -> None:
        """Transaction view should be keyed by user entity."""
        # TODO: Implement
        raise NotImplementedError

    def test_user_view_has_required_features(self) -> None:
        """User feature view should include account age and spending features."""
        # TODO: Implement
        raise NotImplementedError

    def test_aggregation_view_has_required_features(self) -> None:
        """Aggregation view should include rolling counts and amounts."""
        # TODO: Implement
        raise NotImplementedError

    def test_aggregation_view_ttl_is_short(self) -> None:
        """Aggregation features should have a short TTL for freshness."""
        # TODO: Implement
        # Assert aggregation_features_view.ttl <= timedelta(hours=1)
        raise NotImplementedError

    def test_all_views_are_online_enabled(self) -> None:
        """All feature views should be enabled for online serving."""
        # TODO: Implement
        raise NotImplementedError


class TestFeatureService:
    """Tests for the fraud detection feature service."""

    def test_service_includes_all_views(self) -> None:
        """Fraud detection service should combine all three feature views."""
        # TODO: Implement
        # Assert fraud_detection_service.feature_view_projections contains
        # references to all three feature views
        raise NotImplementedError

    def test_service_name_is_correct(self) -> None:
        """Feature service should be named 'fraud_detection'."""
        # TODO: Implement
        raise NotImplementedError
