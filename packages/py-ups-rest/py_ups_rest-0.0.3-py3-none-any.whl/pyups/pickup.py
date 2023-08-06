import requests
import json
from pyups.typings import PICKUP_TYPES, CANCEL_BY, UPSHeader

from typing import Dict, Optional


__all__ = ["Pickup"]


class Pickup:
    """UPS Pickup API"""

    __slots__ = ["_base_url", "_header"]

    def __init__(self, base_url: str, header: UPSHeader):
        self._base_url = base_url
        self._header = header

    def rate(self, data) -> object:
        response: requests.Response = requests.post(
            url=f"https://onlinetools.ups.com/ship/v1707/pickups/rating",
            data=json.dumps(data),
        )
        return json.loads(response.content)

    def create(self, data: Dict[str, any]) -> object:
        response: requests.Response = requests.post(
            url=f"https://onlinetools.ups.com/ship/v1707/pickups",
            headers=self._header,
            data=json.dumps(data),
        )
        return json.loads(response.content)

    def cancel(
        self,
        cancel_by: CANCEL_BY,
        prn: Optional[str],
        data: Optional[Dict[str, any]],
    ) -> object:
        if cancel_by == "prn":
            headers = self._header
            headers["prn"] = prn
            response: requests.Response = requests.post(
                url=f"https://onlinetools.ups.com/ship/v1/pickups/{cancel_by}",
                headers=headers,
            )
            return json.loads(response.content)
        else:
            response: requests.Response = requests.post(
                url=f"https://onlinetools.ups.com/ship/v1/pickups/{cancel_by}",
                headers=self._header,
                data=json.dumps(data),
            )
            return json.loads(response.content)

    def status(
        self, pickup_type: PICKUP_TYPE, data: Optional[Dict[str, any]]
    ) -> object:
        response: requests.Response = requests.get(
            url=f"https://onlinetools.ups.com/ship/v1/pickups/{pickup_type}",
            headers=self._header,
            data=json.dumps(data),
        )
        return json.loads(response.content)
