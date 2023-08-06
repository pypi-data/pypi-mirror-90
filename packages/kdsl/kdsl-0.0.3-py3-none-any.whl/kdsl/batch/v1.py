from __future__ import annotations
import kdsl.core.v1_converters
import kdsl.batch.v1
import kdsl.core.v1
import kdsl.batch.v1_converters
import attr
from typing import Mapping, ClassVar, Optional, Any, Sequence, TypedDict, Union
from kdsl.bases import OmitEnum, K8sObject, OMIT, K8sResource


@attr.s(kw_only=True)
class JobConditionItem(K8sObject):
    status: str = attr.ib(metadata={"yaml_name": "status"})
    lastProbeTime: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "lastProbeTime"}, default=OMIT
    )
    lastTransitionTime: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "lastTransitionTime"}, default=OMIT
    )
    message: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "message"}, default=OMIT
    )
    reason: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "reason"}, default=OMIT
    )


class JobConditionItemOptionalTypedDict(TypedDict, total=(False)):
    lastProbeTime: str
    lastTransitionTime: str
    message: str
    reason: str


class JobConditionItemTypedDict(JobConditionItemOptionalTypedDict, total=(True)):
    status: str


JobConditionItemUnion = Union[JobConditionItem, JobConditionItemTypedDict]


@attr.s(kw_only=True)
class JobStatus(K8sObject):
    active: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "active"}, default=OMIT
    )
    completionTime: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "completionTime"}, default=OMIT
    )
    conditions: Union[
        None, OmitEnum, Mapping[str, kdsl.batch.v1.JobConditionItem]
    ] = attr.ib(
        metadata={"yaml_name": "conditions", "mlist_key": "type"},
        converter=kdsl.batch.v1_converters.optional_mlist_converter_JobConditionItem,
        default=OMIT,
    )
    failed: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "failed"}, default=OMIT
    )
    startTime: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "startTime"}, default=OMIT
    )
    succeeded: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "succeeded"}, default=OMIT
    )


class JobStatusTypedDict(TypedDict, total=(False)):
    active: int
    completionTime: str
    conditions: Mapping[str, kdsl.batch.v1.JobConditionItem]
    failed: int
    startTime: str
    succeeded: int


JobStatusUnion = Union[JobStatus, JobStatusTypedDict]


@attr.s(kw_only=True)
class JobSpec(K8sObject):
    template: kdsl.core.v1.PodTemplateSpec = attr.ib(
        metadata={"yaml_name": "template"},
        converter=kdsl.core.v1_converters.required_converter_PodTemplateSpec,
    )
    activeDeadlineSeconds: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "activeDeadlineSeconds"}, default=OMIT
    )
    backoffLimit: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "backoffLimit"}, default=OMIT
    )
    completions: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "completions"}, default=OMIT
    )
    manualSelector: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "manualSelector"}, default=OMIT
    )
    parallelism: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "parallelism"}, default=OMIT
    )
    selector: Union[None, OmitEnum, kdsl.core.v1.LabelSelector] = attr.ib(
        metadata={"yaml_name": "selector"},
        converter=kdsl.core.v1_converters.optional_converter_LabelSelector,
        default=OMIT,
    )
    ttlSecondsAfterFinished: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "ttlSecondsAfterFinished"}, default=OMIT
    )


class JobSpecOptionalTypedDict(TypedDict, total=(False)):
    activeDeadlineSeconds: int
    backoffLimit: int
    completions: int
    manualSelector: bool
    parallelism: int
    selector: kdsl.core.v1.LabelSelector
    ttlSecondsAfterFinished: int


class JobSpecTypedDict(JobSpecOptionalTypedDict, total=(True)):
    template: kdsl.core.v1.PodTemplateSpec


JobSpecUnion = Union[JobSpec, JobSpecTypedDict]


@attr.s(kw_only=True)
class Job(K8sResource):
    apiVersion: ClassVar[str] = "batch/v1"
    kind: ClassVar[str] = "Job"
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    spec: Union[None, OmitEnum, kdsl.batch.v1.JobSpec] = attr.ib(
        metadata={"yaml_name": "spec"},
        converter=kdsl.batch.v1_converters.optional_converter_JobSpec,
        default=OMIT,
    )
    status: Union[None, OmitEnum, kdsl.batch.v1.JobStatus] = attr.ib(
        metadata={"yaml_name": "status"},
        converter=kdsl.batch.v1_converters.optional_converter_JobStatus,
        default=OMIT,
    )
