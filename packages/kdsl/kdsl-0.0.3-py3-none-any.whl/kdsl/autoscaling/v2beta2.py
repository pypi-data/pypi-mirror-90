from __future__ import annotations
import kdsl.autoscaling.v2beta2
import kdsl.core.v1_converters
import kdsl.autoscaling.v2beta2_converters
import kdsl.core.v1
import attr
from typing import Mapping, ClassVar, Optional, Any, Sequence, TypedDict, Union
from kdsl.bases import OmitEnum, K8sObject, OMIT, K8sResource


@attr.s(kw_only=True)
class ObjectMetricStatus(K8sObject):
    current: kdsl.autoscaling.v2beta2.MetricValueStatus = attr.ib(
        metadata={"yaml_name": "current"},
        converter=kdsl.autoscaling.v2beta2_converters.required_converter_MetricValueStatus,
    )
    describedObject: kdsl.autoscaling.v2beta2.CrossVersionObjectReference = attr.ib(
        metadata={"yaml_name": "describedObject"},
        converter=kdsl.autoscaling.v2beta2_converters.required_converter_CrossVersionObjectReference,
    )
    metric: kdsl.autoscaling.v2beta2.MetricIdentifier = attr.ib(
        metadata={"yaml_name": "metric"},
        converter=kdsl.autoscaling.v2beta2_converters.required_converter_MetricIdentifier,
    )


class ObjectMetricStatusTypedDict(TypedDict, total=(True)):
    current: kdsl.autoscaling.v2beta2.MetricValueStatus
    describedObject: kdsl.autoscaling.v2beta2.CrossVersionObjectReference
    metric: kdsl.autoscaling.v2beta2.MetricIdentifier


ObjectMetricStatusUnion = Union[ObjectMetricStatus, ObjectMetricStatusTypedDict]


@attr.s(kw_only=True)
class PodsMetricSource(K8sObject):
    metric: kdsl.autoscaling.v2beta2.MetricIdentifier = attr.ib(
        metadata={"yaml_name": "metric"},
        converter=kdsl.autoscaling.v2beta2_converters.required_converter_MetricIdentifier,
    )
    target: kdsl.autoscaling.v2beta2.MetricTarget = attr.ib(
        metadata={"yaml_name": "target"},
        converter=kdsl.autoscaling.v2beta2_converters.required_converter_MetricTarget,
    )


class PodsMetricSourceTypedDict(TypedDict, total=(True)):
    metric: kdsl.autoscaling.v2beta2.MetricIdentifier
    target: kdsl.autoscaling.v2beta2.MetricTarget


PodsMetricSourceUnion = Union[PodsMetricSource, PodsMetricSourceTypedDict]


@attr.s(kw_only=True)
class PodsMetricStatus(K8sObject):
    current: kdsl.autoscaling.v2beta2.MetricValueStatus = attr.ib(
        metadata={"yaml_name": "current"},
        converter=kdsl.autoscaling.v2beta2_converters.required_converter_MetricValueStatus,
    )
    metric: kdsl.autoscaling.v2beta2.MetricIdentifier = attr.ib(
        metadata={"yaml_name": "metric"},
        converter=kdsl.autoscaling.v2beta2_converters.required_converter_MetricIdentifier,
    )


class PodsMetricStatusTypedDict(TypedDict, total=(True)):
    current: kdsl.autoscaling.v2beta2.MetricValueStatus
    metric: kdsl.autoscaling.v2beta2.MetricIdentifier


PodsMetricStatusUnion = Union[PodsMetricStatus, PodsMetricStatusTypedDict]


@attr.s(kw_only=True)
class ResourceMetricSource(K8sObject):
    name: str = attr.ib(metadata={"yaml_name": "name"})
    target: kdsl.autoscaling.v2beta2.MetricTarget = attr.ib(
        metadata={"yaml_name": "target"},
        converter=kdsl.autoscaling.v2beta2_converters.required_converter_MetricTarget,
    )


class ResourceMetricSourceTypedDict(TypedDict, total=(True)):
    name: str
    target: kdsl.autoscaling.v2beta2.MetricTarget


ResourceMetricSourceUnion = Union[ResourceMetricSource, ResourceMetricSourceTypedDict]


@attr.s(kw_only=True)
class HorizontalPodAutoscalerSpec(K8sObject):
    maxReplicas: int = attr.ib(metadata={"yaml_name": "maxReplicas"})
    scaleTargetRef: kdsl.autoscaling.v2beta2.CrossVersionObjectReference = attr.ib(
        metadata={"yaml_name": "scaleTargetRef"},
        converter=kdsl.autoscaling.v2beta2_converters.required_converter_CrossVersionObjectReference,
    )
    metrics: Union[
        None, OmitEnum, Sequence[kdsl.autoscaling.v2beta2.MetricSpec]
    ] = attr.ib(
        metadata={"yaml_name": "metrics"},
        converter=kdsl.autoscaling.v2beta2_converters.optional_list_converter_MetricSpec,
        default=OMIT,
    )
    minReplicas: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "minReplicas"}, default=OMIT
    )


class HorizontalPodAutoscalerSpecOptionalTypedDict(TypedDict, total=(False)):
    metrics: Sequence[kdsl.autoscaling.v2beta2.MetricSpec]
    minReplicas: int


class HorizontalPodAutoscalerSpecTypedDict(
    HorizontalPodAutoscalerSpecOptionalTypedDict, total=(True)
):
    maxReplicas: int
    scaleTargetRef: kdsl.autoscaling.v2beta2.CrossVersionObjectReference


HorizontalPodAutoscalerSpecUnion = Union[
    HorizontalPodAutoscalerSpec, HorizontalPodAutoscalerSpecTypedDict
]


@attr.s(kw_only=True)
class MetricValueStatus(K8sObject):
    averageUtilization: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "averageUtilization"}, default=OMIT
    )
    averageValue: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "averageValue"}, default=OMIT
    )
    value: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "value"}, default=OMIT
    )


class MetricValueStatusTypedDict(TypedDict, total=(False)):
    averageUtilization: int
    averageValue: str
    value: str


MetricValueStatusUnion = Union[MetricValueStatus, MetricValueStatusTypedDict]


@attr.s(kw_only=True)
class ExternalMetricStatus(K8sObject):
    current: kdsl.autoscaling.v2beta2.MetricValueStatus = attr.ib(
        metadata={"yaml_name": "current"},
        converter=kdsl.autoscaling.v2beta2_converters.required_converter_MetricValueStatus,
    )
    metric: kdsl.autoscaling.v2beta2.MetricIdentifier = attr.ib(
        metadata={"yaml_name": "metric"},
        converter=kdsl.autoscaling.v2beta2_converters.required_converter_MetricIdentifier,
    )


class ExternalMetricStatusTypedDict(TypedDict, total=(True)):
    current: kdsl.autoscaling.v2beta2.MetricValueStatus
    metric: kdsl.autoscaling.v2beta2.MetricIdentifier


ExternalMetricStatusUnion = Union[ExternalMetricStatus, ExternalMetricStatusTypedDict]


@attr.s(kw_only=True)
class MetricIdentifier(K8sObject):
    name: str = attr.ib(metadata={"yaml_name": "name"})
    selector: Union[None, OmitEnum, kdsl.core.v1.LabelSelector] = attr.ib(
        metadata={"yaml_name": "selector"},
        converter=kdsl.core.v1_converters.optional_converter_LabelSelector,
        default=OMIT,
    )


class MetricIdentifierOptionalTypedDict(TypedDict, total=(False)):
    selector: kdsl.core.v1.LabelSelector


class MetricIdentifierTypedDict(MetricIdentifierOptionalTypedDict, total=(True)):
    name: str


MetricIdentifierUnion = Union[MetricIdentifier, MetricIdentifierTypedDict]


@attr.s(kw_only=True)
class ResourceMetricStatus(K8sObject):
    current: kdsl.autoscaling.v2beta2.MetricValueStatus = attr.ib(
        metadata={"yaml_name": "current"},
        converter=kdsl.autoscaling.v2beta2_converters.required_converter_MetricValueStatus,
    )
    name: str = attr.ib(metadata={"yaml_name": "name"})


class ResourceMetricStatusTypedDict(TypedDict, total=(True)):
    current: kdsl.autoscaling.v2beta2.MetricValueStatus
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
class MetricSpec(K8sObject):
    type: str = attr.ib(metadata={"yaml_name": "type"})
    external: Union[
        None, OmitEnum, kdsl.autoscaling.v2beta2.ExternalMetricSource
    ] = attr.ib(
        metadata={"yaml_name": "external"},
        converter=kdsl.autoscaling.v2beta2_converters.optional_converter_ExternalMetricSource,
        default=OMIT,
    )
    object: Union[
        None, OmitEnum, kdsl.autoscaling.v2beta2.ObjectMetricSource
    ] = attr.ib(
        metadata={"yaml_name": "object"},
        converter=kdsl.autoscaling.v2beta2_converters.optional_converter_ObjectMetricSource,
        default=OMIT,
    )
    pods: Union[None, OmitEnum, kdsl.autoscaling.v2beta2.PodsMetricSource] = attr.ib(
        metadata={"yaml_name": "pods"},
        converter=kdsl.autoscaling.v2beta2_converters.optional_converter_PodsMetricSource,
        default=OMIT,
    )
    resource: Union[
        None, OmitEnum, kdsl.autoscaling.v2beta2.ResourceMetricSource
    ] = attr.ib(
        metadata={"yaml_name": "resource"},
        converter=kdsl.autoscaling.v2beta2_converters.optional_converter_ResourceMetricSource,
        default=OMIT,
    )


class MetricSpecOptionalTypedDict(TypedDict, total=(False)):
    external: kdsl.autoscaling.v2beta2.ExternalMetricSource
    object: kdsl.autoscaling.v2beta2.ObjectMetricSource
    pods: kdsl.autoscaling.v2beta2.PodsMetricSource
    resource: kdsl.autoscaling.v2beta2.ResourceMetricSource


class MetricSpecTypedDict(MetricSpecOptionalTypedDict, total=(True)):
    type: str


MetricSpecUnion = Union[MetricSpec, MetricSpecTypedDict]


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
class HorizontalPodAutoscaler(K8sResource):
    apiVersion: ClassVar[str] = "autoscaling/v2beta2"
    kind: ClassVar[str] = "HorizontalPodAutoscaler"
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    spec: Union[
        None, OmitEnum, kdsl.autoscaling.v2beta2.HorizontalPodAutoscalerSpec
    ] = attr.ib(
        metadata={"yaml_name": "spec"},
        converter=kdsl.autoscaling.v2beta2_converters.optional_converter_HorizontalPodAutoscalerSpec,
        default=OMIT,
    )
    status: Union[
        None, OmitEnum, kdsl.autoscaling.v2beta2.HorizontalPodAutoscalerStatus
    ] = attr.ib(
        metadata={"yaml_name": "status"},
        converter=kdsl.autoscaling.v2beta2_converters.optional_converter_HorizontalPodAutoscalerStatus,
        default=OMIT,
    )


@attr.s(kw_only=True)
class MetricTarget(K8sObject):
    type: str = attr.ib(metadata={"yaml_name": "type"})
    averageUtilization: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "averageUtilization"}, default=OMIT
    )
    averageValue: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "averageValue"}, default=OMIT
    )
    value: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "value"}, default=OMIT
    )


class MetricTargetOptionalTypedDict(TypedDict, total=(False)):
    averageUtilization: int
    averageValue: str
    value: str


class MetricTargetTypedDict(MetricTargetOptionalTypedDict, total=(True)):
    type: str


MetricTargetUnion = Union[MetricTarget, MetricTargetTypedDict]


@attr.s(kw_only=True)
class HorizontalPodAutoscalerStatus(K8sObject):
    conditions: Sequence[
        kdsl.autoscaling.v2beta2.HorizontalPodAutoscalerCondition
    ] = attr.ib(
        metadata={"yaml_name": "conditions"},
        converter=kdsl.autoscaling.v2beta2_converters.required_list_converter_HorizontalPodAutoscalerCondition,
    )
    currentReplicas: int = attr.ib(metadata={"yaml_name": "currentReplicas"})
    desiredReplicas: int = attr.ib(metadata={"yaml_name": "desiredReplicas"})
    currentMetrics: Union[
        None, OmitEnum, Sequence[kdsl.autoscaling.v2beta2.MetricStatus]
    ] = attr.ib(
        metadata={"yaml_name": "currentMetrics"},
        converter=kdsl.autoscaling.v2beta2_converters.optional_list_converter_MetricStatus,
        default=OMIT,
    )
    lastScaleTime: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "lastScaleTime"}, default=OMIT
    )
    observedGeneration: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "observedGeneration"}, default=OMIT
    )


class HorizontalPodAutoscalerStatusOptionalTypedDict(TypedDict, total=(False)):
    currentMetrics: Sequence[kdsl.autoscaling.v2beta2.MetricStatus]
    lastScaleTime: str
    observedGeneration: int


class HorizontalPodAutoscalerStatusTypedDict(
    HorizontalPodAutoscalerStatusOptionalTypedDict, total=(True)
):
    conditions: Sequence[kdsl.autoscaling.v2beta2.HorizontalPodAutoscalerCondition]
    currentReplicas: int
    desiredReplicas: int


HorizontalPodAutoscalerStatusUnion = Union[
    HorizontalPodAutoscalerStatus, HorizontalPodAutoscalerStatusTypedDict
]


@attr.s(kw_only=True)
class ExternalMetricSource(K8sObject):
    metric: kdsl.autoscaling.v2beta2.MetricIdentifier = attr.ib(
        metadata={"yaml_name": "metric"},
        converter=kdsl.autoscaling.v2beta2_converters.required_converter_MetricIdentifier,
    )
    target: kdsl.autoscaling.v2beta2.MetricTarget = attr.ib(
        metadata={"yaml_name": "target"},
        converter=kdsl.autoscaling.v2beta2_converters.required_converter_MetricTarget,
    )


class ExternalMetricSourceTypedDict(TypedDict, total=(True)):
    metric: kdsl.autoscaling.v2beta2.MetricIdentifier
    target: kdsl.autoscaling.v2beta2.MetricTarget


ExternalMetricSourceUnion = Union[ExternalMetricSource, ExternalMetricSourceTypedDict]


@attr.s(kw_only=True)
class ObjectMetricSource(K8sObject):
    describedObject: kdsl.autoscaling.v2beta2.CrossVersionObjectReference = attr.ib(
        metadata={"yaml_name": "describedObject"},
        converter=kdsl.autoscaling.v2beta2_converters.required_converter_CrossVersionObjectReference,
    )
    metric: kdsl.autoscaling.v2beta2.MetricIdentifier = attr.ib(
        metadata={"yaml_name": "metric"},
        converter=kdsl.autoscaling.v2beta2_converters.required_converter_MetricIdentifier,
    )
    target: kdsl.autoscaling.v2beta2.MetricTarget = attr.ib(
        metadata={"yaml_name": "target"},
        converter=kdsl.autoscaling.v2beta2_converters.required_converter_MetricTarget,
    )


class ObjectMetricSourceTypedDict(TypedDict, total=(True)):
    describedObject: kdsl.autoscaling.v2beta2.CrossVersionObjectReference
    metric: kdsl.autoscaling.v2beta2.MetricIdentifier
    target: kdsl.autoscaling.v2beta2.MetricTarget


ObjectMetricSourceUnion = Union[ObjectMetricSource, ObjectMetricSourceTypedDict]


@attr.s(kw_only=True)
class MetricStatus(K8sObject):
    type: str = attr.ib(metadata={"yaml_name": "type"})
    external: Union[
        None, OmitEnum, kdsl.autoscaling.v2beta2.ExternalMetricStatus
    ] = attr.ib(
        metadata={"yaml_name": "external"},
        converter=kdsl.autoscaling.v2beta2_converters.optional_converter_ExternalMetricStatus,
        default=OMIT,
    )
    object: Union[
        None, OmitEnum, kdsl.autoscaling.v2beta2.ObjectMetricStatus
    ] = attr.ib(
        metadata={"yaml_name": "object"},
        converter=kdsl.autoscaling.v2beta2_converters.optional_converter_ObjectMetricStatus,
        default=OMIT,
    )
    pods: Union[None, OmitEnum, kdsl.autoscaling.v2beta2.PodsMetricStatus] = attr.ib(
        metadata={"yaml_name": "pods"},
        converter=kdsl.autoscaling.v2beta2_converters.optional_converter_PodsMetricStatus,
        default=OMIT,
    )
    resource: Union[
        None, OmitEnum, kdsl.autoscaling.v2beta2.ResourceMetricStatus
    ] = attr.ib(
        metadata={"yaml_name": "resource"},
        converter=kdsl.autoscaling.v2beta2_converters.optional_converter_ResourceMetricStatus,
        default=OMIT,
    )


class MetricStatusOptionalTypedDict(TypedDict, total=(False)):
    external: kdsl.autoscaling.v2beta2.ExternalMetricStatus
    object: kdsl.autoscaling.v2beta2.ObjectMetricStatus
    pods: kdsl.autoscaling.v2beta2.PodsMetricStatus
    resource: kdsl.autoscaling.v2beta2.ResourceMetricStatus


class MetricStatusTypedDict(MetricStatusOptionalTypedDict, total=(True)):
    type: str


MetricStatusUnion = Union[MetricStatus, MetricStatusTypedDict]
