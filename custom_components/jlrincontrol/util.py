"""Utility functions"""

import logging
from typing import Any

from homeassistant.const import TEMP_CELSIUS
from homeassistant.util import dt


_LOGGER = logging.getLogger(__name__)


def field_mask(str_value, from_start=0, from_end=0):
    """Redact sensitive field data"""
    str_mask = "x" * (len(str_value) - from_start - from_end)
    return f"{str_value[:from_start]}{str_mask}{str_value[-from_end:]}"


def requires_pin(service_type, service_code):
    """Does service require pin"""
    if "pin" in service_type[service_code].get("params", {}):
        return True
    return False


def get_value_match(data: dict, key: str, value: str) -> bool:
    """Get if attribute matches value"""
    return True if data.get(key) == value else False


def get_is_date_active(data: dict, key: str) -> bool:
    """Get if attribute as datetime before now"""
    try:
        attr_dt = dt.as_utc(dt.parse_datetime(data.get(key)))
        if attr_dt < dt.utcnow():
            return False
        return True
    except (ValueError, TypeError):
        return False


def convert_temp_value(temp_unit, service_code, target_value):
    """
    Convert from C/F to value between 31-57 (31 is LO 57 is HOT)
    needed for service call
    """

    # Handle setting car units (prior to version 2.0)
    if target_value >= 31 and target_value <= 57:
        return target_value

    # Engine start/set rcc value
    if service_code == "REON":
        # Get temp units
        if temp_unit == TEMP_CELSIUS:
            # Convert from C
            return min(57, max(31, int(target_value * 2)))
        else:
            # Convert from F
            return min(57, max(31, target_value - 27))

    # Climate preconditioning
    if service_code == "ECC":
        if temp_unit == TEMP_CELSIUS:
            return min(285, max(155, int(target_value * 10)))
        else:
            # Convert from F
            return min(285, max(155, int(((target_value - 27) / 2) * 10)))


def to_local_datetime(datetime: str):
    """Convert to local time"""
    try:
        return dt.as_local(dt.parse_datetime(datetime))
    except (ValueError, TypeError):
        return None


def get_attribute(obj, path: str) -> Any | None:
    """Get attribute from dotted notation"""
    attrs = path.split(".")
    temp = obj
    for attr in attrs:
        if hasattr(temp, attr):
            temp = getattr(temp, attr)
        else:
            return None
    return temp
