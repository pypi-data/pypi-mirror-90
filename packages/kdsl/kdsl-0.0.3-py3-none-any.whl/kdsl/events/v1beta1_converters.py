from __future__ import annotations
from typing import Literal, Union
from kdsl.bases import OmitEnum, OMIT
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import kdsl.events.v1beta1


def optional_converter_EventSeries(
    value: Union[kdsl.events.v1beta1.EventSeriesUnion, OmitEnum, None]
) -> Union[kdsl.events.v1beta1.EventSeries, OmitEnum, None]:
    import kdsl.events.v1beta1

    return (
        kdsl.events.v1beta1.EventSeries(**value) if isinstance(value, dict) else value
    )


def required_converter_EventSeries(
    value: kdsl.events.v1beta1.EventSeriesUnion,
) -> kdsl.events.v1beta1.EventSeries:
    import kdsl.events.v1beta1

    return (
        kdsl.events.v1beta1.EventSeries(**value) if isinstance(value, dict) else value
    )
