import socket
import logging
from urllib.parse import urlparse
from typing import *
from .scpi_transport_base import ScpiTransportBase
from .scpi_resource import ScpiResource
from .scpi_exceptions import ScpiTransportException

logger = logging.getLogger(__name__)


class ScpiTcpIpTransport(ScpiTransportBase):
    DEFAULT_PORT: int = 5025

    transport_name = 'ScpiTcpIpTransport'
    transport_info = 'TCP/IP SCPI Transport'
    transport_type = 'TCP/IP'

    socket: socket.socket

    @classmethod
    def discover(cls,
                 dnssd_services: List[str] = ('_scpi-raw._tcp.local.',),
                 dnssd_timeout: float = 0.5) -> List[ScpiResource]:
        from zeroconf import Zeroconf, ServiceListener, ServiceBrowser
        import time

        class Listener(ServiceListener):
            def __init__(self):
                self.services = {}

            def remove_service(self, zeroconf, zc_type, zc_name):
                self.services.pop(zc_name)

            def add_service(self, zeroconf, zc_type, zc_name):
                self.services.update({zc_name: zeroconf.get_service_info(zc_type, zc_name)})

            def update_service(self, zeroconf, zc_type, zc_name):
                self.services.update({zc_name: zeroconf.get_service_info(zc_type, zc_name)})

        # Find devices via zeroconf mDNS
        # TODO: Implement DNS-SD for non-.local domains
        listener = Listener()
        ServiceBrowser(Zeroconf(), dnssd_services, listener=listener)

        # Wait for some time to get answers
        time.sleep(dnssd_timeout)

        return [ScpiResource(transport=ScpiTcpIpTransport,
                             location=f'dnssd:{service.name}',
                             address=f'{service.parsed_addresses()[0]}:{service.port}',
                             name=service.get_name(),
                             manufacturer=service.properties[b'Manufacturer'].decode(
                                 'utf-8') if b'Manufacturer' in service.properties else None,
                             model=service.properties[b'Model'].decode(
                                 'utf-8') if b'Model' in service.properties else None,
                             serialnum=service.properties[b'SerialNumber'].decode(
                                 'utf-8') if b'SerialNumber' in service.properties else None,
                             info=service
                             ) for service in listener.services.values()]

    def __init__(self, address: str, timeout: float = 5, **kwargs):
        super().__init__(**kwargs)
        self.logger = logging.getLogger(__name__)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.socket.settimeout(timeout)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        # Get hostname and port
        addr = urlparse('//' + address)
        if (addr.hostname is None):
            raise ScpiTransportException(f'{address} is not a valid hostname')

        try:
            # Try to connect
            self.socket.connect((addr.hostname,
                                 addr.port if addr.port is not None else self.DEFAULT_PORT))

            # Make a file interface for easier handling
            self.io = self.socket.makefile('rwb', buffering=0)
            self.io.flush()
        except OSError as e:
            raise ScpiTransportException(e) from e
