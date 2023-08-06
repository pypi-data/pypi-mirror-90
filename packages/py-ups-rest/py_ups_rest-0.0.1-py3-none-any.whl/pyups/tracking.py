import json
import requests


__all__ = ["Tracking"]


class Tracking:
    """UPS tracking API"""

    __slots__ = ["header"]

    def __init__(self, header):
        self.header = header

    def get(self, inquiry_number: str) -> object:
        response: requests.Response = requests.get(
            url=f"https://onlinetools.ups.com/track/v1/details/{inquiry_number}",
            headers=self.header,
        )
        return json.loads(response.content)
