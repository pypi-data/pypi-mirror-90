from __future__ import annotations
import kdsl.batch.v1beta1
import kdsl.batch.v1beta1_converters
import kdsl.core.v1_converters
import kdsl.batch.v1
import kdsl.core.v1
import kdsl.batch.v1_converters
import attr
from typing import Mapping, ClassVar, Optional, Any, Sequence, TypedDict, Union
from kdsl.bases import OmitEnum, K8sObject, OMIT, K8sResource


@attr.s(kw_only=True)
class CronJob(K8sResource):
    apiVersion: ClassVar[str] = "batch/v1beta1"
    kind: ClassVar[str] = "CronJob"
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    spec: Union[None, OmitEnum, kdsl.batch.v1beta1.CronJobSpec] = attr.ib(
        metadata={"yaml_name": "spec"},
        converter=kdsl.batch.v1beta1_converters.optional_converter_CronJobSpec,
        default=OMIT,
    )
    status: Union[None, OmitEnum, kdsl.batch.v1beta1.CronJobStatus] = attr.ib(
        metadata={"yaml_name": "status"},
        converter=kdsl.batch.v1beta1_converters.optional_converter_CronJobStatus,
        default=OMIT,
    )


@attr.s(kw_only=True)
class CronJobStatus(K8sObject):
    active: Union[None, OmitEnum, Sequence[kdsl.core.v1.ObjectReference]] = attr.ib(
        metadata={"yaml_name": "active"},
        converter=kdsl.core.v1_converters.optional_list_converter_ObjectReference,
        default=OMIT,
    )
    lastScheduleTime: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "lastScheduleTime"}, default=OMIT
    )


class CronJobStatusTypedDict(TypedDict, total=(False)):
    active: Sequence[kdsl.core.v1.ObjectReference]
    lastScheduleTime: str


CronJobStatusUnion = Union[CronJobStatus, CronJobStatusTypedDict]


@attr.s(kw_only=True)
class CronJobSpec(K8sObject):
    jobTemplate: kdsl.batch.v1beta1.JobTemplateSpec = attr.ib(
        metadata={"yaml_name": "jobTemplate"},
        converter=kdsl.batch.v1beta1_converters.required_converter_JobTemplateSpec,
    )
    schedule: str = attr.ib(metadata={"yaml_name": "schedule"})
    concurrencyPolicy: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "concurrencyPolicy"}, default=OMIT
    )
    failedJobsHistoryLimit: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "failedJobsHistoryLimit"}, default=OMIT
    )
    startingDeadlineSeconds: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "startingDeadlineSeconds"}, default=OMIT
    )
    successfulJobsHistoryLimit: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "successfulJobsHistoryLimit"}, default=OMIT
    )
    suspend: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "suspend"}, default=OMIT
    )


class CronJobSpecOptionalTypedDict(TypedDict, total=(False)):
    concurrencyPolicy: str
    failedJobsHistoryLimit: int
    startingDeadlineSeconds: int
    successfulJobsHistoryLimit: int
    suspend: bool


class CronJobSpecTypedDict(CronJobSpecOptionalTypedDict, total=(True)):
    jobTemplate: kdsl.batch.v1beta1.JobTemplateSpec
    schedule: str


CronJobSpecUnion = Union[CronJobSpec, CronJobSpecTypedDict]


@attr.s(kw_only=True)
class JobTemplateSpec(K8sObject):
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


class JobTemplateSpecTypedDict(TypedDict, total=(False)):
    metadata: kdsl.core.v1.ObjectMeta
    spec: kdsl.batch.v1.JobSpec


JobTemplateSpecUnion = Union[JobTemplateSpec, JobTemplateSpecTypedDict]
