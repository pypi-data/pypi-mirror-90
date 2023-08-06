from __future__ import annotations
from typing import Literal, Sequence, Union
from kdsl.bases import OmitEnum, OMIT
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import kdsl.autoscaling.v2beta2


def optional_converter_MetricIdentifier(
    value: Union[kdsl.autoscaling.v2beta2.MetricIdentifierUnion, OmitEnum, None]
) -> Union[kdsl.autoscaling.v2beta2.MetricIdentifier, OmitEnum, None]:
    import kdsl.autoscaling.v2beta2

    return (
        kdsl.autoscaling.v2beta2.MetricIdentifier(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_HorizontalPodAutoscalerSpec(
    value: kdsl.autoscaling.v2beta2.HorizontalPodAutoscalerSpecUnion,
) -> kdsl.autoscaling.v2beta2.HorizontalPodAutoscalerSpec:
    import kdsl.autoscaling.v2beta2

    return (
        kdsl.autoscaling.v2beta2.HorizontalPodAutoscalerSpec(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_ObjectMetricSource(
    value: kdsl.autoscaling.v2beta2.ObjectMetricSourceUnion,
) -> kdsl.autoscaling.v2beta2.ObjectMetricSource:
    import kdsl.autoscaling.v2beta2

    return (
        kdsl.autoscaling.v2beta2.ObjectMetricSource(**value)
        if isinstance(value, dict)
        else value
    )


def optional_list_converter_MetricStatus(
    value: Union[Sequence[kdsl.autoscaling.v2beta2.MetricStatusUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.autoscaling.v2beta2.MetricStatus], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_MetricStatus(x) for x in value]


def required_converter_HorizontalPodAutoscalerCondition(
    value: kdsl.autoscaling.v2beta2.HorizontalPodAutoscalerConditionUnion,
) -> kdsl.autoscaling.v2beta2.HorizontalPodAutoscalerCondition:
    import kdsl.autoscaling.v2beta2

    return (
        kdsl.autoscaling.v2beta2.HorizontalPodAutoscalerCondition(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_PodsMetricSource(
    value: kdsl.autoscaling.v2beta2.PodsMetricSourceUnion,
) -> kdsl.autoscaling.v2beta2.PodsMetricSource:
    import kdsl.autoscaling.v2beta2

    return (
        kdsl.autoscaling.v2beta2.PodsMetricSource(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_MetricStatus(
    value: kdsl.autoscaling.v2beta2.MetricStatusUnion,
) -> kdsl.autoscaling.v2beta2.MetricStatus:
    import kdsl.autoscaling.v2beta2

    return (
        kdsl.autoscaling.v2beta2.MetricStatus(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_ResourceMetricStatus(
    value: kdsl.autoscaling.v2beta2.ResourceMetricStatusUnion,
) -> kdsl.autoscaling.v2beta2.ResourceMetricStatus:
    import kdsl.autoscaling.v2beta2

    return (
        kdsl.autoscaling.v2beta2.ResourceMetricStatus(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_ExternalMetricStatus(
    value: kdsl.autoscaling.v2beta2.ExternalMetricStatusUnion,
) -> kdsl.autoscaling.v2beta2.ExternalMetricStatus:
    import kdsl.autoscaling.v2beta2

    return (
        kdsl.autoscaling.v2beta2.ExternalMetricStatus(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_MetricValueStatus(
    value: Union[kdsl.autoscaling.v2beta2.MetricValueStatusUnion, OmitEnum, None]
) -> Union[kdsl.autoscaling.v2beta2.MetricValueStatus, OmitEnum, None]:
    import kdsl.autoscaling.v2beta2

    return (
        kdsl.autoscaling.v2beta2.MetricValueStatus(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_MetricTarget(
    value: Union[kdsl.autoscaling.v2beta2.MetricTargetUnion, OmitEnum, None]
) -> Union[kdsl.autoscaling.v2beta2.MetricTarget, OmitEnum, None]:
    import kdsl.autoscaling.v2beta2

    return (
        kdsl.autoscaling.v2beta2.MetricTarget(**value)
        if isinstance(value, dict)
        else value
    )


def optional_list_converter_MetricSpec(
    value: Union[Sequence[kdsl.autoscaling.v2beta2.MetricSpecUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.autoscaling.v2beta2.MetricSpec], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_MetricSpec(x) for x in value]


def optional_converter_HorizontalPodAutoscalerStatus(
    value: Union[
        kdsl.autoscaling.v2beta2.HorizontalPodAutoscalerStatusUnion, OmitEnum, None
    ]
) -> Union[kdsl.autoscaling.v2beta2.HorizontalPodAutoscalerStatus, OmitEnum, None]:
    import kdsl.autoscaling.v2beta2

    return (
        kdsl.autoscaling.v2beta2.HorizontalPodAutoscalerStatus(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_PodsMetricStatus(
    value: kdsl.autoscaling.v2beta2.PodsMetricStatusUnion,
) -> kdsl.autoscaling.v2beta2.PodsMetricStatus:
    import kdsl.autoscaling.v2beta2

    return (
        kdsl.autoscaling.v2beta2.PodsMetricStatus(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_CrossVersionObjectReference(
    value: kdsl.autoscaling.v2beta2.CrossVersionObjectReferenceUnion,
) -> kdsl.autoscaling.v2beta2.CrossVersionObjectReference:
    import kdsl.autoscaling.v2beta2

    return (
        kdsl.autoscaling.v2beta2.CrossVersionObjectReference(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_ResourceMetricSource(
    value: kdsl.autoscaling.v2beta2.ResourceMetricSourceUnion,
) -> kdsl.autoscaling.v2beta2.ResourceMetricSource:
    import kdsl.autoscaling.v2beta2

    return (
        kdsl.autoscaling.v2beta2.ResourceMetricSource(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_ExternalMetricSource(
    value: kdsl.autoscaling.v2beta2.ExternalMetricSourceUnion,
) -> kdsl.autoscaling.v2beta2.ExternalMetricSource:
    import kdsl.autoscaling.v2beta2

    return (
        kdsl.autoscaling.v2beta2.ExternalMetricSource(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_ObjectMetricStatus(
    value: Union[kdsl.autoscaling.v2beta2.ObjectMetricStatusUnion, OmitEnum, None]
) -> Union[kdsl.autoscaling.v2beta2.ObjectMetricStatus, OmitEnum, None]:
    import kdsl.autoscaling.v2beta2

    return (
        kdsl.autoscaling.v2beta2.ObjectMetricStatus(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_HorizontalPodAutoscalerSpec(
    value: Union[
        kdsl.autoscaling.v2beta2.HorizontalPodAutoscalerSpecUnion, OmitEnum, None
    ]
) -> Union[kdsl.autoscaling.v2beta2.HorizontalPodAutoscalerSpec, OmitEnum, None]:
    import kdsl.autoscaling.v2beta2

    return (
        kdsl.autoscaling.v2beta2.HorizontalPodAutoscalerSpec(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_MetricSpec(
    value: kdsl.autoscaling.v2beta2.MetricSpecUnion,
) -> kdsl.autoscaling.v2beta2.MetricSpec:
    import kdsl.autoscaling.v2beta2

    return (
        kdsl.autoscaling.v2beta2.MetricSpec(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_ObjectMetricSource(
    value: Union[kdsl.autoscaling.v2beta2.ObjectMetricSourceUnion, OmitEnum, None]
) -> Union[kdsl.autoscaling.v2beta2.ObjectMetricSource, OmitEnum, None]:
    import kdsl.autoscaling.v2beta2

    return (
        kdsl.autoscaling.v2beta2.ObjectMetricSource(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_HorizontalPodAutoscalerCondition(
    value: Union[
        kdsl.autoscaling.v2beta2.HorizontalPodAutoscalerConditionUnion, OmitEnum, None
    ]
) -> Union[kdsl.autoscaling.v2beta2.HorizontalPodAutoscalerCondition, OmitEnum, None]:
    import kdsl.autoscaling.v2beta2

    return (
        kdsl.autoscaling.v2beta2.HorizontalPodAutoscalerCondition(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_PodsMetricSource(
    value: Union[kdsl.autoscaling.v2beta2.PodsMetricSourceUnion, OmitEnum, None]
) -> Union[kdsl.autoscaling.v2beta2.PodsMetricSource, OmitEnum, None]:
    import kdsl.autoscaling.v2beta2

    return (
        kdsl.autoscaling.v2beta2.PodsMetricSource(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_MetricStatus(
    value: Union[kdsl.autoscaling.v2beta2.MetricStatusUnion, OmitEnum, None]
) -> Union[kdsl.autoscaling.v2beta2.MetricStatus, OmitEnum, None]:
    import kdsl.autoscaling.v2beta2

    return (
        kdsl.autoscaling.v2beta2.MetricStatus(**value)
        if isinstance(value, dict)
        else value
    )


def required_list_converter_HorizontalPodAutoscalerCondition(
    value: Sequence[kdsl.autoscaling.v2beta2.HorizontalPodAutoscalerConditionUnion],
) -> Sequence[kdsl.autoscaling.v2beta2.HorizontalPodAutoscalerCondition]:
    return [required_converter_HorizontalPodAutoscalerCondition(x) for x in value]


def optional_converter_ResourceMetricStatus(
    value: Union[kdsl.autoscaling.v2beta2.ResourceMetricStatusUnion, OmitEnum, None]
) -> Union[kdsl.autoscaling.v2beta2.ResourceMetricStatus, OmitEnum, None]:
    import kdsl.autoscaling.v2beta2

    return (
        kdsl.autoscaling.v2beta2.ResourceMetricStatus(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_ExternalMetricStatus(
    value: Union[kdsl.autoscaling.v2beta2.ExternalMetricStatusUnion, OmitEnum, None]
) -> Union[kdsl.autoscaling.v2beta2.ExternalMetricStatus, OmitEnum, None]:
    import kdsl.autoscaling.v2beta2

    return (
        kdsl.autoscaling.v2beta2.ExternalMetricStatus(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_PodsMetricStatus(
    value: Union[kdsl.autoscaling.v2beta2.PodsMetricStatusUnion, OmitEnum, None]
) -> Union[kdsl.autoscaling.v2beta2.PodsMetricStatus, OmitEnum, None]:
    import kdsl.autoscaling.v2beta2

    return (
        kdsl.autoscaling.v2beta2.PodsMetricStatus(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_ResourceMetricSource(
    value: Union[kdsl.autoscaling.v2beta2.ResourceMetricSourceUnion, OmitEnum, None]
) -> Union[kdsl.autoscaling.v2beta2.ResourceMetricSource, OmitEnum, None]:
    import kdsl.autoscaling.v2beta2

    return (
        kdsl.autoscaling.v2beta2.ResourceMetricSource(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_ExternalMetricSource(
    value: Union[kdsl.autoscaling.v2beta2.ExternalMetricSourceUnion, OmitEnum, None]
) -> Union[kdsl.autoscaling.v2beta2.ExternalMetricSource, OmitEnum, None]:
    import kdsl.autoscaling.v2beta2

    return (
        kdsl.autoscaling.v2beta2.ExternalMetricSource(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_CrossVersionObjectReference(
    value: Union[
        kdsl.autoscaling.v2beta2.CrossVersionObjectReferenceUnion, OmitEnum, None
    ]
) -> Union[kdsl.autoscaling.v2beta2.CrossVersionObjectReference, OmitEnum, None]:
    import kdsl.autoscaling.v2beta2

    return (
        kdsl.autoscaling.v2beta2.CrossVersionObjectReference(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_MetricIdentifier(
    value: kdsl.autoscaling.v2beta2.MetricIdentifierUnion,
) -> kdsl.autoscaling.v2beta2.MetricIdentifier:
    import kdsl.autoscaling.v2beta2

    return (
        kdsl.autoscaling.v2beta2.MetricIdentifier(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_MetricSpec(
    value: Union[kdsl.autoscaling.v2beta2.MetricSpecUnion, OmitEnum, None]
) -> Union[kdsl.autoscaling.v2beta2.MetricSpec, OmitEnum, None]:
    import kdsl.autoscaling.v2beta2

    return (
        kdsl.autoscaling.v2beta2.MetricSpec(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_MetricValueStatus(
    value: kdsl.autoscaling.v2beta2.MetricValueStatusUnion,
) -> kdsl.autoscaling.v2beta2.MetricValueStatus:
    import kdsl.autoscaling.v2beta2

    return (
        kdsl.autoscaling.v2beta2.MetricValueStatus(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_MetricTarget(
    value: kdsl.autoscaling.v2beta2.MetricTargetUnion,
) -> kdsl.autoscaling.v2beta2.MetricTarget:
    import kdsl.autoscaling.v2beta2

    return (
        kdsl.autoscaling.v2beta2.MetricTarget(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_HorizontalPodAutoscalerStatus(
    value: kdsl.autoscaling.v2beta2.HorizontalPodAutoscalerStatusUnion,
) -> kdsl.autoscaling.v2beta2.HorizontalPodAutoscalerStatus:
    import kdsl.autoscaling.v2beta2

    return (
        kdsl.autoscaling.v2beta2.HorizontalPodAutoscalerStatus(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_ObjectMetricStatus(
    value: kdsl.autoscaling.v2beta2.ObjectMetricStatusUnion,
) -> kdsl.autoscaling.v2beta2.ObjectMetricStatus:
    import kdsl.autoscaling.v2beta2

    return (
        kdsl.autoscaling.v2beta2.ObjectMetricStatus(**value)
        if isinstance(value, dict)
        else value
    )
