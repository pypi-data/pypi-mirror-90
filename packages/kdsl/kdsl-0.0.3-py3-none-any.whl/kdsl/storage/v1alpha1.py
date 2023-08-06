from __future__ import annotations
import kdsl.storage.v1alpha1_converters
import kdsl.core.v1
import kdsl.core.v1_converters
import kdsl.storage.v1alpha1
import attr
from typing import Mapping, ClassVar, Optional, Any, Sequence, TypedDict, Union
from kdsl.bases import OmitEnum, K8sObject, OMIT, K8sResource


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
class VolumeAttachment(K8sResource):
    apiVersion: ClassVar[str] = "storage.k8s.io/v1alpha1"
    kind: ClassVar[str] = "VolumeAttachment"
    spec: kdsl.storage.v1alpha1.VolumeAttachmentSpec = attr.ib(
        metadata={"yaml_name": "spec"},
        converter=kdsl.storage.v1alpha1_converters.required_converter_VolumeAttachmentSpec,
    )
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    status: Union[
        None, OmitEnum, kdsl.storage.v1alpha1.VolumeAttachmentStatus
    ] = attr.ib(
        metadata={"yaml_name": "status"},
        converter=kdsl.storage.v1alpha1_converters.optional_converter_VolumeAttachmentStatus,
        default=OMIT,
    )


@attr.s(kw_only=True)
class VolumeAttachmentSpec(K8sObject):
    attacher: str = attr.ib(metadata={"yaml_name": "attacher"})
    nodeName: str = attr.ib(metadata={"yaml_name": "nodeName"})
    source: kdsl.storage.v1alpha1.VolumeAttachmentSource = attr.ib(
        metadata={"yaml_name": "source"},
        converter=kdsl.storage.v1alpha1_converters.required_converter_VolumeAttachmentSource,
    )


class VolumeAttachmentSpecTypedDict(TypedDict, total=(True)):
    attacher: str
    nodeName: str
    source: kdsl.storage.v1alpha1.VolumeAttachmentSource


VolumeAttachmentSpecUnion = Union[VolumeAttachmentSpec, VolumeAttachmentSpecTypedDict]


@attr.s(kw_only=True)
class VolumeAttachmentStatus(K8sObject):
    attached: bool = attr.ib(metadata={"yaml_name": "attached"})
    attachError: Union[None, OmitEnum, kdsl.storage.v1alpha1.VolumeError] = attr.ib(
        metadata={"yaml_name": "attachError"},
        converter=kdsl.storage.v1alpha1_converters.optional_converter_VolumeError,
        default=OMIT,
    )
    attachmentMetadata: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(
        metadata={"yaml_name": "attachmentMetadata"}, default=OMIT
    )
    detachError: Union[None, OmitEnum, kdsl.storage.v1alpha1.VolumeError] = attr.ib(
        metadata={"yaml_name": "detachError"},
        converter=kdsl.storage.v1alpha1_converters.optional_converter_VolumeError,
        default=OMIT,
    )


class VolumeAttachmentStatusOptionalTypedDict(TypedDict, total=(False)):
    attachError: kdsl.storage.v1alpha1.VolumeError
    attachmentMetadata: Mapping[str, str]
    detachError: kdsl.storage.v1alpha1.VolumeError


class VolumeAttachmentStatusTypedDict(
    VolumeAttachmentStatusOptionalTypedDict, total=(True)
):
    attached: bool


VolumeAttachmentStatusUnion = Union[
    VolumeAttachmentStatus, VolumeAttachmentStatusTypedDict
]


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
