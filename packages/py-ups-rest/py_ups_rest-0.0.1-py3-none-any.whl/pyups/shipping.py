import json
import requests
from typing import Dict


class Shipping:
    def __init__(self, header):
        self._header = header

    def request(
        self,
        data: Dict[str, any],
        aav: str = "city",
    ) -> object:
        response: requests.Response = requests.post(
            url=f"https://onlinetools.ups.com/ship/V1801/shipments?additionaladdressvalidation={aav}",
            headers=self._header,
            data=json.dumps(data),
        )
        return json.loads(response.content)

    def label(self, data: Dict[str, any]) -> object:
        response: requests.Response = requests.post(
            url=f"https://onlinetools.ups.com/ship/V1903/shipments/labels",
            headers=self._header,
            data=json.dumps(data),
        )
        return json.loads(response.content)

    def void(self, shipment_identification_number: str) -> object:
        # todo add tracking number support
        response: requests.Response = requests.post(
            url=f"https://onlinetools.ups.com/ship/v1/shipments/cancel/{shipment_identification_number.upper()}",
            headers=self._header,
            data=json.dumps(data),
        )
        return json.loads(response.content)
