from __future__ import annotations
from typing import Literal, Sequence, Union
from kdsl.bases import OmitEnum, OMIT
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import kdsl.autoscaling.v2beta1


def required_converter_HorizontalPodAutoscalerSpec(
    value: kdsl.autoscaling.v2beta1.HorizontalPodAutoscalerSpecUnion,
) -> kdsl.autoscaling.v2beta1.HorizontalPodAutoscalerSpec:
    import kdsl.autoscaling.v2beta1

    return (
        kdsl.autoscaling.v2beta1.HorizontalPodAutoscalerSpec(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_PodsMetricStatus(
    value: Union[kdsl.autoscaling.v2beta1.PodsMetricStatusUnion, OmitEnum, None]
) -> Union[kdsl.autoscaling.v2beta1.PodsMetricStatus, OmitEnum, None]:
    import kdsl.autoscaling.v2beta1

    return (
        kdsl.autoscaling.v2beta1.PodsMetricStatus(**value)
        if isinstance(value, dict)
        else value
    )


def required_list_converter_HorizontalPodAutoscalerCondition(
    value: Sequence[kdsl.autoscaling.v2beta1.HorizontalPodAutoscalerConditionUnion],
) -> Sequence[kdsl.autoscaling.v2beta1.HorizontalPodAutoscalerCondition]:
    return [required_converter_HorizontalPodAutoscalerCondition(x) for x in value]


def required_converter_ObjectMetricSource(
    value: kdsl.autoscaling.v2beta1.ObjectMetricSourceUnion,
) -> kdsl.autoscaling.v2beta1.ObjectMetricSource:
    import kdsl.autoscaling.v2beta1

    return (
        kdsl.autoscaling.v2beta1.ObjectMetricSource(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_PodsMetricSource(
    value: Union[kdsl.autoscaling.v2beta1.PodsMetricSourceUnion, OmitEnum, None]
) -> Union[kdsl.autoscaling.v2beta1.PodsMetricSource, OmitEnum, None]:
    import kdsl.autoscaling.v2beta1

    return (
        kdsl.autoscaling.v2beta1.PodsMetricSource(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_ObjectMetricStatus(
    value: kdsl.autoscaling.v2beta1.ObjectMetricStatusUnion,
) -> kdsl.autoscaling.v2beta1.ObjectMetricStatus:
    import kdsl.autoscaling.v2beta1

    return (
        kdsl.autoscaling.v2beta1.ObjectMetricStatus(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_ResourceMetricStatus(
    value: kdsl.autoscaling.v2beta1.ResourceMetricStatusUnion,
) -> kdsl.autoscaling.v2beta1.ResourceMetricStatus:
    import kdsl.autoscaling.v2beta1

    return (
        kdsl.autoscaling.v2beta1.ResourceMetricStatus(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_ExternalMetricStatus(
    value: kdsl.autoscaling.v2beta1.ExternalMetricStatusUnion,
) -> kdsl.autoscaling.v2beta1.ExternalMetricStatus:
    import kdsl.autoscaling.v2beta1

    return (
        kdsl.autoscaling.v2beta1.ExternalMetricStatus(**value)
        if isinstance(value, dict)
        else value
    )


def optional_list_converter_MetricSpec(
    value: Union[Sequence[kdsl.autoscaling.v2beta1.MetricSpecUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.autoscaling.v2beta1.MetricSpec], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_MetricSpec(x) for x in value]


def required_converter_CrossVersionObjectReference(
    value: kdsl.autoscaling.v2beta1.CrossVersionObjectReferenceUnion,
) -> kdsl.autoscaling.v2beta1.CrossVersionObjectReference:
    import kdsl.autoscaling.v2beta1

    return (
        kdsl.autoscaling.v2beta1.CrossVersionObjectReference(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_HorizontalPodAutoscalerSpec(
    value: Union[
        kdsl.autoscaling.v2beta1.HorizontalPodAutoscalerSpecUnion, OmitEnum, None
    ]
) -> Union[kdsl.autoscaling.v2beta1.HorizontalPodAutoscalerSpec, OmitEnum, None]:
    import kdsl.autoscaling.v2beta1

    return (
        kdsl.autoscaling.v2beta1.HorizontalPodAutoscalerSpec(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_MetricSpec(
    value: kdsl.autoscaling.v2beta1.MetricSpecUnion,
) -> kdsl.autoscaling.v2beta1.MetricSpec:
    import kdsl.autoscaling.v2beta1

    return (
        kdsl.autoscaling.v2beta1.MetricSpec(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_ResourceMetricSource(
    value: kdsl.autoscaling.v2beta1.ResourceMetricSourceUnion,
) -> kdsl.autoscaling.v2beta1.ResourceMetricSource:
    import kdsl.autoscaling.v2beta1

    return (
        kdsl.autoscaling.v2beta1.ResourceMetricSource(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_ObjectMetricSource(
    value: Union[kdsl.autoscaling.v2beta1.ObjectMetricSourceUnion, OmitEnum, None]
) -> Union[kdsl.autoscaling.v2beta1.ObjectMetricSource, OmitEnum, None]:
    import kdsl.autoscaling.v2beta1

    return (
        kdsl.autoscaling.v2beta1.ObjectMetricSource(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_ObjectMetricStatus(
    value: Union[kdsl.autoscaling.v2beta1.ObjectMetricStatusUnion, OmitEnum, None]
) -> Union[kdsl.autoscaling.v2beta1.ObjectMetricStatus, OmitEnum, None]:
    import kdsl.autoscaling.v2beta1

    return (
        kdsl.autoscaling.v2beta1.ObjectMetricStatus(**value)
        if isinstance(value, dict)
        else value
    )


def optional_list_converter_MetricStatus(
    value: Union[Sequence[kdsl.autoscaling.v2beta1.MetricStatusUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.autoscaling.v2beta1.MetricStatus], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_MetricStatus(x) for x in value]


def required_converter_HorizontalPodAutoscalerCondition(
    value: kdsl.autoscaling.v2beta1.HorizontalPodAutoscalerConditionUnion,
) -> kdsl.autoscaling.v2beta1.HorizontalPodAutoscalerCondition:
    import kdsl.autoscaling.v2beta1

    return (
        kdsl.autoscaling.v2beta1.HorizontalPodAutoscalerCondition(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_ResourceMetricStatus(
    value: Union[kdsl.autoscaling.v2beta1.ResourceMetricStatusUnion, OmitEnum, None]
) -> Union[kdsl.autoscaling.v2beta1.ResourceMetricStatus, OmitEnum, None]:
    import kdsl.autoscaling.v2beta1

    return (
        kdsl.autoscaling.v2beta1.ResourceMetricStatus(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_MetricStatus(
    value: kdsl.autoscaling.v2beta1.MetricStatusUnion,
) -> kdsl.autoscaling.v2beta1.MetricStatus:
    import kdsl.autoscaling.v2beta1

    return (
        kdsl.autoscaling.v2beta1.MetricStatus(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_ExternalMetricStatus(
    value: Union[kdsl.autoscaling.v2beta1.ExternalMetricStatusUnion, OmitEnum, None]
) -> Union[kdsl.autoscaling.v2beta1.ExternalMetricStatus, OmitEnum, None]:
    import kdsl.autoscaling.v2beta1

    return (
        kdsl.autoscaling.v2beta1.ExternalMetricStatus(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_HorizontalPodAutoscalerStatus(
    value: kdsl.autoscaling.v2beta1.HorizontalPodAutoscalerStatusUnion,
) -> kdsl.autoscaling.v2beta1.HorizontalPodAutoscalerStatus:
    import kdsl.autoscaling.v2beta1

    return (
        kdsl.autoscaling.v2beta1.HorizontalPodAutoscalerStatus(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_CrossVersionObjectReference(
    value: Union[
        kdsl.autoscaling.v2beta1.CrossVersionObjectReferenceUnion, OmitEnum, None
    ]
) -> Union[kdsl.autoscaling.v2beta1.CrossVersionObjectReference, OmitEnum, None]:
    import kdsl.autoscaling.v2beta1

    return (
        kdsl.autoscaling.v2beta1.CrossVersionObjectReference(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_MetricSpec(
    value: Union[kdsl.autoscaling.v2beta1.MetricSpecUnion, OmitEnum, None]
) -> Union[kdsl.autoscaling.v2beta1.MetricSpec, OmitEnum, None]:
    import kdsl.autoscaling.v2beta1

    return (
        kdsl.autoscaling.v2beta1.MetricSpec(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_ExternalMetricSource(
    value: kdsl.autoscaling.v2beta1.ExternalMetricSourceUnion,
) -> kdsl.autoscaling.v2beta1.ExternalMetricSource:
    import kdsl.autoscaling.v2beta1

    return (
        kdsl.autoscaling.v2beta1.ExternalMetricSource(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_PodsMetricStatus(
    value: kdsl.autoscaling.v2beta1.PodsMetricStatusUnion,
) -> kdsl.autoscaling.v2beta1.PodsMetricStatus:
    import kdsl.autoscaling.v2beta1

    return (
        kdsl.autoscaling.v2beta1.PodsMetricStatus(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_ResourceMetricSource(
    value: Union[kdsl.autoscaling.v2beta1.ResourceMetricSourceUnion, OmitEnum, None]
) -> Union[kdsl.autoscaling.v2beta1.ResourceMetricSource, OmitEnum, None]:
    import kdsl.autoscaling.v2beta1

    return (
        kdsl.autoscaling.v2beta1.ResourceMetricSource(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_PodsMetricSource(
    value: kdsl.autoscaling.v2beta1.PodsMetricSourceUnion,
) -> kdsl.autoscaling.v2beta1.PodsMetricSource:
    import kdsl.autoscaling.v2beta1

    return (
        kdsl.autoscaling.v2beta1.PodsMetricSource(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_HorizontalPodAutoscalerCondition(
    value: Union[
        kdsl.autoscaling.v2beta1.HorizontalPodAutoscalerConditionUnion, OmitEnum, None
    ]
) -> Union[kdsl.autoscaling.v2beta1.HorizontalPodAutoscalerCondition, OmitEnum, None]:
    import kdsl.autoscaling.v2beta1

    return (
        kdsl.autoscaling.v2beta1.HorizontalPodAutoscalerCondition(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_MetricStatus(
    value: Union[kdsl.autoscaling.v2beta1.MetricStatusUnion, OmitEnum, None]
) -> Union[kdsl.autoscaling.v2beta1.MetricStatus, OmitEnum, None]:
    import kdsl.autoscaling.v2beta1

    return (
        kdsl.autoscaling.v2beta1.MetricStatus(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_HorizontalPodAutoscalerStatus(
    value: Union[
        kdsl.autoscaling.v2beta1.HorizontalPodAutoscalerStatusUnion, OmitEnum, None
    ]
) -> Union[kdsl.autoscaling.v2beta1.HorizontalPodAutoscalerStatus, OmitEnum, None]:
    import kdsl.autoscaling.v2beta1

    return (
        kdsl.autoscaling.v2beta1.HorizontalPodAutoscalerStatus(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_ExternalMetricSource(
    value: Union[kdsl.autoscaling.v2beta1.ExternalMetricSourceUnion, OmitEnum, None]
) -> Union[kdsl.autoscaling.v2beta1.ExternalMetricSource, OmitEnum, None]:
    import kdsl.autoscaling.v2beta1

    return (
        kdsl.autoscaling.v2beta1.ExternalMetricSource(**value)
        if isinstance(value, dict)
        else value
    )
