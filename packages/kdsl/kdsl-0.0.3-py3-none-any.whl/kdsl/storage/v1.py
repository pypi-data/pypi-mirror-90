from __future__ import annotations
import kdsl.storage.v1
import kdsl.core.v1_converters
import kdsl.core.v1
import attr
import kdsl.storage.v1_converters
from typing import Mapping, ClassVar, Optional, Any, Sequence, TypedDict, Union
from kdsl.bases import OmitEnum, K8sObject, OMIT, K8sResource


@attr.s(kw_only=True)
class VolumeNodeResources(K8sObject):
    count: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "count"}, default=OMIT
    )


class VolumeNodeResourcesTypedDict(TypedDict, total=(False)):
    count: int


VolumeNodeResourcesUnion = Union[VolumeNodeResources, VolumeNodeResourcesTypedDict]


@attr.s(kw_only=True)
class CSINodeSpec(K8sObject):
    drivers: Mapping[str, kdsl.storage.v1.CSINodeDriverItem] = attr.ib(
        metadata={"yaml_name": "drivers", "mlist_key": "name"},
        converter=kdsl.storage.v1_converters.required_mlist_converter_CSINodeDriverItem,
    )


class CSINodeSpecTypedDict(TypedDict, total=(True)):
    drivers: Mapping[str, kdsl.storage.v1.CSINodeDriverItem]


CSINodeSpecUnion = Union[CSINodeSpec, CSINodeSpecTypedDict]


@attr.s(kw_only=True)
class CSINode(K8sResource):
    apiVersion: ClassVar[str] = "storage.k8s.io/v1"
    kind: ClassVar[str] = "CSINode"
    spec: kdsl.storage.v1.CSINodeSpec = attr.ib(
        metadata={"yaml_name": "spec"},
        converter=kdsl.storage.v1_converters.required_converter_CSINodeSpec,
    )
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )


@attr.s(kw_only=True)
class VolumeAttachmentStatus(K8sObject):
    attached: bool = attr.ib(metadata={"yaml_name": "attached"})
    attachError: Union[None, OmitEnum, kdsl.storage.v1.VolumeError] = attr.ib(
        metadata={"yaml_name": "attachError"},
        converter=kdsl.storage.v1_converters.optional_converter_VolumeError,
        default=OMIT,
    )
    attachmentMetadata: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(
        metadata={"yaml_name": "attachmentMetadata"}, default=OMIT
    )
    detachError: Union[None, OmitEnum, kdsl.storage.v1.VolumeError] = attr.ib(
        metadata={"yaml_name": "detachError"},
        converter=kdsl.storage.v1_converters.optional_converter_VolumeError,
        default=OMIT,
    )


class VolumeAttachmentStatusOptionalTypedDict(TypedDict, total=(False)):
    attachError: kdsl.storage.v1.VolumeError
    attachmentMetadata: Mapping[str, str]
    detachError: kdsl.storage.v1.VolumeError


class VolumeAttachmentStatusTypedDict(
    VolumeAttachmentStatusOptionalTypedDict, total=(True)
):
    attached: bool


VolumeAttachmentStatusUnion = Union[
    VolumeAttachmentStatus, VolumeAttachmentStatusTypedDict
]


@attr.s(kw_only=True)
class VolumeAttachment(K8sResource):
    apiVersion: ClassVar[str] = "storage.k8s.io/v1"
    kind: ClassVar[str] = "VolumeAttachment"
    spec: kdsl.storage.v1.VolumeAttachmentSpec = attr.ib(
        metadata={"yaml_name": "spec"},
        converter=kdsl.storage.v1_converters.required_converter_VolumeAttachmentSpec,
    )
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    status: Union[None, OmitEnum, kdsl.storage.v1.VolumeAttachmentStatus] = attr.ib(
        metadata={"yaml_name": "status"},
        converter=kdsl.storage.v1_converters.optional_converter_VolumeAttachmentStatus,
        default=OMIT,
    )


@attr.s(kw_only=True)
class VolumeError(K8sObject):
    message: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "message"}, default=OMIT
    )
    time: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "time"}, default=OMIT
    )


class VolumeErrorTypedDict(TypedDict, total=(False)):
    message: str
    time: str


VolumeErrorUnion = Union[VolumeError, VolumeErrorTypedDict]


@attr.s(kw_only=True)
class VolumeAttachmentSource(K8sObject):
    inlineVolumeSpec: Union[
        None, OmitEnum, kdsl.core.v1.PersistentVolumeSpec
    ] = attr.ib(
        metadata={"yaml_name": "inlineVolumeSpec"},
        converter=kdsl.core.v1_converters.optional_converter_PersistentVolumeSpec,
        default=OMIT,
    )
    persistentVolumeName: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "persistentVolumeName"}, default=OMIT
    )


class VolumeAttachmentSourceTypedDict(TypedDict, total=(False)):
    inlineVolumeSpec: kdsl.core.v1.PersistentVolumeSpec
    persistentVolumeName: str


VolumeAttachmentSourceUnion = Union[
    VolumeAttachmentSource, VolumeAttachmentSourceTypedDict
]


@attr.s(kw_only=True)
class CSINodeDriverItem(K8sObject):
    nodeID: str = attr.ib(metadata={"yaml_name": "nodeID"})
    allocatable: Union[None, OmitEnum, kdsl.storage.v1.VolumeNodeResources] = attr.ib(
        metadata={"yaml_name": "allocatable"},
        converter=kdsl.storage.v1_converters.optional_converter_VolumeNodeResources,
        default=OMIT,
    )
    topologyKeys: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "topologyKeys"}, default=OMIT
    )


class CSINodeDriverItemOptionalTypedDict(TypedDict, total=(False)):
    allocatable: kdsl.storage.v1.VolumeNodeResources
    topologyKeys: Sequence[str]


class CSINodeDriverItemTypedDict(CSINodeDriverItemOptionalTypedDict, total=(True)):
    nodeID: str


CSINodeDriverItemUnion = Union[CSINodeDriverItem, CSINodeDriverItemTypedDict]


@attr.s(kw_only=True)
class StorageClass(K8sResource):
    apiVersion: ClassVar[str] = "storage.k8s.io/v1"
    kind: ClassVar[str] = "StorageClass"
    provisioner: str = attr.ib(metadata={"yaml_name": "provisioner"})
    allowVolumeExpansion: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "allowVolumeExpansion"}, default=OMIT
    )
    allowedTopologies: Union[
        None, OmitEnum, Sequence[kdsl.core.v1.TopologySelectorTerm]
    ] = attr.ib(
        metadata={"yaml_name": "allowedTopologies"},
        converter=kdsl.core.v1_converters.optional_list_converter_TopologySelectorTerm,
        default=OMIT,
    )
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    mountOptions: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "mountOptions"}, default=OMIT
    )
    parameters: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(
        metadata={"yaml_name": "parameters"}, default=OMIT
    )
    reclaimPolicy: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "reclaimPolicy"}, default=OMIT
    )
    volumeBindingMode: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "volumeBindingMode"}, default=OMIT
    )


@attr.s(kw_only=True)
class VolumeAttachmentSpec(K8sObject):
    attacher: str = attr.ib(metadata={"yaml_name": "attacher"})
    nodeName: str = attr.ib(metadata={"yaml_name": "nodeName"})
    source: kdsl.storage.v1.VolumeAttachmentSource = attr.ib(
        metadata={"yaml_name": "source"},
        converter=kdsl.storage.v1_converters.required_converter_VolumeAttachmentSource,
    )


class VolumeAttachmentSpecTypedDict(TypedDict, total=(True)):
    attacher: str
    nodeName: str
    source: kdsl.storage.v1.VolumeAttachmentSource


VolumeAttachmentSpecUnion = Union[VolumeAttachmentSpec, VolumeAttachmentSpecTypedDict]
