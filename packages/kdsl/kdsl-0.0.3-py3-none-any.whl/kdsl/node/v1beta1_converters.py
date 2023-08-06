from __future__ import annotations
from typing import Literal, Union
from kdsl.bases import OmitEnum, OMIT
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import kdsl.node.v1beta1


def optional_converter_Overhead(
    value: Union[kdsl.node.v1beta1.OverheadUnion, OmitEnum, None]
) -> Union[kdsl.node.v1beta1.Overhead, OmitEnum, None]:
    import kdsl.node.v1beta1

    return kdsl.node.v1beta1.Overhead(**value) if isinstance(value, dict) else value


def required_converter_Overhead(
    value: kdsl.node.v1beta1.OverheadUnion,
) -> kdsl.node.v1beta1.Overhead:
    import kdsl.node.v1beta1

    return kdsl.node.v1beta1.Overhead(**value) if isinstance(value, dict) else value


def optional_converter_Scheduling(
    value: Union[kdsl.node.v1beta1.SchedulingUnion, OmitEnum, None]
) -> Union[kdsl.node.v1beta1.Scheduling, OmitEnum, None]:
    import kdsl.node.v1beta1

    return kdsl.node.v1beta1.Scheduling(**value) if isinstance(value, dict) else value


def required_converter_Scheduling(
    value: kdsl.node.v1beta1.SchedulingUnion,
) -> kdsl.node.v1beta1.Scheduling:
    import kdsl.node.v1beta1

    return kdsl.node.v1beta1.Scheduling(**value) if isinstance(value, dict) else value
