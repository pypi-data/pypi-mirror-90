from __future__ import annotations
import kdsl.core.v1
import kdsl.policy.v1beta1
import attr
import kdsl.core.v1_converters
import kdsl.policy.v1beta1_converters
from typing import Mapping, ClassVar, Optional, Any, Sequence, TypedDict, Union
from kdsl.bases import OmitEnum, K8sObject, OMIT, K8sResource


@attr.s(kw_only=True)
class PodDisruptionBudgetSpec(K8sObject):
    maxUnavailable: Union[None, OmitEnum, Union[int, str]] = attr.ib(
        metadata={"yaml_name": "maxUnavailable"}, default=OMIT
    )
    minAvailable: Union[None, OmitEnum, Union[int, str]] = attr.ib(
        metadata={"yaml_name": "minAvailable"}, default=OMIT
    )
    selector: Union[None, OmitEnum, kdsl.core.v1.LabelSelector] = attr.ib(
        metadata={"yaml_name": "selector"},
        converter=kdsl.core.v1_converters.optional_converter_LabelSelector,
        default=OMIT,
    )


class PodDisruptionBudgetSpecTypedDict(TypedDict, total=(False)):
    maxUnavailable: Union[int, str]
    minAvailable: Union[int, str]
    selector: kdsl.core.v1.LabelSelector


PodDisruptionBudgetSpecUnion = Union[
    PodDisruptionBudgetSpec, PodDisruptionBudgetSpecTypedDict
]


@attr.s(kw_only=True)
class AllowedHostPath(K8sObject):
    pathPrefix: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "pathPrefix"}, default=OMIT
    )
    readOnly: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "readOnly"}, default=OMIT
    )


class AllowedHostPathTypedDict(TypedDict, total=(False)):
    pathPrefix: str
    readOnly: bool


AllowedHostPathUnion = Union[AllowedHostPath, AllowedHostPathTypedDict]


@attr.s(kw_only=True)
class PodSecurityPolicy(K8sResource):
    apiVersion: ClassVar[str] = "policy/v1beta1"
    kind: ClassVar[str] = "PodSecurityPolicy"
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    spec: Union[None, OmitEnum, kdsl.policy.v1beta1.PodSecurityPolicySpec] = attr.ib(
        metadata={"yaml_name": "spec"},
        converter=kdsl.policy.v1beta1_converters.optional_converter_PodSecurityPolicySpec,
        default=OMIT,
    )


@attr.s(kw_only=True)
class RunAsGroupStrategyOptions(K8sObject):
    rule: str = attr.ib(metadata={"yaml_name": "rule"})
    ranges: Union[None, OmitEnum, Sequence[kdsl.policy.v1beta1.IDRange]] = attr.ib(
        metadata={"yaml_name": "ranges"},
        converter=kdsl.policy.v1beta1_converters.optional_list_converter_IDRange,
        default=OMIT,
    )


class RunAsGroupStrategyOptionsOptionalTypedDict(TypedDict, total=(False)):
    ranges: Sequence[kdsl.policy.v1beta1.IDRange]


class RunAsGroupStrategyOptionsTypedDict(
    RunAsGroupStrategyOptionsOptionalTypedDict, total=(True)
):
    rule: str


RunAsGroupStrategyOptionsUnion = Union[
    RunAsGroupStrategyOptions, RunAsGroupStrategyOptionsTypedDict
]


@attr.s(kw_only=True)
class PodSecurityPolicySpec(K8sObject):
    fsGroup: kdsl.policy.v1beta1.FSGroupStrategyOptions = attr.ib(
        metadata={"yaml_name": "fsGroup"},
        converter=kdsl.policy.v1beta1_converters.required_converter_FSGroupStrategyOptions,
    )
    runAsUser: kdsl.policy.v1beta1.RunAsUserStrategyOptions = attr.ib(
        metadata={"yaml_name": "runAsUser"},
        converter=kdsl.policy.v1beta1_converters.required_converter_RunAsUserStrategyOptions,
    )
    seLinux: kdsl.policy.v1beta1.SELinuxStrategyOptions = attr.ib(
        metadata={"yaml_name": "seLinux"},
        converter=kdsl.policy.v1beta1_converters.required_converter_SELinuxStrategyOptions,
    )
    supplementalGroups: kdsl.policy.v1beta1.SupplementalGroupsStrategyOptions = attr.ib(
        metadata={"yaml_name": "supplementalGroups"},
        converter=kdsl.policy.v1beta1_converters.required_converter_SupplementalGroupsStrategyOptions,
    )
    allowPrivilegeEscalation: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "allowPrivilegeEscalation"}, default=OMIT
    )
    allowedCSIDrivers: Union[
        None, OmitEnum, Sequence[kdsl.policy.v1beta1.AllowedCSIDriver]
    ] = attr.ib(
        metadata={"yaml_name": "allowedCSIDrivers"},
        converter=kdsl.policy.v1beta1_converters.optional_list_converter_AllowedCSIDriver,
        default=OMIT,
    )
    allowedCapabilities: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "allowedCapabilities"}, default=OMIT
    )
    allowedFlexVolumes: Union[
        None, OmitEnum, Sequence[kdsl.policy.v1beta1.AllowedFlexVolume]
    ] = attr.ib(
        metadata={"yaml_name": "allowedFlexVolumes"},
        converter=kdsl.policy.v1beta1_converters.optional_list_converter_AllowedFlexVolume,
        default=OMIT,
    )
    allowedHostPaths: Union[
        None, OmitEnum, Sequence[kdsl.policy.v1beta1.AllowedHostPath]
    ] = attr.ib(
        metadata={"yaml_name": "allowedHostPaths"},
        converter=kdsl.policy.v1beta1_converters.optional_list_converter_AllowedHostPath,
        default=OMIT,
    )
    allowedProcMountTypes: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "allowedProcMountTypes"}, default=OMIT
    )
    allowedUnsafeSysctls: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "allowedUnsafeSysctls"}, default=OMIT
    )
    defaultAddCapabilities: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "defaultAddCapabilities"}, default=OMIT
    )
    defaultAllowPrivilegeEscalation: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "defaultAllowPrivilegeEscalation"}, default=OMIT
    )
    forbiddenSysctls: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "forbiddenSysctls"}, default=OMIT
    )
    hostIPC: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "hostIPC"}, default=OMIT
    )
    hostNetwork: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "hostNetwork"}, default=OMIT
    )
    hostPID: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "hostPID"}, default=OMIT
    )
    hostPorts: Union[
        None, OmitEnum, Sequence[kdsl.policy.v1beta1.HostPortRange]
    ] = attr.ib(
        metadata={"yaml_name": "hostPorts"},
        converter=kdsl.policy.v1beta1_converters.optional_list_converter_HostPortRange,
        default=OMIT,
    )
    privileged: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "privileged"}, default=OMIT
    )
    readOnlyRootFilesystem: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "readOnlyRootFilesystem"}, default=OMIT
    )
    requiredDropCapabilities: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "requiredDropCapabilities"}, default=OMIT
    )
    runAsGroup: Union[
        None, OmitEnum, kdsl.policy.v1beta1.RunAsGroupStrategyOptions
    ] = attr.ib(
        metadata={"yaml_name": "runAsGroup"},
        converter=kdsl.policy.v1beta1_converters.optional_converter_RunAsGroupStrategyOptions,
        default=OMIT,
    )
    runtimeClass: Union[
        None, OmitEnum, kdsl.policy.v1beta1.RuntimeClassStrategyOptions
    ] = attr.ib(
        metadata={"yaml_name": "runtimeClass"},
        converter=kdsl.policy.v1beta1_converters.optional_converter_RuntimeClassStrategyOptions,
        default=OMIT,
    )
    volumes: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "volumes"}, default=OMIT
    )


class PodSecurityPolicySpecOptionalTypedDict(TypedDict, total=(False)):
    allowPrivilegeEscalation: bool
    allowedCSIDrivers: Sequence[kdsl.policy.v1beta1.AllowedCSIDriver]
    allowedCapabilities: Sequence[str]
    allowedFlexVolumes: Sequence[kdsl.policy.v1beta1.AllowedFlexVolume]
    allowedHostPaths: Sequence[kdsl.policy.v1beta1.AllowedHostPath]
    allowedProcMountTypes: Sequence[str]
    allowedUnsafeSysctls: Sequence[str]
    defaultAddCapabilities: Sequence[str]
    defaultAllowPrivilegeEscalation: bool
    forbiddenSysctls: Sequence[str]
    hostIPC: bool
    hostNetwork: bool
    hostPID: bool
    hostPorts: Sequence[kdsl.policy.v1beta1.HostPortRange]
    privileged: bool
    readOnlyRootFilesystem: bool
    requiredDropCapabilities: Sequence[str]
    runAsGroup: kdsl.policy.v1beta1.RunAsGroupStrategyOptions
    runtimeClass: kdsl.policy.v1beta1.RuntimeClassStrategyOptions
    volumes: Sequence[str]


class PodSecurityPolicySpecTypedDict(
    PodSecurityPolicySpecOptionalTypedDict, total=(True)
):
    fsGroup: kdsl.policy.v1beta1.FSGroupStrategyOptions
    runAsUser: kdsl.policy.v1beta1.RunAsUserStrategyOptions
    seLinux: kdsl.policy.v1beta1.SELinuxStrategyOptions
    supplementalGroups: kdsl.policy.v1beta1.SupplementalGroupsStrategyOptions


PodSecurityPolicySpecUnion = Union[
    PodSecurityPolicySpec, PodSecurityPolicySpecTypedDict
]


@attr.s(kw_only=True)
class RunAsUserStrategyOptions(K8sObject):
    rule: str = attr.ib(metadata={"yaml_name": "rule"})
    ranges: Union[None, OmitEnum, Sequence[kdsl.policy.v1beta1.IDRange]] = attr.ib(
        metadata={"yaml_name": "ranges"},
        converter=kdsl.policy.v1beta1_converters.optional_list_converter_IDRange,
        default=OMIT,
    )


class RunAsUserStrategyOptionsOptionalTypedDict(TypedDict, total=(False)):
    ranges: Sequence[kdsl.policy.v1beta1.IDRange]


class RunAsUserStrategyOptionsTypedDict(
    RunAsUserStrategyOptionsOptionalTypedDict, total=(True)
):
    rule: str


RunAsUserStrategyOptionsUnion = Union[
    RunAsUserStrategyOptions, RunAsUserStrategyOptionsTypedDict
]


@attr.s(kw_only=True)
class FSGroupStrategyOptions(K8sObject):
    ranges: Union[None, OmitEnum, Sequence[kdsl.policy.v1beta1.IDRange]] = attr.ib(
        metadata={"yaml_name": "ranges"},
        converter=kdsl.policy.v1beta1_converters.optional_list_converter_IDRange,
        default=OMIT,
    )
    rule: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "rule"}, default=OMIT
    )


class FSGroupStrategyOptionsTypedDict(TypedDict, total=(False)):
    ranges: Sequence[kdsl.policy.v1beta1.IDRange]
    rule: str


FSGroupStrategyOptionsUnion = Union[
    FSGroupStrategyOptions, FSGroupStrategyOptionsTypedDict
]


@attr.s(kw_only=True)
class HostPortRange(K8sObject):
    max: int = attr.ib(metadata={"yaml_name": "max"})
    min: int = attr.ib(metadata={"yaml_name": "min"})


class HostPortRangeTypedDict(TypedDict, total=(True)):
    max: int
    min: int


HostPortRangeUnion = Union[HostPortRange, HostPortRangeTypedDict]


@attr.s(kw_only=True)
class PodDisruptionBudget(K8sResource):
    apiVersion: ClassVar[str] = "policy/v1beta1"
    kind: ClassVar[str] = "PodDisruptionBudget"
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    spec: Union[None, OmitEnum, kdsl.policy.v1beta1.PodDisruptionBudgetSpec] = attr.ib(
        metadata={"yaml_name": "spec"},
        converter=kdsl.policy.v1beta1_converters.optional_converter_PodDisruptionBudgetSpec,
        default=OMIT,
    )
    status: Union[
        None, OmitEnum, kdsl.policy.v1beta1.PodDisruptionBudgetStatus
    ] = attr.ib(
        metadata={"yaml_name": "status"},
        converter=kdsl.policy.v1beta1_converters.optional_converter_PodDisruptionBudgetStatus,
        default=OMIT,
    )


@attr.s(kw_only=True)
class IDRange(K8sObject):
    max: int = attr.ib(metadata={"yaml_name": "max"})
    min: int = attr.ib(metadata={"yaml_name": "min"})


class IDRangeTypedDict(TypedDict, total=(True)):
    max: int
    min: int


IDRangeUnion = Union[IDRange, IDRangeTypedDict]


@attr.s(kw_only=True)
class RuntimeClassStrategyOptions(K8sObject):
    allowedRuntimeClassNames: Sequence[str] = attr.ib(
        metadata={"yaml_name": "allowedRuntimeClassNames"}
    )
    defaultRuntimeClassName: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "defaultRuntimeClassName"}, default=OMIT
    )


class RuntimeClassStrategyOptionsOptionalTypedDict(TypedDict, total=(False)):
    defaultRuntimeClassName: str


class RuntimeClassStrategyOptionsTypedDict(
    RuntimeClassStrategyOptionsOptionalTypedDict, total=(True)
):
    allowedRuntimeClassNames: Sequence[str]


RuntimeClassStrategyOptionsUnion = Union[
    RuntimeClassStrategyOptions, RuntimeClassStrategyOptionsTypedDict
]


@attr.s(kw_only=True)
class AllowedCSIDriver(K8sObject):
    name: str = attr.ib(metadata={"yaml_name": "name"})


class AllowedCSIDriverTypedDict(TypedDict, total=(True)):
    name: str


AllowedCSIDriverUnion = Union[AllowedCSIDriver, AllowedCSIDriverTypedDict]


@attr.s(kw_only=True)
class Eviction(K8sResource):
    apiVersion: ClassVar[str] = "policy/v1beta1"
    kind: ClassVar[str] = "Eviction"
    deleteOptions: Union[None, OmitEnum, kdsl.core.v1.DeleteOptions] = attr.ib(
        metadata={"yaml_name": "deleteOptions"},
        converter=kdsl.core.v1_converters.optional_converter_DeleteOptions,
        default=OMIT,
    )
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )


@attr.s(kw_only=True)
class SELinuxStrategyOptions(K8sObject):
    rule: str = attr.ib(metadata={"yaml_name": "rule"})
    seLinuxOptions: Union[None, OmitEnum, kdsl.core.v1.SELinuxOptions] = attr.ib(
        metadata={"yaml_name": "seLinuxOptions"},
        converter=kdsl.core.v1_converters.optional_converter_SELinuxOptions,
        default=OMIT,
    )


class SELinuxStrategyOptionsOptionalTypedDict(TypedDict, total=(False)):
    seLinuxOptions: kdsl.core.v1.SELinuxOptions


class SELinuxStrategyOptionsTypedDict(
    SELinuxStrategyOptionsOptionalTypedDict, total=(True)
):
    rule: str


SELinuxStrategyOptionsUnion = Union[
    SELinuxStrategyOptions, SELinuxStrategyOptionsTypedDict
]


@attr.s(kw_only=True)
class PodDisruptionBudgetStatus(K8sObject):
    currentHealthy: int = attr.ib(metadata={"yaml_name": "currentHealthy"})
    desiredHealthy: int = attr.ib(metadata={"yaml_name": "desiredHealthy"})
    disruptionsAllowed: int = attr.ib(metadata={"yaml_name": "disruptionsAllowed"})
    expectedPods: int = attr.ib(metadata={"yaml_name": "expectedPods"})
    disruptedPods: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(
        metadata={"yaml_name": "disruptedPods"}, default=OMIT
    )
    observedGeneration: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "observedGeneration"}, default=OMIT
    )


class PodDisruptionBudgetStatusOptionalTypedDict(TypedDict, total=(False)):
    disruptedPods: Mapping[str, str]
    observedGeneration: int


class PodDisruptionBudgetStatusTypedDict(
    PodDisruptionBudgetStatusOptionalTypedDict, total=(True)
):
    currentHealthy: int
    desiredHealthy: int
    disruptionsAllowed: int
    expectedPods: int


PodDisruptionBudgetStatusUnion = Union[
    PodDisruptionBudgetStatus, PodDisruptionBudgetStatusTypedDict
]


@attr.s(kw_only=True)
class AllowedFlexVolume(K8sObject):
    driver: str = attr.ib(metadata={"yaml_name": "driver"})


class AllowedFlexVolumeTypedDict(TypedDict, total=(True)):
    driver: str


AllowedFlexVolumeUnion = Union[AllowedFlexVolume, AllowedFlexVolumeTypedDict]


@attr.s(kw_only=True)
class SupplementalGroupsStrategyOptions(K8sObject):
    ranges: Union[None, OmitEnum, Sequence[kdsl.policy.v1beta1.IDRange]] = attr.ib(
        metadata={"yaml_name": "ranges"},
        converter=kdsl.policy.v1beta1_converters.optional_list_converter_IDRange,
        default=OMIT,
    )
    rule: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "rule"}, default=OMIT
    )


class SupplementalGroupsStrategyOptionsTypedDict(TypedDict, total=(False)):
    ranges: Sequence[kdsl.policy.v1beta1.IDRange]
    rule: str


SupplementalGroupsStrategyOptionsUnion = Union[
    SupplementalGroupsStrategyOptions, SupplementalGroupsStrategyOptionsTypedDict
]
