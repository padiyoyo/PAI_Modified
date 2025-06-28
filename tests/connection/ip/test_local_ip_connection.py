import asyncio
from unittest.mock import AsyncMock

import pytest

from paradox.connections.ip.commands import IPModuleConnectCommand
from paradox.connections.ip.connection import LocalIPConnection
from paradox.connections.protocols import ConnectionProtocol


@pytest.mark.asyncio
async def test_connect(mocker):
    connection = LocalIPConnection(host="localhost", port=1000, password="test")

    protocol = mocker.Mock(spec=ConnectionProtocol)
    protocol.is_active.return_value = True

    create_connection_mock = AsyncMock(return_value=(None, protocol))
    mocker.patch.object(
        asyncio.get_event_loop(), "create_connection", create_connection_mock
    )
    connect_command_execute = mocker.patch.object(
        IPModuleConnectCommand, "execute", AsyncMock()
    )

    assert connection.connected is False

    await connection.connect()

    create_connection_mock.assert_called_once()
    connect_command_execute.assert_called_once()

    assert connection.connected is True
