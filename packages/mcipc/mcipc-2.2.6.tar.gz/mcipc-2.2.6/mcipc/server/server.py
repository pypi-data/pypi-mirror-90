"""The actual server."""

from json import dumps
from logging import getLogger
from socket import socket

from mcipc.server.datastructures import Handshake, SLPResponse
from mcipc.server.datatypes import VarInt
from mcipc.server.enumerations import State


__all__ = ['MAX_PLAYERS', 'PROTOCOL', 'VERSION', 'get_response', 'StubServer']


LOGGER = getLogger(__file__)
MAX_PLAYERS = 20
PROTOCOL = 485
VERSION = '1.16.4'


def get_response(text: str) -> bytes:
    """Returns the response text message."""

    payload = dumps({'text': text}).encode('latin-1')
    payload_length = bytes(VarInt(len(payload)))
    payload = bytes(VarInt(0)) + payload_length + payload
    payload_length = bytes(VarInt(len(payload)))
    return payload_length + payload


class StubServer:
    """A stub minecraft server."""

    def __init__(self, description: str, *, version: str = VERSION,
                 max_players: int = MAX_PLAYERS, protocol: int = PROTOCOL):
        """Description, max players and protocol information."""
        self.description = description
        self.version = version
        self.max_players = max_players
        self.protocol = protocol

    @property
    def slp_content(self) -> dict:
        """Returns the content of an SLP response."""
        return {
            'version': {
                'name': self.version,
                'protocol': self.protocol
            },
            'players': {
                'max': self.max_players,
                'online': 0
            },
            'description': {
                'text': self.description
            }
        }

    @property
    def slp_response(self) -> SLPResponse:
        """Returns an SLP response."""
        return SLPResponse(VarInt(0), self.slp_content)

    @staticmethod
    def _perform_handshake(connection: socket) -> State:
        """Handle handshake requests."""
        handshake = Handshake.from_socket(connection)
        LOGGER.debug('Got handshake: %s', handshake)
        return handshake.next_state

    def _perform_status(self, connection: socket):
        """Handles status requests."""
        packet_id = connection.recv(1)

        if packet_id == b'\x01':
            LOGGER.debug('Got packet id: %s', packet_id)
            slp_response = bytes(self.slp_response)
            LOGGER.debug('Sending SLP response: %s', slp_response)
            connection.send(slp_response)

    def _perform_login(self, connection: socket):
        """Handles the login response."""
        raise NotImplementedError()

    def _handle_login(self, connection: socket):
        """Performs a login."""
        size = VarInt.from_socket(connection)
        packet_id = VarInt.from_socket(connection)
        packet_id_length = len(bytes(packet_id))
        payload = connection.recv(size - packet_id_length)
        LOGGER.debug('Got packet ID: %s', packet_id)
        user_name = payload[2:].decode('latin-1')
        LOGGER.debug('User "%s" logged in.', user_name)
        self._perform_login(connection)

    def _process(self, connection: socket, state: State = State.HANDSHAKE):
        """Runs the connection processing."""
        LOGGER.debug('Current state: %s', state)

        if state == State.HANDSHAKE:
            state = self._perform_handshake(connection)
            self._process(connection, state=state)
        elif state == State.STATUS:
            self._perform_status(connection)
        elif state == State.LOGIN:
            self._handle_login(connection)

    def spawn(self, address: str, port: int):
        """Spawns the server on the respective socket."""
        with socket() as sock:
            sock.bind((address, port))
            sock.listen()

            while True:
                connection, address = sock.accept()

                with connection:
                    LOGGER.debug('New connection from: %s', address)
                    self._process(connection)
