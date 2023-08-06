from __future__ import annotations
import kdsl.autoscaling.v2beta1
import kdsl.core.v1
import kdsl.core.v1_converters
import kdsl.autoscaling.v2beta1_converters
import attr
from typing import Mapping, ClassVar, Optional, Any, Sequence, TypedDict, Union
from kdsl.bases import OmitEnum, K8sObject, OMIT, K8sResource


@attr.s(kw_only=True)
class MetricSpec(K8sObject):
    type: str = attr.ib(metadata={"yaml_name": "type"})
    external: Union[
        None, OmitEnum, kdsl.autoscaling.v2beta1.ExternalMetricSource
    ] = attr.ib(
        metadata={"yaml_name": "external"},
        converter=kdsl.autoscaling.v2beta1_converters.optional_converter_ExternalMetricSource,
        default=OMIT,
    )
    object: Union[
        None, OmitEnum, kdsl.autoscaling.v2beta1.ObjectMetricSource
    ] = attr.ib(
        metadata={"yaml_name": "object"},
        converter=kdsl.autoscaling.v2beta1_converters.optional_converter_ObjectMetricSource,
        default=OMIT,
    )
    pods: Union[None, OmitEnum, kdsl.autoscaling.v2beta1.PodsMetricSource] = attr.ib(
        metadata={"yaml_name": "pods"},
        converter=kdsl.autoscaling.v2beta1_converters.optional_converter_PodsMetricSource,
        default=OMIT,
    )
    resource: Union[
        None, OmitEnum, kdsl.autoscaling.v2beta1.ResourceMetricSource
    ] = attr.ib(
        metadata={"yaml_name": "resource"},
        converter=kdsl.autoscaling.v2beta1_converters.optional_converter_ResourceMetricSource,
        default=OMIT,
    )


class MetricSpecOptionalTypedDict(TypedDict, total=(False)):
    external: kdsl.autoscaling.v2beta1.ExternalMetricSource
    object: kdsl.autoscaling.v2beta1.ObjectMetricSource
    pods: kdsl.autoscaling.v2beta1.PodsMetricSource
    resource: kdsl.autoscaling.v2beta1.ResourceMetricSource


class MetricSpecTypedDict(MetricSpecOptionalTypedDict, total=(True)):
    type: str


MetricSpecUnion = Union[MetricSpec, MetricSpecTypedDict]


@attr.s(kw_only=True)
class HorizontalPodAutoscaler(K8sResource):
    apiVersion: ClassVar[str] = "autoscaling/v2beta1"
    kind: ClassVar[str] = "HorizontalPodAutoscaler"
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    spec: Union[
        None, OmitEnum, kdsl.autoscaling.v2beta1.HorizontalPodAutoscalerSpec
    ] = attr.ib(
        metadata={"yaml_name": "spec"},
        converter=kdsl.autoscaling.v2beta1_converters.optional_converter_HorizontalPodAutoscalerSpec,
        default=OMIT,
    )
    status: Union[
        None, OmitEnum, kdsl.autoscaling.v2beta1.HorizontalPodAutoscalerStatus
    ] = attr.ib(
        metadata={"yaml_name": "status"},
        converter=kdsl.autoscaling.v2beta1_converters.optional_converter_HorizontalPodAutoscalerStatus,
        default=OMIT,
    )


@attr.s(kw_only=True)
class PodsMetricStatus(K8sObject):
    currentAverageValue: str = attr.ib(metadata={"yaml_name": "currentAverageValue"})
    metricName: str = attr.ib(metadata={"yaml_name": "metricName"})
    selector: Union[None, OmitEnum, kdsl.core.v1.LabelSelector] = attr.ib(
        metadata={"yaml_name": "selector"},
        converter=kdsl.core.v1_converters.optional_converter_LabelSelector,
        default=OMIT,
    )


class PodsMetricStatusOptionalTypedDict(TypedDict, total=(False)):
    selector: kdsl.core.v1.LabelSelector


class PodsMetricStatusTypedDict(PodsMetricStatusOptionalTypedDict, total=(True)):
    currentAverageValue: str
    metricName: str


PodsMetricStatusUnion = Union[PodsMetricStatus, PodsMetricStatusTypedDict]


@attr.s(kw_only=True)
class ObjectMetricSource(K8sObject):
    metricName: str = attr.ib(metadata={"yaml_name": "metricName"})
    target: kdsl.autoscaling.v2beta1.CrossVersionObjectReference = attr.ib(
        metadata={"yaml_name": "target"},
        converter=kdsl.autoscaling.v2beta1_converters.required_converter_CrossVersionObjectReference,
    )
    targetValue: str = attr.ib(metadata={"yaml_name": "targetValue"})
    averageValue: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "averageValue"}, default=OMIT
    )
    selector: Union[None, OmitEnum, kdsl.core.v1.LabelSelector] = attr.ib(
        metadata={"yaml_name": "selector"},
        converter=kdsl.core.v1_converters.optional_converter_LabelSelector,
        default=OMIT,
    )


class ObjectMetricSourceOptionalTypedDict(TypedDict, total=(False)):
    averageValue: str
    selector: kdsl.core.v1.LabelSelector


class ObjectMetricSourceTypedDict(ObjectMetricSourceOptionalTypedDict, total=(True)):
    metricName: str
    target: kdsl.autoscaling.v2beta1.CrossVersionObjectReference
    targetValue: str


ObjectMetricSourceUnion = Union[ObjectMetricSource, ObjectMetricSourceTypedDict]


@attr.s(kw_only=True)
class CrossVersionObjectReference(K8sObject):
    kind: str = attr.ib(metadata={"yaml_name": "kind"})
    name: str = attr.ib(metadata={"yaml_name": "name"})
    apiVersion: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "apiVersion"}, default=OMIT
    )


class CrossVersionObjectReferenceOptionalTypedDict(TypedDict, total=(False)):
    apiVersion: str


class CrossVersionObjectReferenceTypedDict(
    CrossVersionObjectReferenceOptionalTypedDict, total=(True)
):
    kind: str
    name: str


CrossVersionObjectReferenceUnion = Union[
    CrossVersionObjectReference, CrossVersionObjectReferenceTypedDict
]


@attr.s(kw_only=True)
class ObjectMetricStatus(K8sObject):
    currentValue: str = attr.ib(metadata={"yaml_name": "currentValue"})
    metricName: str = attr.ib(metadata={"yaml_name": "metricName"})
    target: kdsl.autoscaling.v2beta1.CrossVersionObjectReference = attr.ib(
        metadata={"yaml_name": "target"},
        converter=kdsl.autoscaling.v2beta1_converters.required_converter_CrossVersionObjectReference,
    )
    averageValue: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "averageValue"}, default=OMIT
    )
    selector: Union[None, OmitEnum, kdsl.core.v1.LabelSelector] = attr.ib(
        metadata={"yaml_name": "selector"},
        converter=kdsl.core.v1_converters.optional_converter_LabelSelector,
        default=OMIT,
    )


class ObjectMetricStatusOptionalTypedDict(TypedDict, total=(False)):
    averageValue: str
    selector: kdsl.core.v1.LabelSelector


class ObjectMetricStatusTypedDict(ObjectMetricStatusOptionalTypedDict, total=(True)):
    currentValue: str
    metricName: str
    target: kdsl.autoscaling.v2beta1.CrossVersionObjectReference


ObjectMetricStatusUnion = Union[ObjectMetricStatus, ObjectMetricStatusTypedDict]


@attr.s(kw_only=True)
class ExternalMetricSource(K8sObject):
    metricName: str = attr.ib(metadata={"yaml_name": "metricName"})
    metricSelector: Union[None, OmitEnum, kdsl.core.v1.LabelSelector] = attr.ib(
        metadata={"yaml_name": "metricSelector"},
        converter=kdsl.core.v1_converters.optional_converter_LabelSelector,
        default=OMIT,
    )
    targetAverageValue: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "targetAverageValue"}, default=OMIT
    )
    targetValue: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "targetValue"}, default=OMIT
    )


class ExternalMetricSourceOptionalTypedDict(TypedDict, total=(False)):
    metricSelector: kdsl.core.v1.LabelSelector
    targetAverageValue: str
    targetValue: str


class ExternalMetricSourceTypedDict(
    ExternalMetricSourceOptionalTypedDict, total=(True)
):
    metricName: str


ExternalMetricSourceUnion = Union[ExternalMetricSource, ExternalMetricSourceTypedDict]


@attr.s(kw_only=True)
class HorizontalPodAutoscalerSpec(K8sObject):
    maxReplicas: int = attr.ib(metadata={"yaml_name": "maxReplicas"})
    scaleTargetRef: kdsl.autoscaling.v2beta1.CrossVersionObjectReference = attr.ib(
        metadata={"yaml_name": "scaleTargetRef"},
        converter=kdsl.autoscaling.v2beta1_converters.required_converter_CrossVersionObjectReference,
    )
    metrics: Union[
        None, OmitEnum, Sequence[kdsl.autoscaling.v2beta1.MetricSpec]
    ] = attr.ib(
        metadata={"yaml_name": "metrics"},
        converter=kdsl.autoscaling.v2beta1_converters.optional_list_converter_MetricSpec,
        default=OMIT,
    )
    minReplicas: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "minReplicas"}, default=OMIT
    )


class HorizontalPodAutoscalerSpecOptionalTypedDict(TypedDict, total=(False)):
    metrics: Sequence[kdsl.autoscaling.v2beta1.MetricSpec]
    minReplicas: int


class HorizontalPodAutoscalerSpecTypedDict(
    HorizontalPodAutoscalerSpecOptionalTypedDict, total=(True)
):
    maxReplicas: int
    scaleTargetRef: kdsl.autoscaling.v2beta1.CrossVersionObjectReference


HorizontalPodAutoscalerSpecUnion = Union[
    HorizontalPodAutoscalerSpec, HorizontalPodAutoscalerSpecTypedDict
]


@attr.s(kw_only=True)
class MetricStatus(K8sObject):
    type: str = attr.ib(metadata={"yaml_name": "type"})
    external: Union[
        None, OmitEnum, kdsl.autoscaling.v2beta1.ExternalMetricStatus
    ] = attr.ib(
        metadata={"yaml_name": "external"},
        converter=kdsl.autoscaling.v2beta1_converters.optional_converter_ExternalMetricStatus,
        default=OMIT,
    )
    object: Union[
        None, OmitEnum, kdsl.autoscaling.v2beta1.ObjectMetricStatus
    ] = attr.ib(
        metadata={"yaml_name": "object"},
        converter=kdsl.autoscaling.v2beta1_converters.optional_converter_ObjectMetricStatus,
        default=OMIT,
    )
    pods: Union[None, OmitEnum, kdsl.autoscaling.v2beta1.PodsMetricStatus] = attr.ib(
        metadata={"yaml_name": "pods"},
        converter=kdsl.autoscaling.v2beta1_converters.optional_converter_PodsMetricStatus,
        default=OMIT,
    )
    resource: Union[
        None, OmitEnum, kdsl.autoscaling.v2beta1.ResourceMetricStatus
    ] = attr.ib(
        metadata={"yaml_name": "resource"},
        converter=kdsl.autoscaling.v2beta1_converters.optional_converter_ResourceMetricStatus,
        default=OMIT,
    )


class MetricStatusOptionalTypedDict(TypedDict, total=(False)):
    external: kdsl.autoscaling.v2beta1.ExternalMetricStatus
    object: kdsl.autoscaling.v2beta1.ObjectMetricStatus
    pods: kdsl.autoscaling.v2beta1.PodsMetricStatus
    resource: kdsl.autoscaling.v2beta1.ResourceMetricStatus


class MetricStatusTypedDict(MetricStatusOptionalTypedDict, total=(True)):
    type: str


MetricStatusUnion = Union[MetricStatus, MetricStatusTypedDict]


@attr.s(kw_only=True)
class HorizontalPodAutoscalerStatus(K8sObject):
    conditions: Sequence[
        kdsl.autoscaling.v2beta1.HorizontalPodAutoscalerCondition
    ] = attr.ib(
        metadata={"yaml_name": "conditions"},
        converter=kdsl.autoscaling.v2beta1_converters.required_list_converter_HorizontalPodAutoscalerCondition,
    )
    currentReplicas: int = attr.ib(metadata={"yaml_name": "currentReplicas"})
    desiredReplicas: int = attr.ib(metadata={"yaml_name": "desiredReplicas"})
    currentMetrics: Union[
        None, OmitEnum, Sequence[kdsl.autoscaling.v2beta1.MetricStatus]
    ] = attr.ib(
        metadata={"yaml_name": "currentMetrics"},
        converter=kdsl.autoscaling.v2beta1_converters.optional_list_converter_MetricStatus,
        default=OMIT,
    )
    lastScaleTime: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "lastScaleTime"}, default=OMIT
    )
    observedGeneration: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "observedGeneration"}, default=OMIT
    )


class HorizontalPodAutoscalerStatusOptionalTypedDict(TypedDict, total=(False)):
    currentMetrics: Sequence[kdsl.autoscaling.v2beta1.MetricStatus]
    lastScaleTime: str
    observedGeneration: int


class HorizontalPodAutoscalerStatusTypedDict(
    HorizontalPodAutoscalerStatusOptionalTypedDict, total=(True)
):
    conditions: Sequence[kdsl.autoscaling.v2beta1.HorizontalPodAutoscalerCondition]
    currentReplicas: int
    desiredReplicas: int


HorizontalPodAutoscalerStatusUnion = Union[
    HorizontalPodAutoscalerStatus, HorizontalPodAutoscalerStatusTypedDict
]


@attr.s(kw_only=True)
class PodsMetricSource(K8sObject):
    metricName: str = attr.ib(metadata={"yaml_name": "metricName"})
    targetAverageValue: str = attr.ib(metadata={"yaml_name": "targetAverageValue"})
    selector: Union[None, OmitEnum, kdsl.core.v1.LabelSelector] = attr.ib(
        metadata={"yaml_name": "selector"},
        converter=kdsl.core.v1_converters.optional_converter_LabelSelector,
        default=OMIT,
    )


class PodsMetricSourceOptionalTypedDict(TypedDict, total=(False)):
    selector: kdsl.core.v1.LabelSelector


class PodsMetricSourceTypedDict(PodsMetricSourceOptionalTypedDict, total=(True)):
    metricName: str
    targetAverageValue: str


PodsMetricSourceUnion = Union[PodsMetricSource, PodsMetricSourceTypedDict]


@attr.s(kw_only=True)
class ResourceMetricStatus(K8sObject):
    currentAverageValue: str = attr.ib(metadata={"yaml_name": "currentAverageValue"})
    name: str = attr.ib(metadata={"yaml_name": "name"})
    currentAverageUtilization: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "currentAverageUtilization"}, default=OMIT
    )


class ResourceMetricStatusOptionalTypedDict(TypedDict, total=(False)):
    currentAverageUtilization: int


class ResourceMetricStatusTypedDict(
    ResourceMetricStatusOptionalTypedDict, total=(True)
):
    currentAverageValue: str
    name: str


ResourceMetricStatusUnion = Union[ResourceMetricStatus, ResourceMetricStatusTypedDict]


@attr.s(kw_only=True)
class HorizontalPodAutoscalerCondition(K8sObject):
    status: str = attr.ib(metadata={"yaml_name": "status"})
    type: str = attr.ib(metadata={"yaml_name": "type"})
    lastTransitionTime: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "lastTransitionTime"}, default=OMIT
    )
    message: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "message"}, default=OMIT
    )
    reason: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "reason"}, default=OMIT
    )


class HorizontalPodAutoscalerConditionOptionalTypedDict(TypedDict, total=(False)):
    lastTransitionTime: str
    message: str
    reason: str


class HorizontalPodAutoscalerConditionTypedDict(
    HorizontalPodAutoscalerConditionOptionalTypedDict, total=(True)
):
    status: str
    type: str


HorizontalPodAutoscalerConditionUnion = Union[
    HorizontalPodAutoscalerCondition, HorizontalPodAutoscalerConditionTypedDict
]


@attr.s(kw_only=True)
class ExternalMetricStatus(K8sObject):
    currentValue: str = attr.ib(metadata={"yaml_name": "currentValue"})
    metricName: str = attr.ib(metadata={"yaml_name": "metricName"})
    currentAverageValue: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "currentAverageValue"}, default=OMIT
    )
    metricSelector: Union[None, OmitEnum, kdsl.core.v1.LabelSelector] = attr.ib(
        metadata={"yaml_name": "metricSelector"},
        converter=kdsl.core.v1_converters.optional_converter_LabelSelector,
        default=OMIT,
    )


class ExternalMetricStatusOptionalTypedDict(TypedDict, total=(False)):
    currentAverageValue: str
    metricSelector: kdsl.core.v1.LabelSelector


class ExternalMetricStatusTypedDict(
    ExternalMetricStatusOptionalTypedDict, total=(True)
):
    currentValue: str
    metricName: str


ExternalMetricStatusUnion = Union[ExternalMetricStatus, ExternalMetricStatusTypedDict]


@attr.s(kw_only=True)
class ResourceMetricSource(K8sObject):
    name: str = attr.ib(metadata={"yaml_name": "name"})
    targetAverageUtilization: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "targetAverageUtilization"}, default=OMIT
    )
    targetAverageValue: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "targetAverageValue"}, default=OMIT
    )


class ResourceMetricSourceOptionalTypedDict(TypedDict, total=(False)):
    targetAverageUtilization: int
    targetAverageValue: str


class ResourceMetricSourceTypedDict(
    ResourceMetricSourceOptionalTypedDict, total=(True)
):
    name: str


ResourceMetricSourceUnion = Union[ResourceMetricSource, ResourceMetricSourceTypedDict]
