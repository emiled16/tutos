"""PredictService implementation with unary and streaming RPCs."""

from __future__ import annotations

import logging
import time
from typing import Iterator

import grpc
import numpy as np

from grpc.server.model_manager import ModelManager
from grpc.utils.serialization import ndarray_from_proto, ndarray_to_proto

logger = logging.getLogger(__name__)


class PredictServicer:
    """Implements the PredictService gRPC interface.

    Handles unary predictions, streaming predictions, model listing,
    and model reloading.
    """

    def __init__(self, model_manager: ModelManager) -> None:
        """Initialize with a model manager.

        Args:
            model_manager: Manager for loading and accessing models.
        """
        self.model_manager = model_manager

    def Predict(self, request, context: grpc.ServicerContext):
        """Handle a unary prediction request.

        Args:
            request: PredictRequest with model_name and features.
            context: gRPC servicer context for setting status codes.

        Returns:
            PredictResponse with predictions and metadata.
        """
        # TODO: Implement
        # - Extract model_name and model_version from request
        # - Get the model from model_manager
        # - If model not found, abort with NOT_FOUND status
        # - Deserialize features from NDArray proto to numpy
        # - Time the prediction
        # - Run inference: model.predict(features)
        # - Serialize predictions to NDArray proto
        # - Return PredictResponse with predictions, model info, latency
        raise NotImplementedError

    def StreamPredict(self, request, context: grpc.ServicerContext):
        """Handle a server-streaming prediction request.

        Splits the input batch into individual samples and streams
        predictions one at a time.

        Args:
            request: PredictRequest with batched features.
            context: gRPC servicer context.

        Yields:
            PredictResponse for each sample in the batch.
        """
        # TODO: Implement
        # - Deserialize the full feature batch from the request
        # - Get the model from model_manager
        # - If model not found, abort with NOT_FOUND
        # - For each sample in the batch:
        #   - Check if context is still active (not cancelled)
        #   - Run prediction on the single sample
        #   - Yield a PredictResponse
        raise NotImplementedError

    def ListModels(self, request, context: grpc.ServicerContext):
        """List all loaded models.

        Returns:
            ListModelsResponse with info about each loaded model.
        """
        # TODO: Implement
        # - Get all models from model_manager
        # - Build ModelInfo proto for each
        # - Return ListModelsResponse
        raise NotImplementedError

    def ReloadModel(self, request, context: grpc.ServicerContext):
        """Hot-reload a model.

        Args:
            request: ReloadModelRequest with model name and optional path.
            context: gRPC servicer context.

        Returns:
            ReloadModelResponse with success status and model info.
        """
        # TODO: Implement
        # - Call model_manager.reload(request.model_name, request.model_path)
        # - Return ReloadModelResponse with success/failure and model info
        # - Handle errors gracefully with INTERNAL status
        raise NotImplementedError
