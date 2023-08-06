from typing import Dict, Literal, Optional, TypedDict


__all__ = [
    "UPSHeader",
    "PICKUP_TYPES",
    "CANCEL_BY",
    "ADDITIONAL_ADDRESS_VALIDATION",
]


class UPSHeader(TypedDict):
    transId: str
    transactionSrc: str
    AccessLicenseNumber: str
    Username: Optional[str]
    Password: Optional[str]
    AuthenticationToken: Optional[str]
    Authorization: Optional[str]


PICKUP_TYPES = Literal["oncall", "smart", "both"]

CANCEL_BY = Literal["accountnumber", "prn"]

ADDITIONAL_ADDRESS_VALIDATION = Literal["city"]
