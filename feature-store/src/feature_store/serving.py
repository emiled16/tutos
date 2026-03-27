"""FastAPI endpoint for online feature serving and fraud prediction."""

from __future__ import annotations

from typing import Any

import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from feature_store.materialization import get_feature_store

app = FastAPI(title="Fraud Detection Feature Server")


class PredictionRequest(BaseModel):
    """Request body for fraud prediction."""

    user_id: str
    transaction_amount: float = Field(gt=0)
    merchant_id: str = ""


class PredictionResponse(BaseModel):
    """Response body with prediction and feature values."""

    user_id: str
    fraud_probability: float
    is_fraud: bool
    features: dict[str, Any]


class FeatureResponse(BaseModel):
    """Response body with raw feature values."""

    user_id: str
    features: dict[str, Any]


def get_online_features(user_id: str) -> dict[str, Any]:
    """Retrieve online features for a user from the feature store.

    Args:
        user_id: The user entity key.

    Returns:
        Dictionary mapping feature names to their values.

    Raises:
        HTTPException: If feature retrieval fails.
    """
    # TODO: Implement
    # - Get the FeatureStore instance
    # - Call store.get_online_features with the fraud_detection feature service
    #   and entity rows [{"user_id": user_id}]
    # - Convert the result to a dict
    # - Raise HTTPException(404) if user has no features
    raise NotImplementedError


def predict_fraud(features: dict[str, Any], amount: float) -> float:
    """Run fraud prediction using retrieved features and transaction amount.

    Args:
        features: Feature dictionary from the online store.
        amount: Current transaction amount.

    Returns:
        Fraud probability between 0 and 1.
    """
    # TODO: Implement
    # - Build a feature vector from the features dict + amount
    # - Apply a simple heuristic or load a trained sklearn model
    # - For the scaffold, implement a rule-based heuristic:
    #   - High amount relative to user's average → higher risk
    #   - High transaction velocity → higher risk
    #   - New account → higher risk
    # - Return a probability [0, 1]
    raise NotImplementedError


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/features/{user_id}", response_model=FeatureResponse)
async def get_features(user_id: str) -> FeatureResponse:
    """Retrieve feature values for a user.

    Args:
        user_id: The user to look up.
    """
    # TODO: Implement
    # - Call get_online_features(user_id)
    # - Return FeatureResponse with the features
    raise NotImplementedError


@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest) -> PredictionResponse:
    """Predict fraud probability for a transaction.

    Args:
        request: Prediction request with user_id and transaction_amount.
    """
    # TODO: Implement
    # - Retrieve online features for the user
    # - Call predict_fraud with features and transaction amount
    # - Return PredictionResponse with probability and is_fraud flag
    #   (is_fraud = probability > 0.5)
    raise NotImplementedError
