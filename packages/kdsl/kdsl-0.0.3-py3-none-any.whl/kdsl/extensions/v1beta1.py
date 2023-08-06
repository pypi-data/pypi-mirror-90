from __future__ import annotations
import kdsl.extensions.v1beta1
import kdsl.core.v1
import kdsl.core.v1_converters
import attr
import kdsl.extensions.v1beta1_converters
from typing import Mapping, ClassVar, Optional, Any, Sequence, TypedDict, Union
from kdsl.bases import OmitEnum, K8sObject, OMIT, K8sResource


@attr.s(kw_only=True)
class RunAsUserStrategyOptions(K8sObject):
    rule: str = attr.ib(metadata={"yaml_name": "rule"})
    ranges: Union[None, OmitEnum, Sequence[kdsl.extensions.v1beta1.IDRange]] = attr.ib(
        metadata={"yaml_name": "ranges"},
        converter=kdsl.extensions.v1beta1_converters.optional_list_converter_IDRange,
        default=OMIT,
    )


class RunAsUserStrategyOptionsOptionalTypedDict(TypedDict, total=(False)):
    ranges: Sequence[kdsl.extensions.v1beta1.IDRange]


class RunAsUserStrategyOptionsTypedDict(
    RunAsUserStrategyOptionsOptionalTypedDict, total=(True)
):
    rule: str


RunAsUserStrategyOptionsUnion = Union[
    RunAsUserStrategyOptions, RunAsUserStrategyOptionsTypedDict
]


@attr.s(kw_only=True)
class Ingress(K8sResource):
    apiVersion: ClassVar[str] = "extensions/v1beta1"
    kind: ClassVar[str] = "Ingress"
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    spec: Union[None, OmitEnum, kdsl.extensions.v1beta1.IngressSpec] = attr.ib(
        metadata={"yaml_name": "spec"},
        converter=kdsl.extensions.v1beta1_converters.optional_converter_IngressSpec,
        default=OMIT,
    )
    status: Union[None, OmitEnum, kdsl.extensions.v1beta1.IngressStatus] = attr.ib(
        metadata={"yaml_name": "status"},
        converter=kdsl.extensions.v1beta1_converters.optional_converter_IngressStatus,
        default=OMIT,
    )


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
class NetworkPolicyEgressRule(K8sObject):
    ports: Union[
        None, OmitEnum, Sequence[kdsl.extensions.v1beta1.NetworkPolicyPort]
    ] = attr.ib(
        metadata={"yaml_name": "ports"},
        converter=kdsl.extensions.v1beta1_converters.optional_list_converter_NetworkPolicyPort,
        default=OMIT,
    )
    to: Union[
        None, OmitEnum, Sequence[kdsl.extensions.v1beta1.NetworkPolicyPeer]
    ] = attr.ib(
        metadata={"yaml_name": "to"},
        converter=kdsl.extensions.v1beta1_converters.optional_list_converter_NetworkPolicyPeer,
        default=OMIT,
    )


class NetworkPolicyEgressRuleTypedDict(TypedDict, total=(False)):
    ports: Sequence[kdsl.extensions.v1beta1.NetworkPolicyPort]
    to: Sequence[kdsl.extensions.v1beta1.NetworkPolicyPeer]


NetworkPolicyEgressRuleUnion = Union[
    NetworkPolicyEgressRule, NetworkPolicyEgressRuleTypedDict
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
class RollbackConfig(K8sObject):
    revision: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "revision"}, default=OMIT
    )


class RollbackConfigTypedDict(TypedDict, total=(False)):
    revision: int


RollbackConfigUnion = Union[RollbackConfig, RollbackConfigTypedDict]


@attr.s(kw_only=True)
class DaemonSetUpdateStrategy(K8sObject):
    rollingUpdate: Union[
        None, OmitEnum, kdsl.extensions.v1beta1.RollingUpdateDaemonSet
    ] = attr.ib(
        metadata={"yaml_name": "rollingUpdate"},
        converter=kdsl.extensions.v1beta1_converters.optional_converter_RollingUpdateDaemonSet,
        default=OMIT,
    )
    type: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "type"}, default=OMIT
    )


class DaemonSetUpdateStrategyTypedDict(TypedDict, total=(False)):
    rollingUpdate: kdsl.extensions.v1beta1.RollingUpdateDaemonSet
    type: str


DaemonSetUpdateStrategyUnion = Union[
    DaemonSetUpdateStrategy, DaemonSetUpdateStrategyTypedDict
]


@attr.s(kw_only=True)
class DaemonSetStatus(K8sObject):
    currentNumberScheduled: int = attr.ib(
        metadata={"yaml_name": "currentNumberScheduled"}
    )
    desiredNumberScheduled: int = attr.ib(
        metadata={"yaml_name": "desiredNumberScheduled"}
    )
    numberMisscheduled: int = attr.ib(metadata={"yaml_name": "numberMisscheduled"})
    numberReady: int = attr.ib(metadata={"yaml_name": "numberReady"})
    collisionCount: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "collisionCount"}, default=OMIT
    )
    conditions: Union[
        None, OmitEnum, Mapping[str, kdsl.extensions.v1beta1.DaemonSetConditionItem]
    ] = attr.ib(
        metadata={"yaml_name": "conditions", "mlist_key": "type"},
        converter=kdsl.extensions.v1beta1_converters.optional_mlist_converter_DaemonSetConditionItem,
        default=OMIT,
    )
    numberAvailable: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "numberAvailable"}, default=OMIT
    )
    numberUnavailable: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "numberUnavailable"}, default=OMIT
    )
    observedGeneration: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "observedGeneration"}, default=OMIT
    )
    updatedNumberScheduled: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "updatedNumberScheduled"}, default=OMIT
    )


class DaemonSetStatusOptionalTypedDict(TypedDict, total=(False)):
    collisionCount: int
    conditions: Mapping[str, kdsl.extensions.v1beta1.DaemonSetConditionItem]
    numberAvailable: int
    numberUnavailable: int
    observedGeneration: int
    updatedNumberScheduled: int


class DaemonSetStatusTypedDict(DaemonSetStatusOptionalTypedDict, total=(True)):
    currentNumberScheduled: int
    desiredNumberScheduled: int
    numberMisscheduled: int
    numberReady: int


DaemonSetStatusUnion = Union[DaemonSetStatus, DaemonSetStatusTypedDict]


@attr.s(kw_only=True)
class RollingUpdateDeployment(K8sObject):
    maxSurge: Union[None, OmitEnum, Union[int, str]] = attr.ib(
        metadata={"yaml_name": "maxSurge"}, default=OMIT
    )
    maxUnavailable: Union[None, OmitEnum, Union[int, str]] = attr.ib(
        metadata={"yaml_name": "maxUnavailable"}, default=OMIT
    )


class RollingUpdateDeploymentTypedDict(TypedDict, total=(False)):
    maxSurge: Union[int, str]
    maxUnavailable: Union[int, str]


RollingUpdateDeploymentUnion = Union[
    RollingUpdateDeployment, RollingUpdateDeploymentTypedDict
]


@attr.s(kw_only=True)
class NetworkPolicy(K8sResource):
    apiVersion: ClassVar[str] = "extensions/v1beta1"
    kind: ClassVar[str] = "NetworkPolicy"
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    spec: Union[None, OmitEnum, kdsl.extensions.v1beta1.NetworkPolicySpec] = attr.ib(
        metadata={"yaml_name": "spec"},
        converter=kdsl.extensions.v1beta1_converters.optional_converter_NetworkPolicySpec,
        default=OMIT,
    )


@attr.s(kw_only=True)
class IngressBackend(K8sObject):
    serviceName: str = attr.ib(metadata={"yaml_name": "serviceName"})
    servicePort: Union[int, str] = attr.ib(metadata={"yaml_name": "servicePort"})


class IngressBackendTypedDict(TypedDict, total=(True)):
    serviceName: str
    servicePort: Union[int, str]


IngressBackendUnion = Union[IngressBackend, IngressBackendTypedDict]


@attr.s(kw_only=True)
class ReplicaSetConditionItem(K8sObject):
    status: str = attr.ib(metadata={"yaml_name": "status"})
    lastTransitionTime: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "lastTransitionTime"}, default=OMIT
    )
    message: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "message"}, default=OMIT
    )
    reason: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "reason"}, default=OMIT
    )


class ReplicaSetConditionItemOptionalTypedDict(TypedDict, total=(False)):
    lastTransitionTime: str
    message: str
    reason: str


class ReplicaSetConditionItemTypedDict(
    ReplicaSetConditionItemOptionalTypedDict, total=(True)
):
    status: str


ReplicaSetConditionItemUnion = Union[
    ReplicaSetConditionItem, ReplicaSetConditionItemTypedDict
]


@attr.s(kw_only=True)
class FSGroupStrategyOptions(K8sObject):
    ranges: Union[None, OmitEnum, Sequence[kdsl.extensions.v1beta1.IDRange]] = attr.ib(
        metadata={"yaml_name": "ranges"},
        converter=kdsl.extensions.v1beta1_converters.optional_list_converter_IDRange,
        default=OMIT,
    )
    rule: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "rule"}, default=OMIT
    )


class FSGroupStrategyOptionsTypedDict(TypedDict, total=(False)):
    ranges: Sequence[kdsl.extensions.v1beta1.IDRange]
    rule: str


FSGroupStrategyOptionsUnion = Union[
    FSGroupStrategyOptions, FSGroupStrategyOptionsTypedDict
]


@attr.s(kw_only=True)
class IngressTLS(K8sObject):
    hosts: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "hosts"}, default=OMIT
    )
    secretName: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "secretName"}, default=OMIT
    )


class IngressTLSTypedDict(TypedDict, total=(False)):
    hosts: Sequence[str]
    secretName: str


IngressTLSUnion = Union[IngressTLS, IngressTLSTypedDict]


@attr.s(kw_only=True)
class ReplicaSetSpec(K8sObject):
    minReadySeconds: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "minReadySeconds"}, default=OMIT
    )
    replicas: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "replicas"}, default=OMIT
    )
    selector: Union[None, OmitEnum, kdsl.core.v1.LabelSelector] = attr.ib(
        metadata={"yaml_name": "selector"},
        converter=kdsl.core.v1_converters.optional_converter_LabelSelector,
        default=OMIT,
    )
    template: Union[None, OmitEnum, kdsl.core.v1.PodTemplateSpec] = attr.ib(
        metadata={"yaml_name": "template"},
        converter=kdsl.core.v1_converters.optional_converter_PodTemplateSpec,
        default=OMIT,
    )


class ReplicaSetSpecTypedDict(TypedDict, total=(False)):
    minReadySeconds: int
    replicas: int
    selector: kdsl.core.v1.LabelSelector
    template: kdsl.core.v1.PodTemplateSpec


ReplicaSetSpecUnion = Union[ReplicaSetSpec, ReplicaSetSpecTypedDict]


@attr.s(kw_only=True)
class RollingUpdateDaemonSet(K8sObject):
    maxUnavailable: Union[None, OmitEnum, Union[int, str]] = attr.ib(
        metadata={"yaml_name": "maxUnavailable"}, default=OMIT
    )


class RollingUpdateDaemonSetTypedDict(TypedDict, total=(False)):
    maxUnavailable: Union[int, str]


RollingUpdateDaemonSetUnion = Union[
    RollingUpdateDaemonSet, RollingUpdateDaemonSetTypedDict
]


@attr.s(kw_only=True)
class NetworkPolicySpec(K8sObject):
    podSelector: kdsl.core.v1.LabelSelector = attr.ib(
        metadata={"yaml_name": "podSelector"},
        converter=kdsl.core.v1_converters.required_converter_LabelSelector,
    )
    egress: Union[
        None, OmitEnum, Sequence[kdsl.extensions.v1beta1.NetworkPolicyEgressRule]
    ] = attr.ib(
        metadata={"yaml_name": "egress"},
        converter=kdsl.extensions.v1beta1_converters.optional_list_converter_NetworkPolicyEgressRule,
        default=OMIT,
    )
    ingress: Union[
        None, OmitEnum, Sequence[kdsl.extensions.v1beta1.NetworkPolicyIngressRule]
    ] = attr.ib(
        metadata={"yaml_name": "ingress"},
        converter=kdsl.extensions.v1beta1_converters.optional_list_converter_NetworkPolicyIngressRule,
        default=OMIT,
    )
    policyTypes: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "policyTypes"}, default=OMIT
    )


class NetworkPolicySpecOptionalTypedDict(TypedDict, total=(False)):
    egress: Sequence[kdsl.extensions.v1beta1.NetworkPolicyEgressRule]
    ingress: Sequence[kdsl.extensions.v1beta1.NetworkPolicyIngressRule]
    policyTypes: Sequence[str]


class NetworkPolicySpecTypedDict(NetworkPolicySpecOptionalTypedDict, total=(True)):
    podSelector: kdsl.core.v1.LabelSelector


NetworkPolicySpecUnion = Union[NetworkPolicySpec, NetworkPolicySpecTypedDict]


@attr.s(kw_only=True)
class DeploymentStrategy(K8sObject):
    rollingUpdate: Union[
        None, OmitEnum, kdsl.extensions.v1beta1.RollingUpdateDeployment
    ] = attr.ib(
        metadata={"yaml_name": "rollingUpdate"},
        converter=kdsl.extensions.v1beta1_converters.optional_converter_RollingUpdateDeployment,
        default=OMIT,
    )
    type: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "type"}, default=OMIT
    )


class DeploymentStrategyTypedDict(TypedDict, total=(False)):
    rollingUpdate: kdsl.extensions.v1beta1.RollingUpdateDeployment
    type: str


DeploymentStrategyUnion = Union[DeploymentStrategy, DeploymentStrategyTypedDict]


@attr.s(kw_only=True)
class ReplicaSet(K8sResource):
    apiVersion: ClassVar[str] = "extensions/v1beta1"
    kind: ClassVar[str] = "ReplicaSet"
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    spec: Union[None, OmitEnum, kdsl.extensions.v1beta1.ReplicaSetSpec] = attr.ib(
        metadata={"yaml_name": "spec"},
        converter=kdsl.extensions.v1beta1_converters.optional_converter_ReplicaSetSpec,
        default=OMIT,
    )
    status: Union[None, OmitEnum, kdsl.extensions.v1beta1.ReplicaSetStatus] = attr.ib(
        metadata={"yaml_name": "status"},
        converter=kdsl.extensions.v1beta1_converters.optional_converter_ReplicaSetStatus,
        default=OMIT,
    )


@attr.s(kw_only=True)
class PodSecurityPolicySpec(K8sObject):
    fsGroup: kdsl.extensions.v1beta1.FSGroupStrategyOptions = attr.ib(
        metadata={"yaml_name": "fsGroup"},
        converter=kdsl.extensions.v1beta1_converters.required_converter_FSGroupStrategyOptions,
    )
    runAsUser: kdsl.extensions.v1beta1.RunAsUserStrategyOptions = attr.ib(
        metadata={"yaml_name": "runAsUser"},
        converter=kdsl.extensions.v1beta1_converters.required_converter_RunAsUserStrategyOptions,
    )
    seLinux: kdsl.extensions.v1beta1.SELinuxStrategyOptions = attr.ib(
        metadata={"yaml_name": "seLinux"},
        converter=kdsl.extensions.v1beta1_converters.required_converter_SELinuxStrategyOptions,
    )
    supplementalGroups: kdsl.extensions.v1beta1.SupplementalGroupsStrategyOptions = attr.ib(
        metadata={"yaml_name": "supplementalGroups"},
        converter=kdsl.extensions.v1beta1_converters.required_converter_SupplementalGroupsStrategyOptions,
    )
    allowPrivilegeEscalation: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "allowPrivilegeEscalation"}, default=OMIT
    )
    allowedCSIDrivers: Union[
        None, OmitEnum, Sequence[kdsl.extensions.v1beta1.AllowedCSIDriver]
    ] = attr.ib(
        metadata={"yaml_name": "allowedCSIDrivers"},
        converter=kdsl.extensions.v1beta1_converters.optional_list_converter_AllowedCSIDriver,
        default=OMIT,
    )
    allowedCapabilities: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "allowedCapabilities"}, default=OMIT
    )
    allowedFlexVolumes: Union[
        None, OmitEnum, Sequence[kdsl.extensions.v1beta1.AllowedFlexVolume]
    ] = attr.ib(
        metadata={"yaml_name": "allowedFlexVolumes"},
        converter=kdsl.extensions.v1beta1_converters.optional_list_converter_AllowedFlexVolume,
        default=OMIT,
    )
    allowedHostPaths: Union[
        None, OmitEnum, Sequence[kdsl.extensions.v1beta1.AllowedHostPath]
    ] = attr.ib(
        metadata={"yaml_name": "allowedHostPaths"},
        converter=kdsl.extensions.v1beta1_converters.optional_list_converter_AllowedHostPath,
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
        None, OmitEnum, Sequence[kdsl.extensions.v1beta1.HostPortRange]
    ] = attr.ib(
        metadata={"yaml_name": "hostPorts"},
        converter=kdsl.extensions.v1beta1_converters.optional_list_converter_HostPortRange,
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
        None, OmitEnum, kdsl.extensions.v1beta1.RunAsGroupStrategyOptions
    ] = attr.ib(
        metadata={"yaml_name": "runAsGroup"},
        converter=kdsl.extensions.v1beta1_converters.optional_converter_RunAsGroupStrategyOptions,
        default=OMIT,
    )
    runtimeClass: Union[
        None, OmitEnum, kdsl.extensions.v1beta1.RuntimeClassStrategyOptions
    ] = attr.ib(
        metadata={"yaml_name": "runtimeClass"},
        converter=kdsl.extensions.v1beta1_converters.optional_converter_RuntimeClassStrategyOptions,
        default=OMIT,
    )
    volumes: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "volumes"}, default=OMIT
    )


class PodSecurityPolicySpecOptionalTypedDict(TypedDict, total=(False)):
    allowPrivilegeEscalation: bool
    allowedCSIDrivers: Sequence[kdsl.extensions.v1beta1.AllowedCSIDriver]
    allowedCapabilities: Sequence[str]
    allowedFlexVolumes: Sequence[kdsl.extensions.v1beta1.AllowedFlexVolume]
    allowedHostPaths: Sequence[kdsl.extensions.v1beta1.AllowedHostPath]
    allowedProcMountTypes: Sequence[str]
    allowedUnsafeSysctls: Sequence[str]
    defaultAddCapabilities: Sequence[str]
    defaultAllowPrivilegeEscalation: bool
    forbiddenSysctls: Sequence[str]
    hostIPC: bool
    hostNetwork: bool
    hostPID: bool
    hostPorts: Sequence[kdsl.extensions.v1beta1.HostPortRange]
    privileged: bool
    readOnlyRootFilesystem: bool
    requiredDropCapabilities: Sequence[str]
    runAsGroup: kdsl.extensions.v1beta1.RunAsGroupStrategyOptions
    runtimeClass: kdsl.extensions.v1beta1.RuntimeClassStrategyOptions
    volumes: Sequence[str]


class PodSecurityPolicySpecTypedDict(
    PodSecurityPolicySpecOptionalTypedDict, total=(True)
):
    fsGroup: kdsl.extensions.v1beta1.FSGroupStrategyOptions
    runAsUser: kdsl.extensions.v1beta1.RunAsUserStrategyOptions
    seLinux: kdsl.extensions.v1beta1.SELinuxStrategyOptions
    supplementalGroups: kdsl.extensions.v1beta1.SupplementalGroupsStrategyOptions


PodSecurityPolicySpecUnion = Union[
    PodSecurityPolicySpec, PodSecurityPolicySpecTypedDict
]


@attr.s(kw_only=True)
class Deployment(K8sResource):
    apiVersion: ClassVar[str] = "extensions/v1beta1"
    kind: ClassVar[str] = "Deployment"
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    spec: Union[None, OmitEnum, kdsl.extensions.v1beta1.DeploymentSpec] = attr.ib(
        metadata={"yaml_name": "spec"},
        converter=kdsl.extensions.v1beta1_converters.optional_converter_DeploymentSpec,
        default=OMIT,
    )
    status: Union[None, OmitEnum, kdsl.extensions.v1beta1.DeploymentStatus] = attr.ib(
        metadata={"yaml_name": "status"},
        converter=kdsl.extensions.v1beta1_converters.optional_converter_DeploymentStatus,
        default=OMIT,
    )


@attr.s(kw_only=True)
class IngressSpec(K8sObject):
    backend: Union[None, OmitEnum, kdsl.extensions.v1beta1.IngressBackend] = attr.ib(
        metadata={"yaml_name": "backend"},
        converter=kdsl.extensions.v1beta1_converters.optional_converter_IngressBackend,
        default=OMIT,
    )
    rules: Union[
        None, OmitEnum, Sequence[kdsl.extensions.v1beta1.IngressRule]
    ] = attr.ib(
        metadata={"yaml_name": "rules"},
        converter=kdsl.extensions.v1beta1_converters.optional_list_converter_IngressRule,
        default=OMIT,
    )
    tls: Union[None, OmitEnum, Sequence[kdsl.extensions.v1beta1.IngressTLS]] = attr.ib(
        metadata={"yaml_name": "tls"},
        converter=kdsl.extensions.v1beta1_converters.optional_list_converter_IngressTLS,
        default=OMIT,
    )


class IngressSpecTypedDict(TypedDict, total=(False)):
    backend: kdsl.extensions.v1beta1.IngressBackend
    rules: Sequence[kdsl.extensions.v1beta1.IngressRule]
    tls: Sequence[kdsl.extensions.v1beta1.IngressTLS]


IngressSpecUnion = Union[IngressSpec, IngressSpecTypedDict]


@attr.s(kw_only=True)
class IngressStatus(K8sObject):
    loadBalancer: Union[None, OmitEnum, kdsl.core.v1.LoadBalancerStatus] = attr.ib(
        metadata={"yaml_name": "loadBalancer"},
        converter=kdsl.core.v1_converters.optional_converter_LoadBalancerStatus,
        default=OMIT,
    )


class IngressStatusTypedDict(TypedDict, total=(False)):
    loadBalancer: kdsl.core.v1.LoadBalancerStatus


IngressStatusUnion = Union[IngressStatus, IngressStatusTypedDict]


@attr.s(kw_only=True)
class DaemonSetSpec(K8sObject):
    template: kdsl.core.v1.PodTemplateSpec = attr.ib(
        metadata={"yaml_name": "template"},
        converter=kdsl.core.v1_converters.required_converter_PodTemplateSpec,
    )
    minReadySeconds: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "minReadySeconds"}, default=OMIT
    )
    revisionHistoryLimit: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "revisionHistoryLimit"}, default=OMIT
    )
    selector: Union[None, OmitEnum, kdsl.core.v1.LabelSelector] = attr.ib(
        metadata={"yaml_name": "selector"},
        converter=kdsl.core.v1_converters.optional_converter_LabelSelector,
        default=OMIT,
    )
    templateGeneration: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "templateGeneration"}, default=OMIT
    )
    updateStrategy: Union[
        None, OmitEnum, kdsl.extensions.v1beta1.DaemonSetUpdateStrategy
    ] = attr.ib(
        metadata={"yaml_name": "updateStrategy"},
        converter=kdsl.extensions.v1beta1_converters.optional_converter_DaemonSetUpdateStrategy,
        default=OMIT,
    )


class DaemonSetSpecOptionalTypedDict(TypedDict, total=(False)):
    minReadySeconds: int
    revisionHistoryLimit: int
    selector: kdsl.core.v1.LabelSelector
    templateGeneration: int
    updateStrategy: kdsl.extensions.v1beta1.DaemonSetUpdateStrategy


class DaemonSetSpecTypedDict(DaemonSetSpecOptionalTypedDict, total=(True)):
    template: kdsl.core.v1.PodTemplateSpec


DaemonSetSpecUnion = Union[DaemonSetSpec, DaemonSetSpecTypedDict]


@attr.s(kw_only=True)
class HTTPIngressRuleValue(K8sObject):
    paths: Sequence[kdsl.extensions.v1beta1.HTTPIngressPath] = attr.ib(
        metadata={"yaml_name": "paths"},
        converter=kdsl.extensions.v1beta1_converters.required_list_converter_HTTPIngressPath,
    )


class HTTPIngressRuleValueTypedDict(TypedDict, total=(True)):
    paths: Sequence[kdsl.extensions.v1beta1.HTTPIngressPath]


HTTPIngressRuleValueUnion = Union[HTTPIngressRuleValue, HTTPIngressRuleValueTypedDict]


@attr.s(kw_only=True)
class NetworkPolicyIngressRule(K8sObject):
    from_: Union[
        None, OmitEnum, Sequence[kdsl.extensions.v1beta1.NetworkPolicyPeer]
    ] = attr.ib(
        metadata={"yaml_name": "from"},
        converter=kdsl.extensions.v1beta1_converters.optional_list_converter_NetworkPolicyPeer,
        default=OMIT,
    )
    ports: Union[
        None, OmitEnum, Sequence[kdsl.extensions.v1beta1.NetworkPolicyPort]
    ] = attr.ib(
        metadata={"yaml_name": "ports"},
        converter=kdsl.extensions.v1beta1_converters.optional_list_converter_NetworkPolicyPort,
        default=OMIT,
    )


class NetworkPolicyIngressRuleTypedDict(TypedDict, total=(False)):
    from_: Sequence[kdsl.extensions.v1beta1.NetworkPolicyPeer]
    ports: Sequence[kdsl.extensions.v1beta1.NetworkPolicyPort]


NetworkPolicyIngressRuleUnion = Union[
    NetworkPolicyIngressRule, NetworkPolicyIngressRuleTypedDict
]


@attr.s(kw_only=True)
class IDRange(K8sObject):
    max: int = attr.ib(metadata={"yaml_name": "max"})
    min: int = attr.ib(metadata={"yaml_name": "min"})


class IDRangeTypedDict(TypedDict, total=(True)):
    max: int
    min: int


IDRangeUnion = Union[IDRange, IDRangeTypedDict]


@attr.s(kw_only=True)
class DeploymentConditionItem(K8sObject):
    status: str = attr.ib(metadata={"yaml_name": "status"})
    lastTransitionTime: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "lastTransitionTime"}, default=OMIT
    )
    lastUpdateTime: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "lastUpdateTime"}, default=OMIT
    )
    message: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "message"}, default=OMIT
    )
    reason: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "reason"}, default=OMIT
    )


class DeploymentConditionItemOptionalTypedDict(TypedDict, total=(False)):
    lastTransitionTime: str
    lastUpdateTime: str
    message: str
    reason: str


class DeploymentConditionItemTypedDict(
    DeploymentConditionItemOptionalTypedDict, total=(True)
):
    status: str


DeploymentConditionItemUnion = Union[
    DeploymentConditionItem, DeploymentConditionItemTypedDict
]


@attr.s(kw_only=True)
class ReplicaSetStatus(K8sObject):
    replicas: int = attr.ib(metadata={"yaml_name": "replicas"})
    availableReplicas: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "availableReplicas"}, default=OMIT
    )
    conditions: Union[
        None, OmitEnum, Mapping[str, kdsl.extensions.v1beta1.ReplicaSetConditionItem]
    ] = attr.ib(
        metadata={"yaml_name": "conditions", "mlist_key": "type"},
        converter=kdsl.extensions.v1beta1_converters.optional_mlist_converter_ReplicaSetConditionItem,
        default=OMIT,
    )
    fullyLabeledReplicas: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "fullyLabeledReplicas"}, default=OMIT
    )
    observedGeneration: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "observedGeneration"}, default=OMIT
    )
    readyReplicas: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "readyReplicas"}, default=OMIT
    )


class ReplicaSetStatusOptionalTypedDict(TypedDict, total=(False)):
    availableReplicas: int
    conditions: Mapping[str, kdsl.extensions.v1beta1.ReplicaSetConditionItem]
    fullyLabeledReplicas: int
    observedGeneration: int
    readyReplicas: int


class ReplicaSetStatusTypedDict(ReplicaSetStatusOptionalTypedDict, total=(True)):
    replicas: int


ReplicaSetStatusUnion = Union[ReplicaSetStatus, ReplicaSetStatusTypedDict]


@attr.s(kw_only=True)
class DaemonSet(K8sResource):
    apiVersion: ClassVar[str] = "extensions/v1beta1"
    kind: ClassVar[str] = "DaemonSet"
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    spec: Union[None, OmitEnum, kdsl.extensions.v1beta1.DaemonSetSpec] = attr.ib(
        metadata={"yaml_name": "spec"},
        converter=kdsl.extensions.v1beta1_converters.optional_converter_DaemonSetSpec,
        default=OMIT,
    )
    status: Union[None, OmitEnum, kdsl.extensions.v1beta1.DaemonSetStatus] = attr.ib(
        metadata={"yaml_name": "status"},
        converter=kdsl.extensions.v1beta1_converters.optional_converter_DaemonSetStatus,
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
class RunAsGroupStrategyOptions(K8sObject):
    rule: str = attr.ib(metadata={"yaml_name": "rule"})
    ranges: Union[None, OmitEnum, Sequence[kdsl.extensions.v1beta1.IDRange]] = attr.ib(
        metadata={"yaml_name": "ranges"},
        converter=kdsl.extensions.v1beta1_converters.optional_list_converter_IDRange,
        default=OMIT,
    )


class RunAsGroupStrategyOptionsOptionalTypedDict(TypedDict, total=(False)):
    ranges: Sequence[kdsl.extensions.v1beta1.IDRange]


class RunAsGroupStrategyOptionsTypedDict(
    RunAsGroupStrategyOptionsOptionalTypedDict, total=(True)
):
    rule: str


RunAsGroupStrategyOptionsUnion = Union[
    RunAsGroupStrategyOptions, RunAsGroupStrategyOptionsTypedDict
]


@attr.s(kw_only=True)
class IngressRule(K8sObject):
    host: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "host"}, default=OMIT
    )
    http: Union[None, OmitEnum, kdsl.extensions.v1beta1.HTTPIngressRuleValue] = attr.ib(
        metadata={"yaml_name": "http"},
        converter=kdsl.extensions.v1beta1_converters.optional_converter_HTTPIngressRuleValue,
        default=OMIT,
    )


class IngressRuleTypedDict(TypedDict, total=(False)):
    host: str
    http: kdsl.extensions.v1beta1.HTTPIngressRuleValue


IngressRuleUnion = Union[IngressRule, IngressRuleTypedDict]


@attr.s(kw_only=True)
class HTTPIngressPath(K8sObject):
    backend: kdsl.extensions.v1beta1.IngressBackend = attr.ib(
        metadata={"yaml_name": "backend"},
        converter=kdsl.extensions.v1beta1_converters.required_converter_IngressBackend,
    )
    path: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "path"}, default=OMIT
    )


class HTTPIngressPathOptionalTypedDict(TypedDict, total=(False)):
    path: str


class HTTPIngressPathTypedDict(HTTPIngressPathOptionalTypedDict, total=(True)):
    backend: kdsl.extensions.v1beta1.IngressBackend


HTTPIngressPathUnion = Union[HTTPIngressPath, HTTPIngressPathTypedDict]


@attr.s(kw_only=True)
class SupplementalGroupsStrategyOptions(K8sObject):
    ranges: Union[None, OmitEnum, Sequence[kdsl.extensions.v1beta1.IDRange]] = attr.ib(
        metadata={"yaml_name": "ranges"},
        converter=kdsl.extensions.v1beta1_converters.optional_list_converter_IDRange,
        default=OMIT,
    )
    rule: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "rule"}, default=OMIT
    )


class SupplementalGroupsStrategyOptionsTypedDict(TypedDict, total=(False)):
    ranges: Sequence[kdsl.extensions.v1beta1.IDRange]
    rule: str


SupplementalGroupsStrategyOptionsUnion = Union[
    SupplementalGroupsStrategyOptions, SupplementalGroupsStrategyOptionsTypedDict
]


@attr.s(kw_only=True)
class NetworkPolicyPort(K8sObject):
    port: Union[None, OmitEnum, Union[int, str]] = attr.ib(
        metadata={"yaml_name": "port"}, default=OMIT
    )
    protocol: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "protocol"}, default=OMIT
    )


class NetworkPolicyPortTypedDict(TypedDict, total=(False)):
    port: Union[int, str]
    protocol: str


NetworkPolicyPortUnion = Union[NetworkPolicyPort, NetworkPolicyPortTypedDict]


@attr.s(kw_only=True)
class DeploymentSpec(K8sObject):
    template: kdsl.core.v1.PodTemplateSpec = attr.ib(
        metadata={"yaml_name": "template"},
        converter=kdsl.core.v1_converters.required_converter_PodTemplateSpec,
    )
    minReadySeconds: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "minReadySeconds"}, default=OMIT
    )
    paused: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "paused"}, default=OMIT
    )
    progressDeadlineSeconds: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "progressDeadlineSeconds"}, default=OMIT
    )
    replicas: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "replicas"}, default=OMIT
    )
    revisionHistoryLimit: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "revisionHistoryLimit"}, default=OMIT
    )
    rollbackTo: Union[None, OmitEnum, kdsl.extensions.v1beta1.RollbackConfig] = attr.ib(
        metadata={"yaml_name": "rollbackTo"},
        converter=kdsl.extensions.v1beta1_converters.optional_converter_RollbackConfig,
        default=OMIT,
    )
    selector: Union[None, OmitEnum, kdsl.core.v1.LabelSelector] = attr.ib(
        metadata={"yaml_name": "selector"},
        converter=kdsl.core.v1_converters.optional_converter_LabelSelector,
        default=OMIT,
    )
    strategy: Union[
        None, OmitEnum, kdsl.extensions.v1beta1.DeploymentStrategy
    ] = attr.ib(
        metadata={"yaml_name": "strategy"},
        converter=kdsl.extensions.v1beta1_converters.optional_converter_DeploymentStrategy,
        default=OMIT,
    )


class DeploymentSpecOptionalTypedDict(TypedDict, total=(False)):
    minReadySeconds: int
    paused: bool
    progressDeadlineSeconds: int
    replicas: int
    revisionHistoryLimit: int
    rollbackTo: kdsl.extensions.v1beta1.RollbackConfig
    selector: kdsl.core.v1.LabelSelector
    strategy: kdsl.extensions.v1beta1.DeploymentStrategy


class DeploymentSpecTypedDict(DeploymentSpecOptionalTypedDict, total=(True)):
    template: kdsl.core.v1.PodTemplateSpec


DeploymentSpecUnion = Union[DeploymentSpec, DeploymentSpecTypedDict]


@attr.s(kw_only=True)
class NetworkPolicyPeer(K8sObject):
    ipBlock: Union[None, OmitEnum, kdsl.extensions.v1beta1.IPBlock] = attr.ib(
        metadata={"yaml_name": "ipBlock"},
        converter=kdsl.extensions.v1beta1_converters.optional_converter_IPBlock,
        default=OMIT,
    )
    namespaceSelector: Union[None, OmitEnum, kdsl.core.v1.LabelSelector] = attr.ib(
        metadata={"yaml_name": "namespaceSelector"},
        converter=kdsl.core.v1_converters.optional_converter_LabelSelector,
        default=OMIT,
    )
    podSelector: Union[None, OmitEnum, kdsl.core.v1.LabelSelector] = attr.ib(
        metadata={"yaml_name": "podSelector"},
        converter=kdsl.core.v1_converters.optional_converter_LabelSelector,
        default=OMIT,
    )


class NetworkPolicyPeerTypedDict(TypedDict, total=(False)):
    ipBlock: kdsl.extensions.v1beta1.IPBlock
    namespaceSelector: kdsl.core.v1.LabelSelector
    podSelector: kdsl.core.v1.LabelSelector


NetworkPolicyPeerUnion = Union[NetworkPolicyPeer, NetworkPolicyPeerTypedDict]


@attr.s(kw_only=True)
class PodSecurityPolicy(K8sResource):
    apiVersion: ClassVar[str] = "extensions/v1beta1"
    kind: ClassVar[str] = "PodSecurityPolicy"
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    spec: Union[
        None, OmitEnum, kdsl.extensions.v1beta1.PodSecurityPolicySpec
    ] = attr.ib(
        metadata={"yaml_name": "spec"},
        converter=kdsl.extensions.v1beta1_converters.optional_converter_PodSecurityPolicySpec,
        default=OMIT,
    )


@attr.s(kw_only=True)
class AllowedFlexVolume(K8sObject):
    driver: str = attr.ib(metadata={"yaml_name": "driver"})


class AllowedFlexVolumeTypedDict(TypedDict, total=(True)):
    driver: str


AllowedFlexVolumeUnion = Union[AllowedFlexVolume, AllowedFlexVolumeTypedDict]


@attr.s(kw_only=True)
class DaemonSetConditionItem(K8sObject):
    status: str = attr.ib(metadata={"yaml_name": "status"})
    lastTransitionTime: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "lastTransitionTime"}, default=OMIT
    )
    message: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "message"}, default=OMIT
    )
    reason: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "reason"}, default=OMIT
    )


class DaemonSetConditionItemOptionalTypedDict(TypedDict, total=(False)):
    lastTransitionTime: str
    message: str
    reason: str


class DaemonSetConditionItemTypedDict(
    DaemonSetConditionItemOptionalTypedDict, total=(True)
):
    status: str


DaemonSetConditionItemUnion = Union[
    DaemonSetConditionItem, DaemonSetConditionItemTypedDict
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
class IPBlock(K8sObject):
    cidr: str = attr.ib(metadata={"yaml_name": "cidr"})
    except_: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "except"}, default=OMIT
    )


class IPBlockOptionalTypedDict(TypedDict, total=(False)):
    except_: Sequence[str]


class IPBlockTypedDict(IPBlockOptionalTypedDict, total=(True)):
    cidr: str


IPBlockUnion = Union[IPBlock, IPBlockTypedDict]


@attr.s(kw_only=True)
class DeploymentStatus(K8sObject):
    availableReplicas: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "availableReplicas"}, default=OMIT
    )
    collisionCount: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "collisionCount"}, default=OMIT
    )
    conditions: Union[
        None, OmitEnum, Mapping[str, kdsl.extensions.v1beta1.DeploymentConditionItem]
    ] = attr.ib(
        metadata={"yaml_name": "conditions", "mlist_key": "type"},
        converter=kdsl.extensions.v1beta1_converters.optional_mlist_converter_DeploymentConditionItem,
        default=OMIT,
    )
    observedGeneration: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "observedGeneration"}, default=OMIT
    )
    readyReplicas: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "readyReplicas"}, default=OMIT
    )
    replicas: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "replicas"}, default=OMIT
    )
    unavailableReplicas: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "unavailableReplicas"}, default=OMIT
    )
    updatedReplicas: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "updatedReplicas"}, default=OMIT
    )


class DeploymentStatusTypedDict(TypedDict, total=(False)):
    availableReplicas: int
    collisionCount: int
    conditions: Mapping[str, kdsl.extensions.v1beta1.DeploymentConditionItem]
    observedGeneration: int
    readyReplicas: int
    replicas: int
    unavailableReplicas: int
    updatedReplicas: int


DeploymentStatusUnion = Union[DeploymentStatus, DeploymentStatusTypedDict]


@attr.s(kw_only=True)
class AllowedCSIDriver(K8sObject):
    name: str = attr.ib(metadata={"yaml_name": "name"})


class AllowedCSIDriverTypedDict(TypedDict, total=(True)):
    name: str


AllowedCSIDriverUnion = Union[AllowedCSIDriver, AllowedCSIDriverTypedDict]
