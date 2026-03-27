"""WebSocket server for real-time anomaly detection streaming."""

from __future__ import annotations

import asyncio
import logging
import signal
import uuid
from typing import Any

import websockets
from websockets.server import WebSocketServerProtocol

from socket_project.alerting.alert_manager import AlertManager
from socket_project.alerting.notifier import Notifier, WebSocketSink
from socket_project.detection.detector import AnomalyDetector
from socket_project.models.messages import WSMessage
from socket_project.server.connection_manager import ConnectionManager
from socket_project.server.handlers import MessageHandler
from socket_project.streaming.data_producer import DataProducer
from socket_project.streaming.stream_processor import StreamProcessor

logger = logging.getLogger(__name__)


class AnomalyDetectionServer:
    """WebSocket server that streams anomaly detection results to clients.

    Orchestrates the full pipeline: data production → stream processing →
    anomaly detection → alert management → client notification.
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 8765,
        detectors: list[AnomalyDetector] | None = None,
    ) -> None:
        self.host = host
        self.port = port
        self.connection_manager = ConnectionManager()
        self.handler = MessageHandler(self.connection_manager)
        self.producer = DataProducer()
        self.processor = StreamProcessor()
        self.alert_manager = AlertManager()
        self.detectors: list[AnomalyDetector] = detectors or []

        ws_sink = WebSocketSink(broadcast_fn=self.connection_manager.broadcast)
        self.notifier = Notifier(sinks=[ws_sink])
        self._server: Any = None

    async def _client_handler(self, websocket: WebSocketServerProtocol) -> None:
        """Handle a single client connection lifecycle.

        Registers the client, processes incoming messages, and ensures
        cleanup on disconnect.
        """
        client_id = str(uuid.uuid4())
        # TODO: Implement the connection lifecycle:
        #   1. Register the client via connection_manager.connect
        #   2. Send a welcome ack message
        #   3. Enter a receive loop: async for message in websocket
        #   4. Pass each message to self.handler.handle
        #   5. Send the response back to the client
        #   6. On ConnectionClosed / Exception, disconnect and log
        raise NotImplementedError

    async def _detection_pipeline(self) -> None:
        """Run the data production → detection → alerting pipeline.

        Continuously produces data, processes it through detectors,
        and dispatches alerts for anomalous points.
        """
        # TODO: Implement:
        #   1. Iterate over self.producer.stream()
        #   2. For each point, run it through self.processor.process()
        #   3. If stats are available, run each detector
        #   4. For anomalous scores, run through alert_manager.process()
        #   5. If an alert is produced, broadcast via self.notifier.notify()
        #   6. Also broadcast the raw data point to subscribed clients
        raise NotImplementedError

    async def start(self) -> None:
        """Start the WebSocket server and the detection pipeline."""
        # TODO: Implement:
        #   1. Start the websockets.serve server on self.host:self.port
        #   2. Launch _detection_pipeline as a concurrent task
        #   3. Set up signal handlers for graceful shutdown
        #   4. Log startup info
        #   5. Await until shutdown is triggered
        raise NotImplementedError

    async def stop(self) -> None:
        """Gracefully shut down the server and pipeline."""
        logger.info("Shutting down server...")
        self.producer.stop()
        if self._server is not None:
            self._server.close()
            await self._server.wait_closed()
        logger.info("Server stopped.")


async def main() -> None:
    """Entry point for running the server directly."""
    logging.basicConfig(level=logging.INFO)
    server = AnomalyDetectionServer()
    await server.start()


if __name__ == "__main__":
    asyncio.run(main())
