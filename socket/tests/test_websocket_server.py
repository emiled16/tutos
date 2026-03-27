"""Tests for the WebSocket server and connection management."""

from __future__ import annotations

import asyncio
import json
from unittest.mock import AsyncMock, MagicMock

import pytest

from socket_project.models.messages import CommandType, MessageType, WSMessage
from socket_project.server.connection_manager import ConnectionManager
from socket_project.server.handlers import MessageHandler


class TestConnectionManager:
    """Tests for ConnectionManager client tracking and room management."""

    @pytest.fixture
    def manager(self) -> ConnectionManager:
        return ConnectionManager()

    @pytest.fixture
    def mock_websocket(self) -> AsyncMock:
        ws = AsyncMock()
        ws.send = AsyncMock()
        ws.close = AsyncMock()
        return ws

    async def test_connect_registers_client(
        self,
        manager: ConnectionManager,
        mock_websocket: AsyncMock,
    ) -> None:
        # TODO: Implement — call manager.connect with the mock websocket,
        # assert client_count == 1, assert the client_id is tracked.
        pass

    async def test_disconnect_removes_client(
        self,
        manager: ConnectionManager,
        mock_websocket: AsyncMock,
    ) -> None:
        # TODO: Implement — connect then disconnect a client,
        # assert client_count == 0.
        pass

    async def test_subscribe_adds_to_room(
        self,
        manager: ConnectionManager,
        mock_websocket: AsyncMock,
    ) -> None:
        # TODO: Implement — connect a client, subscribe to "cpu_usage",
        # assert the subscription is in get_subscriptions.
        pass

    async def test_unsubscribe_removes_from_room(
        self,
        manager: ConnectionManager,
        mock_websocket: AsyncMock,
    ) -> None:
        # TODO: Implement — subscribe then unsubscribe, assert the
        # metric is no longer in subscriptions.
        pass

    async def test_broadcast_sends_to_all(
        self,
        manager: ConnectionManager,
    ) -> None:
        # TODO: Implement — connect multiple mock clients, broadcast
        # a message, assert all received it.
        pass

    async def test_broadcast_to_room_sends_only_to_subscribers(
        self,
        manager: ConnectionManager,
    ) -> None:
        # TODO: Implement — connect two clients, subscribe only one
        # to "cpu_usage", broadcast to that room, assert only the
        # subscriber received the message.
        pass

    async def test_disconnect_cleans_up_rooms(
        self,
        manager: ConnectionManager,
        mock_websocket: AsyncMock,
    ) -> None:
        # TODO: Implement — connect and subscribe a client, then
        # disconnect. Assert the room no longer contains the client_id.
        pass


class TestMessageHandler:
    """Tests for the message handler routing logic."""

    @pytest.fixture
    def handler(self) -> MessageHandler:
        manager = ConnectionManager()
        return MessageHandler(manager)

    async def test_handle_subscribe_command(self, handler: MessageHandler) -> None:
        # TODO: Implement — send a subscribe command JSON, assert the
        # response is an ack and the subscription was registered.
        pass

    async def test_handle_invalid_json_returns_error(self, handler: MessageHandler) -> None:
        # TODO: Implement — send malformed JSON, assert the response
        # is an error WSMessage.
        pass

    async def test_handle_heartbeat_returns_pong(self, handler: MessageHandler) -> None:
        # TODO: Implement — send a heartbeat command, assert the
        # response contains "pong".
        pass
