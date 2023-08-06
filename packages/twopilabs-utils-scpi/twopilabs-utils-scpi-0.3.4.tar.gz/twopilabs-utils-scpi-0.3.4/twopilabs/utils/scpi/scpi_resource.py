from typing import NamedTuple, Any, Optional, Type, List
from .scpi_transport_base import ScpiTransports, ScpiTransportBase


class ScpiResource(NamedTuple):
    transport: Type[ScpiTransports]
    address: str
    location: Optional[str] = None
    name: Optional[str] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    serialnum: Optional[str] = None
    info: Optional[Any] = None

    @classmethod
    def discover(cls, **kwargs) -> List['ScpiResource']:
        """Find SCPI devices connected to system.

        By default lists all available possible SCPI devices. However behaviour can be controlled using
        kwargs supported by the transport classes."""

        transport_classes = ScpiTransportBase.__subclasses__()
        resources = []

        for transport_class in transport_classes:
            # filter keyword arguments accepted by transport and call transport's find_devices method
            args = {k:v for k, v in kwargs.items() if k in transport_class.discover.__code__.co_varnames}
            resources += transport_class.discover(**args)

        return resources

    @property
    def resource_name(self) -> str:
        return 'ScpiResource'

    @property
    def resource_type(self) -> str:
        return 'SCPI'

    @property
    def resource_info(self) -> str:
        return 'SCPI Resource'
