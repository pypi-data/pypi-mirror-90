from pyups.pickup import Pickup
from pyups.tracking import Tracking
from pyups.shipping import Shipping
from pyups.rates import Rates
from pyups.typings import UPSHeader


__all__ = ["UPS"]


class UPS(object):
    """UPS Client"""

    __slots__ = ["_header", "_base_url", "_pickup", "_tracking", "_shipping", "_rates"]

    def __init__(self, header: UPSHeader, production: bool = True):
        self._header: UPSHeader = header
        self._base_url = "https://onlinetools.ups.com" if production is True else "https://wwwcie.ups.com"
        self._pickup = None
        self._tracking = None
        self._shipping = None
        self._rates = None

    @property
    def pickup(self):
        if self._pickup is None:
            self._pickup = Pickup(base_url=self._base_url, header=self._header)
        return self._pickup

    @property
    def shipping(self):
        if self._shipping is None:
            self._shipping = Shipping(base_url=self._base_url, header=self._header)
        return self._shipping

    @property
    def pickup(self):
        if self._pickup is None:
            self._pickup = Pickup(base_url=self._base_url, header=self._header)
        return self._pickup

    @property
    def tracking(self):
        if self._tracking is None:
            self._tracking = Tracking(base_url=self._base_url, header=self._header)
        return self._tracking

    @property
    def rates(self):
        if self._rates is None:
            self._rates = Rates(base_url=self._base_url, header=self._header)
        return self._rates
