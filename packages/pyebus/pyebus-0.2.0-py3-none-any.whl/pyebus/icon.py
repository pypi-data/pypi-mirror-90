"""MDI Icon Utility."""
from . import types


def get_icon(fielddef):
    """Get Default Icon for `fielddef`."""
    msgdef = fielddef.msgdef
    type_ = fielddef.type_
    if msgdef.read or msgdef.update:
        if fielddef.unit in ("°C", "K", "°F"):
            return "mdi:thermometer"
        elif isinstance(type_, (types.TimeType, types.DateType, types.DateTimeType, types.HourMinuteType)):
            return "mdi:timer"
        elif isinstance(type_, types.EnumType):
            if tuple(sorted(type_.values)) in [("off", "on"), ("no", "yes")]:
                return "mdi:toggle-switch"
    return None
