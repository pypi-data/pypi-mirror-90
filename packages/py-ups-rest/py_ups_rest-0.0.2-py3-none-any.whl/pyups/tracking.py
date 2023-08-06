import json
import requests
from pyups.typings import UPSHeader

__all__ = ["Tracking"]


class Tracking:
    """UPS tracking API"""

    __slots__ = ["_header", "_base_url"]

    def __init__(self, base_url: str, header: UPSHeader):
        self._base_url = base_url
        self._header = header

    def get(self, inquiry_number: str) -> object:
        response: requests.Response = requests.get(
            url=f"{self._base_url}/track/v1/details/{inquiry_number}",
            headers=self._header,
        )
        return json.loads(response.content)
