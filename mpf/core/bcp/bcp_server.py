"""Bcp server for clients which connect and disconnect randomly."""
import asyncio
import logging

from mpf.core.utility_functions import Util


class BcpServer():

    """Server socket which listens for incoming BCP clients."""

    def __init__(self, machine, ip, port, type):
        """Initialise BCP server."""
        self.machine = machine
        self.log = logging.getLogger('BCPServer')
        self._server = None
        self._ip = ip
        self._port = port
        self._type = type

    @asyncio.coroutine
    def start(self):
        """Start the server."""
        self._server = yield from self.machine.clock.start_server(
            self._accept_client, self._ip, self._port, loop=self.machine.clock.loop)

    def stop(self):
        """Stop the BCP server, i.e. closes the listening socket(s)."""
        if self._server:
            self._server.close()

        self._server = None

    @asyncio.coroutine
    def _accept_client(self, client_reader, client_writer):
        """Accept an connection and create client."""
        self.log.info("New client connected.")
        client = Util.string_to_class(self._type)(self.machine, None, self.machine.bcp)
        client.accept_connection(client_reader, client_writer)
        client.exit_on_close = False
        self.machine.bcp.transport.register_transport(client)