from __future__ import annotations
import kdsl.autoscaling.v1_converters
import kdsl.core.v1
import kdsl.core.v1_converters
import kdsl.autoscaling.v1
import attr
from typing import Mapping, ClassVar, Optional, Any, Sequence, TypedDict, Union
from kdsl.bases import OmitEnum, K8sObject, OMIT, K8sResource


@attr.s(kw_only=True)
class HorizontalPodAutoscaler(K8sResource):
    apiVersion: ClassVar[str] = "autoscaling/v1"
    kind: ClassVar[str] = "HorizontalPodAutoscaler"
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    spec: Union[
        None, OmitEnum, kdsl.autoscaling.v1.HorizontalPodAutoscalerSpec
    ] = attr.ib(
        metadata={"yaml_name": "spec"},
        converter=kdsl.autoscaling.v1_converters.optional_converter_HorizontalPodAutoscalerSpec,
        default=OMIT,
    )
    status: Union[
        None, OmitEnum, kdsl.autoscaling.v1.HorizontalPodAutoscalerStatus
    ] = attr.ib(
        metadata={"yaml_name": "status"},
        converter=kdsl.autoscaling.v1_converters.optional_converter_HorizontalPodAutoscalerStatus,
        default=OMIT,
    )


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
class HorizontalPodAutoscalerStatus(K8sObject):
    currentReplicas: int = attr.ib(metadata={"yaml_name": "currentReplicas"})
    desiredReplicas: int = attr.ib(metadata={"yaml_name": "desiredReplicas"})
    currentCPUUtilizationPercentage: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "currentCPUUtilizationPercentage"}, default=OMIT
    )
    lastScaleTime: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "lastScaleTime"}, default=OMIT
    )
    observedGeneration: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "observedGeneration"}, default=OMIT
    )


class HorizontalPodAutoscalerStatusOptionalTypedDict(TypedDict, total=(False)):
    currentCPUUtilizationPercentage: int
    lastScaleTime: str
    observedGeneration: int


class HorizontalPodAutoscalerStatusTypedDict(
    HorizontalPodAutoscalerStatusOptionalTypedDict, total=(True)
):
    currentReplicas: int
    desiredReplicas: int


HorizontalPodAutoscalerStatusUnion = Union[
    HorizontalPodAutoscalerStatus, HorizontalPodAutoscalerStatusTypedDict
]


@attr.s(kw_only=True)
class HorizontalPodAutoscalerSpec(K8sObject):
    maxReplicas: int = attr.ib(metadata={"yaml_name": "maxReplicas"})
    scaleTargetRef: kdsl.autoscaling.v1.CrossVersionObjectReference = attr.ib(
        metadata={"yaml_name": "scaleTargetRef"},
        converter=kdsl.autoscaling.v1_converters.required_converter_CrossVersionObjectReference,
    )
    minReplicas: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "minReplicas"}, default=OMIT
    )
    targetCPUUtilizationPercentage: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "targetCPUUtilizationPercentage"}, default=OMIT
    )


class HorizontalPodAutoscalerSpecOptionalTypedDict(TypedDict, total=(False)):
    minReplicas: int
    targetCPUUtilizationPercentage: int


class HorizontalPodAutoscalerSpecTypedDict(
    HorizontalPodAutoscalerSpecOptionalTypedDict, total=(True)
):
    maxReplicas: int
    scaleTargetRef: kdsl.autoscaling.v1.CrossVersionObjectReference


HorizontalPodAutoscalerSpecUnion = Union[
    HorizontalPodAutoscalerSpec, HorizontalPodAutoscalerSpecTypedDict
]
