import json
import requests
from pyups.typings import UPSHeader
from typing import Dict


class Shipping:
    """UPS Shipping API"""

    __slots__ = ["_base_url", "_header"]

    def __init__(self, base_url: str, header: UPSHeader):
        self._base_url = base_url
        self._header = header

    def request(
        self,
        data: Dict[str, any],
        aav: str = "city",
    ) -> object:
        response: requests.Response = requests.post(
            url=f"{self._base_url}/ship/V1801/shipments?additionaladdressvalidation={aav}",
            headers=self._header,
            data=json.dumps(data),
        )
        return json.loads(response.content)

    def label(self, data: Dict[str, any]) -> object:
        response: requests.Response = requests.post(
            url=f"{self._base_url}/ship/V1903/shipments/labels",
            headers=self._header,
            data=json.dumps(data),
        )
        return json.loads(response.content)

    def void(self, shipment_identification_number: str) -> object:
        # todo add tracking number support
        response: requests.Response = requests.post(
            url=f"{self._base_url}/ship/v1/shipments/cancel/{shipment_identification_number.upper()}",
            headers=self._header,
            data=json.dumps(data),
        )
        return json.loads(response.content)
