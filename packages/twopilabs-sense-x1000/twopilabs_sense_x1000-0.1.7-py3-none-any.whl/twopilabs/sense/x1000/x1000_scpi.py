from twopilabs.utils.scpi import ScpiDevice, ScpiResource
from .scpi_core import ScpiCore
from .scpi_system import ScpiSystem
from .scpi_control import ScpiControl
from .scpi_sense import ScpiSense
from .scpi_calc import ScpiCalc
from .scpi_trigger import ScpiTrigger
from .scpi_initiate import ScpiInitiate
from .x1000_base import SenseX1000Base

class SenseX1000ScpiDevice(ScpiDevice):
    def __init__(self, resource: ScpiResource, **kwargs) -> None:
        ScpiDevice.__init__(self, resource, **kwargs)
        self.core       = ScpiCore(self)
        self.system     = ScpiSystem(self)
        self.control    = ScpiControl(self)
        self.sense      = ScpiSense(self)
        self.calc       = ScpiCalc(self)
        self.trigger    = ScpiTrigger(self)
        self.initiate   = ScpiInitiate(self)

    @classmethod
    def find_devices(cls, **kwargs):
        # Set search constraints and discover SCPI resources
        kwargs.update({'usb_vid': SenseX1000Base.USB_VID})
        kwargs.update({'usb_pid': SenseX1000Base.USB_PID})
        kwargs.update({'dnssd_services': ['_scpi-raw._tcp.local.']})

        resources = ScpiResource.discover(**kwargs)

        # Filter based on resource name
        return [resource for resource in resources if resource.name.startswith('2πSENSE X1000')]
