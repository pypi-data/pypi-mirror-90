from pyups.pickup import Pickup
from pyups.tracking import Tracking
from pyups.shipping import Shipping
from pyups.typings import UPSHeader


__all__ = ["UPS"]


class UPS(object):
    """UPS Client"""

    __slots__ = ["_header", "_pickup", "_tracking", "_shipping"]

    def __init__(self, header: UPSHeader):
        self._header = header
        self._pickup = None
        self._tracking = None
        self._shipping = None

    @property
    def pickup(self):
        if self._pickup is None:
            self._pickup = Pickup(header=self._header)
        return self._pickup

    @property
    def shipping(self):
        if self._shipping is None:
            self._shipping = Shipping(header=self._header)
        return self._shipping

    @property
    def pickup(self):
        if self._pickup is None:
            self._pickup = Pickup(header=self._header)
        return self._pickup

    @property
    def tracking(self):
        if self._tracking is None:
            self._tracking = Tracking(header=self._header)
        return self._tracking
