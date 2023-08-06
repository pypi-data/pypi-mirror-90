from __future__ import annotations
from typing import Literal, Union
from kdsl.bases import OmitEnum, OMIT
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import kdsl.autoscaling.v1


def optional_converter_CrossVersionObjectReference(
    value: Union[kdsl.autoscaling.v1.CrossVersionObjectReferenceUnion, OmitEnum, None]
) -> Union[kdsl.autoscaling.v1.CrossVersionObjectReference, OmitEnum, None]:
    import kdsl.autoscaling.v1

    return (
        kdsl.autoscaling.v1.CrossVersionObjectReference(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_HorizontalPodAutoscalerSpec(
    value: kdsl.autoscaling.v1.HorizontalPodAutoscalerSpecUnion,
) -> kdsl.autoscaling.v1.HorizontalPodAutoscalerSpec:
    import kdsl.autoscaling.v1

    return (
        kdsl.autoscaling.v1.HorizontalPodAutoscalerSpec(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_HorizontalPodAutoscalerSpec(
    value: Union[kdsl.autoscaling.v1.HorizontalPodAutoscalerSpecUnion, OmitEnum, None]
) -> Union[kdsl.autoscaling.v1.HorizontalPodAutoscalerSpec, OmitEnum, None]:
    import kdsl.autoscaling.v1

    return (
        kdsl.autoscaling.v1.HorizontalPodAutoscalerSpec(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_CrossVersionObjectReference(
    value: kdsl.autoscaling.v1.CrossVersionObjectReferenceUnion,
) -> kdsl.autoscaling.v1.CrossVersionObjectReference:
    import kdsl.autoscaling.v1

    return (
        kdsl.autoscaling.v1.CrossVersionObjectReference(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_HorizontalPodAutoscalerStatus(
    value: kdsl.autoscaling.v1.HorizontalPodAutoscalerStatusUnion,
) -> kdsl.autoscaling.v1.HorizontalPodAutoscalerStatus:
    import kdsl.autoscaling.v1

    return (
        kdsl.autoscaling.v1.HorizontalPodAutoscalerStatus(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_HorizontalPodAutoscalerStatus(
    value: Union[kdsl.autoscaling.v1.HorizontalPodAutoscalerStatusUnion, OmitEnum, None]
) -> Union[kdsl.autoscaling.v1.HorizontalPodAutoscalerStatus, OmitEnum, None]:
    import kdsl.autoscaling.v1

    return (
        kdsl.autoscaling.v1.HorizontalPodAutoscalerStatus(**value)
        if isinstance(value, dict)
        else value
    )
