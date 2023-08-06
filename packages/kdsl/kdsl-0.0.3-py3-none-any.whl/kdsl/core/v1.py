from __future__ import annotations
import kdsl.core.v1
import kdsl.core.v1_converters
import attr
from typing import Mapping, ClassVar, Optional, Any, Sequence, TypedDict, Union
from kdsl.bases import OmitEnum, OMIT, K8sObject, K8sResource


@attr.s(kw_only=True)
class PhotonPersistentDiskVolumeSource(K8sObject):
    pdID: str = attr.ib(metadata={"yaml_name": "pdID"})
    fsType: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "fsType"}, default=OMIT
    )


class PhotonPersistentDiskVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    fsType: str


class PhotonPersistentDiskVolumeSourceTypedDict(
    PhotonPersistentDiskVolumeSourceOptionalTypedDict, total=(True)
):
    pdID: str


PhotonPersistentDiskVolumeSourceUnion = Union[
    PhotonPersistentDiskVolumeSource, PhotonPersistentDiskVolumeSourceTypedDict
]


@attr.s(kw_only=True)
class SecretProjection(K8sObject):
    items: Union[None, OmitEnum, Sequence[kdsl.core.v1.KeyToPath]] = attr.ib(
        metadata={"yaml_name": "items"},
        converter=kdsl.core.v1_converters.optional_list_converter_KeyToPath,
        default=OMIT,
    )
    name: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "name"}, default=OMIT
    )
    optional: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "optional"}, default=OMIT
    )


class SecretProjectionTypedDict(TypedDict, total=(False)):
    items: Sequence[kdsl.core.v1.KeyToPath]
    name: str
    optional: bool


SecretProjectionUnion = Union[SecretProjection, SecretProjectionTypedDict]


@attr.s(kw_only=True)
class SecretReference(K8sObject):
    name: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "name"}, default=OMIT
    )
    namespace: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "namespace"}, default=OMIT
    )


class SecretReferenceTypedDict(TypedDict, total=(False)):
    name: str
    namespace: str


SecretReferenceUnion = Union[SecretReference, SecretReferenceTypedDict]


@attr.s(kw_only=True)
class TypedLocalObjectReference(K8sObject):
    kind: str = attr.ib(metadata={"yaml_name": "kind"})
    name: str = attr.ib(metadata={"yaml_name": "name"})
    apiGroup: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "apiGroup"}, default=OMIT
    )


class TypedLocalObjectReferenceOptionalTypedDict(TypedDict, total=(False)):
    apiGroup: str


class TypedLocalObjectReferenceTypedDict(
    TypedLocalObjectReferenceOptionalTypedDict, total=(True)
):
    kind: str
    name: str


TypedLocalObjectReferenceUnion = Union[
    TypedLocalObjectReference, TypedLocalObjectReferenceTypedDict
]


@attr.s(kw_only=True)
class LocalVolumeSource(K8sObject):
    path: str = attr.ib(metadata={"yaml_name": "path"})
    fsType: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "fsType"}, default=OMIT
    )


class LocalVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    fsType: str


class LocalVolumeSourceTypedDict(LocalVolumeSourceOptionalTypedDict, total=(True)):
    path: str


LocalVolumeSourceUnion = Union[LocalVolumeSource, LocalVolumeSourceTypedDict]


@attr.s(kw_only=True)
class NodeStatus(K8sObject):
    addresses: Union[
        None, OmitEnum, Mapping[str, kdsl.core.v1.NodeAddressItem]
    ] = attr.ib(
        metadata={"yaml_name": "addresses", "mlist_key": "type"},
        converter=kdsl.core.v1_converters.optional_mlist_converter_NodeAddressItem,
        default=OMIT,
    )
    allocatable: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(
        metadata={"yaml_name": "allocatable"}, default=OMIT
    )
    capacity: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(
        metadata={"yaml_name": "capacity"}, default=OMIT
    )
    conditions: Union[
        None, OmitEnum, Mapping[str, kdsl.core.v1.NodeConditionItem]
    ] = attr.ib(
        metadata={"yaml_name": "conditions", "mlist_key": "type"},
        converter=kdsl.core.v1_converters.optional_mlist_converter_NodeConditionItem,
        default=OMIT,
    )
    config: Union[None, OmitEnum, kdsl.core.v1.NodeConfigStatus] = attr.ib(
        metadata={"yaml_name": "config"},
        converter=kdsl.core.v1_converters.optional_converter_NodeConfigStatus,
        default=OMIT,
    )
    daemonEndpoints: Union[None, OmitEnum, kdsl.core.v1.NodeDaemonEndpoints] = attr.ib(
        metadata={"yaml_name": "daemonEndpoints"},
        converter=kdsl.core.v1_converters.optional_converter_NodeDaemonEndpoints,
        default=OMIT,
    )
    images: Union[None, OmitEnum, Sequence[kdsl.core.v1.ContainerImage]] = attr.ib(
        metadata={"yaml_name": "images"},
        converter=kdsl.core.v1_converters.optional_list_converter_ContainerImage,
        default=OMIT,
    )
    nodeInfo: Union[None, OmitEnum, kdsl.core.v1.NodeSystemInfo] = attr.ib(
        metadata={"yaml_name": "nodeInfo"},
        converter=kdsl.core.v1_converters.optional_converter_NodeSystemInfo,
        default=OMIT,
    )
    phase: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "phase"}, default=OMIT
    )
    volumesAttached: Union[
        None, OmitEnum, Sequence[kdsl.core.v1.AttachedVolume]
    ] = attr.ib(
        metadata={"yaml_name": "volumesAttached"},
        converter=kdsl.core.v1_converters.optional_list_converter_AttachedVolume,
        default=OMIT,
    )
    volumesInUse: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "volumesInUse"}, default=OMIT
    )


class NodeStatusTypedDict(TypedDict, total=(False)):
    addresses: Mapping[str, kdsl.core.v1.NodeAddressItem]
    allocatable: Mapping[str, str]
    capacity: Mapping[str, str]
    conditions: Mapping[str, kdsl.core.v1.NodeConditionItem]
    config: kdsl.core.v1.NodeConfigStatus
    daemonEndpoints: kdsl.core.v1.NodeDaemonEndpoints
    images: Sequence[kdsl.core.v1.ContainerImage]
    nodeInfo: kdsl.core.v1.NodeSystemInfo
    phase: str
    volumesAttached: Sequence[kdsl.core.v1.AttachedVolume]
    volumesInUse: Sequence[str]


NodeStatusUnion = Union[NodeStatus, NodeStatusTypedDict]


@attr.s(kw_only=True)
class NodeSelectorTerm(K8sObject):
    matchExpressions: Union[
        None, OmitEnum, Sequence[kdsl.core.v1.NodeSelectorRequirement]
    ] = attr.ib(
        metadata={"yaml_name": "matchExpressions"},
        converter=kdsl.core.v1_converters.optional_list_converter_NodeSelectorRequirement,
        default=OMIT,
    )
    matchFields: Union[
        None, OmitEnum, Sequence[kdsl.core.v1.NodeSelectorRequirement]
    ] = attr.ib(
        metadata={"yaml_name": "matchFields"},
        converter=kdsl.core.v1_converters.optional_list_converter_NodeSelectorRequirement,
        default=OMIT,
    )


class NodeSelectorTermTypedDict(TypedDict, total=(False)):
    matchExpressions: Sequence[kdsl.core.v1.NodeSelectorRequirement]
    matchFields: Sequence[kdsl.core.v1.NodeSelectorRequirement]


NodeSelectorTermUnion = Union[NodeSelectorTerm, NodeSelectorTermTypedDict]


@attr.s(kw_only=True)
class AzureFilePersistentVolumeSource(K8sObject):
    secretName: str = attr.ib(metadata={"yaml_name": "secretName"})
    shareName: str = attr.ib(metadata={"yaml_name": "shareName"})
    readOnly: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "readOnly"}, default=OMIT
    )
    secretNamespace: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "secretNamespace"}, default=OMIT
    )


class AzureFilePersistentVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    readOnly: bool
    secretNamespace: str


class AzureFilePersistentVolumeSourceTypedDict(
    AzureFilePersistentVolumeSourceOptionalTypedDict, total=(True)
):
    secretName: str
    shareName: str


AzureFilePersistentVolumeSourceUnion = Union[
    AzureFilePersistentVolumeSource, AzureFilePersistentVolumeSourceTypedDict
]


@attr.s(kw_only=True)
class EmptyDirVolumeSource(K8sObject):
    medium: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "medium"}, default=OMIT
    )
    sizeLimit: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "sizeLimit"}, default=OMIT
    )


class EmptyDirVolumeSourceTypedDict(TypedDict, total=(False)):
    medium: str
    sizeLimit: str


EmptyDirVolumeSourceUnion = Union[EmptyDirVolumeSource, EmptyDirVolumeSourceTypedDict]


@attr.s(kw_only=True)
class VolumeProjection(K8sObject):
    configMap: Union[None, OmitEnum, kdsl.core.v1.ConfigMapProjection] = attr.ib(
        metadata={"yaml_name": "configMap"},
        converter=kdsl.core.v1_converters.optional_converter_ConfigMapProjection,
        default=OMIT,
    )
    downwardAPI: Union[None, OmitEnum, kdsl.core.v1.DownwardAPIProjection] = attr.ib(
        metadata={"yaml_name": "downwardAPI"},
        converter=kdsl.core.v1_converters.optional_converter_DownwardAPIProjection,
        default=OMIT,
    )
    secret: Union[None, OmitEnum, kdsl.core.v1.SecretProjection] = attr.ib(
        metadata={"yaml_name": "secret"},
        converter=kdsl.core.v1_converters.optional_converter_SecretProjection,
        default=OMIT,
    )
    serviceAccountToken: Union[
        None, OmitEnum, kdsl.core.v1.ServiceAccountTokenProjection
    ] = attr.ib(
        metadata={"yaml_name": "serviceAccountToken"},
        converter=kdsl.core.v1_converters.optional_converter_ServiceAccountTokenProjection,
        default=OMIT,
    )


class VolumeProjectionTypedDict(TypedDict, total=(False)):
    configMap: kdsl.core.v1.ConfigMapProjection
    downwardAPI: kdsl.core.v1.DownwardAPIProjection
    secret: kdsl.core.v1.SecretProjection
    serviceAccountToken: kdsl.core.v1.ServiceAccountTokenProjection


VolumeProjectionUnion = Union[VolumeProjection, VolumeProjectionTypedDict]


@attr.s(kw_only=True)
class DeleteOptions(K8sObject):
    apiVersion: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "apiVersion"}, default=OMIT
    )
    dryRun: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "dryRun"}, default=OMIT
    )
    gracePeriodSeconds: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "gracePeriodSeconds"}, default=OMIT
    )
    kind: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "kind"}, default=OMIT
    )
    orphanDependents: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "orphanDependents"}, default=OMIT
    )
    preconditions: Union[None, OmitEnum, kdsl.core.v1.Preconditions] = attr.ib(
        metadata={"yaml_name": "preconditions"},
        converter=kdsl.core.v1_converters.optional_converter_Preconditions,
        default=OMIT,
    )
    propagationPolicy: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "propagationPolicy"}, default=OMIT
    )


class DeleteOptionsTypedDict(TypedDict, total=(False)):
    apiVersion: str
    dryRun: Sequence[str]
    gracePeriodSeconds: int
    kind: str
    orphanDependents: bool
    preconditions: kdsl.core.v1.Preconditions
    propagationPolicy: str


DeleteOptionsUnion = Union[DeleteOptions, DeleteOptionsTypedDict]


@attr.s(kw_only=True)
class FlexPersistentVolumeSource(K8sObject):
    driver: str = attr.ib(metadata={"yaml_name": "driver"})
    fsType: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "fsType"}, default=OMIT
    )
    options: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(
        metadata={"yaml_name": "options"}, default=OMIT
    )
    readOnly: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "readOnly"}, default=OMIT
    )
    secretRef: Union[None, OmitEnum, kdsl.core.v1.SecretReference] = attr.ib(
        metadata={"yaml_name": "secretRef"},
        converter=kdsl.core.v1_converters.optional_converter_SecretReference,
        default=OMIT,
    )


class FlexPersistentVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    fsType: str
    options: Mapping[str, str]
    readOnly: bool
    secretRef: kdsl.core.v1.SecretReference


class FlexPersistentVolumeSourceTypedDict(
    FlexPersistentVolumeSourceOptionalTypedDict, total=(True)
):
    driver: str


FlexPersistentVolumeSourceUnion = Union[
    FlexPersistentVolumeSource, FlexPersistentVolumeSourceTypedDict
]


@attr.s(kw_only=True)
class Event(K8sResource):
    apiVersion: ClassVar[str] = "v1"
    kind: ClassVar[str] = "Event"
    involvedObject: kdsl.core.v1.ObjectReference = attr.ib(
        metadata={"yaml_name": "involvedObject"},
        converter=kdsl.core.v1_converters.required_converter_ObjectReference,
    )
    metadata: kdsl.core.v1.ObjectMeta = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.required_converter_ObjectMeta,
    )
    action: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "action"}, default=OMIT
    )
    count: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "count"}, default=OMIT
    )
    eventTime: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "eventTime"}, default=OMIT
    )
    firstTimestamp: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "firstTimestamp"}, default=OMIT
    )
    lastTimestamp: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "lastTimestamp"}, default=OMIT
    )
    message: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "message"}, default=OMIT
    )
    reason: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "reason"}, default=OMIT
    )
    related: Union[None, OmitEnum, kdsl.core.v1.ObjectReference] = attr.ib(
        metadata={"yaml_name": "related"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectReference,
        default=OMIT,
    )
    reportingComponent: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "reportingComponent"}, default=OMIT
    )
    reportingInstance: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "reportingInstance"}, default=OMIT
    )
    series: Union[None, OmitEnum, kdsl.core.v1.EventSeries] = attr.ib(
        metadata={"yaml_name": "series"},
        converter=kdsl.core.v1_converters.optional_converter_EventSeries,
        default=OMIT,
    )
    source: Union[None, OmitEnum, kdsl.core.v1.EventSource] = attr.ib(
        metadata={"yaml_name": "source"},
        converter=kdsl.core.v1_converters.optional_converter_EventSource,
        default=OMIT,
    )
    type: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "type"}, default=OMIT
    )


@attr.s(kw_only=True)
class Service(K8sResource):
    apiVersion: ClassVar[str] = "v1"
    kind: ClassVar[str] = "Service"
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    spec: Union[None, OmitEnum, kdsl.core.v1.ServiceSpec] = attr.ib(
        metadata={"yaml_name": "spec"},
        converter=kdsl.core.v1_converters.optional_converter_ServiceSpec,
        default=OMIT,
    )
    status: Union[None, OmitEnum, kdsl.core.v1.ServiceStatus] = attr.ib(
        metadata={"yaml_name": "status"},
        converter=kdsl.core.v1_converters.optional_converter_ServiceStatus,
        default=OMIT,
    )


@attr.s(kw_only=True)
class PodSpec(K8sObject):
    containers: Mapping[str, kdsl.core.v1.ContainerItem] = attr.ib(
        metadata={"yaml_name": "containers", "mlist_key": "name"},
        converter=kdsl.core.v1_converters.required_mlist_converter_ContainerItem,
    )
    activeDeadlineSeconds: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "activeDeadlineSeconds"}, default=OMIT
    )
    affinity: Union[None, OmitEnum, kdsl.core.v1.Affinity] = attr.ib(
        metadata={"yaml_name": "affinity"},
        converter=kdsl.core.v1_converters.optional_converter_Affinity,
        default=OMIT,
    )
    automountServiceAccountToken: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "automountServiceAccountToken"}, default=OMIT
    )
    dnsConfig: Union[None, OmitEnum, kdsl.core.v1.PodDNSConfig] = attr.ib(
        metadata={"yaml_name": "dnsConfig"},
        converter=kdsl.core.v1_converters.optional_converter_PodDNSConfig,
        default=OMIT,
    )
    dnsPolicy: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "dnsPolicy"}, default=OMIT
    )
    enableServiceLinks: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "enableServiceLinks"}, default=OMIT
    )
    ephemeralContainers: Union[
        None, OmitEnum, Mapping[str, kdsl.core.v1.EphemeralContainerItem]
    ] = attr.ib(
        metadata={"yaml_name": "ephemeralContainers", "mlist_key": "name"},
        converter=kdsl.core.v1_converters.optional_mlist_converter_EphemeralContainerItem,
        default=OMIT,
    )
    hostAliases: Union[
        None, OmitEnum, Mapping[str, kdsl.core.v1.HostAliasItem]
    ] = attr.ib(
        metadata={"yaml_name": "hostAliases", "mlist_key": "ip"},
        converter=kdsl.core.v1_converters.optional_mlist_converter_HostAliasItem,
        default=OMIT,
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
    hostname: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "hostname"}, default=OMIT
    )
    imagePullSecrets: Union[
        None, OmitEnum, Sequence[kdsl.core.v1.LocalObjectReference]
    ] = attr.ib(
        metadata={"yaml_name": "imagePullSecrets"},
        converter=kdsl.core.v1_converters.optional_list_converter_LocalObjectReference,
        default=OMIT,
    )
    initContainers: Union[
        None, OmitEnum, Mapping[str, kdsl.core.v1.ContainerItem]
    ] = attr.ib(
        metadata={"yaml_name": "initContainers", "mlist_key": "name"},
        converter=kdsl.core.v1_converters.optional_mlist_converter_ContainerItem,
        default=OMIT,
    )
    nodeName: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "nodeName"}, default=OMIT
    )
    nodeSelector: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(
        metadata={"yaml_name": "nodeSelector"}, default=OMIT
    )
    overhead: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(
        metadata={"yaml_name": "overhead"}, default=OMIT
    )
    preemptionPolicy: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "preemptionPolicy"}, default=OMIT
    )
    priority: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "priority"}, default=OMIT
    )
    priorityClassName: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "priorityClassName"}, default=OMIT
    )
    readinessGates: Union[
        None, OmitEnum, Sequence[kdsl.core.v1.PodReadinessGate]
    ] = attr.ib(
        metadata={"yaml_name": "readinessGates"},
        converter=kdsl.core.v1_converters.optional_list_converter_PodReadinessGate,
        default=OMIT,
    )
    restartPolicy: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "restartPolicy"}, default=OMIT
    )
    runtimeClassName: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "runtimeClassName"}, default=OMIT
    )
    schedulerName: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "schedulerName"}, default=OMIT
    )
    securityContext: Union[None, OmitEnum, kdsl.core.v1.PodSecurityContext] = attr.ib(
        metadata={"yaml_name": "securityContext"},
        converter=kdsl.core.v1_converters.optional_converter_PodSecurityContext,
        default=OMIT,
    )
    serviceAccount: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "serviceAccount"}, default=OMIT
    )
    serviceAccountName: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "serviceAccountName"}, default=OMIT
    )
    shareProcessNamespace: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "shareProcessNamespace"}, default=OMIT
    )
    subdomain: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "subdomain"}, default=OMIT
    )
    terminationGracePeriodSeconds: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "terminationGracePeriodSeconds"}, default=OMIT
    )
    tolerations: Union[None, OmitEnum, Sequence[kdsl.core.v1.Toleration]] = attr.ib(
        metadata={"yaml_name": "tolerations"},
        converter=kdsl.core.v1_converters.optional_list_converter_Toleration,
        default=OMIT,
    )
    topologySpreadConstraints: Union[
        None, OmitEnum, Mapping[str, kdsl.core.v1.TopologySpreadConstraintItem]
    ] = attr.ib(
        metadata={"yaml_name": "topologySpreadConstraints", "mlist_key": "topologyKey"},
        converter=kdsl.core.v1_converters.optional_mlist_converter_TopologySpreadConstraintItem,
        default=OMIT,
    )
    volumes: Union[None, OmitEnum, Mapping[str, kdsl.core.v1.VolumeItem]] = attr.ib(
        metadata={"yaml_name": "volumes", "mlist_key": "name"},
        converter=kdsl.core.v1_converters.optional_mlist_converter_VolumeItem,
        default=OMIT,
    )


class PodSpecOptionalTypedDict(TypedDict, total=(False)):
    activeDeadlineSeconds: int
    affinity: kdsl.core.v1.Affinity
    automountServiceAccountToken: bool
    dnsConfig: kdsl.core.v1.PodDNSConfig
    dnsPolicy: str
    enableServiceLinks: bool
    ephemeralContainers: Mapping[str, kdsl.core.v1.EphemeralContainerItem]
    hostAliases: Mapping[str, kdsl.core.v1.HostAliasItem]
    hostIPC: bool
    hostNetwork: bool
    hostPID: bool
    hostname: str
    imagePullSecrets: Sequence[kdsl.core.v1.LocalObjectReference]
    initContainers: Mapping[str, kdsl.core.v1.ContainerItem]
    nodeName: str
    nodeSelector: Mapping[str, str]
    overhead: Mapping[str, str]
    preemptionPolicy: str
    priority: int
    priorityClassName: str
    readinessGates: Sequence[kdsl.core.v1.PodReadinessGate]
    restartPolicy: str
    runtimeClassName: str
    schedulerName: str
    securityContext: kdsl.core.v1.PodSecurityContext
    serviceAccount: str
    serviceAccountName: str
    shareProcessNamespace: bool
    subdomain: str
    terminationGracePeriodSeconds: int
    tolerations: Sequence[kdsl.core.v1.Toleration]
    topologySpreadConstraints: Mapping[str, kdsl.core.v1.TopologySpreadConstraintItem]
    volumes: Mapping[str, kdsl.core.v1.VolumeItem]


class PodSpecTypedDict(PodSpecOptionalTypedDict, total=(True)):
    containers: Mapping[str, kdsl.core.v1.ContainerItem]


PodSpecUnion = Union[PodSpec, PodSpecTypedDict]


@attr.s(kw_only=True)
class Capabilities(K8sObject):
    add: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "add"}, default=OMIT
    )
    drop: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "drop"}, default=OMIT
    )


class CapabilitiesTypedDict(TypedDict, total=(False)):
    add: Sequence[str]
    drop: Sequence[str]


CapabilitiesUnion = Union[Capabilities, CapabilitiesTypedDict]


@attr.s(kw_only=True)
class ContainerState(K8sObject):
    running: Union[None, OmitEnum, kdsl.core.v1.ContainerStateRunning] = attr.ib(
        metadata={"yaml_name": "running"},
        converter=kdsl.core.v1_converters.optional_converter_ContainerStateRunning,
        default=OMIT,
    )
    terminated: Union[None, OmitEnum, kdsl.core.v1.ContainerStateTerminated] = attr.ib(
        metadata={"yaml_name": "terminated"},
        converter=kdsl.core.v1_converters.optional_converter_ContainerStateTerminated,
        default=OMIT,
    )
    waiting: Union[None, OmitEnum, kdsl.core.v1.ContainerStateWaiting] = attr.ib(
        metadata={"yaml_name": "waiting"},
        converter=kdsl.core.v1_converters.optional_converter_ContainerStateWaiting,
        default=OMIT,
    )


class ContainerStateTypedDict(TypedDict, total=(False)):
    running: kdsl.core.v1.ContainerStateRunning
    terminated: kdsl.core.v1.ContainerStateTerminated
    waiting: kdsl.core.v1.ContainerStateWaiting


ContainerStateUnion = Union[ContainerState, ContainerStateTypedDict]


@attr.s(kw_only=True)
class PodAntiAffinity(K8sObject):
    preferredDuringSchedulingIgnoredDuringExecution: Union[
        None, OmitEnum, Sequence[kdsl.core.v1.WeightedPodAffinityTerm]
    ] = attr.ib(
        metadata={"yaml_name": "preferredDuringSchedulingIgnoredDuringExecution"},
        converter=kdsl.core.v1_converters.optional_list_converter_WeightedPodAffinityTerm,
        default=OMIT,
    )
    requiredDuringSchedulingIgnoredDuringExecution: Union[
        None, OmitEnum, Sequence[kdsl.core.v1.PodAffinityTerm]
    ] = attr.ib(
        metadata={"yaml_name": "requiredDuringSchedulingIgnoredDuringExecution"},
        converter=kdsl.core.v1_converters.optional_list_converter_PodAffinityTerm,
        default=OMIT,
    )


class PodAntiAffinityTypedDict(TypedDict, total=(False)):
    preferredDuringSchedulingIgnoredDuringExecution: Sequence[
        kdsl.core.v1.WeightedPodAffinityTerm
    ]
    requiredDuringSchedulingIgnoredDuringExecution: Sequence[
        kdsl.core.v1.PodAffinityTerm
    ]


PodAntiAffinityUnion = Union[PodAntiAffinity, PodAntiAffinityTypedDict]


@attr.s(kw_only=True)
class ContainerStatus(K8sObject):
    image: str = attr.ib(metadata={"yaml_name": "image"})
    imageID: str = attr.ib(metadata={"yaml_name": "imageID"})
    name: str = attr.ib(metadata={"yaml_name": "name"})
    ready: bool = attr.ib(metadata={"yaml_name": "ready"})
    restartCount: int = attr.ib(metadata={"yaml_name": "restartCount"})
    containerID: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "containerID"}, default=OMIT
    )
    lastState: Union[None, OmitEnum, kdsl.core.v1.ContainerState] = attr.ib(
        metadata={"yaml_name": "lastState"},
        converter=kdsl.core.v1_converters.optional_converter_ContainerState,
        default=OMIT,
    )
    started: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "started"}, default=OMIT
    )
    state: Union[None, OmitEnum, kdsl.core.v1.ContainerState] = attr.ib(
        metadata={"yaml_name": "state"},
        converter=kdsl.core.v1_converters.optional_converter_ContainerState,
        default=OMIT,
    )


class ContainerStatusOptionalTypedDict(TypedDict, total=(False)):
    containerID: str
    lastState: kdsl.core.v1.ContainerState
    started: bool
    state: kdsl.core.v1.ContainerState


class ContainerStatusTypedDict(ContainerStatusOptionalTypedDict, total=(True)):
    image: str
    imageID: str
    name: str
    ready: bool
    restartCount: int


ContainerStatusUnion = Union[ContainerStatus, ContainerStatusTypedDict]


@attr.s(kw_only=True)
class RBDPersistentVolumeSource(K8sObject):
    image: str = attr.ib(metadata={"yaml_name": "image"})
    monitors: Sequence[str] = attr.ib(metadata={"yaml_name": "monitors"})
    fsType: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "fsType"}, default=OMIT
    )
    keyring: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "keyring"}, default=OMIT
    )
    pool: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "pool"}, default=OMIT
    )
    readOnly: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "readOnly"}, default=OMIT
    )
    secretRef: Union[None, OmitEnum, kdsl.core.v1.SecretReference] = attr.ib(
        metadata={"yaml_name": "secretRef"},
        converter=kdsl.core.v1_converters.optional_converter_SecretReference,
        default=OMIT,
    )
    user: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "user"}, default=OMIT
    )


class RBDPersistentVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    fsType: str
    keyring: str
    pool: str
    readOnly: bool
    secretRef: kdsl.core.v1.SecretReference
    user: str


class RBDPersistentVolumeSourceTypedDict(
    RBDPersistentVolumeSourceOptionalTypedDict, total=(True)
):
    image: str
    monitors: Sequence[str]


RBDPersistentVolumeSourceUnion = Union[
    RBDPersistentVolumeSource, RBDPersistentVolumeSourceTypedDict
]


@attr.s(kw_only=True)
class PersistentVolumeSpec(K8sObject):
    accessModes: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "accessModes"}, default=OMIT
    )
    awsElasticBlockStore: Union[
        None, OmitEnum, kdsl.core.v1.AWSElasticBlockStoreVolumeSource
    ] = attr.ib(
        metadata={"yaml_name": "awsElasticBlockStore"},
        converter=kdsl.core.v1_converters.optional_converter_AWSElasticBlockStoreVolumeSource,
        default=OMIT,
    )
    azureDisk: Union[None, OmitEnum, kdsl.core.v1.AzureDiskVolumeSource] = attr.ib(
        metadata={"yaml_name": "azureDisk"},
        converter=kdsl.core.v1_converters.optional_converter_AzureDiskVolumeSource,
        default=OMIT,
    )
    azureFile: Union[
        None, OmitEnum, kdsl.core.v1.AzureFilePersistentVolumeSource
    ] = attr.ib(
        metadata={"yaml_name": "azureFile"},
        converter=kdsl.core.v1_converters.optional_converter_AzureFilePersistentVolumeSource,
        default=OMIT,
    )
    capacity: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(
        metadata={"yaml_name": "capacity"}, default=OMIT
    )
    cephfs: Union[None, OmitEnum, kdsl.core.v1.CephFSPersistentVolumeSource] = attr.ib(
        metadata={"yaml_name": "cephfs"},
        converter=kdsl.core.v1_converters.optional_converter_CephFSPersistentVolumeSource,
        default=OMIT,
    )
    cinder: Union[None, OmitEnum, kdsl.core.v1.CinderPersistentVolumeSource] = attr.ib(
        metadata={"yaml_name": "cinder"},
        converter=kdsl.core.v1_converters.optional_converter_CinderPersistentVolumeSource,
        default=OMIT,
    )
    claimRef: Union[None, OmitEnum, kdsl.core.v1.ObjectReference] = attr.ib(
        metadata={"yaml_name": "claimRef"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectReference,
        default=OMIT,
    )
    csi: Union[None, OmitEnum, kdsl.core.v1.CSIPersistentVolumeSource] = attr.ib(
        metadata={"yaml_name": "csi"},
        converter=kdsl.core.v1_converters.optional_converter_CSIPersistentVolumeSource,
        default=OMIT,
    )
    fc: Union[None, OmitEnum, kdsl.core.v1.FCVolumeSource] = attr.ib(
        metadata={"yaml_name": "fc"},
        converter=kdsl.core.v1_converters.optional_converter_FCVolumeSource,
        default=OMIT,
    )
    flexVolume: Union[
        None, OmitEnum, kdsl.core.v1.FlexPersistentVolumeSource
    ] = attr.ib(
        metadata={"yaml_name": "flexVolume"},
        converter=kdsl.core.v1_converters.optional_converter_FlexPersistentVolumeSource,
        default=OMIT,
    )
    flocker: Union[None, OmitEnum, kdsl.core.v1.FlockerVolumeSource] = attr.ib(
        metadata={"yaml_name": "flocker"},
        converter=kdsl.core.v1_converters.optional_converter_FlockerVolumeSource,
        default=OMIT,
    )
    gcePersistentDisk: Union[
        None, OmitEnum, kdsl.core.v1.GCEPersistentDiskVolumeSource
    ] = attr.ib(
        metadata={"yaml_name": "gcePersistentDisk"},
        converter=kdsl.core.v1_converters.optional_converter_GCEPersistentDiskVolumeSource,
        default=OMIT,
    )
    glusterfs: Union[
        None, OmitEnum, kdsl.core.v1.GlusterfsPersistentVolumeSource
    ] = attr.ib(
        metadata={"yaml_name": "glusterfs"},
        converter=kdsl.core.v1_converters.optional_converter_GlusterfsPersistentVolumeSource,
        default=OMIT,
    )
    hostPath: Union[None, OmitEnum, kdsl.core.v1.HostPathVolumeSource] = attr.ib(
        metadata={"yaml_name": "hostPath"},
        converter=kdsl.core.v1_converters.optional_converter_HostPathVolumeSource,
        default=OMIT,
    )
    iscsi: Union[None, OmitEnum, kdsl.core.v1.ISCSIPersistentVolumeSource] = attr.ib(
        metadata={"yaml_name": "iscsi"},
        converter=kdsl.core.v1_converters.optional_converter_ISCSIPersistentVolumeSource,
        default=OMIT,
    )
    local: Union[None, OmitEnum, kdsl.core.v1.LocalVolumeSource] = attr.ib(
        metadata={"yaml_name": "local"},
        converter=kdsl.core.v1_converters.optional_converter_LocalVolumeSource,
        default=OMIT,
    )
    mountOptions: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "mountOptions"}, default=OMIT
    )
    nfs: Union[None, OmitEnum, kdsl.core.v1.NFSVolumeSource] = attr.ib(
        metadata={"yaml_name": "nfs"},
        converter=kdsl.core.v1_converters.optional_converter_NFSVolumeSource,
        default=OMIT,
    )
    nodeAffinity: Union[None, OmitEnum, kdsl.core.v1.VolumeNodeAffinity] = attr.ib(
        metadata={"yaml_name": "nodeAffinity"},
        converter=kdsl.core.v1_converters.optional_converter_VolumeNodeAffinity,
        default=OMIT,
    )
    persistentVolumeReclaimPolicy: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "persistentVolumeReclaimPolicy"}, default=OMIT
    )
    photonPersistentDisk: Union[
        None, OmitEnum, kdsl.core.v1.PhotonPersistentDiskVolumeSource
    ] = attr.ib(
        metadata={"yaml_name": "photonPersistentDisk"},
        converter=kdsl.core.v1_converters.optional_converter_PhotonPersistentDiskVolumeSource,
        default=OMIT,
    )
    portworxVolume: Union[None, OmitEnum, kdsl.core.v1.PortworxVolumeSource] = attr.ib(
        metadata={"yaml_name": "portworxVolume"},
        converter=kdsl.core.v1_converters.optional_converter_PortworxVolumeSource,
        default=OMIT,
    )
    quobyte: Union[None, OmitEnum, kdsl.core.v1.QuobyteVolumeSource] = attr.ib(
        metadata={"yaml_name": "quobyte"},
        converter=kdsl.core.v1_converters.optional_converter_QuobyteVolumeSource,
        default=OMIT,
    )
    rbd: Union[None, OmitEnum, kdsl.core.v1.RBDPersistentVolumeSource] = attr.ib(
        metadata={"yaml_name": "rbd"},
        converter=kdsl.core.v1_converters.optional_converter_RBDPersistentVolumeSource,
        default=OMIT,
    )
    scaleIO: Union[
        None, OmitEnum, kdsl.core.v1.ScaleIOPersistentVolumeSource
    ] = attr.ib(
        metadata={"yaml_name": "scaleIO"},
        converter=kdsl.core.v1_converters.optional_converter_ScaleIOPersistentVolumeSource,
        default=OMIT,
    )
    storageClassName: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "storageClassName"}, default=OMIT
    )
    storageos: Union[
        None, OmitEnum, kdsl.core.v1.StorageOSPersistentVolumeSource
    ] = attr.ib(
        metadata={"yaml_name": "storageos"},
        converter=kdsl.core.v1_converters.optional_converter_StorageOSPersistentVolumeSource,
        default=OMIT,
    )
    volumeMode: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "volumeMode"}, default=OMIT
    )
    vsphereVolume: Union[
        None, OmitEnum, kdsl.core.v1.VsphereVirtualDiskVolumeSource
    ] = attr.ib(
        metadata={"yaml_name": "vsphereVolume"},
        converter=kdsl.core.v1_converters.optional_converter_VsphereVirtualDiskVolumeSource,
        default=OMIT,
    )


class PersistentVolumeSpecTypedDict(TypedDict, total=(False)):
    accessModes: Sequence[str]
    awsElasticBlockStore: kdsl.core.v1.AWSElasticBlockStoreVolumeSource
    azureDisk: kdsl.core.v1.AzureDiskVolumeSource
    azureFile: kdsl.core.v1.AzureFilePersistentVolumeSource
    capacity: Mapping[str, str]
    cephfs: kdsl.core.v1.CephFSPersistentVolumeSource
    cinder: kdsl.core.v1.CinderPersistentVolumeSource
    claimRef: kdsl.core.v1.ObjectReference
    csi: kdsl.core.v1.CSIPersistentVolumeSource
    fc: kdsl.core.v1.FCVolumeSource
    flexVolume: kdsl.core.v1.FlexPersistentVolumeSource
    flocker: kdsl.core.v1.FlockerVolumeSource
    gcePersistentDisk: kdsl.core.v1.GCEPersistentDiskVolumeSource
    glusterfs: kdsl.core.v1.GlusterfsPersistentVolumeSource
    hostPath: kdsl.core.v1.HostPathVolumeSource
    iscsi: kdsl.core.v1.ISCSIPersistentVolumeSource
    local: kdsl.core.v1.LocalVolumeSource
    mountOptions: Sequence[str]
    nfs: kdsl.core.v1.NFSVolumeSource
    nodeAffinity: kdsl.core.v1.VolumeNodeAffinity
    persistentVolumeReclaimPolicy: str
    photonPersistentDisk: kdsl.core.v1.PhotonPersistentDiskVolumeSource
    portworxVolume: kdsl.core.v1.PortworxVolumeSource
    quobyte: kdsl.core.v1.QuobyteVolumeSource
    rbd: kdsl.core.v1.RBDPersistentVolumeSource
    scaleIO: kdsl.core.v1.ScaleIOPersistentVolumeSource
    storageClassName: str
    storageos: kdsl.core.v1.StorageOSPersistentVolumeSource
    volumeMode: str
    vsphereVolume: kdsl.core.v1.VsphereVirtualDiskVolumeSource


PersistentVolumeSpecUnion = Union[PersistentVolumeSpec, PersistentVolumeSpecTypedDict]


@attr.s(kw_only=True)
class CSIVolumeSource(K8sObject):
    driver: str = attr.ib(metadata={"yaml_name": "driver"})
    fsType: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "fsType"}, default=OMIT
    )
    nodePublishSecretRef: Union[
        None, OmitEnum, kdsl.core.v1.LocalObjectReference
    ] = attr.ib(
        metadata={"yaml_name": "nodePublishSecretRef"},
        converter=kdsl.core.v1_converters.optional_converter_LocalObjectReference,
        default=OMIT,
    )
    readOnly: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "readOnly"}, default=OMIT
    )
    volumeAttributes: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(
        metadata={"yaml_name": "volumeAttributes"}, default=OMIT
    )


class CSIVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    fsType: str
    nodePublishSecretRef: kdsl.core.v1.LocalObjectReference
    readOnly: bool
    volumeAttributes: Mapping[str, str]


class CSIVolumeSourceTypedDict(CSIVolumeSourceOptionalTypedDict, total=(True)):
    driver: str


CSIVolumeSourceUnion = Union[CSIVolumeSource, CSIVolumeSourceTypedDict]


@attr.s(kw_only=True)
class ReplicationControllerStatus(K8sObject):
    replicas: int = attr.ib(metadata={"yaml_name": "replicas"})
    availableReplicas: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "availableReplicas"}, default=OMIT
    )
    conditions: Union[
        None, OmitEnum, Mapping[str, kdsl.core.v1.ReplicationControllerConditionItem]
    ] = attr.ib(
        metadata={"yaml_name": "conditions", "mlist_key": "type"},
        converter=kdsl.core.v1_converters.optional_mlist_converter_ReplicationControllerConditionItem,
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


class ReplicationControllerStatusOptionalTypedDict(TypedDict, total=(False)):
    availableReplicas: int
    conditions: Mapping[str, kdsl.core.v1.ReplicationControllerConditionItem]
    fullyLabeledReplicas: int
    observedGeneration: int
    readyReplicas: int


class ReplicationControllerStatusTypedDict(
    ReplicationControllerStatusOptionalTypedDict, total=(True)
):
    replicas: int


ReplicationControllerStatusUnion = Union[
    ReplicationControllerStatus, ReplicationControllerStatusTypedDict
]


@attr.s(kw_only=True)
class NamespaceStatus(K8sObject):
    conditions: Union[
        None, OmitEnum, Mapping[str, kdsl.core.v1.NamespaceConditionItem]
    ] = attr.ib(
        metadata={"yaml_name": "conditions", "mlist_key": "type"},
        converter=kdsl.core.v1_converters.optional_mlist_converter_NamespaceConditionItem,
        default=OMIT,
    )
    phase: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "phase"}, default=OMIT
    )


class NamespaceStatusTypedDict(TypedDict, total=(False)):
    conditions: Mapping[str, kdsl.core.v1.NamespaceConditionItem]
    phase: str


NamespaceStatusUnion = Union[NamespaceStatus, NamespaceStatusTypedDict]


@attr.s(kw_only=True)
class EventSource(K8sObject):
    component: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "component"}, default=OMIT
    )
    host: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "host"}, default=OMIT
    )


class EventSourceTypedDict(TypedDict, total=(False)):
    component: str
    host: str


EventSourceUnion = Union[EventSource, EventSourceTypedDict]


@attr.s(kw_only=True)
class VsphereVirtualDiskVolumeSource(K8sObject):
    volumePath: str = attr.ib(metadata={"yaml_name": "volumePath"})
    fsType: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "fsType"}, default=OMIT
    )
    storagePolicyID: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "storagePolicyID"}, default=OMIT
    )
    storagePolicyName: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "storagePolicyName"}, default=OMIT
    )


class VsphereVirtualDiskVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    fsType: str
    storagePolicyID: str
    storagePolicyName: str


class VsphereVirtualDiskVolumeSourceTypedDict(
    VsphereVirtualDiskVolumeSourceOptionalTypedDict, total=(True)
):
    volumePath: str


VsphereVirtualDiskVolumeSourceUnion = Union[
    VsphereVirtualDiskVolumeSource, VsphereVirtualDiskVolumeSourceTypedDict
]


@attr.s(kw_only=True)
class TopologySelectorLabelRequirement(K8sObject):
    key: str = attr.ib(metadata={"yaml_name": "key"})
    values: Sequence[str] = attr.ib(metadata={"yaml_name": "values"})


class TopologySelectorLabelRequirementTypedDict(TypedDict, total=(True)):
    key: str
    values: Sequence[str]


TopologySelectorLabelRequirementUnion = Union[
    TopologySelectorLabelRequirement, TopologySelectorLabelRequirementTypedDict
]


@attr.s(kw_only=True)
class PersistentVolumeClaimStatus(K8sObject):
    accessModes: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "accessModes"}, default=OMIT
    )
    capacity: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(
        metadata={"yaml_name": "capacity"}, default=OMIT
    )
    conditions: Union[
        None, OmitEnum, Mapping[str, kdsl.core.v1.PersistentVolumeClaimConditionItem]
    ] = attr.ib(
        metadata={"yaml_name": "conditions", "mlist_key": "type"},
        converter=kdsl.core.v1_converters.optional_mlist_converter_PersistentVolumeClaimConditionItem,
        default=OMIT,
    )
    phase: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "phase"}, default=OMIT
    )


class PersistentVolumeClaimStatusTypedDict(TypedDict, total=(False)):
    accessModes: Sequence[str]
    capacity: Mapping[str, str]
    conditions: Mapping[str, kdsl.core.v1.PersistentVolumeClaimConditionItem]
    phase: str


PersistentVolumeClaimStatusUnion = Union[
    PersistentVolumeClaimStatus, PersistentVolumeClaimStatusTypedDict
]


@attr.s(kw_only=True)
class EmbeddedPersistentVolumeClaim(K8sObject):
    apiVersion: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "apiVersion"}, default=OMIT
    )
    kind: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "kind"}, default=OMIT
    )
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    spec: Union[None, OmitEnum, kdsl.core.v1.PersistentVolumeClaimSpec] = attr.ib(
        metadata={"yaml_name": "spec"},
        converter=kdsl.core.v1_converters.optional_converter_PersistentVolumeClaimSpec,
        default=OMIT,
    )
    status: Union[None, OmitEnum, kdsl.core.v1.PersistentVolumeClaimStatus] = attr.ib(
        metadata={"yaml_name": "status"},
        converter=kdsl.core.v1_converters.optional_converter_PersistentVolumeClaimStatus,
        default=OMIT,
    )


class EmbeddedPersistentVolumeClaimTypedDict(TypedDict, total=(False)):
    apiVersion: str
    kind: str
    metadata: kdsl.core.v1.ObjectMeta
    spec: kdsl.core.v1.PersistentVolumeClaimSpec
    status: kdsl.core.v1.PersistentVolumeClaimStatus


EmbeddedPersistentVolumeClaimUnion = Union[
    EmbeddedPersistentVolumeClaim, EmbeddedPersistentVolumeClaimTypedDict
]


@attr.s(kw_only=True)
class ResourceFieldSelector(K8sObject):
    resource: str = attr.ib(metadata={"yaml_name": "resource"})
    containerName: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "containerName"}, default=OMIT
    )
    divisor: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "divisor"}, default=OMIT
    )


class ResourceFieldSelectorOptionalTypedDict(TypedDict, total=(False)):
    containerName: str
    divisor: str


class ResourceFieldSelectorTypedDict(
    ResourceFieldSelectorOptionalTypedDict, total=(True)
):
    resource: str


ResourceFieldSelectorUnion = Union[
    ResourceFieldSelector, ResourceFieldSelectorTypedDict
]


@attr.s(kw_only=True)
class PersistentVolumeClaimVolumeSource(K8sObject):
    claimName: str = attr.ib(metadata={"yaml_name": "claimName"})
    readOnly: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "readOnly"}, default=OMIT
    )


class PersistentVolumeClaimVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    readOnly: bool


class PersistentVolumeClaimVolumeSourceTypedDict(
    PersistentVolumeClaimVolumeSourceOptionalTypedDict, total=(True)
):
    claimName: str


PersistentVolumeClaimVolumeSourceUnion = Union[
    PersistentVolumeClaimVolumeSource, PersistentVolumeClaimVolumeSourceTypedDict
]


@attr.s(kw_only=True)
class ISCSIVolumeSource(K8sObject):
    iqn: str = attr.ib(metadata={"yaml_name": "iqn"})
    lun: int = attr.ib(metadata={"yaml_name": "lun"})
    targetPortal: str = attr.ib(metadata={"yaml_name": "targetPortal"})
    chapAuthDiscovery: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "chapAuthDiscovery"}, default=OMIT
    )
    chapAuthSession: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "chapAuthSession"}, default=OMIT
    )
    fsType: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "fsType"}, default=OMIT
    )
    initiatorName: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "initiatorName"}, default=OMIT
    )
    iscsiInterface: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "iscsiInterface"}, default=OMIT
    )
    portals: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "portals"}, default=OMIT
    )
    readOnly: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "readOnly"}, default=OMIT
    )
    secretRef: Union[None, OmitEnum, kdsl.core.v1.LocalObjectReference] = attr.ib(
        metadata={"yaml_name": "secretRef"},
        converter=kdsl.core.v1_converters.optional_converter_LocalObjectReference,
        default=OMIT,
    )


class ISCSIVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    chapAuthDiscovery: bool
    chapAuthSession: bool
    fsType: str
    initiatorName: str
    iscsiInterface: str
    portals: Sequence[str]
    readOnly: bool
    secretRef: kdsl.core.v1.LocalObjectReference


class ISCSIVolumeSourceTypedDict(ISCSIVolumeSourceOptionalTypedDict, total=(True)):
    iqn: str
    lun: int
    targetPortal: str


ISCSIVolumeSourceUnion = Union[ISCSIVolumeSource, ISCSIVolumeSourceTypedDict]


@attr.s(kw_only=True)
class ObjectMeta(K8sObject):
    annotations: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(
        metadata={"yaml_name": "annotations"}, default=OMIT
    )
    clusterName: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "clusterName"}, default=OMIT
    )
    creationTimestamp: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "creationTimestamp"}, default=OMIT
    )
    deletionGracePeriodSeconds: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "deletionGracePeriodSeconds"}, default=OMIT
    )
    deletionTimestamp: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "deletionTimestamp"}, default=OMIT
    )
    finalizers: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "finalizers"}, default=OMIT
    )
    generateName: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "generateName"}, default=OMIT
    )
    generation: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "generation"}, default=OMIT
    )
    labels: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(
        metadata={"yaml_name": "labels"}, default=OMIT
    )
    managedFields: Union[
        None, OmitEnum, Sequence[kdsl.core.v1.ManagedFieldsEntry]
    ] = attr.ib(
        metadata={"yaml_name": "managedFields"},
        converter=kdsl.core.v1_converters.optional_list_converter_ManagedFieldsEntry,
        default=OMIT,
    )
    name: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "name"}, default=OMIT
    )
    namespace: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "namespace"}, default=OMIT
    )
    ownerReferences: Union[
        None, OmitEnum, Mapping[str, kdsl.core.v1.OwnerReferenceItem]
    ] = attr.ib(
        metadata={"yaml_name": "ownerReferences", "mlist_key": "uid"},
        converter=kdsl.core.v1_converters.optional_mlist_converter_OwnerReferenceItem,
        default=OMIT,
    )
    resourceVersion: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "resourceVersion"}, default=OMIT
    )
    selfLink: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "selfLink"}, default=OMIT
    )
    uid: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "uid"}, default=OMIT
    )


class ObjectMetaTypedDict(TypedDict, total=(False)):
    annotations: Mapping[str, str]
    clusterName: str
    creationTimestamp: str
    deletionGracePeriodSeconds: int
    deletionTimestamp: str
    finalizers: Sequence[str]
    generateName: str
    generation: int
    labels: Mapping[str, str]
    managedFields: Sequence[kdsl.core.v1.ManagedFieldsEntry]
    name: str
    namespace: str
    ownerReferences: Mapping[str, kdsl.core.v1.OwnerReferenceItem]
    resourceVersion: str
    selfLink: str
    uid: str


ObjectMetaUnion = Union[ObjectMeta, ObjectMetaTypedDict]


@attr.s(kw_only=True)
class NodeConditionItem(K8sObject):
    status: str = attr.ib(metadata={"yaml_name": "status"})
    lastHeartbeatTime: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "lastHeartbeatTime"}, default=OMIT
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


class NodeConditionItemOptionalTypedDict(TypedDict, total=(False)):
    lastHeartbeatTime: str
    lastTransitionTime: str
    message: str
    reason: str


class NodeConditionItemTypedDict(NodeConditionItemOptionalTypedDict, total=(True)):
    status: str


NodeConditionItemUnion = Union[NodeConditionItem, NodeConditionItemTypedDict]


@attr.s(kw_only=True)
class VolumeMountItem(K8sObject):
    name: str = attr.ib(metadata={"yaml_name": "name"})
    mountPropagation: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "mountPropagation"}, default=OMIT
    )
    readOnly: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "readOnly"}, default=OMIT
    )
    subPath: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "subPath"}, default=OMIT
    )
    subPathExpr: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "subPathExpr"}, default=OMIT
    )


class VolumeMountItemOptionalTypedDict(TypedDict, total=(False)):
    mountPropagation: str
    readOnly: bool
    subPath: str
    subPathExpr: str


class VolumeMountItemTypedDict(VolumeMountItemOptionalTypedDict, total=(True)):
    name: str


VolumeMountItemUnion = Union[VolumeMountItem, VolumeMountItemTypedDict]


@attr.s(kw_only=True)
class LimitRange(K8sResource):
    apiVersion: ClassVar[str] = "v1"
    kind: ClassVar[str] = "LimitRange"
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    spec: Union[None, OmitEnum, kdsl.core.v1.LimitRangeSpec] = attr.ib(
        metadata={"yaml_name": "spec"},
        converter=kdsl.core.v1_converters.optional_converter_LimitRangeSpec,
        default=OMIT,
    )


@attr.s(kw_only=True)
class LocalObjectReference(K8sObject):
    name: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "name"}, default=OMIT
    )


class LocalObjectReferenceTypedDict(TypedDict, total=(False)):
    name: str


LocalObjectReferenceUnion = Union[LocalObjectReference, LocalObjectReferenceTypedDict]


@attr.s(kw_only=True)
class PersistentVolumeClaimSpec(K8sObject):
    accessModes: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "accessModes"}, default=OMIT
    )
    dataSource: Union[None, OmitEnum, kdsl.core.v1.TypedLocalObjectReference] = attr.ib(
        metadata={"yaml_name": "dataSource"},
        converter=kdsl.core.v1_converters.optional_converter_TypedLocalObjectReference,
        default=OMIT,
    )
    resources: Union[None, OmitEnum, kdsl.core.v1.ResourceRequirements] = attr.ib(
        metadata={"yaml_name": "resources"},
        converter=kdsl.core.v1_converters.optional_converter_ResourceRequirements,
        default=OMIT,
    )
    selector: Union[None, OmitEnum, kdsl.core.v1.LabelSelector] = attr.ib(
        metadata={"yaml_name": "selector"},
        converter=kdsl.core.v1_converters.optional_converter_LabelSelector,
        default=OMIT,
    )
    storageClassName: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "storageClassName"}, default=OMIT
    )
    volumeMode: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "volumeMode"}, default=OMIT
    )
    volumeName: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "volumeName"}, default=OMIT
    )


class PersistentVolumeClaimSpecTypedDict(TypedDict, total=(False)):
    accessModes: Sequence[str]
    dataSource: kdsl.core.v1.TypedLocalObjectReference
    resources: kdsl.core.v1.ResourceRequirements
    selector: kdsl.core.v1.LabelSelector
    storageClassName: str
    volumeMode: str
    volumeName: str


PersistentVolumeClaimSpecUnion = Union[
    PersistentVolumeClaimSpec, PersistentVolumeClaimSpecTypedDict
]


@attr.s(kw_only=True)
class FlockerVolumeSource(K8sObject):
    datasetName: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "datasetName"}, default=OMIT
    )
    datasetUUID: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "datasetUUID"}, default=OMIT
    )


class FlockerVolumeSourceTypedDict(TypedDict, total=(False)):
    datasetName: str
    datasetUUID: str


FlockerVolumeSourceUnion = Union[FlockerVolumeSource, FlockerVolumeSourceTypedDict]


@attr.s(kw_only=True)
class LoadBalancerIngress(K8sObject):
    hostname: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "hostname"}, default=OMIT
    )
    ip: Union[None, OmitEnum, str] = attr.ib(metadata={"yaml_name": "ip"}, default=OMIT)


class LoadBalancerIngressTypedDict(TypedDict, total=(False)):
    hostname: str
    ip: str


LoadBalancerIngressUnion = Union[LoadBalancerIngress, LoadBalancerIngressTypedDict]


@attr.s(kw_only=True)
class EphemeralContainerItem(K8sObject):
    args: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "args"}, default=OMIT
    )
    command: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "command"}, default=OMIT
    )
    env: Union[None, OmitEnum, Mapping[str, kdsl.core.v1.EnvVarItem]] = attr.ib(
        metadata={"yaml_name": "env", "mlist_key": "name"},
        converter=kdsl.core.v1_converters.optional_mlist_converter_EnvVarItem,
        default=OMIT,
    )
    envFrom: Union[None, OmitEnum, Sequence[kdsl.core.v1.EnvFromSource]] = attr.ib(
        metadata={"yaml_name": "envFrom"},
        converter=kdsl.core.v1_converters.optional_list_converter_EnvFromSource,
        default=OMIT,
    )
    image: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "image"}, default=OMIT
    )
    imagePullPolicy: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "imagePullPolicy"}, default=OMIT
    )
    lifecycle: Union[None, OmitEnum, kdsl.core.v1.Lifecycle] = attr.ib(
        metadata={"yaml_name": "lifecycle"},
        converter=kdsl.core.v1_converters.optional_converter_Lifecycle,
        default=OMIT,
    )
    livenessProbe: Union[None, OmitEnum, kdsl.core.v1.Probe] = attr.ib(
        metadata={"yaml_name": "livenessProbe"},
        converter=kdsl.core.v1_converters.optional_converter_Probe,
        default=OMIT,
    )
    ports: Union[None, OmitEnum, Sequence[kdsl.core.v1.ContainerPort]] = attr.ib(
        metadata={"yaml_name": "ports"},
        converter=kdsl.core.v1_converters.optional_list_converter_ContainerPort,
        default=OMIT,
    )
    readinessProbe: Union[None, OmitEnum, kdsl.core.v1.Probe] = attr.ib(
        metadata={"yaml_name": "readinessProbe"},
        converter=kdsl.core.v1_converters.optional_converter_Probe,
        default=OMIT,
    )
    resources: Union[None, OmitEnum, kdsl.core.v1.ResourceRequirements] = attr.ib(
        metadata={"yaml_name": "resources"},
        converter=kdsl.core.v1_converters.optional_converter_ResourceRequirements,
        default=OMIT,
    )
    securityContext: Union[None, OmitEnum, kdsl.core.v1.SecurityContext] = attr.ib(
        metadata={"yaml_name": "securityContext"},
        converter=kdsl.core.v1_converters.optional_converter_SecurityContext,
        default=OMIT,
    )
    startupProbe: Union[None, OmitEnum, kdsl.core.v1.Probe] = attr.ib(
        metadata={"yaml_name": "startupProbe"},
        converter=kdsl.core.v1_converters.optional_converter_Probe,
        default=OMIT,
    )
    stdin: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "stdin"}, default=OMIT
    )
    stdinOnce: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "stdinOnce"}, default=OMIT
    )
    targetContainerName: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "targetContainerName"}, default=OMIT
    )
    terminationMessagePath: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "terminationMessagePath"}, default=OMIT
    )
    terminationMessagePolicy: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "terminationMessagePolicy"}, default=OMIT
    )
    tty: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "tty"}, default=OMIT
    )
    volumeDevices: Union[
        None, OmitEnum, Mapping[str, kdsl.core.v1.VolumeDeviceItem]
    ] = attr.ib(
        metadata={"yaml_name": "volumeDevices", "mlist_key": "devicePath"},
        converter=kdsl.core.v1_converters.optional_mlist_converter_VolumeDeviceItem,
        default=OMIT,
    )
    volumeMounts: Union[
        None, OmitEnum, Mapping[str, kdsl.core.v1.VolumeMountItem]
    ] = attr.ib(
        metadata={"yaml_name": "volumeMounts", "mlist_key": "mountPath"},
        converter=kdsl.core.v1_converters.optional_mlist_converter_VolumeMountItem,
        default=OMIT,
    )
    workingDir: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "workingDir"}, default=OMIT
    )


class EphemeralContainerItemTypedDict(TypedDict, total=(False)):
    args: Sequence[str]
    command: Sequence[str]
    env: Mapping[str, kdsl.core.v1.EnvVarItem]
    envFrom: Sequence[kdsl.core.v1.EnvFromSource]
    image: str
    imagePullPolicy: str
    lifecycle: kdsl.core.v1.Lifecycle
    livenessProbe: kdsl.core.v1.Probe
    ports: Sequence[kdsl.core.v1.ContainerPort]
    readinessProbe: kdsl.core.v1.Probe
    resources: kdsl.core.v1.ResourceRequirements
    securityContext: kdsl.core.v1.SecurityContext
    startupProbe: kdsl.core.v1.Probe
    stdin: bool
    stdinOnce: bool
    targetContainerName: str
    terminationMessagePath: str
    terminationMessagePolicy: str
    tty: bool
    volumeDevices: Mapping[str, kdsl.core.v1.VolumeDeviceItem]
    volumeMounts: Mapping[str, kdsl.core.v1.VolumeMountItem]
    workingDir: str


EphemeralContainerItemUnion = Union[
    EphemeralContainerItem, EphemeralContainerItemTypedDict
]


@attr.s(kw_only=True)
class GlusterfsPersistentVolumeSource(K8sObject):
    endpoints: str = attr.ib(metadata={"yaml_name": "endpoints"})
    path: str = attr.ib(metadata={"yaml_name": "path"})
    endpointsNamespace: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "endpointsNamespace"}, default=OMIT
    )
    readOnly: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "readOnly"}, default=OMIT
    )


class GlusterfsPersistentVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    endpointsNamespace: str
    readOnly: bool


class GlusterfsPersistentVolumeSourceTypedDict(
    GlusterfsPersistentVolumeSourceOptionalTypedDict, total=(True)
):
    endpoints: str
    path: str


GlusterfsPersistentVolumeSourceUnion = Union[
    GlusterfsPersistentVolumeSource, GlusterfsPersistentVolumeSourceTypedDict
]


@attr.s(kw_only=True)
class CinderPersistentVolumeSource(K8sObject):
    volumeID: str = attr.ib(metadata={"yaml_name": "volumeID"})
    fsType: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "fsType"}, default=OMIT
    )
    readOnly: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "readOnly"}, default=OMIT
    )
    secretRef: Union[None, OmitEnum, kdsl.core.v1.SecretReference] = attr.ib(
        metadata={"yaml_name": "secretRef"},
        converter=kdsl.core.v1_converters.optional_converter_SecretReference,
        default=OMIT,
    )


class CinderPersistentVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    fsType: str
    readOnly: bool
    secretRef: kdsl.core.v1.SecretReference


class CinderPersistentVolumeSourceTypedDict(
    CinderPersistentVolumeSourceOptionalTypedDict, total=(True)
):
    volumeID: str


CinderPersistentVolumeSourceUnion = Union[
    CinderPersistentVolumeSource, CinderPersistentVolumeSourceTypedDict
]


@attr.s(kw_only=True)
class ProjectedVolumeSource(K8sObject):
    sources: Sequence[kdsl.core.v1.VolumeProjection] = attr.ib(
        metadata={"yaml_name": "sources"},
        converter=kdsl.core.v1_converters.required_list_converter_VolumeProjection,
    )
    defaultMode: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "defaultMode"}, default=OMIT
    )


class ProjectedVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    defaultMode: int


class ProjectedVolumeSourceTypedDict(
    ProjectedVolumeSourceOptionalTypedDict, total=(True)
):
    sources: Sequence[kdsl.core.v1.VolumeProjection]


ProjectedVolumeSourceUnion = Union[
    ProjectedVolumeSource, ProjectedVolumeSourceTypedDict
]


@attr.s(kw_only=True)
class ConfigMap(K8sResource):
    apiVersion: ClassVar[str] = "v1"
    kind: ClassVar[str] = "ConfigMap"
    binaryData: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(
        metadata={"yaml_name": "binaryData"}, default=OMIT
    )
    data: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(
        metadata={"yaml_name": "data"}, default=OMIT
    )
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )


@attr.s(kw_only=True)
class AWSElasticBlockStoreVolumeSource(K8sObject):
    volumeID: str = attr.ib(metadata={"yaml_name": "volumeID"})
    fsType: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "fsType"}, default=OMIT
    )
    partition: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "partition"}, default=OMIT
    )
    readOnly: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "readOnly"}, default=OMIT
    )


class AWSElasticBlockStoreVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    fsType: str
    partition: int
    readOnly: bool


class AWSElasticBlockStoreVolumeSourceTypedDict(
    AWSElasticBlockStoreVolumeSourceOptionalTypedDict, total=(True)
):
    volumeID: str


AWSElasticBlockStoreVolumeSourceUnion = Union[
    AWSElasticBlockStoreVolumeSource, AWSElasticBlockStoreVolumeSourceTypedDict
]


@attr.s(kw_only=True)
class PersistentVolumeStatus(K8sObject):
    message: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "message"}, default=OMIT
    )
    phase: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "phase"}, default=OMIT
    )
    reason: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "reason"}, default=OMIT
    )


class PersistentVolumeStatusTypedDict(TypedDict, total=(False)):
    message: str
    phase: str
    reason: str


PersistentVolumeStatusUnion = Union[
    PersistentVolumeStatus, PersistentVolumeStatusTypedDict
]


@attr.s(kw_only=True)
class NodeAffinity(K8sObject):
    preferredDuringSchedulingIgnoredDuringExecution: Union[
        None, OmitEnum, Sequence[kdsl.core.v1.PreferredSchedulingTerm]
    ] = attr.ib(
        metadata={"yaml_name": "preferredDuringSchedulingIgnoredDuringExecution"},
        converter=kdsl.core.v1_converters.optional_list_converter_PreferredSchedulingTerm,
        default=OMIT,
    )
    requiredDuringSchedulingIgnoredDuringExecution: Union[
        None, OmitEnum, kdsl.core.v1.NodeSelector
    ] = attr.ib(
        metadata={"yaml_name": "requiredDuringSchedulingIgnoredDuringExecution"},
        converter=kdsl.core.v1_converters.optional_converter_NodeSelector,
        default=OMIT,
    )


class NodeAffinityTypedDict(TypedDict, total=(False)):
    preferredDuringSchedulingIgnoredDuringExecution: Sequence[
        kdsl.core.v1.PreferredSchedulingTerm
    ]
    requiredDuringSchedulingIgnoredDuringExecution: kdsl.core.v1.NodeSelector


NodeAffinityUnion = Union[NodeAffinity, NodeAffinityTypedDict]


@attr.s(kw_only=True)
class ConfigMapProjection(K8sObject):
    items: Union[None, OmitEnum, Sequence[kdsl.core.v1.KeyToPath]] = attr.ib(
        metadata={"yaml_name": "items"},
        converter=kdsl.core.v1_converters.optional_list_converter_KeyToPath,
        default=OMIT,
    )
    name: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "name"}, default=OMIT
    )
    optional: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "optional"}, default=OMIT
    )


class ConfigMapProjectionTypedDict(TypedDict, total=(False)):
    items: Sequence[kdsl.core.v1.KeyToPath]
    name: str
    optional: bool


ConfigMapProjectionUnion = Union[ConfigMapProjection, ConfigMapProjectionTypedDict]


@attr.s(kw_only=True)
class PodIP(K8sObject):
    ip: Union[None, OmitEnum, str] = attr.ib(metadata={"yaml_name": "ip"}, default=OMIT)


class PodIPTypedDict(TypedDict, total=(False)):
    ip: str


PodIPUnion = Union[PodIP, PodIPTypedDict]


@attr.s(kw_only=True)
class EnvVarItem(K8sObject):
    value: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "value"}, default=OMIT
    )
    valueFrom: Union[None, OmitEnum, kdsl.core.v1.EnvVarSource] = attr.ib(
        metadata={"yaml_name": "valueFrom"},
        converter=kdsl.core.v1_converters.optional_converter_EnvVarSource,
        default=OMIT,
    )


class EnvVarItemTypedDict(TypedDict, total=(False)):
    value: str
    valueFrom: kdsl.core.v1.EnvVarSource


EnvVarItemUnion = Union[EnvVarItem, EnvVarItemTypedDict]


@attr.s(kw_only=True)
class NodeAddressItem(K8sObject):
    address: str = attr.ib(metadata={"yaml_name": "address"})


class NodeAddressItemTypedDict(TypedDict, total=(True)):
    address: str


NodeAddressItemUnion = Union[NodeAddressItem, NodeAddressItemTypedDict]


@attr.s(kw_only=True)
class CinderVolumeSource(K8sObject):
    volumeID: str = attr.ib(metadata={"yaml_name": "volumeID"})
    fsType: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "fsType"}, default=OMIT
    )
    readOnly: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "readOnly"}, default=OMIT
    )
    secretRef: Union[None, OmitEnum, kdsl.core.v1.LocalObjectReference] = attr.ib(
        metadata={"yaml_name": "secretRef"},
        converter=kdsl.core.v1_converters.optional_converter_LocalObjectReference,
        default=OMIT,
    )


class CinderVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    fsType: str
    readOnly: bool
    secretRef: kdsl.core.v1.LocalObjectReference


class CinderVolumeSourceTypedDict(CinderVolumeSourceOptionalTypedDict, total=(True)):
    volumeID: str


CinderVolumeSourceUnion = Union[CinderVolumeSource, CinderVolumeSourceTypedDict]


@attr.s(kw_only=True)
class TopologySpreadConstraintItem(K8sObject):
    maxSkew: int = attr.ib(metadata={"yaml_name": "maxSkew"})
    whenUnsatisfiable: str = attr.ib(metadata={"yaml_name": "whenUnsatisfiable"})
    labelSelector: Union[None, OmitEnum, kdsl.core.v1.LabelSelector] = attr.ib(
        metadata={"yaml_name": "labelSelector"},
        converter=kdsl.core.v1_converters.optional_converter_LabelSelector,
        default=OMIT,
    )


class TopologySpreadConstraintItemOptionalTypedDict(TypedDict, total=(False)):
    labelSelector: kdsl.core.v1.LabelSelector


class TopologySpreadConstraintItemTypedDict(
    TopologySpreadConstraintItemOptionalTypedDict, total=(True)
):
    maxSkew: int
    whenUnsatisfiable: str


TopologySpreadConstraintItemUnion = Union[
    TopologySpreadConstraintItem, TopologySpreadConstraintItemTypedDict
]


@attr.s(kw_only=True)
class NFSVolumeSource(K8sObject):
    path: str = attr.ib(metadata={"yaml_name": "path"})
    server: str = attr.ib(metadata={"yaml_name": "server"})
    readOnly: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "readOnly"}, default=OMIT
    )


class NFSVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    readOnly: bool


class NFSVolumeSourceTypedDict(NFSVolumeSourceOptionalTypedDict, total=(True)):
    path: str
    server: str


NFSVolumeSourceUnion = Union[NFSVolumeSource, NFSVolumeSourceTypedDict]


@attr.s(kw_only=True)
class ContainerStateWaiting(K8sObject):
    message: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "message"}, default=OMIT
    )
    reason: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "reason"}, default=OMIT
    )


class ContainerStateWaitingTypedDict(TypedDict, total=(False)):
    message: str
    reason: str


ContainerStateWaitingUnion = Union[
    ContainerStateWaiting, ContainerStateWaitingTypedDict
]


@attr.s(kw_only=True)
class ConfigMapVolumeSource(K8sObject):
    defaultMode: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "defaultMode"}, default=OMIT
    )
    items: Union[None, OmitEnum, Sequence[kdsl.core.v1.KeyToPath]] = attr.ib(
        metadata={"yaml_name": "items"},
        converter=kdsl.core.v1_converters.optional_list_converter_KeyToPath,
        default=OMIT,
    )
    name: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "name"}, default=OMIT
    )
    optional: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "optional"}, default=OMIT
    )


class ConfigMapVolumeSourceTypedDict(TypedDict, total=(False)):
    defaultMode: int
    items: Sequence[kdsl.core.v1.KeyToPath]
    name: str
    optional: bool


ConfigMapVolumeSourceUnion = Union[
    ConfigMapVolumeSource, ConfigMapVolumeSourceTypedDict
]


@attr.s(kw_only=True)
class ObjectFieldSelector(K8sObject):
    fieldPath: str = attr.ib(metadata={"yaml_name": "fieldPath"})
    apiVersion: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "apiVersion"}, default=OMIT
    )


class ObjectFieldSelectorOptionalTypedDict(TypedDict, total=(False)):
    apiVersion: str


class ObjectFieldSelectorTypedDict(ObjectFieldSelectorOptionalTypedDict, total=(True)):
    fieldPath: str


ObjectFieldSelectorUnion = Union[ObjectFieldSelector, ObjectFieldSelectorTypedDict]


@attr.s(kw_only=True)
class ReplicationController(K8sResource):
    apiVersion: ClassVar[str] = "v1"
    kind: ClassVar[str] = "ReplicationController"
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    spec: Union[None, OmitEnum, kdsl.core.v1.ReplicationControllerSpec] = attr.ib(
        metadata={"yaml_name": "spec"},
        converter=kdsl.core.v1_converters.optional_converter_ReplicationControllerSpec,
        default=OMIT,
    )
    status: Union[None, OmitEnum, kdsl.core.v1.ReplicationControllerStatus] = attr.ib(
        metadata={"yaml_name": "status"},
        converter=kdsl.core.v1_converters.optional_converter_ReplicationControllerStatus,
        default=OMIT,
    )


@attr.s(kw_only=True)
class TCPSocketAction(K8sObject):
    port: Union[int, str] = attr.ib(metadata={"yaml_name": "port"})
    host: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "host"}, default=OMIT
    )


class TCPSocketActionOptionalTypedDict(TypedDict, total=(False)):
    host: str


class TCPSocketActionTypedDict(TCPSocketActionOptionalTypedDict, total=(True)):
    port: Union[int, str]


TCPSocketActionUnion = Union[TCPSocketAction, TCPSocketActionTypedDict]


@attr.s(kw_only=True)
class PersistentVolume(K8sResource):
    apiVersion: ClassVar[str] = "v1"
    kind: ClassVar[str] = "PersistentVolume"
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    spec: Union[None, OmitEnum, kdsl.core.v1.PersistentVolumeSpec] = attr.ib(
        metadata={"yaml_name": "spec"},
        converter=kdsl.core.v1_converters.optional_converter_PersistentVolumeSpec,
        default=OMIT,
    )
    status: Union[None, OmitEnum, kdsl.core.v1.PersistentVolumeStatus] = attr.ib(
        metadata={"yaml_name": "status"},
        converter=kdsl.core.v1_converters.optional_converter_PersistentVolumeStatus,
        default=OMIT,
    )


@attr.s(kw_only=True)
class CSIPersistentVolumeSource(K8sObject):
    driver: str = attr.ib(metadata={"yaml_name": "driver"})
    volumeHandle: str = attr.ib(metadata={"yaml_name": "volumeHandle"})
    controllerExpandSecretRef: Union[
        None, OmitEnum, kdsl.core.v1.SecretReference
    ] = attr.ib(
        metadata={"yaml_name": "controllerExpandSecretRef"},
        converter=kdsl.core.v1_converters.optional_converter_SecretReference,
        default=OMIT,
    )
    controllerPublishSecretRef: Union[
        None, OmitEnum, kdsl.core.v1.SecretReference
    ] = attr.ib(
        metadata={"yaml_name": "controllerPublishSecretRef"},
        converter=kdsl.core.v1_converters.optional_converter_SecretReference,
        default=OMIT,
    )
    fsType: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "fsType"}, default=OMIT
    )
    nodePublishSecretRef: Union[None, OmitEnum, kdsl.core.v1.SecretReference] = attr.ib(
        metadata={"yaml_name": "nodePublishSecretRef"},
        converter=kdsl.core.v1_converters.optional_converter_SecretReference,
        default=OMIT,
    )
    nodeStageSecretRef: Union[None, OmitEnum, kdsl.core.v1.SecretReference] = attr.ib(
        metadata={"yaml_name": "nodeStageSecretRef"},
        converter=kdsl.core.v1_converters.optional_converter_SecretReference,
        default=OMIT,
    )
    readOnly: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "readOnly"}, default=OMIT
    )
    volumeAttributes: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(
        metadata={"yaml_name": "volumeAttributes"}, default=OMIT
    )


class CSIPersistentVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    controllerExpandSecretRef: kdsl.core.v1.SecretReference
    controllerPublishSecretRef: kdsl.core.v1.SecretReference
    fsType: str
    nodePublishSecretRef: kdsl.core.v1.SecretReference
    nodeStageSecretRef: kdsl.core.v1.SecretReference
    readOnly: bool
    volumeAttributes: Mapping[str, str]


class CSIPersistentVolumeSourceTypedDict(
    CSIPersistentVolumeSourceOptionalTypedDict, total=(True)
):
    driver: str
    volumeHandle: str


CSIPersistentVolumeSourceUnion = Union[
    CSIPersistentVolumeSource, CSIPersistentVolumeSourceTypedDict
]


@attr.s(kw_only=True)
class DownwardAPIProjection(K8sObject):
    items: Union[
        None, OmitEnum, Sequence[kdsl.core.v1.DownwardAPIVolumeFile]
    ] = attr.ib(
        metadata={"yaml_name": "items"},
        converter=kdsl.core.v1_converters.optional_list_converter_DownwardAPIVolumeFile,
        default=OMIT,
    )


class DownwardAPIProjectionTypedDict(TypedDict, total=(False)):
    items: Sequence[kdsl.core.v1.DownwardAPIVolumeFile]


DownwardAPIProjectionUnion = Union[
    DownwardAPIProjection, DownwardAPIProjectionTypedDict
]


@attr.s(kw_only=True)
class HostAliasItem(K8sObject):
    hostnames: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "hostnames"}, default=OMIT
    )


class HostAliasItemTypedDict(TypedDict, total=(False)):
    hostnames: Sequence[str]


HostAliasItemUnion = Union[HostAliasItem, HostAliasItemTypedDict]


@attr.s(kw_only=True)
class NodeSelectorRequirement(K8sObject):
    key: str = attr.ib(metadata={"yaml_name": "key"})
    operator: str = attr.ib(metadata={"yaml_name": "operator"})
    values: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "values"}, default=OMIT
    )


class NodeSelectorRequirementOptionalTypedDict(TypedDict, total=(False)):
    values: Sequence[str]


class NodeSelectorRequirementTypedDict(
    NodeSelectorRequirementOptionalTypedDict, total=(True)
):
    key: str
    operator: str


NodeSelectorRequirementUnion = Union[
    NodeSelectorRequirement, NodeSelectorRequirementTypedDict
]


@attr.s(kw_only=True)
class ContainerStateRunning(K8sObject):
    startedAt: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "startedAt"}, default=OMIT
    )


class ContainerStateRunningTypedDict(TypedDict, total=(False)):
    startedAt: str


ContainerStateRunningUnion = Union[
    ContainerStateRunning, ContainerStateRunningTypedDict
]


@attr.s(kw_only=True)
class DaemonEndpoint(K8sObject):
    Port: int = attr.ib(metadata={"yaml_name": "Port"})


class DaemonEndpointTypedDict(TypedDict, total=(True)):
    Port: int


DaemonEndpointUnion = Union[DaemonEndpoint, DaemonEndpointTypedDict]


@attr.s(kw_only=True)
class Volume(K8sObject):
    name: str = attr.ib(metadata={"yaml_name": "name"})
    awsElasticBlockStore: Union[
        None, OmitEnum, kdsl.core.v1.AWSElasticBlockStoreVolumeSource
    ] = attr.ib(
        metadata={"yaml_name": "awsElasticBlockStore"},
        converter=kdsl.core.v1_converters.optional_converter_AWSElasticBlockStoreVolumeSource,
        default=OMIT,
    )
    azureDisk: Union[None, OmitEnum, kdsl.core.v1.AzureDiskVolumeSource] = attr.ib(
        metadata={"yaml_name": "azureDisk"},
        converter=kdsl.core.v1_converters.optional_converter_AzureDiskVolumeSource,
        default=OMIT,
    )
    azureFile: Union[None, OmitEnum, kdsl.core.v1.AzureFileVolumeSource] = attr.ib(
        metadata={"yaml_name": "azureFile"},
        converter=kdsl.core.v1_converters.optional_converter_AzureFileVolumeSource,
        default=OMIT,
    )
    cephfs: Union[None, OmitEnum, kdsl.core.v1.CephFSVolumeSource] = attr.ib(
        metadata={"yaml_name": "cephfs"},
        converter=kdsl.core.v1_converters.optional_converter_CephFSVolumeSource,
        default=OMIT,
    )
    cinder: Union[None, OmitEnum, kdsl.core.v1.CinderVolumeSource] = attr.ib(
        metadata={"yaml_name": "cinder"},
        converter=kdsl.core.v1_converters.optional_converter_CinderVolumeSource,
        default=OMIT,
    )
    configMap: Union[None, OmitEnum, kdsl.core.v1.ConfigMapVolumeSource] = attr.ib(
        metadata={"yaml_name": "configMap"},
        converter=kdsl.core.v1_converters.optional_converter_ConfigMapVolumeSource,
        default=OMIT,
    )
    csi: Union[None, OmitEnum, kdsl.core.v1.CSIVolumeSource] = attr.ib(
        metadata={"yaml_name": "csi"},
        converter=kdsl.core.v1_converters.optional_converter_CSIVolumeSource,
        default=OMIT,
    )
    downwardAPI: Union[None, OmitEnum, kdsl.core.v1.DownwardAPIVolumeSource] = attr.ib(
        metadata={"yaml_name": "downwardAPI"},
        converter=kdsl.core.v1_converters.optional_converter_DownwardAPIVolumeSource,
        default=OMIT,
    )
    emptyDir: Union[None, OmitEnum, kdsl.core.v1.EmptyDirVolumeSource] = attr.ib(
        metadata={"yaml_name": "emptyDir"},
        converter=kdsl.core.v1_converters.optional_converter_EmptyDirVolumeSource,
        default=OMIT,
    )
    fc: Union[None, OmitEnum, kdsl.core.v1.FCVolumeSource] = attr.ib(
        metadata={"yaml_name": "fc"},
        converter=kdsl.core.v1_converters.optional_converter_FCVolumeSource,
        default=OMIT,
    )
    flexVolume: Union[None, OmitEnum, kdsl.core.v1.FlexVolumeSource] = attr.ib(
        metadata={"yaml_name": "flexVolume"},
        converter=kdsl.core.v1_converters.optional_converter_FlexVolumeSource,
        default=OMIT,
    )
    flocker: Union[None, OmitEnum, kdsl.core.v1.FlockerVolumeSource] = attr.ib(
        metadata={"yaml_name": "flocker"},
        converter=kdsl.core.v1_converters.optional_converter_FlockerVolumeSource,
        default=OMIT,
    )
    gcePersistentDisk: Union[
        None, OmitEnum, kdsl.core.v1.GCEPersistentDiskVolumeSource
    ] = attr.ib(
        metadata={"yaml_name": "gcePersistentDisk"},
        converter=kdsl.core.v1_converters.optional_converter_GCEPersistentDiskVolumeSource,
        default=OMIT,
    )
    gitRepo: Union[None, OmitEnum, kdsl.core.v1.GitRepoVolumeSource] = attr.ib(
        metadata={"yaml_name": "gitRepo"},
        converter=kdsl.core.v1_converters.optional_converter_GitRepoVolumeSource,
        default=OMIT,
    )
    glusterfs: Union[None, OmitEnum, kdsl.core.v1.GlusterfsVolumeSource] = attr.ib(
        metadata={"yaml_name": "glusterfs"},
        converter=kdsl.core.v1_converters.optional_converter_GlusterfsVolumeSource,
        default=OMIT,
    )
    hostPath: Union[None, OmitEnum, kdsl.core.v1.HostPathVolumeSource] = attr.ib(
        metadata={"yaml_name": "hostPath"},
        converter=kdsl.core.v1_converters.optional_converter_HostPathVolumeSource,
        default=OMIT,
    )
    iscsi: Union[None, OmitEnum, kdsl.core.v1.ISCSIVolumeSource] = attr.ib(
        metadata={"yaml_name": "iscsi"},
        converter=kdsl.core.v1_converters.optional_converter_ISCSIVolumeSource,
        default=OMIT,
    )
    nfs: Union[None, OmitEnum, kdsl.core.v1.NFSVolumeSource] = attr.ib(
        metadata={"yaml_name": "nfs"},
        converter=kdsl.core.v1_converters.optional_converter_NFSVolumeSource,
        default=OMIT,
    )
    persistentVolumeClaim: Union[
        None, OmitEnum, kdsl.core.v1.PersistentVolumeClaimVolumeSource
    ] = attr.ib(
        metadata={"yaml_name": "persistentVolumeClaim"},
        converter=kdsl.core.v1_converters.optional_converter_PersistentVolumeClaimVolumeSource,
        default=OMIT,
    )
    photonPersistentDisk: Union[
        None, OmitEnum, kdsl.core.v1.PhotonPersistentDiskVolumeSource
    ] = attr.ib(
        metadata={"yaml_name": "photonPersistentDisk"},
        converter=kdsl.core.v1_converters.optional_converter_PhotonPersistentDiskVolumeSource,
        default=OMIT,
    )
    portworxVolume: Union[None, OmitEnum, kdsl.core.v1.PortworxVolumeSource] = attr.ib(
        metadata={"yaml_name": "portworxVolume"},
        converter=kdsl.core.v1_converters.optional_converter_PortworxVolumeSource,
        default=OMIT,
    )
    projected: Union[None, OmitEnum, kdsl.core.v1.ProjectedVolumeSource] = attr.ib(
        metadata={"yaml_name": "projected"},
        converter=kdsl.core.v1_converters.optional_converter_ProjectedVolumeSource,
        default=OMIT,
    )
    quobyte: Union[None, OmitEnum, kdsl.core.v1.QuobyteVolumeSource] = attr.ib(
        metadata={"yaml_name": "quobyte"},
        converter=kdsl.core.v1_converters.optional_converter_QuobyteVolumeSource,
        default=OMIT,
    )
    rbd: Union[None, OmitEnum, kdsl.core.v1.RBDVolumeSource] = attr.ib(
        metadata={"yaml_name": "rbd"},
        converter=kdsl.core.v1_converters.optional_converter_RBDVolumeSource,
        default=OMIT,
    )
    scaleIO: Union[None, OmitEnum, kdsl.core.v1.ScaleIOVolumeSource] = attr.ib(
        metadata={"yaml_name": "scaleIO"},
        converter=kdsl.core.v1_converters.optional_converter_ScaleIOVolumeSource,
        default=OMIT,
    )
    secret: Union[None, OmitEnum, kdsl.core.v1.SecretVolumeSource] = attr.ib(
        metadata={"yaml_name": "secret"},
        converter=kdsl.core.v1_converters.optional_converter_SecretVolumeSource,
        default=OMIT,
    )
    storageos: Union[None, OmitEnum, kdsl.core.v1.StorageOSVolumeSource] = attr.ib(
        metadata={"yaml_name": "storageos"},
        converter=kdsl.core.v1_converters.optional_converter_StorageOSVolumeSource,
        default=OMIT,
    )
    vsphereVolume: Union[
        None, OmitEnum, kdsl.core.v1.VsphereVirtualDiskVolumeSource
    ] = attr.ib(
        metadata={"yaml_name": "vsphereVolume"},
        converter=kdsl.core.v1_converters.optional_converter_VsphereVirtualDiskVolumeSource,
        default=OMIT,
    )


class VolumeOptionalTypedDict(TypedDict, total=(False)):
    awsElasticBlockStore: kdsl.core.v1.AWSElasticBlockStoreVolumeSource
    azureDisk: kdsl.core.v1.AzureDiskVolumeSource
    azureFile: kdsl.core.v1.AzureFileVolumeSource
    cephfs: kdsl.core.v1.CephFSVolumeSource
    cinder: kdsl.core.v1.CinderVolumeSource
    configMap: kdsl.core.v1.ConfigMapVolumeSource
    csi: kdsl.core.v1.CSIVolumeSource
    downwardAPI: kdsl.core.v1.DownwardAPIVolumeSource
    emptyDir: kdsl.core.v1.EmptyDirVolumeSource
    fc: kdsl.core.v1.FCVolumeSource
    flexVolume: kdsl.core.v1.FlexVolumeSource
    flocker: kdsl.core.v1.FlockerVolumeSource
    gcePersistentDisk: kdsl.core.v1.GCEPersistentDiskVolumeSource
    gitRepo: kdsl.core.v1.GitRepoVolumeSource
    glusterfs: kdsl.core.v1.GlusterfsVolumeSource
    hostPath: kdsl.core.v1.HostPathVolumeSource
    iscsi: kdsl.core.v1.ISCSIVolumeSource
    nfs: kdsl.core.v1.NFSVolumeSource
    persistentVolumeClaim: kdsl.core.v1.PersistentVolumeClaimVolumeSource
    photonPersistentDisk: kdsl.core.v1.PhotonPersistentDiskVolumeSource
    portworxVolume: kdsl.core.v1.PortworxVolumeSource
    projected: kdsl.core.v1.ProjectedVolumeSource
    quobyte: kdsl.core.v1.QuobyteVolumeSource
    rbd: kdsl.core.v1.RBDVolumeSource
    scaleIO: kdsl.core.v1.ScaleIOVolumeSource
    secret: kdsl.core.v1.SecretVolumeSource
    storageos: kdsl.core.v1.StorageOSVolumeSource
    vsphereVolume: kdsl.core.v1.VsphereVirtualDiskVolumeSource


class VolumeTypedDict(VolumeOptionalTypedDict, total=(True)):
    name: str


VolumeUnion = Union[Volume, VolumeTypedDict]


@attr.s(kw_only=True)
class ResourceQuotaStatus(K8sObject):
    hard: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(
        metadata={"yaml_name": "hard"}, default=OMIT
    )
    used: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(
        metadata={"yaml_name": "used"}, default=OMIT
    )


class ResourceQuotaStatusTypedDict(TypedDict, total=(False)):
    hard: Mapping[str, str]
    used: Mapping[str, str]


ResourceQuotaStatusUnion = Union[ResourceQuotaStatus, ResourceQuotaStatusTypedDict]


@attr.s(kw_only=True)
class ConfigMapNodeConfigSource(K8sObject):
    kubeletConfigKey: str = attr.ib(metadata={"yaml_name": "kubeletConfigKey"})
    name: str = attr.ib(metadata={"yaml_name": "name"})
    namespace: str = attr.ib(metadata={"yaml_name": "namespace"})
    resourceVersion: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "resourceVersion"}, default=OMIT
    )
    uid: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "uid"}, default=OMIT
    )


class ConfigMapNodeConfigSourceOptionalTypedDict(TypedDict, total=(False)):
    resourceVersion: str
    uid: str


class ConfigMapNodeConfigSourceTypedDict(
    ConfigMapNodeConfigSourceOptionalTypedDict, total=(True)
):
    kubeletConfigKey: str
    name: str
    namespace: str


ConfigMapNodeConfigSourceUnion = Union[
    ConfigMapNodeConfigSource, ConfigMapNodeConfigSourceTypedDict
]


@attr.s(kw_only=True)
class PodReadinessGate(K8sObject):
    conditionType: str = attr.ib(metadata={"yaml_name": "conditionType"})


class PodReadinessGateTypedDict(TypedDict, total=(True)):
    conditionType: str


PodReadinessGateUnion = Union[PodReadinessGate, PodReadinessGateTypedDict]


@attr.s(kw_only=True)
class StorageOSVolumeSource(K8sObject):
    fsType: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "fsType"}, default=OMIT
    )
    readOnly: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "readOnly"}, default=OMIT
    )
    secretRef: Union[None, OmitEnum, kdsl.core.v1.LocalObjectReference] = attr.ib(
        metadata={"yaml_name": "secretRef"},
        converter=kdsl.core.v1_converters.optional_converter_LocalObjectReference,
        default=OMIT,
    )
    volumeName: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "volumeName"}, default=OMIT
    )
    volumeNamespace: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "volumeNamespace"}, default=OMIT
    )


class StorageOSVolumeSourceTypedDict(TypedDict, total=(False)):
    fsType: str
    readOnly: bool
    secretRef: kdsl.core.v1.LocalObjectReference
    volumeName: str
    volumeNamespace: str


StorageOSVolumeSourceUnion = Union[
    StorageOSVolumeSource, StorageOSVolumeSourceTypedDict
]


@attr.s(kw_only=True)
class Affinity(K8sObject):
    nodeAffinity: Union[None, OmitEnum, kdsl.core.v1.NodeAffinity] = attr.ib(
        metadata={"yaml_name": "nodeAffinity"},
        converter=kdsl.core.v1_converters.optional_converter_NodeAffinity,
        default=OMIT,
    )
    podAffinity: Union[None, OmitEnum, kdsl.core.v1.PodAffinity] = attr.ib(
        metadata={"yaml_name": "podAffinity"},
        converter=kdsl.core.v1_converters.optional_converter_PodAffinity,
        default=OMIT,
    )
    podAntiAffinity: Union[None, OmitEnum, kdsl.core.v1.PodAntiAffinity] = attr.ib(
        metadata={"yaml_name": "podAntiAffinity"},
        converter=kdsl.core.v1_converters.optional_converter_PodAntiAffinity,
        default=OMIT,
    )


class AffinityTypedDict(TypedDict, total=(False)):
    nodeAffinity: kdsl.core.v1.NodeAffinity
    podAffinity: kdsl.core.v1.PodAffinity
    podAntiAffinity: kdsl.core.v1.PodAntiAffinity


AffinityUnion = Union[Affinity, AffinityTypedDict]


@attr.s(kw_only=True)
class PersistentVolumeClaimConditionItem(K8sObject):
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


class PersistentVolumeClaimConditionItemOptionalTypedDict(TypedDict, total=(False)):
    lastProbeTime: str
    lastTransitionTime: str
    message: str
    reason: str


class PersistentVolumeClaimConditionItemTypedDict(
    PersistentVolumeClaimConditionItemOptionalTypedDict, total=(True)
):
    status: str


PersistentVolumeClaimConditionItemUnion = Union[
    PersistentVolumeClaimConditionItem, PersistentVolumeClaimConditionItemTypedDict
]


@attr.s(kw_only=True)
class PersistentVolumeClaim(K8sResource):
    apiVersion: ClassVar[str] = "v1"
    kind: ClassVar[str] = "PersistentVolumeClaim"
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    spec: Union[None, OmitEnum, kdsl.core.v1.PersistentVolumeClaimSpec] = attr.ib(
        metadata={"yaml_name": "spec"},
        converter=kdsl.core.v1_converters.optional_converter_PersistentVolumeClaimSpec,
        default=OMIT,
    )
    status: Union[None, OmitEnum, kdsl.core.v1.PersistentVolumeClaimStatus] = attr.ib(
        metadata={"yaml_name": "status"},
        converter=kdsl.core.v1_converters.optional_converter_PersistentVolumeClaimStatus,
        default=OMIT,
    )


@attr.s(kw_only=True)
class ISCSIPersistentVolumeSource(K8sObject):
    iqn: str = attr.ib(metadata={"yaml_name": "iqn"})
    lun: int = attr.ib(metadata={"yaml_name": "lun"})
    targetPortal: str = attr.ib(metadata={"yaml_name": "targetPortal"})
    chapAuthDiscovery: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "chapAuthDiscovery"}, default=OMIT
    )
    chapAuthSession: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "chapAuthSession"}, default=OMIT
    )
    fsType: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "fsType"}, default=OMIT
    )
    initiatorName: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "initiatorName"}, default=OMIT
    )
    iscsiInterface: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "iscsiInterface"}, default=OMIT
    )
    portals: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "portals"}, default=OMIT
    )
    readOnly: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "readOnly"}, default=OMIT
    )
    secretRef: Union[None, OmitEnum, kdsl.core.v1.SecretReference] = attr.ib(
        metadata={"yaml_name": "secretRef"},
        converter=kdsl.core.v1_converters.optional_converter_SecretReference,
        default=OMIT,
    )


class ISCSIPersistentVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    chapAuthDiscovery: bool
    chapAuthSession: bool
    fsType: str
    initiatorName: str
    iscsiInterface: str
    portals: Sequence[str]
    readOnly: bool
    secretRef: kdsl.core.v1.SecretReference


class ISCSIPersistentVolumeSourceTypedDict(
    ISCSIPersistentVolumeSourceOptionalTypedDict, total=(True)
):
    iqn: str
    lun: int
    targetPortal: str


ISCSIPersistentVolumeSourceUnion = Union[
    ISCSIPersistentVolumeSource, ISCSIPersistentVolumeSourceTypedDict
]


@attr.s(kw_only=True)
class HostPathVolumeSource(K8sObject):
    path: str = attr.ib(metadata={"yaml_name": "path"})
    type: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "type"}, default=OMIT
    )


class HostPathVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    type: str


class HostPathVolumeSourceTypedDict(
    HostPathVolumeSourceOptionalTypedDict, total=(True)
):
    path: str


HostPathVolumeSourceUnion = Union[HostPathVolumeSource, HostPathVolumeSourceTypedDict]


@attr.s(kw_only=True)
class ContainerStateTerminated(K8sObject):
    exitCode: int = attr.ib(metadata={"yaml_name": "exitCode"})
    containerID: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "containerID"}, default=OMIT
    )
    finishedAt: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "finishedAt"}, default=OMIT
    )
    message: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "message"}, default=OMIT
    )
    reason: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "reason"}, default=OMIT
    )
    signal: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "signal"}, default=OMIT
    )
    startedAt: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "startedAt"}, default=OMIT
    )


class ContainerStateTerminatedOptionalTypedDict(TypedDict, total=(False)):
    containerID: str
    finishedAt: str
    message: str
    reason: str
    signal: int
    startedAt: str


class ContainerStateTerminatedTypedDict(
    ContainerStateTerminatedOptionalTypedDict, total=(True)
):
    exitCode: int


ContainerStateTerminatedUnion = Union[
    ContainerStateTerminated, ContainerStateTerminatedTypedDict
]


@attr.s(kw_only=True)
class Endpoints(K8sResource):
    apiVersion: ClassVar[str] = "v1"
    kind: ClassVar[str] = "Endpoints"
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    subsets: Union[None, OmitEnum, Sequence[kdsl.core.v1.EndpointSubset]] = attr.ib(
        metadata={"yaml_name": "subsets"},
        converter=kdsl.core.v1_converters.optional_list_converter_EndpointSubset,
        default=OMIT,
    )


@attr.s(kw_only=True)
class LabelSelector(K8sObject):
    matchExpressions: Union[
        None, OmitEnum, Sequence[kdsl.core.v1.LabelSelectorRequirement]
    ] = attr.ib(
        metadata={"yaml_name": "matchExpressions"},
        converter=kdsl.core.v1_converters.optional_list_converter_LabelSelectorRequirement,
        default=OMIT,
    )
    matchLabels: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(
        metadata={"yaml_name": "matchLabels"}, default=OMIT
    )


class LabelSelectorTypedDict(TypedDict, total=(False)):
    matchExpressions: Sequence[kdsl.core.v1.LabelSelectorRequirement]
    matchLabels: Mapping[str, str]


LabelSelectorUnion = Union[LabelSelector, LabelSelectorTypedDict]


@attr.s(kw_only=True)
class CephFSPersistentVolumeSource(K8sObject):
    monitors: Sequence[str] = attr.ib(metadata={"yaml_name": "monitors"})
    path: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "path"}, default=OMIT
    )
    readOnly: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "readOnly"}, default=OMIT
    )
    secretFile: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "secretFile"}, default=OMIT
    )
    secretRef: Union[None, OmitEnum, kdsl.core.v1.SecretReference] = attr.ib(
        metadata={"yaml_name": "secretRef"},
        converter=kdsl.core.v1_converters.optional_converter_SecretReference,
        default=OMIT,
    )
    user: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "user"}, default=OMIT
    )


class CephFSPersistentVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    path: str
    readOnly: bool
    secretFile: str
    secretRef: kdsl.core.v1.SecretReference
    user: str


class CephFSPersistentVolumeSourceTypedDict(
    CephFSPersistentVolumeSourceOptionalTypedDict, total=(True)
):
    monitors: Sequence[str]


CephFSPersistentVolumeSourceUnion = Union[
    CephFSPersistentVolumeSource, CephFSPersistentVolumeSourceTypedDict
]


@attr.s(kw_only=True)
class VolumeNodeAffinity(K8sObject):
    required: Union[None, OmitEnum, kdsl.core.v1.NodeSelector] = attr.ib(
        metadata={"yaml_name": "required"},
        converter=kdsl.core.v1_converters.optional_converter_NodeSelector,
        default=OMIT,
    )


class VolumeNodeAffinityTypedDict(TypedDict, total=(False)):
    required: kdsl.core.v1.NodeSelector


VolumeNodeAffinityUnion = Union[VolumeNodeAffinity, VolumeNodeAffinityTypedDict]


@attr.s(kw_only=True)
class PodAffinity(K8sObject):
    preferredDuringSchedulingIgnoredDuringExecution: Union[
        None, OmitEnum, Sequence[kdsl.core.v1.WeightedPodAffinityTerm]
    ] = attr.ib(
        metadata={"yaml_name": "preferredDuringSchedulingIgnoredDuringExecution"},
        converter=kdsl.core.v1_converters.optional_list_converter_WeightedPodAffinityTerm,
        default=OMIT,
    )
    requiredDuringSchedulingIgnoredDuringExecution: Union[
        None, OmitEnum, Sequence[kdsl.core.v1.PodAffinityTerm]
    ] = attr.ib(
        metadata={"yaml_name": "requiredDuringSchedulingIgnoredDuringExecution"},
        converter=kdsl.core.v1_converters.optional_list_converter_PodAffinityTerm,
        default=OMIT,
    )


class PodAffinityTypedDict(TypedDict, total=(False)):
    preferredDuringSchedulingIgnoredDuringExecution: Sequence[
        kdsl.core.v1.WeightedPodAffinityTerm
    ]
    requiredDuringSchedulingIgnoredDuringExecution: Sequence[
        kdsl.core.v1.PodAffinityTerm
    ]


PodAffinityUnion = Union[PodAffinity, PodAffinityTypedDict]


@attr.s(kw_only=True)
class ServiceSpec(K8sObject):
    clusterIP: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "clusterIP"}, default=OMIT
    )
    externalIPs: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "externalIPs"}, default=OMIT
    )
    externalName: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "externalName"}, default=OMIT
    )
    externalTrafficPolicy: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "externalTrafficPolicy"}, default=OMIT
    )
    healthCheckNodePort: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "healthCheckNodePort"}, default=OMIT
    )
    ipFamily: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "ipFamily"}, default=OMIT
    )
    loadBalancerIP: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "loadBalancerIP"}, default=OMIT
    )
    loadBalancerSourceRanges: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "loadBalancerSourceRanges"}, default=OMIT
    )
    ports: Union[None, OmitEnum, Mapping[int, kdsl.core.v1.ServicePortItem]] = attr.ib(
        metadata={"yaml_name": "ports", "mlist_key": "port"},
        converter=kdsl.core.v1_converters.optional_mlist_converter_ServicePortItem,
        default=OMIT,
    )
    publishNotReadyAddresses: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "publishNotReadyAddresses"}, default=OMIT
    )
    selector: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(
        metadata={"yaml_name": "selector"}, default=OMIT
    )
    sessionAffinity: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "sessionAffinity"}, default=OMIT
    )
    sessionAffinityConfig: Union[
        None, OmitEnum, kdsl.core.v1.SessionAffinityConfig
    ] = attr.ib(
        metadata={"yaml_name": "sessionAffinityConfig"},
        converter=kdsl.core.v1_converters.optional_converter_SessionAffinityConfig,
        default=OMIT,
    )
    topologyKeys: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "topologyKeys"}, default=OMIT
    )
    type: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "type"}, default=OMIT
    )


class ServiceSpecTypedDict(TypedDict, total=(False)):
    clusterIP: str
    externalIPs: Sequence[str]
    externalName: str
    externalTrafficPolicy: str
    healthCheckNodePort: int
    ipFamily: str
    loadBalancerIP: str
    loadBalancerSourceRanges: Sequence[str]
    ports: Mapping[int, kdsl.core.v1.ServicePortItem]
    publishNotReadyAddresses: bool
    selector: Mapping[str, str]
    sessionAffinity: str
    sessionAffinityConfig: kdsl.core.v1.SessionAffinityConfig
    topologyKeys: Sequence[str]
    type: str


ServiceSpecUnion = Union[ServiceSpec, ServiceSpecTypedDict]


@attr.s(kw_only=True)
class NamespaceSpec(K8sObject):
    finalizers: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "finalizers"}, default=OMIT
    )


class NamespaceSpecTypedDict(TypedDict, total=(False)):
    finalizers: Sequence[str]


NamespaceSpecUnion = Union[NamespaceSpec, NamespaceSpecTypedDict]


@attr.s(kw_only=True)
class FlexVolumeSource(K8sObject):
    driver: str = attr.ib(metadata={"yaml_name": "driver"})
    fsType: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "fsType"}, default=OMIT
    )
    options: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(
        metadata={"yaml_name": "options"}, default=OMIT
    )
    readOnly: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "readOnly"}, default=OMIT
    )
    secretRef: Union[None, OmitEnum, kdsl.core.v1.LocalObjectReference] = attr.ib(
        metadata={"yaml_name": "secretRef"},
        converter=kdsl.core.v1_converters.optional_converter_LocalObjectReference,
        default=OMIT,
    )


class FlexVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    fsType: str
    options: Mapping[str, str]
    readOnly: bool
    secretRef: kdsl.core.v1.LocalObjectReference


class FlexVolumeSourceTypedDict(FlexVolumeSourceOptionalTypedDict, total=(True)):
    driver: str


FlexVolumeSourceUnion = Union[FlexVolumeSource, FlexVolumeSourceTypedDict]


@attr.s(kw_only=True)
class PodTemplateSpec(K8sObject):
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    spec: Union[None, OmitEnum, kdsl.core.v1.PodSpec] = attr.ib(
        metadata={"yaml_name": "spec"},
        converter=kdsl.core.v1_converters.optional_converter_PodSpec,
        default=OMIT,
    )


class PodTemplateSpecTypedDict(TypedDict, total=(False)):
    metadata: kdsl.core.v1.ObjectMeta
    spec: kdsl.core.v1.PodSpec


PodTemplateSpecUnion = Union[PodTemplateSpec, PodTemplateSpecTypedDict]


@attr.s(kw_only=True)
class EndpointSubset(K8sObject):
    addresses: Union[None, OmitEnum, Sequence[kdsl.core.v1.EndpointAddress]] = attr.ib(
        metadata={"yaml_name": "addresses"},
        converter=kdsl.core.v1_converters.optional_list_converter_EndpointAddress,
        default=OMIT,
    )
    notReadyAddresses: Union[
        None, OmitEnum, Sequence[kdsl.core.v1.EndpointAddress]
    ] = attr.ib(
        metadata={"yaml_name": "notReadyAddresses"},
        converter=kdsl.core.v1_converters.optional_list_converter_EndpointAddress,
        default=OMIT,
    )
    ports: Union[None, OmitEnum, Sequence[kdsl.core.v1.EndpointPort]] = attr.ib(
        metadata={"yaml_name": "ports"},
        converter=kdsl.core.v1_converters.optional_list_converter_EndpointPort,
        default=OMIT,
    )


class EndpointSubsetTypedDict(TypedDict, total=(False)):
    addresses: Sequence[kdsl.core.v1.EndpointAddress]
    notReadyAddresses: Sequence[kdsl.core.v1.EndpointAddress]
    ports: Sequence[kdsl.core.v1.EndpointPort]


EndpointSubsetUnion = Union[EndpointSubset, EndpointSubsetTypedDict]


@attr.s(kw_only=True)
class Toleration(K8sObject):
    effect: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "effect"}, default=OMIT
    )
    key: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "key"}, default=OMIT
    )
    operator: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "operator"}, default=OMIT
    )
    tolerationSeconds: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "tolerationSeconds"}, default=OMIT
    )
    value: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "value"}, default=OMIT
    )


class TolerationTypedDict(TypedDict, total=(False)):
    effect: str
    key: str
    operator: str
    tolerationSeconds: int
    value: str


TolerationUnion = Union[Toleration, TolerationTypedDict]


@attr.s(kw_only=True)
class Lifecycle(K8sObject):
    postStart: Union[None, OmitEnum, kdsl.core.v1.Handler] = attr.ib(
        metadata={"yaml_name": "postStart"},
        converter=kdsl.core.v1_converters.optional_converter_Handler,
        default=OMIT,
    )
    preStop: Union[None, OmitEnum, kdsl.core.v1.Handler] = attr.ib(
        metadata={"yaml_name": "preStop"},
        converter=kdsl.core.v1_converters.optional_converter_Handler,
        default=OMIT,
    )


class LifecycleTypedDict(TypedDict, total=(False)):
    postStart: kdsl.core.v1.Handler
    preStop: kdsl.core.v1.Handler


LifecycleUnion = Union[Lifecycle, LifecycleTypedDict]


@attr.s(kw_only=True)
class WindowsSecurityContextOptions(K8sObject):
    gmsaCredentialSpec: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "gmsaCredentialSpec"}, default=OMIT
    )
    gmsaCredentialSpecName: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "gmsaCredentialSpecName"}, default=OMIT
    )
    runAsUserName: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "runAsUserName"}, default=OMIT
    )


class WindowsSecurityContextOptionsTypedDict(TypedDict, total=(False)):
    gmsaCredentialSpec: str
    gmsaCredentialSpecName: str
    runAsUserName: str


WindowsSecurityContextOptionsUnion = Union[
    WindowsSecurityContextOptions, WindowsSecurityContextOptionsTypedDict
]


@attr.s(kw_only=True)
class NodeConfigStatus(K8sObject):
    active: Union[None, OmitEnum, kdsl.core.v1.NodeConfigSource] = attr.ib(
        metadata={"yaml_name": "active"},
        converter=kdsl.core.v1_converters.optional_converter_NodeConfigSource,
        default=OMIT,
    )
    assigned: Union[None, OmitEnum, kdsl.core.v1.NodeConfigSource] = attr.ib(
        metadata={"yaml_name": "assigned"},
        converter=kdsl.core.v1_converters.optional_converter_NodeConfigSource,
        default=OMIT,
    )
    error: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "error"}, default=OMIT
    )
    lastKnownGood: Union[None, OmitEnum, kdsl.core.v1.NodeConfigSource] = attr.ib(
        metadata={"yaml_name": "lastKnownGood"},
        converter=kdsl.core.v1_converters.optional_converter_NodeConfigSource,
        default=OMIT,
    )


class NodeConfigStatusTypedDict(TypedDict, total=(False)):
    active: kdsl.core.v1.NodeConfigSource
    assigned: kdsl.core.v1.NodeConfigSource
    error: str
    lastKnownGood: kdsl.core.v1.NodeConfigSource


NodeConfigStatusUnion = Union[NodeConfigStatus, NodeConfigStatusTypedDict]


@attr.s(kw_only=True)
class ClientIPConfig(K8sObject):
    timeoutSeconds: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "timeoutSeconds"}, default=OMIT
    )


class ClientIPConfigTypedDict(TypedDict, total=(False)):
    timeoutSeconds: int


ClientIPConfigUnion = Union[ClientIPConfig, ClientIPConfigTypedDict]


@attr.s(kw_only=True)
class ContainerPortItem(K8sObject):
    hostIP: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "hostIP"}, default=OMIT
    )
    hostPort: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "hostPort"}, default=OMIT
    )
    name: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "name"}, default=OMIT
    )
    protocol: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "protocol"}, default=OMIT
    )


class ContainerPortItemTypedDict(TypedDict, total=(False)):
    hostIP: str
    hostPort: int
    name: str
    protocol: str


ContainerPortItemUnion = Union[ContainerPortItem, ContainerPortItemTypedDict]


@attr.s(kw_only=True)
class EnvFromSource(K8sObject):
    configMapRef: Union[None, OmitEnum, kdsl.core.v1.ConfigMapEnvSource] = attr.ib(
        metadata={"yaml_name": "configMapRef"},
        converter=kdsl.core.v1_converters.optional_converter_ConfigMapEnvSource,
        default=OMIT,
    )
    prefix: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "prefix"}, default=OMIT
    )
    secretRef: Union[None, OmitEnum, kdsl.core.v1.SecretEnvSource] = attr.ib(
        metadata={"yaml_name": "secretRef"},
        converter=kdsl.core.v1_converters.optional_converter_SecretEnvSource,
        default=OMIT,
    )


class EnvFromSourceTypedDict(TypedDict, total=(False)):
    configMapRef: kdsl.core.v1.ConfigMapEnvSource
    prefix: str
    secretRef: kdsl.core.v1.SecretEnvSource


EnvFromSourceUnion = Union[EnvFromSource, EnvFromSourceTypedDict]


@attr.s(kw_only=True)
class NodeConfigSource(K8sObject):
    configMap: Union[None, OmitEnum, kdsl.core.v1.ConfigMapNodeConfigSource] = attr.ib(
        metadata={"yaml_name": "configMap"},
        converter=kdsl.core.v1_converters.optional_converter_ConfigMapNodeConfigSource,
        default=OMIT,
    )


class NodeConfigSourceTypedDict(TypedDict, total=(False)):
    configMap: kdsl.core.v1.ConfigMapNodeConfigSource


NodeConfigSourceUnion = Union[NodeConfigSource, NodeConfigSourceTypedDict]


@attr.s(kw_only=True)
class Handler(K8sObject):
    exec: Union[None, OmitEnum, kdsl.core.v1.ExecAction] = attr.ib(
        metadata={"yaml_name": "exec"},
        converter=kdsl.core.v1_converters.optional_converter_ExecAction,
        default=OMIT,
    )
    httpGet: Union[None, OmitEnum, kdsl.core.v1.HTTPGetAction] = attr.ib(
        metadata={"yaml_name": "httpGet"},
        converter=kdsl.core.v1_converters.optional_converter_HTTPGetAction,
        default=OMIT,
    )
    tcpSocket: Union[None, OmitEnum, kdsl.core.v1.TCPSocketAction] = attr.ib(
        metadata={"yaml_name": "tcpSocket"},
        converter=kdsl.core.v1_converters.optional_converter_TCPSocketAction,
        default=OMIT,
    )


class HandlerTypedDict(TypedDict, total=(False)):
    exec: kdsl.core.v1.ExecAction
    httpGet: kdsl.core.v1.HTTPGetAction
    tcpSocket: kdsl.core.v1.TCPSocketAction


HandlerUnion = Union[Handler, HandlerTypedDict]


@attr.s(kw_only=True)
class VolumeDeviceItem(K8sObject):
    name: str = attr.ib(metadata={"yaml_name": "name"})


class VolumeDeviceItemTypedDict(TypedDict, total=(True)):
    name: str


VolumeDeviceItemUnion = Union[VolumeDeviceItem, VolumeDeviceItemTypedDict]


@attr.s(kw_only=True)
class ServiceStatus(K8sObject):
    loadBalancer: Union[None, OmitEnum, kdsl.core.v1.LoadBalancerStatus] = attr.ib(
        metadata={"yaml_name": "loadBalancer"},
        converter=kdsl.core.v1_converters.optional_converter_LoadBalancerStatus,
        default=OMIT,
    )


class ServiceStatusTypedDict(TypedDict, total=(False)):
    loadBalancer: kdsl.core.v1.LoadBalancerStatus


ServiceStatusUnion = Union[ServiceStatus, ServiceStatusTypedDict]


@attr.s(kw_only=True)
class ObjectReferenceItem(K8sObject):
    apiVersion: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "apiVersion"}, default=OMIT
    )
    fieldPath: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "fieldPath"}, default=OMIT
    )
    kind: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "kind"}, default=OMIT
    )
    namespace: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "namespace"}, default=OMIT
    )
    resourceVersion: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "resourceVersion"}, default=OMIT
    )
    uid: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "uid"}, default=OMIT
    )


class ObjectReferenceItemTypedDict(TypedDict, total=(False)):
    apiVersion: str
    fieldPath: str
    kind: str
    namespace: str
    resourceVersion: str
    uid: str


ObjectReferenceItemUnion = Union[ObjectReferenceItem, ObjectReferenceItemTypedDict]


@attr.s(kw_only=True)
class PodAffinityTerm(K8sObject):
    topologyKey: str = attr.ib(metadata={"yaml_name": "topologyKey"})
    labelSelector: Union[None, OmitEnum, kdsl.core.v1.LabelSelector] = attr.ib(
        metadata={"yaml_name": "labelSelector"},
        converter=kdsl.core.v1_converters.optional_converter_LabelSelector,
        default=OMIT,
    )
    namespaces: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "namespaces"}, default=OMIT
    )


class PodAffinityTermOptionalTypedDict(TypedDict, total=(False)):
    labelSelector: kdsl.core.v1.LabelSelector
    namespaces: Sequence[str]


class PodAffinityTermTypedDict(PodAffinityTermOptionalTypedDict, total=(True)):
    topologyKey: str


PodAffinityTermUnion = Union[PodAffinityTerm, PodAffinityTermTypedDict]


@attr.s(kw_only=True)
class ContainerPort(K8sObject):
    containerPort: int = attr.ib(metadata={"yaml_name": "containerPort"})
    hostIP: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "hostIP"}, default=OMIT
    )
    hostPort: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "hostPort"}, default=OMIT
    )
    name: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "name"}, default=OMIT
    )
    protocol: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "protocol"}, default=OMIT
    )


class ContainerPortOptionalTypedDict(TypedDict, total=(False)):
    hostIP: str
    hostPort: int
    name: str
    protocol: str


class ContainerPortTypedDict(ContainerPortOptionalTypedDict, total=(True)):
    containerPort: int


ContainerPortUnion = Union[ContainerPort, ContainerPortTypedDict]


@attr.s(kw_only=True)
class Probe(K8sObject):
    exec: Union[None, OmitEnum, kdsl.core.v1.ExecAction] = attr.ib(
        metadata={"yaml_name": "exec"},
        converter=kdsl.core.v1_converters.optional_converter_ExecAction,
        default=OMIT,
    )
    failureThreshold: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "failureThreshold"}, default=OMIT
    )
    httpGet: Union[None, OmitEnum, kdsl.core.v1.HTTPGetAction] = attr.ib(
        metadata={"yaml_name": "httpGet"},
        converter=kdsl.core.v1_converters.optional_converter_HTTPGetAction,
        default=OMIT,
    )
    initialDelaySeconds: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "initialDelaySeconds"}, default=OMIT
    )
    periodSeconds: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "periodSeconds"}, default=OMIT
    )
    successThreshold: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "successThreshold"}, default=OMIT
    )
    tcpSocket: Union[None, OmitEnum, kdsl.core.v1.TCPSocketAction] = attr.ib(
        metadata={"yaml_name": "tcpSocket"},
        converter=kdsl.core.v1_converters.optional_converter_TCPSocketAction,
        default=OMIT,
    )
    timeoutSeconds: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "timeoutSeconds"}, default=OMIT
    )


class ProbeTypedDict(TypedDict, total=(False)):
    exec: kdsl.core.v1.ExecAction
    failureThreshold: int
    httpGet: kdsl.core.v1.HTTPGetAction
    initialDelaySeconds: int
    periodSeconds: int
    successThreshold: int
    tcpSocket: kdsl.core.v1.TCPSocketAction
    timeoutSeconds: int


ProbeUnion = Union[Probe, ProbeTypedDict]


@attr.s(kw_only=True)
class DownwardAPIVolumeSource(K8sObject):
    defaultMode: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "defaultMode"}, default=OMIT
    )
    items: Union[
        None, OmitEnum, Sequence[kdsl.core.v1.DownwardAPIVolumeFile]
    ] = attr.ib(
        metadata={"yaml_name": "items"},
        converter=kdsl.core.v1_converters.optional_list_converter_DownwardAPIVolumeFile,
        default=OMIT,
    )


class DownwardAPIVolumeSourceTypedDict(TypedDict, total=(False)):
    defaultMode: int
    items: Sequence[kdsl.core.v1.DownwardAPIVolumeFile]


DownwardAPIVolumeSourceUnion = Union[
    DownwardAPIVolumeSource, DownwardAPIVolumeSourceTypedDict
]


@attr.s(kw_only=True)
class PreferredSchedulingTerm(K8sObject):
    preference: kdsl.core.v1.NodeSelectorTerm = attr.ib(
        metadata={"yaml_name": "preference"},
        converter=kdsl.core.v1_converters.required_converter_NodeSelectorTerm,
    )
    weight: int = attr.ib(metadata={"yaml_name": "weight"})


class PreferredSchedulingTermTypedDict(TypedDict, total=(True)):
    preference: kdsl.core.v1.NodeSelectorTerm
    weight: int


PreferredSchedulingTermUnion = Union[
    PreferredSchedulingTerm, PreferredSchedulingTermTypedDict
]


@attr.s(kw_only=True)
class GitRepoVolumeSource(K8sObject):
    repository: str = attr.ib(metadata={"yaml_name": "repository"})
    directory: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "directory"}, default=OMIT
    )
    revision: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "revision"}, default=OMIT
    )


class GitRepoVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    directory: str
    revision: str


class GitRepoVolumeSourceTypedDict(GitRepoVolumeSourceOptionalTypedDict, total=(True)):
    repository: str


GitRepoVolumeSourceUnion = Union[GitRepoVolumeSource, GitRepoVolumeSourceTypedDict]


@attr.s(kw_only=True)
class PodSecurityContext(K8sObject):
    fsGroup: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "fsGroup"}, default=OMIT
    )
    runAsGroup: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "runAsGroup"}, default=OMIT
    )
    runAsNonRoot: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "runAsNonRoot"}, default=OMIT
    )
    runAsUser: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "runAsUser"}, default=OMIT
    )
    seLinuxOptions: Union[None, OmitEnum, kdsl.core.v1.SELinuxOptions] = attr.ib(
        metadata={"yaml_name": "seLinuxOptions"},
        converter=kdsl.core.v1_converters.optional_converter_SELinuxOptions,
        default=OMIT,
    )
    supplementalGroups: Union[None, OmitEnum, Sequence[int]] = attr.ib(
        metadata={"yaml_name": "supplementalGroups"}, default=OMIT
    )
    sysctls: Union[None, OmitEnum, Sequence[kdsl.core.v1.Sysctl]] = attr.ib(
        metadata={"yaml_name": "sysctls"},
        converter=kdsl.core.v1_converters.optional_list_converter_Sysctl,
        default=OMIT,
    )
    windowsOptions: Union[
        None, OmitEnum, kdsl.core.v1.WindowsSecurityContextOptions
    ] = attr.ib(
        metadata={"yaml_name": "windowsOptions"},
        converter=kdsl.core.v1_converters.optional_converter_WindowsSecurityContextOptions,
        default=OMIT,
    )


class PodSecurityContextTypedDict(TypedDict, total=(False)):
    fsGroup: int
    runAsGroup: int
    runAsNonRoot: bool
    runAsUser: int
    seLinuxOptions: kdsl.core.v1.SELinuxOptions
    supplementalGroups: Sequence[int]
    sysctls: Sequence[kdsl.core.v1.Sysctl]
    windowsOptions: kdsl.core.v1.WindowsSecurityContextOptions


PodSecurityContextUnion = Union[PodSecurityContext, PodSecurityContextTypedDict]


@attr.s(kw_only=True)
class NamespaceConditionItem(K8sObject):
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


class NamespaceConditionItemOptionalTypedDict(TypedDict, total=(False)):
    lastTransitionTime: str
    message: str
    reason: str


class NamespaceConditionItemTypedDict(
    NamespaceConditionItemOptionalTypedDict, total=(True)
):
    status: str


NamespaceConditionItemUnion = Union[
    NamespaceConditionItem, NamespaceConditionItemTypedDict
]


@attr.s(kw_only=True)
class ReplicationControllerSpec(K8sObject):
    minReadySeconds: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "minReadySeconds"}, default=OMIT
    )
    replicas: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "replicas"}, default=OMIT
    )
    selector: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(
        metadata={"yaml_name": "selector"}, default=OMIT
    )
    template: Union[None, OmitEnum, kdsl.core.v1.PodTemplateSpec] = attr.ib(
        metadata={"yaml_name": "template"},
        converter=kdsl.core.v1_converters.optional_converter_PodTemplateSpec,
        default=OMIT,
    )


class ReplicationControllerSpecTypedDict(TypedDict, total=(False)):
    minReadySeconds: int
    replicas: int
    selector: Mapping[str, str]
    template: kdsl.core.v1.PodTemplateSpec


ReplicationControllerSpecUnion = Union[
    ReplicationControllerSpec, ReplicationControllerSpecTypedDict
]


@attr.s(kw_only=True)
class Sysctl(K8sObject):
    name: str = attr.ib(metadata={"yaml_name": "name"})
    value: str = attr.ib(metadata={"yaml_name": "value"})


class SysctlTypedDict(TypedDict, total=(True)):
    name: str
    value: str


SysctlUnion = Union[Sysctl, SysctlTypedDict]


@attr.s(kw_only=True)
class LabelSelectorRequirement(K8sObject):
    key: str = attr.ib(metadata={"yaml_name": "key"})
    operator: str = attr.ib(metadata={"yaml_name": "operator"})
    values: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "values"}, default=OMIT
    )


class LabelSelectorRequirementOptionalTypedDict(TypedDict, total=(False)):
    values: Sequence[str]


class LabelSelectorRequirementTypedDict(
    LabelSelectorRequirementOptionalTypedDict, total=(True)
):
    key: str
    operator: str


LabelSelectorRequirementUnion = Union[
    LabelSelectorRequirement, LabelSelectorRequirementTypedDict
]


@attr.s(kw_only=True)
class LimitRangeItem(K8sObject):
    default: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(
        metadata={"yaml_name": "default"}, default=OMIT
    )
    defaultRequest: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(
        metadata={"yaml_name": "defaultRequest"}, default=OMIT
    )
    max: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(
        metadata={"yaml_name": "max"}, default=OMIT
    )
    maxLimitRequestRatio: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(
        metadata={"yaml_name": "maxLimitRequestRatio"}, default=OMIT
    )
    min: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(
        metadata={"yaml_name": "min"}, default=OMIT
    )
    type: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "type"}, default=OMIT
    )


class LimitRangeItemTypedDict(TypedDict, total=(False)):
    default: Mapping[str, str]
    defaultRequest: Mapping[str, str]
    max: Mapping[str, str]
    maxLimitRequestRatio: Mapping[str, str]
    min: Mapping[str, str]
    type: str


LimitRangeItemUnion = Union[LimitRangeItem, LimitRangeItemTypedDict]


@attr.s(kw_only=True)
class ScaleIOPersistentVolumeSource(K8sObject):
    gateway: str = attr.ib(metadata={"yaml_name": "gateway"})
    secretRef: kdsl.core.v1.SecretReference = attr.ib(
        metadata={"yaml_name": "secretRef"},
        converter=kdsl.core.v1_converters.required_converter_SecretReference,
    )
    system: str = attr.ib(metadata={"yaml_name": "system"})
    fsType: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "fsType"}, default=OMIT
    )
    protectionDomain: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "protectionDomain"}, default=OMIT
    )
    readOnly: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "readOnly"}, default=OMIT
    )
    sslEnabled: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "sslEnabled"}, default=OMIT
    )
    storageMode: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "storageMode"}, default=OMIT
    )
    storagePool: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "storagePool"}, default=OMIT
    )
    volumeName: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "volumeName"}, default=OMIT
    )


class ScaleIOPersistentVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    fsType: str
    protectionDomain: str
    readOnly: bool
    sslEnabled: bool
    storageMode: str
    storagePool: str
    volumeName: str


class ScaleIOPersistentVolumeSourceTypedDict(
    ScaleIOPersistentVolumeSourceOptionalTypedDict, total=(True)
):
    gateway: str
    secretRef: kdsl.core.v1.SecretReference
    system: str


ScaleIOPersistentVolumeSourceUnion = Union[
    ScaleIOPersistentVolumeSource, ScaleIOPersistentVolumeSourceTypedDict
]


@attr.s(kw_only=True)
class EndpointAddress(K8sObject):
    ip: str = attr.ib(metadata={"yaml_name": "ip"})
    hostname: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "hostname"}, default=OMIT
    )
    nodeName: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "nodeName"}, default=OMIT
    )
    targetRef: Union[None, OmitEnum, kdsl.core.v1.ObjectReference] = attr.ib(
        metadata={"yaml_name": "targetRef"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectReference,
        default=OMIT,
    )


class EndpointAddressOptionalTypedDict(TypedDict, total=(False)):
    hostname: str
    nodeName: str
    targetRef: kdsl.core.v1.ObjectReference


class EndpointAddressTypedDict(EndpointAddressOptionalTypedDict, total=(True)):
    ip: str


EndpointAddressUnion = Union[EndpointAddress, EndpointAddressTypedDict]


@attr.s(kw_only=True)
class SecretVolumeSource(K8sObject):
    defaultMode: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "defaultMode"}, default=OMIT
    )
    items: Union[None, OmitEnum, Sequence[kdsl.core.v1.KeyToPath]] = attr.ib(
        metadata={"yaml_name": "items"},
        converter=kdsl.core.v1_converters.optional_list_converter_KeyToPath,
        default=OMIT,
    )
    optional: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "optional"}, default=OMIT
    )
    secretName: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "secretName"}, default=OMIT
    )


class SecretVolumeSourceTypedDict(TypedDict, total=(False)):
    defaultMode: int
    items: Sequence[kdsl.core.v1.KeyToPath]
    optional: bool
    secretName: str


SecretVolumeSourceUnion = Union[SecretVolumeSource, SecretVolumeSourceTypedDict]


@attr.s(kw_only=True)
class Secret(K8sResource):
    apiVersion: ClassVar[str] = "v1"
    kind: ClassVar[str] = "Secret"
    data: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(
        metadata={"yaml_name": "data"}, default=OMIT
    )
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    stringData: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(
        metadata={"yaml_name": "stringData"}, default=OMIT
    )
    type: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "type"}, default=OMIT
    )


@attr.s(kw_only=True)
class SELinuxOptions(K8sObject):
    level: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "level"}, default=OMIT
    )
    role: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "role"}, default=OMIT
    )
    type: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "type"}, default=OMIT
    )
    user: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "user"}, default=OMIT
    )


class SELinuxOptionsTypedDict(TypedDict, total=(False)):
    level: str
    role: str
    type: str
    user: str


SELinuxOptionsUnion = Union[SELinuxOptions, SELinuxOptionsTypedDict]


@attr.s(kw_only=True)
class Pod(K8sResource):
    apiVersion: ClassVar[str] = "v1"
    kind: ClassVar[str] = "Pod"
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    spec: Union[None, OmitEnum, kdsl.core.v1.PodSpec] = attr.ib(
        metadata={"yaml_name": "spec"},
        converter=kdsl.core.v1_converters.optional_converter_PodSpec,
        default=OMIT,
    )
    status: Union[None, OmitEnum, kdsl.core.v1.PodStatus] = attr.ib(
        metadata={"yaml_name": "status"},
        converter=kdsl.core.v1_converters.optional_converter_PodStatus,
        default=OMIT,
    )


@attr.s(kw_only=True)
class Binding(K8sResource):
    apiVersion: ClassVar[str] = "v1"
    kind: ClassVar[str] = "Binding"
    target: kdsl.core.v1.ObjectReference = attr.ib(
        metadata={"yaml_name": "target"},
        converter=kdsl.core.v1_converters.required_converter_ObjectReference,
    )
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )


@attr.s(kw_only=True)
class SecurityContext(K8sObject):
    allowPrivilegeEscalation: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "allowPrivilegeEscalation"}, default=OMIT
    )
    capabilities: Union[None, OmitEnum, kdsl.core.v1.Capabilities] = attr.ib(
        metadata={"yaml_name": "capabilities"},
        converter=kdsl.core.v1_converters.optional_converter_Capabilities,
        default=OMIT,
    )
    privileged: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "privileged"}, default=OMIT
    )
    procMount: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "procMount"}, default=OMIT
    )
    readOnlyRootFilesystem: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "readOnlyRootFilesystem"}, default=OMIT
    )
    runAsGroup: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "runAsGroup"}, default=OMIT
    )
    runAsNonRoot: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "runAsNonRoot"}, default=OMIT
    )
    runAsUser: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "runAsUser"}, default=OMIT
    )
    seLinuxOptions: Union[None, OmitEnum, kdsl.core.v1.SELinuxOptions] = attr.ib(
        metadata={"yaml_name": "seLinuxOptions"},
        converter=kdsl.core.v1_converters.optional_converter_SELinuxOptions,
        default=OMIT,
    )
    windowsOptions: Union[
        None, OmitEnum, kdsl.core.v1.WindowsSecurityContextOptions
    ] = attr.ib(
        metadata={"yaml_name": "windowsOptions"},
        converter=kdsl.core.v1_converters.optional_converter_WindowsSecurityContextOptions,
        default=OMIT,
    )


class SecurityContextTypedDict(TypedDict, total=(False)):
    allowPrivilegeEscalation: bool
    capabilities: kdsl.core.v1.Capabilities
    privileged: bool
    procMount: str
    readOnlyRootFilesystem: bool
    runAsGroup: int
    runAsNonRoot: bool
    runAsUser: int
    seLinuxOptions: kdsl.core.v1.SELinuxOptions
    windowsOptions: kdsl.core.v1.WindowsSecurityContextOptions


SecurityContextUnion = Union[SecurityContext, SecurityContextTypedDict]


@attr.s(kw_only=True)
class SessionAffinityConfig(K8sObject):
    clientIP: Union[None, OmitEnum, kdsl.core.v1.ClientIPConfig] = attr.ib(
        metadata={"yaml_name": "clientIP"},
        converter=kdsl.core.v1_converters.optional_converter_ClientIPConfig,
        default=OMIT,
    )


class SessionAffinityConfigTypedDict(TypedDict, total=(False)):
    clientIP: kdsl.core.v1.ClientIPConfig


SessionAffinityConfigUnion = Union[
    SessionAffinityConfig, SessionAffinityConfigTypedDict
]


@attr.s(kw_only=True)
class PodDNSConfigOption(K8sObject):
    name: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "name"}, default=OMIT
    )
    value: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "value"}, default=OMIT
    )


class PodDNSConfigOptionTypedDict(TypedDict, total=(False)):
    name: str
    value: str


PodDNSConfigOptionUnion = Union[PodDNSConfigOption, PodDNSConfigOptionTypedDict]


@attr.s(kw_only=True)
class LimitRangeSpec(K8sObject):
    limits: Sequence[kdsl.core.v1.LimitRangeItem] = attr.ib(
        metadata={"yaml_name": "limits"},
        converter=kdsl.core.v1_converters.required_list_converter_LimitRangeItem,
    )


class LimitRangeSpecTypedDict(TypedDict, total=(True)):
    limits: Sequence[kdsl.core.v1.LimitRangeItem]


LimitRangeSpecUnion = Union[LimitRangeSpec, LimitRangeSpecTypedDict]


@attr.s(kw_only=True)
class ContainerImage(K8sObject):
    names: Sequence[str] = attr.ib(metadata={"yaml_name": "names"})
    sizeBytes: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "sizeBytes"}, default=OMIT
    )


class ContainerImageOptionalTypedDict(TypedDict, total=(False)):
    sizeBytes: int


class ContainerImageTypedDict(ContainerImageOptionalTypedDict, total=(True)):
    names: Sequence[str]


ContainerImageUnion = Union[ContainerImage, ContainerImageTypedDict]


@attr.s(kw_only=True)
class HTTPGetAction(K8sObject):
    port: Union[int, str] = attr.ib(metadata={"yaml_name": "port"})
    host: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "host"}, default=OMIT
    )
    httpHeaders: Union[None, OmitEnum, Sequence[kdsl.core.v1.HTTPHeader]] = attr.ib(
        metadata={"yaml_name": "httpHeaders"},
        converter=kdsl.core.v1_converters.optional_list_converter_HTTPHeader,
        default=OMIT,
    )
    path: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "path"}, default=OMIT
    )
    scheme: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "scheme"}, default=OMIT
    )


class HTTPGetActionOptionalTypedDict(TypedDict, total=(False)):
    host: str
    httpHeaders: Sequence[kdsl.core.v1.HTTPHeader]
    path: str
    scheme: str


class HTTPGetActionTypedDict(HTTPGetActionOptionalTypedDict, total=(True)):
    port: Union[int, str]


HTTPGetActionUnion = Union[HTTPGetAction, HTTPGetActionTypedDict]


@attr.s(kw_only=True)
class ScaleIOVolumeSource(K8sObject):
    gateway: str = attr.ib(metadata={"yaml_name": "gateway"})
    secretRef: kdsl.core.v1.LocalObjectReference = attr.ib(
        metadata={"yaml_name": "secretRef"},
        converter=kdsl.core.v1_converters.required_converter_LocalObjectReference,
    )
    system: str = attr.ib(metadata={"yaml_name": "system"})
    fsType: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "fsType"}, default=OMIT
    )
    protectionDomain: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "protectionDomain"}, default=OMIT
    )
    readOnly: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "readOnly"}, default=OMIT
    )
    sslEnabled: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "sslEnabled"}, default=OMIT
    )
    storageMode: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "storageMode"}, default=OMIT
    )
    storagePool: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "storagePool"}, default=OMIT
    )
    volumeName: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "volumeName"}, default=OMIT
    )


class ScaleIOVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    fsType: str
    protectionDomain: str
    readOnly: bool
    sslEnabled: bool
    storageMode: str
    storagePool: str
    volumeName: str


class ScaleIOVolumeSourceTypedDict(ScaleIOVolumeSourceOptionalTypedDict, total=(True)):
    gateway: str
    secretRef: kdsl.core.v1.LocalObjectReference
    system: str


ScaleIOVolumeSourceUnion = Union[ScaleIOVolumeSource, ScaleIOVolumeSourceTypedDict]


@attr.s(kw_only=True)
class ResourceQuota(K8sResource):
    apiVersion: ClassVar[str] = "v1"
    kind: ClassVar[str] = "ResourceQuota"
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    spec: Union[None, OmitEnum, kdsl.core.v1.ResourceQuotaSpec] = attr.ib(
        metadata={"yaml_name": "spec"},
        converter=kdsl.core.v1_converters.optional_converter_ResourceQuotaSpec,
        default=OMIT,
    )
    status: Union[None, OmitEnum, kdsl.core.v1.ResourceQuotaStatus] = attr.ib(
        metadata={"yaml_name": "status"},
        converter=kdsl.core.v1_converters.optional_converter_ResourceQuotaStatus,
        default=OMIT,
    )


@attr.s(kw_only=True)
class ExecAction(K8sObject):
    command: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "command"}, default=OMIT
    )


class ExecActionTypedDict(TypedDict, total=(False)):
    command: Sequence[str]


ExecActionUnion = Union[ExecAction, ExecActionTypedDict]


@attr.s(kw_only=True)
class ScopedResourceSelectorRequirement(K8sObject):
    operator: str = attr.ib(metadata={"yaml_name": "operator"})
    scopeName: str = attr.ib(metadata={"yaml_name": "scopeName"})
    values: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "values"}, default=OMIT
    )


class ScopedResourceSelectorRequirementOptionalTypedDict(TypedDict, total=(False)):
    values: Sequence[str]


class ScopedResourceSelectorRequirementTypedDict(
    ScopedResourceSelectorRequirementOptionalTypedDict, total=(True)
):
    operator: str
    scopeName: str


ScopedResourceSelectorRequirementUnion = Union[
    ScopedResourceSelectorRequirement, ScopedResourceSelectorRequirementTypedDict
]


@attr.s(kw_only=True)
class AzureDiskVolumeSource(K8sObject):
    diskName: str = attr.ib(metadata={"yaml_name": "diskName"})
    diskURI: str = attr.ib(metadata={"yaml_name": "diskURI"})
    cachingMode: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "cachingMode"}, default=OMIT
    )
    fsType: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "fsType"}, default=OMIT
    )
    kind: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "kind"}, default=OMIT
    )
    readOnly: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "readOnly"}, default=OMIT
    )


class AzureDiskVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    cachingMode: str
    fsType: str
    kind: str
    readOnly: bool


class AzureDiskVolumeSourceTypedDict(
    AzureDiskVolumeSourceOptionalTypedDict, total=(True)
):
    diskName: str
    diskURI: str


AzureDiskVolumeSourceUnion = Union[
    AzureDiskVolumeSource, AzureDiskVolumeSourceTypedDict
]


@attr.s(kw_only=True)
class ObjectReference(K8sObject):
    apiVersion: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "apiVersion"}, default=OMIT
    )
    fieldPath: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "fieldPath"}, default=OMIT
    )
    kind: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "kind"}, default=OMIT
    )
    name: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "name"}, default=OMIT
    )
    namespace: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "namespace"}, default=OMIT
    )
    resourceVersion: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "resourceVersion"}, default=OMIT
    )
    uid: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "uid"}, default=OMIT
    )


class ObjectReferenceTypedDict(TypedDict, total=(False)):
    apiVersion: str
    fieldPath: str
    kind: str
    name: str
    namespace: str
    resourceVersion: str
    uid: str


ObjectReferenceUnion = Union[ObjectReference, ObjectReferenceTypedDict]


@attr.s(kw_only=True)
class SecretEnvSource(K8sObject):
    name: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "name"}, default=OMIT
    )
    optional: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "optional"}, default=OMIT
    )


class SecretEnvSourceTypedDict(TypedDict, total=(False)):
    name: str
    optional: bool


SecretEnvSourceUnion = Union[SecretEnvSource, SecretEnvSourceTypedDict]


@attr.s(kw_only=True)
class ContainerItem(K8sObject):
    args: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "args"}, default=OMIT
    )
    command: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "command"}, default=OMIT
    )
    env: Union[None, OmitEnum, Mapping[str, kdsl.core.v1.EnvVarItem]] = attr.ib(
        metadata={"yaml_name": "env", "mlist_key": "name"},
        converter=kdsl.core.v1_converters.optional_mlist_converter_EnvVarItem,
        default=OMIT,
    )
    envFrom: Union[None, OmitEnum, Sequence[kdsl.core.v1.EnvFromSource]] = attr.ib(
        metadata={"yaml_name": "envFrom"},
        converter=kdsl.core.v1_converters.optional_list_converter_EnvFromSource,
        default=OMIT,
    )
    image: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "image"}, default=OMIT
    )
    imagePullPolicy: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "imagePullPolicy"}, default=OMIT
    )
    lifecycle: Union[None, OmitEnum, kdsl.core.v1.Lifecycle] = attr.ib(
        metadata={"yaml_name": "lifecycle"},
        converter=kdsl.core.v1_converters.optional_converter_Lifecycle,
        default=OMIT,
    )
    livenessProbe: Union[None, OmitEnum, kdsl.core.v1.Probe] = attr.ib(
        metadata={"yaml_name": "livenessProbe"},
        converter=kdsl.core.v1_converters.optional_converter_Probe,
        default=OMIT,
    )
    ports: Union[
        None, OmitEnum, Mapping[int, kdsl.core.v1.ContainerPortItem]
    ] = attr.ib(
        metadata={"yaml_name": "ports", "mlist_key": "containerPort"},
        converter=kdsl.core.v1_converters.optional_mlist_converter_ContainerPortItem,
        default=OMIT,
    )
    readinessProbe: Union[None, OmitEnum, kdsl.core.v1.Probe] = attr.ib(
        metadata={"yaml_name": "readinessProbe"},
        converter=kdsl.core.v1_converters.optional_converter_Probe,
        default=OMIT,
    )
    resources: Union[None, OmitEnum, kdsl.core.v1.ResourceRequirements] = attr.ib(
        metadata={"yaml_name": "resources"},
        converter=kdsl.core.v1_converters.optional_converter_ResourceRequirements,
        default=OMIT,
    )
    securityContext: Union[None, OmitEnum, kdsl.core.v1.SecurityContext] = attr.ib(
        metadata={"yaml_name": "securityContext"},
        converter=kdsl.core.v1_converters.optional_converter_SecurityContext,
        default=OMIT,
    )
    startupProbe: Union[None, OmitEnum, kdsl.core.v1.Probe] = attr.ib(
        metadata={"yaml_name": "startupProbe"},
        converter=kdsl.core.v1_converters.optional_converter_Probe,
        default=OMIT,
    )
    stdin: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "stdin"}, default=OMIT
    )
    stdinOnce: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "stdinOnce"}, default=OMIT
    )
    terminationMessagePath: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "terminationMessagePath"}, default=OMIT
    )
    terminationMessagePolicy: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "terminationMessagePolicy"}, default=OMIT
    )
    tty: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "tty"}, default=OMIT
    )
    volumeDevices: Union[
        None, OmitEnum, Mapping[str, kdsl.core.v1.VolumeDeviceItem]
    ] = attr.ib(
        metadata={"yaml_name": "volumeDevices", "mlist_key": "devicePath"},
        converter=kdsl.core.v1_converters.optional_mlist_converter_VolumeDeviceItem,
        default=OMIT,
    )
    volumeMounts: Union[
        None, OmitEnum, Mapping[str, kdsl.core.v1.VolumeMountItem]
    ] = attr.ib(
        metadata={"yaml_name": "volumeMounts", "mlist_key": "mountPath"},
        converter=kdsl.core.v1_converters.optional_mlist_converter_VolumeMountItem,
        default=OMIT,
    )
    workingDir: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "workingDir"}, default=OMIT
    )


class ContainerItemTypedDict(TypedDict, total=(False)):
    args: Sequence[str]
    command: Sequence[str]
    env: Mapping[str, kdsl.core.v1.EnvVarItem]
    envFrom: Sequence[kdsl.core.v1.EnvFromSource]
    image: str
    imagePullPolicy: str
    lifecycle: kdsl.core.v1.Lifecycle
    livenessProbe: kdsl.core.v1.Probe
    ports: Mapping[int, kdsl.core.v1.ContainerPortItem]
    readinessProbe: kdsl.core.v1.Probe
    resources: kdsl.core.v1.ResourceRequirements
    securityContext: kdsl.core.v1.SecurityContext
    startupProbe: kdsl.core.v1.Probe
    stdin: bool
    stdinOnce: bool
    terminationMessagePath: str
    terminationMessagePolicy: str
    tty: bool
    volumeDevices: Mapping[str, kdsl.core.v1.VolumeDeviceItem]
    volumeMounts: Mapping[str, kdsl.core.v1.VolumeMountItem]
    workingDir: str


ContainerItemUnion = Union[ContainerItem, ContainerItemTypedDict]


@attr.s(kw_only=True)
class SecretKeySelector(K8sObject):
    key: str = attr.ib(metadata={"yaml_name": "key"})
    name: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "name"}, default=OMIT
    )
    optional: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "optional"}, default=OMIT
    )


class SecretKeySelectorOptionalTypedDict(TypedDict, total=(False)):
    name: str
    optional: bool


class SecretKeySelectorTypedDict(SecretKeySelectorOptionalTypedDict, total=(True)):
    key: str


SecretKeySelectorUnion = Union[SecretKeySelector, SecretKeySelectorTypedDict]


@attr.s(kw_only=True)
class NodeSpec(K8sObject):
    configSource: Union[None, OmitEnum, kdsl.core.v1.NodeConfigSource] = attr.ib(
        metadata={"yaml_name": "configSource"},
        converter=kdsl.core.v1_converters.optional_converter_NodeConfigSource,
        default=OMIT,
    )
    externalID: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "externalID"}, default=OMIT
    )
    podCIDR: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "podCIDR"}, default=OMIT
    )
    podCIDRs: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "podCIDRs"}, default=OMIT
    )
    providerID: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "providerID"}, default=OMIT
    )
    taints: Union[None, OmitEnum, Sequence[kdsl.core.v1.Taint]] = attr.ib(
        metadata={"yaml_name": "taints"},
        converter=kdsl.core.v1_converters.optional_list_converter_Taint,
        default=OMIT,
    )
    unschedulable: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "unschedulable"}, default=OMIT
    )


class NodeSpecTypedDict(TypedDict, total=(False)):
    configSource: kdsl.core.v1.NodeConfigSource
    externalID: str
    podCIDR: str
    podCIDRs: Sequence[str]
    providerID: str
    taints: Sequence[kdsl.core.v1.Taint]
    unschedulable: bool


NodeSpecUnion = Union[NodeSpec, NodeSpecTypedDict]


@attr.s(kw_only=True)
class ConfigMapKeySelector(K8sObject):
    key: str = attr.ib(metadata={"yaml_name": "key"})
    name: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "name"}, default=OMIT
    )
    optional: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "optional"}, default=OMIT
    )


class ConfigMapKeySelectorOptionalTypedDict(TypedDict, total=(False)):
    name: str
    optional: bool


class ConfigMapKeySelectorTypedDict(
    ConfigMapKeySelectorOptionalTypedDict, total=(True)
):
    key: str


ConfigMapKeySelectorUnion = Union[ConfigMapKeySelector, ConfigMapKeySelectorTypedDict]


@attr.s(kw_only=True)
class PortworxVolumeSource(K8sObject):
    volumeID: str = attr.ib(metadata={"yaml_name": "volumeID"})
    fsType: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "fsType"}, default=OMIT
    )
    readOnly: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "readOnly"}, default=OMIT
    )


class PortworxVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    fsType: str
    readOnly: bool


class PortworxVolumeSourceTypedDict(
    PortworxVolumeSourceOptionalTypedDict, total=(True)
):
    volumeID: str


PortworxVolumeSourceUnion = Union[PortworxVolumeSource, PortworxVolumeSourceTypedDict]


@attr.s(kw_only=True)
class Preconditions(K8sObject):
    resourceVersion: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "resourceVersion"}, default=OMIT
    )
    uid: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "uid"}, default=OMIT
    )


class PreconditionsTypedDict(TypedDict, total=(False)):
    resourceVersion: str
    uid: str


PreconditionsUnion = Union[Preconditions, PreconditionsTypedDict]


@attr.s(kw_only=True)
class ConfigMapEnvSource(K8sObject):
    name: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "name"}, default=OMIT
    )
    optional: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "optional"}, default=OMIT
    )


class ConfigMapEnvSourceTypedDict(TypedDict, total=(False)):
    name: str
    optional: bool


ConfigMapEnvSourceUnion = Union[ConfigMapEnvSource, ConfigMapEnvSourceTypedDict]


@attr.s(kw_only=True)
class EventSeries(K8sObject):
    count: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "count"}, default=OMIT
    )
    lastObservedTime: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "lastObservedTime"}, default=OMIT
    )
    state: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "state"}, default=OMIT
    )


class EventSeriesTypedDict(TypedDict, total=(False)):
    count: int
    lastObservedTime: str
    state: str


EventSeriesUnion = Union[EventSeries, EventSeriesTypedDict]


@attr.s(kw_only=True)
class NodeSelector(K8sObject):
    nodeSelectorTerms: Sequence[kdsl.core.v1.NodeSelectorTerm] = attr.ib(
        metadata={"yaml_name": "nodeSelectorTerms"},
        converter=kdsl.core.v1_converters.required_list_converter_NodeSelectorTerm,
    )


class NodeSelectorTypedDict(TypedDict, total=(True)):
    nodeSelectorTerms: Sequence[kdsl.core.v1.NodeSelectorTerm]


NodeSelectorUnion = Union[NodeSelector, NodeSelectorTypedDict]


@attr.s(kw_only=True)
class Node(K8sResource):
    apiVersion: ClassVar[str] = "v1"
    kind: ClassVar[str] = "Node"
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    spec: Union[None, OmitEnum, kdsl.core.v1.NodeSpec] = attr.ib(
        metadata={"yaml_name": "spec"},
        converter=kdsl.core.v1_converters.optional_converter_NodeSpec,
        default=OMIT,
    )
    status: Union[None, OmitEnum, kdsl.core.v1.NodeStatus] = attr.ib(
        metadata={"yaml_name": "status"},
        converter=kdsl.core.v1_converters.optional_converter_NodeStatus,
        default=OMIT,
    )


@attr.s(kw_only=True)
class HTTPHeader(K8sObject):
    name: str = attr.ib(metadata={"yaml_name": "name"})
    value: str = attr.ib(metadata={"yaml_name": "value"})


class HTTPHeaderTypedDict(TypedDict, total=(True)):
    name: str
    value: str


HTTPHeaderUnion = Union[HTTPHeader, HTTPHeaderTypedDict]


@attr.s(kw_only=True)
class TopologySelectorTerm(K8sObject):
    matchLabelExpressions: Union[
        None, OmitEnum, Sequence[kdsl.core.v1.TopologySelectorLabelRequirement]
    ] = attr.ib(
        metadata={"yaml_name": "matchLabelExpressions"},
        converter=kdsl.core.v1_converters.optional_list_converter_TopologySelectorLabelRequirement,
        default=OMIT,
    )


class TopologySelectorTermTypedDict(TypedDict, total=(False)):
    matchLabelExpressions: Sequence[kdsl.core.v1.TopologySelectorLabelRequirement]


TopologySelectorTermUnion = Union[TopologySelectorTerm, TopologySelectorTermTypedDict]


@attr.s(kw_only=True)
class EnvVarSource(K8sObject):
    configMapKeyRef: Union[None, OmitEnum, kdsl.core.v1.ConfigMapKeySelector] = attr.ib(
        metadata={"yaml_name": "configMapKeyRef"},
        converter=kdsl.core.v1_converters.optional_converter_ConfigMapKeySelector,
        default=OMIT,
    )
    fieldRef: Union[None, OmitEnum, kdsl.core.v1.ObjectFieldSelector] = attr.ib(
        metadata={"yaml_name": "fieldRef"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectFieldSelector,
        default=OMIT,
    )
    resourceFieldRef: Union[
        None, OmitEnum, kdsl.core.v1.ResourceFieldSelector
    ] = attr.ib(
        metadata={"yaml_name": "resourceFieldRef"},
        converter=kdsl.core.v1_converters.optional_converter_ResourceFieldSelector,
        default=OMIT,
    )
    secretKeyRef: Union[None, OmitEnum, kdsl.core.v1.SecretKeySelector] = attr.ib(
        metadata={"yaml_name": "secretKeyRef"},
        converter=kdsl.core.v1_converters.optional_converter_SecretKeySelector,
        default=OMIT,
    )


class EnvVarSourceTypedDict(TypedDict, total=(False)):
    configMapKeyRef: kdsl.core.v1.ConfigMapKeySelector
    fieldRef: kdsl.core.v1.ObjectFieldSelector
    resourceFieldRef: kdsl.core.v1.ResourceFieldSelector
    secretKeyRef: kdsl.core.v1.SecretKeySelector


EnvVarSourceUnion = Union[EnvVarSource, EnvVarSourceTypedDict]


@attr.s(kw_only=True)
class DownwardAPIVolumeFile(K8sObject):
    path: str = attr.ib(metadata={"yaml_name": "path"})
    fieldRef: Union[None, OmitEnum, kdsl.core.v1.ObjectFieldSelector] = attr.ib(
        metadata={"yaml_name": "fieldRef"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectFieldSelector,
        default=OMIT,
    )
    mode: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "mode"}, default=OMIT
    )
    resourceFieldRef: Union[
        None, OmitEnum, kdsl.core.v1.ResourceFieldSelector
    ] = attr.ib(
        metadata={"yaml_name": "resourceFieldRef"},
        converter=kdsl.core.v1_converters.optional_converter_ResourceFieldSelector,
        default=OMIT,
    )


class DownwardAPIVolumeFileOptionalTypedDict(TypedDict, total=(False)):
    fieldRef: kdsl.core.v1.ObjectFieldSelector
    mode: int
    resourceFieldRef: kdsl.core.v1.ResourceFieldSelector


class DownwardAPIVolumeFileTypedDict(
    DownwardAPIVolumeFileOptionalTypedDict, total=(True)
):
    path: str


DownwardAPIVolumeFileUnion = Union[
    DownwardAPIVolumeFile, DownwardAPIVolumeFileTypedDict
]


@attr.s(kw_only=True)
class RBDVolumeSource(K8sObject):
    image: str = attr.ib(metadata={"yaml_name": "image"})
    monitors: Sequence[str] = attr.ib(metadata={"yaml_name": "monitors"})
    fsType: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "fsType"}, default=OMIT
    )
    keyring: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "keyring"}, default=OMIT
    )
    pool: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "pool"}, default=OMIT
    )
    readOnly: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "readOnly"}, default=OMIT
    )
    secretRef: Union[None, OmitEnum, kdsl.core.v1.LocalObjectReference] = attr.ib(
        metadata={"yaml_name": "secretRef"},
        converter=kdsl.core.v1_converters.optional_converter_LocalObjectReference,
        default=OMIT,
    )
    user: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "user"}, default=OMIT
    )


class RBDVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    fsType: str
    keyring: str
    pool: str
    readOnly: bool
    secretRef: kdsl.core.v1.LocalObjectReference
    user: str


class RBDVolumeSourceTypedDict(RBDVolumeSourceOptionalTypedDict, total=(True)):
    image: str
    monitors: Sequence[str]


RBDVolumeSourceUnion = Union[RBDVolumeSource, RBDVolumeSourceTypedDict]


@attr.s(kw_only=True)
class EndpointPort(K8sObject):
    port: int = attr.ib(metadata={"yaml_name": "port"})
    name: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "name"}, default=OMIT
    )
    protocol: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "protocol"}, default=OMIT
    )


class EndpointPortOptionalTypedDict(TypedDict, total=(False)):
    name: str
    protocol: str


class EndpointPortTypedDict(EndpointPortOptionalTypedDict, total=(True)):
    port: int


EndpointPortUnion = Union[EndpointPort, EndpointPortTypedDict]


@attr.s(kw_only=True)
class PodStatus(K8sObject):
    conditions: Union[
        None, OmitEnum, Mapping[str, kdsl.core.v1.PodConditionItem]
    ] = attr.ib(
        metadata={"yaml_name": "conditions", "mlist_key": "type"},
        converter=kdsl.core.v1_converters.optional_mlist_converter_PodConditionItem,
        default=OMIT,
    )
    containerStatuses: Union[
        None, OmitEnum, Sequence[kdsl.core.v1.ContainerStatus]
    ] = attr.ib(
        metadata={"yaml_name": "containerStatuses"},
        converter=kdsl.core.v1_converters.optional_list_converter_ContainerStatus,
        default=OMIT,
    )
    ephemeralContainerStatuses: Union[
        None, OmitEnum, Sequence[kdsl.core.v1.ContainerStatus]
    ] = attr.ib(
        metadata={"yaml_name": "ephemeralContainerStatuses"},
        converter=kdsl.core.v1_converters.optional_list_converter_ContainerStatus,
        default=OMIT,
    )
    hostIP: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "hostIP"}, default=OMIT
    )
    initContainerStatuses: Union[
        None, OmitEnum, Sequence[kdsl.core.v1.ContainerStatus]
    ] = attr.ib(
        metadata={"yaml_name": "initContainerStatuses"},
        converter=kdsl.core.v1_converters.optional_list_converter_ContainerStatus,
        default=OMIT,
    )
    message: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "message"}, default=OMIT
    )
    nominatedNodeName: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "nominatedNodeName"}, default=OMIT
    )
    phase: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "phase"}, default=OMIT
    )
    podIP: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "podIP"}, default=OMIT
    )
    podIPs: Union[None, OmitEnum, Sequence[kdsl.core.v1.PodIP]] = attr.ib(
        metadata={"yaml_name": "podIPs"},
        converter=kdsl.core.v1_converters.optional_list_converter_PodIP,
        default=OMIT,
    )
    qosClass: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "qosClass"}, default=OMIT
    )
    reason: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "reason"}, default=OMIT
    )
    startTime: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "startTime"}, default=OMIT
    )


class PodStatusTypedDict(TypedDict, total=(False)):
    conditions: Mapping[str, kdsl.core.v1.PodConditionItem]
    containerStatuses: Sequence[kdsl.core.v1.ContainerStatus]
    ephemeralContainerStatuses: Sequence[kdsl.core.v1.ContainerStatus]
    hostIP: str
    initContainerStatuses: Sequence[kdsl.core.v1.ContainerStatus]
    message: str
    nominatedNodeName: str
    phase: str
    podIP: str
    podIPs: Sequence[kdsl.core.v1.PodIP]
    qosClass: str
    reason: str
    startTime: str


PodStatusUnion = Union[PodStatus, PodStatusTypedDict]


@attr.s(kw_only=True)
class ServicePortItem(K8sObject):
    name: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "name"}, default=OMIT
    )
    nodePort: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "nodePort"}, default=OMIT
    )
    protocol: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "protocol"}, default=OMIT
    )
    targetPort: Union[None, OmitEnum, Union[int, str]] = attr.ib(
        metadata={"yaml_name": "targetPort"}, default=OMIT
    )


class ServicePortItemTypedDict(TypedDict, total=(False)):
    name: str
    nodePort: int
    protocol: str
    targetPort: Union[int, str]


ServicePortItemUnion = Union[ServicePortItem, ServicePortItemTypedDict]


@attr.s(kw_only=True)
class KeyToPath(K8sObject):
    key: str = attr.ib(metadata={"yaml_name": "key"})
    path: str = attr.ib(metadata={"yaml_name": "path"})
    mode: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "mode"}, default=OMIT
    )


class KeyToPathOptionalTypedDict(TypedDict, total=(False)):
    mode: int


class KeyToPathTypedDict(KeyToPathOptionalTypedDict, total=(True)):
    key: str
    path: str


KeyToPathUnion = Union[KeyToPath, KeyToPathTypedDict]


@attr.s(kw_only=True)
class StorageOSPersistentVolumeSource(K8sObject):
    fsType: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "fsType"}, default=OMIT
    )
    readOnly: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "readOnly"}, default=OMIT
    )
    secretRef: Union[None, OmitEnum, kdsl.core.v1.ObjectReference] = attr.ib(
        metadata={"yaml_name": "secretRef"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectReference,
        default=OMIT,
    )
    volumeName: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "volumeName"}, default=OMIT
    )
    volumeNamespace: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "volumeNamespace"}, default=OMIT
    )


class StorageOSPersistentVolumeSourceTypedDict(TypedDict, total=(False)):
    fsType: str
    readOnly: bool
    secretRef: kdsl.core.v1.ObjectReference
    volumeName: str
    volumeNamespace: str


StorageOSPersistentVolumeSourceUnion = Union[
    StorageOSPersistentVolumeSource, StorageOSPersistentVolumeSourceTypedDict
]


@attr.s(kw_only=True)
class AzureFileVolumeSource(K8sObject):
    secretName: str = attr.ib(metadata={"yaml_name": "secretName"})
    shareName: str = attr.ib(metadata={"yaml_name": "shareName"})
    readOnly: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "readOnly"}, default=OMIT
    )


class AzureFileVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    readOnly: bool


class AzureFileVolumeSourceTypedDict(
    AzureFileVolumeSourceOptionalTypedDict, total=(True)
):
    secretName: str
    shareName: str


AzureFileVolumeSourceUnion = Union[
    AzureFileVolumeSource, AzureFileVolumeSourceTypedDict
]


@attr.s(kw_only=True)
class ManagedFieldsEntry(K8sObject):
    apiVersion: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "apiVersion"}, default=OMIT
    )
    fieldsType: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "fieldsType"}, default=OMIT
    )
    fieldsV1: Union[None, OmitEnum, Mapping[str, Any]] = attr.ib(
        metadata={"yaml_name": "fieldsV1"}, default=OMIT
    )
    manager: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "manager"}, default=OMIT
    )
    operation: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "operation"}, default=OMIT
    )
    time: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "time"}, default=OMIT
    )


class ManagedFieldsEntryTypedDict(TypedDict, total=(False)):
    apiVersion: str
    fieldsType: str
    fieldsV1: Mapping[str, Any]
    manager: str
    operation: str
    time: str


ManagedFieldsEntryUnion = Union[ManagedFieldsEntry, ManagedFieldsEntryTypedDict]


@attr.s(kw_only=True)
class LoadBalancerStatus(K8sObject):
    ingress: Union[
        None, OmitEnum, Sequence[kdsl.core.v1.LoadBalancerIngress]
    ] = attr.ib(
        metadata={"yaml_name": "ingress"},
        converter=kdsl.core.v1_converters.optional_list_converter_LoadBalancerIngress,
        default=OMIT,
    )


class LoadBalancerStatusTypedDict(TypedDict, total=(False)):
    ingress: Sequence[kdsl.core.v1.LoadBalancerIngress]


LoadBalancerStatusUnion = Union[LoadBalancerStatus, LoadBalancerStatusTypedDict]


@attr.s(kw_only=True)
class EnvVar(K8sObject):
    name: str = attr.ib(metadata={"yaml_name": "name"})
    value: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "value"}, default=OMIT
    )
    valueFrom: Union[None, OmitEnum, kdsl.core.v1.EnvVarSource] = attr.ib(
        metadata={"yaml_name": "valueFrom"},
        converter=kdsl.core.v1_converters.optional_converter_EnvVarSource,
        default=OMIT,
    )


class EnvVarOptionalTypedDict(TypedDict, total=(False)):
    value: str
    valueFrom: kdsl.core.v1.EnvVarSource


class EnvVarTypedDict(EnvVarOptionalTypedDict, total=(True)):
    name: str


EnvVarUnion = Union[EnvVar, EnvVarTypedDict]


@attr.s(kw_only=True)
class WeightedPodAffinityTerm(K8sObject):
    podAffinityTerm: kdsl.core.v1.PodAffinityTerm = attr.ib(
        metadata={"yaml_name": "podAffinityTerm"},
        converter=kdsl.core.v1_converters.required_converter_PodAffinityTerm,
    )
    weight: int = attr.ib(metadata={"yaml_name": "weight"})


class WeightedPodAffinityTermTypedDict(TypedDict, total=(True)):
    podAffinityTerm: kdsl.core.v1.PodAffinityTerm
    weight: int


WeightedPodAffinityTermUnion = Union[
    WeightedPodAffinityTerm, WeightedPodAffinityTermTypedDict
]


@attr.s(kw_only=True)
class VolumeMount(K8sObject):
    mountPath: str = attr.ib(metadata={"yaml_name": "mountPath"})
    name: str = attr.ib(metadata={"yaml_name": "name"})
    mountPropagation: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "mountPropagation"}, default=OMIT
    )
    readOnly: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "readOnly"}, default=OMIT
    )
    subPath: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "subPath"}, default=OMIT
    )
    subPathExpr: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "subPathExpr"}, default=OMIT
    )


class VolumeMountOptionalTypedDict(TypedDict, total=(False)):
    mountPropagation: str
    readOnly: bool
    subPath: str
    subPathExpr: str


class VolumeMountTypedDict(VolumeMountOptionalTypedDict, total=(True)):
    mountPath: str
    name: str


VolumeMountUnion = Union[VolumeMount, VolumeMountTypedDict]


@attr.s(kw_only=True)
class NodeDaemonEndpoints(K8sObject):
    kubeletEndpoint: Union[None, OmitEnum, kdsl.core.v1.DaemonEndpoint] = attr.ib(
        metadata={"yaml_name": "kubeletEndpoint"},
        converter=kdsl.core.v1_converters.optional_converter_DaemonEndpoint,
        default=OMIT,
    )


class NodeDaemonEndpointsTypedDict(TypedDict, total=(False)):
    kubeletEndpoint: kdsl.core.v1.DaemonEndpoint


NodeDaemonEndpointsUnion = Union[NodeDaemonEndpoints, NodeDaemonEndpointsTypedDict]


@attr.s(kw_only=True)
class AttachedVolume(K8sObject):
    devicePath: str = attr.ib(metadata={"yaml_name": "devicePath"})
    name: str = attr.ib(metadata={"yaml_name": "name"})


class AttachedVolumeTypedDict(TypedDict, total=(True)):
    devicePath: str
    name: str


AttachedVolumeUnion = Union[AttachedVolume, AttachedVolumeTypedDict]


@attr.s(kw_only=True)
class GCEPersistentDiskVolumeSource(K8sObject):
    pdName: str = attr.ib(metadata={"yaml_name": "pdName"})
    fsType: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "fsType"}, default=OMIT
    )
    partition: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "partition"}, default=OMIT
    )
    readOnly: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "readOnly"}, default=OMIT
    )


class GCEPersistentDiskVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    fsType: str
    partition: int
    readOnly: bool


class GCEPersistentDiskVolumeSourceTypedDict(
    GCEPersistentDiskVolumeSourceOptionalTypedDict, total=(True)
):
    pdName: str


GCEPersistentDiskVolumeSourceUnion = Union[
    GCEPersistentDiskVolumeSource, GCEPersistentDiskVolumeSourceTypedDict
]


@attr.s(kw_only=True)
class PodDNSConfig(K8sObject):
    nameservers: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "nameservers"}, default=OMIT
    )
    options: Union[None, OmitEnum, Sequence[kdsl.core.v1.PodDNSConfigOption]] = attr.ib(
        metadata={"yaml_name": "options"},
        converter=kdsl.core.v1_converters.optional_list_converter_PodDNSConfigOption,
        default=OMIT,
    )
    searches: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "searches"}, default=OMIT
    )


class PodDNSConfigTypedDict(TypedDict, total=(False)):
    nameservers: Sequence[str]
    options: Sequence[kdsl.core.v1.PodDNSConfigOption]
    searches: Sequence[str]


PodDNSConfigUnion = Union[PodDNSConfig, PodDNSConfigTypedDict]


@attr.s(kw_only=True)
class VolumeItem(K8sObject):
    awsElasticBlockStore: Union[
        None, OmitEnum, kdsl.core.v1.AWSElasticBlockStoreVolumeSource
    ] = attr.ib(
        metadata={"yaml_name": "awsElasticBlockStore"},
        converter=kdsl.core.v1_converters.optional_converter_AWSElasticBlockStoreVolumeSource,
        default=OMIT,
    )
    azureDisk: Union[None, OmitEnum, kdsl.core.v1.AzureDiskVolumeSource] = attr.ib(
        metadata={"yaml_name": "azureDisk"},
        converter=kdsl.core.v1_converters.optional_converter_AzureDiskVolumeSource,
        default=OMIT,
    )
    azureFile: Union[None, OmitEnum, kdsl.core.v1.AzureFileVolumeSource] = attr.ib(
        metadata={"yaml_name": "azureFile"},
        converter=kdsl.core.v1_converters.optional_converter_AzureFileVolumeSource,
        default=OMIT,
    )
    cephfs: Union[None, OmitEnum, kdsl.core.v1.CephFSVolumeSource] = attr.ib(
        metadata={"yaml_name": "cephfs"},
        converter=kdsl.core.v1_converters.optional_converter_CephFSVolumeSource,
        default=OMIT,
    )
    cinder: Union[None, OmitEnum, kdsl.core.v1.CinderVolumeSource] = attr.ib(
        metadata={"yaml_name": "cinder"},
        converter=kdsl.core.v1_converters.optional_converter_CinderVolumeSource,
        default=OMIT,
    )
    configMap: Union[None, OmitEnum, kdsl.core.v1.ConfigMapVolumeSource] = attr.ib(
        metadata={"yaml_name": "configMap"},
        converter=kdsl.core.v1_converters.optional_converter_ConfigMapVolumeSource,
        default=OMIT,
    )
    csi: Union[None, OmitEnum, kdsl.core.v1.CSIVolumeSource] = attr.ib(
        metadata={"yaml_name": "csi"},
        converter=kdsl.core.v1_converters.optional_converter_CSIVolumeSource,
        default=OMIT,
    )
    downwardAPI: Union[None, OmitEnum, kdsl.core.v1.DownwardAPIVolumeSource] = attr.ib(
        metadata={"yaml_name": "downwardAPI"},
        converter=kdsl.core.v1_converters.optional_converter_DownwardAPIVolumeSource,
        default=OMIT,
    )
    emptyDir: Union[None, OmitEnum, kdsl.core.v1.EmptyDirVolumeSource] = attr.ib(
        metadata={"yaml_name": "emptyDir"},
        converter=kdsl.core.v1_converters.optional_converter_EmptyDirVolumeSource,
        default=OMIT,
    )
    fc: Union[None, OmitEnum, kdsl.core.v1.FCVolumeSource] = attr.ib(
        metadata={"yaml_name": "fc"},
        converter=kdsl.core.v1_converters.optional_converter_FCVolumeSource,
        default=OMIT,
    )
    flexVolume: Union[None, OmitEnum, kdsl.core.v1.FlexVolumeSource] = attr.ib(
        metadata={"yaml_name": "flexVolume"},
        converter=kdsl.core.v1_converters.optional_converter_FlexVolumeSource,
        default=OMIT,
    )
    flocker: Union[None, OmitEnum, kdsl.core.v1.FlockerVolumeSource] = attr.ib(
        metadata={"yaml_name": "flocker"},
        converter=kdsl.core.v1_converters.optional_converter_FlockerVolumeSource,
        default=OMIT,
    )
    gcePersistentDisk: Union[
        None, OmitEnum, kdsl.core.v1.GCEPersistentDiskVolumeSource
    ] = attr.ib(
        metadata={"yaml_name": "gcePersistentDisk"},
        converter=kdsl.core.v1_converters.optional_converter_GCEPersistentDiskVolumeSource,
        default=OMIT,
    )
    gitRepo: Union[None, OmitEnum, kdsl.core.v1.GitRepoVolumeSource] = attr.ib(
        metadata={"yaml_name": "gitRepo"},
        converter=kdsl.core.v1_converters.optional_converter_GitRepoVolumeSource,
        default=OMIT,
    )
    glusterfs: Union[None, OmitEnum, kdsl.core.v1.GlusterfsVolumeSource] = attr.ib(
        metadata={"yaml_name": "glusterfs"},
        converter=kdsl.core.v1_converters.optional_converter_GlusterfsVolumeSource,
        default=OMIT,
    )
    hostPath: Union[None, OmitEnum, kdsl.core.v1.HostPathVolumeSource] = attr.ib(
        metadata={"yaml_name": "hostPath"},
        converter=kdsl.core.v1_converters.optional_converter_HostPathVolumeSource,
        default=OMIT,
    )
    iscsi: Union[None, OmitEnum, kdsl.core.v1.ISCSIVolumeSource] = attr.ib(
        metadata={"yaml_name": "iscsi"},
        converter=kdsl.core.v1_converters.optional_converter_ISCSIVolumeSource,
        default=OMIT,
    )
    nfs: Union[None, OmitEnum, kdsl.core.v1.NFSVolumeSource] = attr.ib(
        metadata={"yaml_name": "nfs"},
        converter=kdsl.core.v1_converters.optional_converter_NFSVolumeSource,
        default=OMIT,
    )
    persistentVolumeClaim: Union[
        None, OmitEnum, kdsl.core.v1.PersistentVolumeClaimVolumeSource
    ] = attr.ib(
        metadata={"yaml_name": "persistentVolumeClaim"},
        converter=kdsl.core.v1_converters.optional_converter_PersistentVolumeClaimVolumeSource,
        default=OMIT,
    )
    photonPersistentDisk: Union[
        None, OmitEnum, kdsl.core.v1.PhotonPersistentDiskVolumeSource
    ] = attr.ib(
        metadata={"yaml_name": "photonPersistentDisk"},
        converter=kdsl.core.v1_converters.optional_converter_PhotonPersistentDiskVolumeSource,
        default=OMIT,
    )
    portworxVolume: Union[None, OmitEnum, kdsl.core.v1.PortworxVolumeSource] = attr.ib(
        metadata={"yaml_name": "portworxVolume"},
        converter=kdsl.core.v1_converters.optional_converter_PortworxVolumeSource,
        default=OMIT,
    )
    projected: Union[None, OmitEnum, kdsl.core.v1.ProjectedVolumeSource] = attr.ib(
        metadata={"yaml_name": "projected"},
        converter=kdsl.core.v1_converters.optional_converter_ProjectedVolumeSource,
        default=OMIT,
    )
    quobyte: Union[None, OmitEnum, kdsl.core.v1.QuobyteVolumeSource] = attr.ib(
        metadata={"yaml_name": "quobyte"},
        converter=kdsl.core.v1_converters.optional_converter_QuobyteVolumeSource,
        default=OMIT,
    )
    rbd: Union[None, OmitEnum, kdsl.core.v1.RBDVolumeSource] = attr.ib(
        metadata={"yaml_name": "rbd"},
        converter=kdsl.core.v1_converters.optional_converter_RBDVolumeSource,
        default=OMIT,
    )
    scaleIO: Union[None, OmitEnum, kdsl.core.v1.ScaleIOVolumeSource] = attr.ib(
        metadata={"yaml_name": "scaleIO"},
        converter=kdsl.core.v1_converters.optional_converter_ScaleIOVolumeSource,
        default=OMIT,
    )
    secret: Union[None, OmitEnum, kdsl.core.v1.SecretVolumeSource] = attr.ib(
        metadata={"yaml_name": "secret"},
        converter=kdsl.core.v1_converters.optional_converter_SecretVolumeSource,
        default=OMIT,
    )
    storageos: Union[None, OmitEnum, kdsl.core.v1.StorageOSVolumeSource] = attr.ib(
        metadata={"yaml_name": "storageos"},
        converter=kdsl.core.v1_converters.optional_converter_StorageOSVolumeSource,
        default=OMIT,
    )
    vsphereVolume: Union[
        None, OmitEnum, kdsl.core.v1.VsphereVirtualDiskVolumeSource
    ] = attr.ib(
        metadata={"yaml_name": "vsphereVolume"},
        converter=kdsl.core.v1_converters.optional_converter_VsphereVirtualDiskVolumeSource,
        default=OMIT,
    )


class VolumeItemTypedDict(TypedDict, total=(False)):
    awsElasticBlockStore: kdsl.core.v1.AWSElasticBlockStoreVolumeSource
    azureDisk: kdsl.core.v1.AzureDiskVolumeSource
    azureFile: kdsl.core.v1.AzureFileVolumeSource
    cephfs: kdsl.core.v1.CephFSVolumeSource
    cinder: kdsl.core.v1.CinderVolumeSource
    configMap: kdsl.core.v1.ConfigMapVolumeSource
    csi: kdsl.core.v1.CSIVolumeSource
    downwardAPI: kdsl.core.v1.DownwardAPIVolumeSource
    emptyDir: kdsl.core.v1.EmptyDirVolumeSource
    fc: kdsl.core.v1.FCVolumeSource
    flexVolume: kdsl.core.v1.FlexVolumeSource
    flocker: kdsl.core.v1.FlockerVolumeSource
    gcePersistentDisk: kdsl.core.v1.GCEPersistentDiskVolumeSource
    gitRepo: kdsl.core.v1.GitRepoVolumeSource
    glusterfs: kdsl.core.v1.GlusterfsVolumeSource
    hostPath: kdsl.core.v1.HostPathVolumeSource
    iscsi: kdsl.core.v1.ISCSIVolumeSource
    nfs: kdsl.core.v1.NFSVolumeSource
    persistentVolumeClaim: kdsl.core.v1.PersistentVolumeClaimVolumeSource
    photonPersistentDisk: kdsl.core.v1.PhotonPersistentDiskVolumeSource
    portworxVolume: kdsl.core.v1.PortworxVolumeSource
    projected: kdsl.core.v1.ProjectedVolumeSource
    quobyte: kdsl.core.v1.QuobyteVolumeSource
    rbd: kdsl.core.v1.RBDVolumeSource
    scaleIO: kdsl.core.v1.ScaleIOVolumeSource
    secret: kdsl.core.v1.SecretVolumeSource
    storageos: kdsl.core.v1.StorageOSVolumeSource
    vsphereVolume: kdsl.core.v1.VsphereVirtualDiskVolumeSource


VolumeItemUnion = Union[VolumeItem, VolumeItemTypedDict]


@attr.s(kw_only=True)
class ResourceRequirements(K8sObject):
    limits: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(
        metadata={"yaml_name": "limits"}, default=OMIT
    )
    requests: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(
        metadata={"yaml_name": "requests"}, default=OMIT
    )


class ResourceRequirementsTypedDict(TypedDict, total=(False)):
    limits: Mapping[str, str]
    requests: Mapping[str, str]


ResourceRequirementsUnion = Union[ResourceRequirements, ResourceRequirementsTypedDict]


@attr.s(kw_only=True)
class QuobyteVolumeSource(K8sObject):
    registry: str = attr.ib(metadata={"yaml_name": "registry"})
    volume: str = attr.ib(metadata={"yaml_name": "volume"})
    group: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "group"}, default=OMIT
    )
    readOnly: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "readOnly"}, default=OMIT
    )
    tenant: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "tenant"}, default=OMIT
    )
    user: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "user"}, default=OMIT
    )


class QuobyteVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    group: str
    readOnly: bool
    tenant: str
    user: str


class QuobyteVolumeSourceTypedDict(QuobyteVolumeSourceOptionalTypedDict, total=(True)):
    registry: str
    volume: str


QuobyteVolumeSourceUnion = Union[QuobyteVolumeSource, QuobyteVolumeSourceTypedDict]


@attr.s(kw_only=True)
class NodeSystemInfo(K8sObject):
    architecture: str = attr.ib(metadata={"yaml_name": "architecture"})
    bootID: str = attr.ib(metadata={"yaml_name": "bootID"})
    containerRuntimeVersion: str = attr.ib(
        metadata={"yaml_name": "containerRuntimeVersion"}
    )
    kernelVersion: str = attr.ib(metadata={"yaml_name": "kernelVersion"})
    kubeProxyVersion: str = attr.ib(metadata={"yaml_name": "kubeProxyVersion"})
    kubeletVersion: str = attr.ib(metadata={"yaml_name": "kubeletVersion"})
    machineID: str = attr.ib(metadata={"yaml_name": "machineID"})
    operatingSystem: str = attr.ib(metadata={"yaml_name": "operatingSystem"})
    osImage: str = attr.ib(metadata={"yaml_name": "osImage"})
    systemUUID: str = attr.ib(metadata={"yaml_name": "systemUUID"})


class NodeSystemInfoTypedDict(TypedDict, total=(True)):
    architecture: str
    bootID: str
    containerRuntimeVersion: str
    kernelVersion: str
    kubeProxyVersion: str
    kubeletVersion: str
    machineID: str
    operatingSystem: str
    osImage: str
    systemUUID: str


NodeSystemInfoUnion = Union[NodeSystemInfo, NodeSystemInfoTypedDict]


@attr.s(kw_only=True)
class ServiceAccountTokenProjection(K8sObject):
    path: str = attr.ib(metadata={"yaml_name": "path"})
    audience: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "audience"}, default=OMIT
    )
    expirationSeconds: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "expirationSeconds"}, default=OMIT
    )


class ServiceAccountTokenProjectionOptionalTypedDict(TypedDict, total=(False)):
    audience: str
    expirationSeconds: int


class ServiceAccountTokenProjectionTypedDict(
    ServiceAccountTokenProjectionOptionalTypedDict, total=(True)
):
    path: str


ServiceAccountTokenProjectionUnion = Union[
    ServiceAccountTokenProjection, ServiceAccountTokenProjectionTypedDict
]


@attr.s(kw_only=True)
class Taint(K8sObject):
    effect: str = attr.ib(metadata={"yaml_name": "effect"})
    key: str = attr.ib(metadata={"yaml_name": "key"})
    timeAdded: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "timeAdded"}, default=OMIT
    )
    value: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "value"}, default=OMIT
    )


class TaintOptionalTypedDict(TypedDict, total=(False)):
    timeAdded: str
    value: str


class TaintTypedDict(TaintOptionalTypedDict, total=(True)):
    effect: str
    key: str


TaintUnion = Union[Taint, TaintTypedDict]


@attr.s(kw_only=True)
class GlusterfsVolumeSource(K8sObject):
    endpoints: str = attr.ib(metadata={"yaml_name": "endpoints"})
    path: str = attr.ib(metadata={"yaml_name": "path"})
    readOnly: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "readOnly"}, default=OMIT
    )


class GlusterfsVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    readOnly: bool


class GlusterfsVolumeSourceTypedDict(
    GlusterfsVolumeSourceOptionalTypedDict, total=(True)
):
    endpoints: str
    path: str


GlusterfsVolumeSourceUnion = Union[
    GlusterfsVolumeSource, GlusterfsVolumeSourceTypedDict
]


@attr.s(kw_only=True)
class CephFSVolumeSource(K8sObject):
    monitors: Sequence[str] = attr.ib(metadata={"yaml_name": "monitors"})
    path: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "path"}, default=OMIT
    )
    readOnly: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "readOnly"}, default=OMIT
    )
    secretFile: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "secretFile"}, default=OMIT
    )
    secretRef: Union[None, OmitEnum, kdsl.core.v1.LocalObjectReference] = attr.ib(
        metadata={"yaml_name": "secretRef"},
        converter=kdsl.core.v1_converters.optional_converter_LocalObjectReference,
        default=OMIT,
    )
    user: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "user"}, default=OMIT
    )


class CephFSVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    path: str
    readOnly: bool
    secretFile: str
    secretRef: kdsl.core.v1.LocalObjectReference
    user: str


class CephFSVolumeSourceTypedDict(CephFSVolumeSourceOptionalTypedDict, total=(True)):
    monitors: Sequence[str]


CephFSVolumeSourceUnion = Union[CephFSVolumeSource, CephFSVolumeSourceTypedDict]


@attr.s(kw_only=True)
class OwnerReferenceItem(K8sObject):
    apiVersion: str = attr.ib(metadata={"yaml_name": "apiVersion"})
    kind: str = attr.ib(metadata={"yaml_name": "kind"})
    name: str = attr.ib(metadata={"yaml_name": "name"})
    blockOwnerDeletion: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "blockOwnerDeletion"}, default=OMIT
    )
    controller: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "controller"}, default=OMIT
    )


class OwnerReferenceItemOptionalTypedDict(TypedDict, total=(False)):
    blockOwnerDeletion: bool
    controller: bool


class OwnerReferenceItemTypedDict(OwnerReferenceItemOptionalTypedDict, total=(True)):
    apiVersion: str
    kind: str
    name: str


OwnerReferenceItemUnion = Union[OwnerReferenceItem, OwnerReferenceItemTypedDict]


@attr.s(kw_only=True)
class ReplicationControllerConditionItem(K8sObject):
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


class ReplicationControllerConditionItemOptionalTypedDict(TypedDict, total=(False)):
    lastTransitionTime: str
    message: str
    reason: str


class ReplicationControllerConditionItemTypedDict(
    ReplicationControllerConditionItemOptionalTypedDict, total=(True)
):
    status: str


ReplicationControllerConditionItemUnion = Union[
    ReplicationControllerConditionItem, ReplicationControllerConditionItemTypedDict
]


@attr.s(kw_only=True)
class ScopeSelector(K8sObject):
    matchExpressions: Union[
        None, OmitEnum, Sequence[kdsl.core.v1.ScopedResourceSelectorRequirement]
    ] = attr.ib(
        metadata={"yaml_name": "matchExpressions"},
        converter=kdsl.core.v1_converters.optional_list_converter_ScopedResourceSelectorRequirement,
        default=OMIT,
    )


class ScopeSelectorTypedDict(TypedDict, total=(False)):
    matchExpressions: Sequence[kdsl.core.v1.ScopedResourceSelectorRequirement]


ScopeSelectorUnion = Union[ScopeSelector, ScopeSelectorTypedDict]


@attr.s(kw_only=True)
class PodConditionItem(K8sObject):
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


class PodConditionItemOptionalTypedDict(TypedDict, total=(False)):
    lastProbeTime: str
    lastTransitionTime: str
    message: str
    reason: str


class PodConditionItemTypedDict(PodConditionItemOptionalTypedDict, total=(True)):
    status: str


PodConditionItemUnion = Union[PodConditionItem, PodConditionItemTypedDict]


@attr.s(kw_only=True)
class FCVolumeSource(K8sObject):
    fsType: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "fsType"}, default=OMIT
    )
    lun: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "lun"}, default=OMIT
    )
    readOnly: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "readOnly"}, default=OMIT
    )
    targetWWNs: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "targetWWNs"}, default=OMIT
    )
    wwids: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "wwids"}, default=OMIT
    )


class FCVolumeSourceTypedDict(TypedDict, total=(False)):
    fsType: str
    lun: int
    readOnly: bool
    targetWWNs: Sequence[str]
    wwids: Sequence[str]


FCVolumeSourceUnion = Union[FCVolumeSource, FCVolumeSourceTypedDict]


@attr.s(kw_only=True)
class PodTemplate(K8sResource):
    apiVersion: ClassVar[str] = "v1"
    kind: ClassVar[str] = "PodTemplate"
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    template: Union[None, OmitEnum, kdsl.core.v1.PodTemplateSpec] = attr.ib(
        metadata={"yaml_name": "template"},
        converter=kdsl.core.v1_converters.optional_converter_PodTemplateSpec,
        default=OMIT,
    )


@attr.s(kw_only=True)
class ServiceAccount(K8sResource):
    apiVersion: ClassVar[str] = "v1"
    kind: ClassVar[str] = "ServiceAccount"
    automountServiceAccountToken: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "automountServiceAccountToken"}, default=OMIT
    )
    imagePullSecrets: Union[
        None, OmitEnum, Sequence[kdsl.core.v1.LocalObjectReference]
    ] = attr.ib(
        metadata={"yaml_name": "imagePullSecrets"},
        converter=kdsl.core.v1_converters.optional_list_converter_LocalObjectReference,
        default=OMIT,
    )
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    secrets: Union[
        None, OmitEnum, Mapping[str, kdsl.core.v1.ObjectReferenceItem]
    ] = attr.ib(
        metadata={"yaml_name": "secrets", "mlist_key": "name"},
        converter=kdsl.core.v1_converters.optional_mlist_converter_ObjectReferenceItem,
        default=OMIT,
    )


@attr.s(kw_only=True)
class ResourceQuotaSpec(K8sObject):
    hard: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(
        metadata={"yaml_name": "hard"}, default=OMIT
    )
    scopeSelector: Union[None, OmitEnum, kdsl.core.v1.ScopeSelector] = attr.ib(
        metadata={"yaml_name": "scopeSelector"},
        converter=kdsl.core.v1_converters.optional_converter_ScopeSelector,
        default=OMIT,
    )
    scopes: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "scopes"}, default=OMIT
    )


class ResourceQuotaSpecTypedDict(TypedDict, total=(False)):
    hard: Mapping[str, str]
    scopeSelector: kdsl.core.v1.ScopeSelector
    scopes: Sequence[str]


ResourceQuotaSpecUnion = Union[ResourceQuotaSpec, ResourceQuotaSpecTypedDict]


@attr.s(kw_only=True)
class Namespace(K8sResource):
    apiVersion: ClassVar[str] = "v1"
    kind: ClassVar[str] = "Namespace"
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    spec: Union[None, OmitEnum, kdsl.core.v1.NamespaceSpec] = attr.ib(
        metadata={"yaml_name": "spec"},
        converter=kdsl.core.v1_converters.optional_converter_NamespaceSpec,
        default=OMIT,
    )
    status: Union[None, OmitEnum, kdsl.core.v1.NamespaceStatus] = attr.ib(
        metadata={"yaml_name": "status"},
        converter=kdsl.core.v1_converters.optional_converter_NamespaceStatus,
        default=OMIT,
    )
