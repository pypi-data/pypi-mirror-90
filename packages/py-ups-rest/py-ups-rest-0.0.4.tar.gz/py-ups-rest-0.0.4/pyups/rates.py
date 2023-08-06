import requests
import json
from pyups.typings import UPSHeader
from typing import Dict


class Rates:
    """UPS Rates API"""

    __slots__ = ["_base_url", "_header"]

    def __init__(self, base_url: str, header: UPSHeader):
        self._base_url = base_url
        self._header = header

    def get(self, data: Dict[str, any], request_option: str = "Rate") -> object:
        response: requests.Response = requests.get(
            url=f"{self._base_url}/ship/1801/rating/{request_option}?additionalinfo=timeintransit",
            headers=self._header,
            data=json.dumps(data),
        )
        return json.loads(response)
