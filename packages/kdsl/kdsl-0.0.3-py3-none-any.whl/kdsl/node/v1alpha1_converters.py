from __future__ import annotations
from typing import Literal, Union
from kdsl.bases import OmitEnum, OMIT
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import kdsl.node.v1alpha1


def optional_converter_Overhead(
    value: Union[kdsl.node.v1alpha1.OverheadUnion, OmitEnum, None]
) -> Union[kdsl.node.v1alpha1.Overhead, OmitEnum, None]:
    import kdsl.node.v1alpha1

    return kdsl.node.v1alpha1.Overhead(**value) if isinstance(value, dict) else value


def required_converter_RuntimeClassSpec(
    value: kdsl.node.v1alpha1.RuntimeClassSpecUnion,
) -> kdsl.node.v1alpha1.RuntimeClassSpec:
    import kdsl.node.v1alpha1

    return (
        kdsl.node.v1alpha1.RuntimeClassSpec(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_Scheduling(
    value: kdsl.node.v1alpha1.SchedulingUnion,
) -> kdsl.node.v1alpha1.Scheduling:
    import kdsl.node.v1alpha1

    return kdsl.node.v1alpha1.Scheduling(**value) if isinstance(value, dict) else value


def optional_converter_Scheduling(
    value: Union[kdsl.node.v1alpha1.SchedulingUnion, OmitEnum, None]
) -> Union[kdsl.node.v1alpha1.Scheduling, OmitEnum, None]:
    import kdsl.node.v1alpha1

    return kdsl.node.v1alpha1.Scheduling(**value) if isinstance(value, dict) else value


def optional_converter_RuntimeClassSpec(
    value: Union[kdsl.node.v1alpha1.RuntimeClassSpecUnion, OmitEnum, None]
) -> Union[kdsl.node.v1alpha1.RuntimeClassSpec, OmitEnum, None]:
    import kdsl.node.v1alpha1

    return (
        kdsl.node.v1alpha1.RuntimeClassSpec(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_Overhead(
    value: kdsl.node.v1alpha1.OverheadUnion,
) -> kdsl.node.v1alpha1.Overhead:
    import kdsl.node.v1alpha1

    return kdsl.node.v1alpha1.Overhead(**value) if isinstance(value, dict) else value
