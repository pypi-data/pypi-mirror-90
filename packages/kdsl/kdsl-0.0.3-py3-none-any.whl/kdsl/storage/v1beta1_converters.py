from __future__ import annotations
from typing import Mapping, Literal, Union
from kdsl.bases import OmitEnum, OMIT
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import kdsl.storage.v1beta1


def required_converter_CSINodeSpec(
    value: kdsl.storage.v1beta1.CSINodeSpecUnion,
) -> kdsl.storage.v1beta1.CSINodeSpec:
    import kdsl.storage.v1beta1

    return (
        kdsl.storage.v1beta1.CSINodeSpec(**value) if isinstance(value, dict) else value
    )


def required_converter_VolumeNodeResources(
    value: kdsl.storage.v1beta1.VolumeNodeResourcesUnion,
) -> kdsl.storage.v1beta1.VolumeNodeResources:
    import kdsl.storage.v1beta1

    return (
        kdsl.storage.v1beta1.VolumeNodeResources(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_VolumeError(
    value: Union[kdsl.storage.v1beta1.VolumeErrorUnion, OmitEnum, None]
) -> Union[kdsl.storage.v1beta1.VolumeError, OmitEnum, None]:
    import kdsl.storage.v1beta1

    return (
        kdsl.storage.v1beta1.VolumeError(**value) if isinstance(value, dict) else value
    )


def optional_converter_VolumeAttachmentSpec(
    value: Union[kdsl.storage.v1beta1.VolumeAttachmentSpecUnion, OmitEnum, None]
) -> Union[kdsl.storage.v1beta1.VolumeAttachmentSpec, OmitEnum, None]:
    import kdsl.storage.v1beta1

    return (
        kdsl.storage.v1beta1.VolumeAttachmentSpec(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_CSINodeDriverItem(
    value: kdsl.storage.v1beta1.CSINodeDriverItemUnion,
) -> kdsl.storage.v1beta1.CSINodeDriverItem:
    import kdsl.storage.v1beta1

    return (
        kdsl.storage.v1beta1.CSINodeDriverItem(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_CSIDriverSpec(
    value: Union[kdsl.storage.v1beta1.CSIDriverSpecUnion, OmitEnum, None]
) -> Union[kdsl.storage.v1beta1.CSIDriverSpec, OmitEnum, None]:
    import kdsl.storage.v1beta1

    return (
        kdsl.storage.v1beta1.CSIDriverSpec(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_VolumeAttachmentSource(
    value: Union[kdsl.storage.v1beta1.VolumeAttachmentSourceUnion, OmitEnum, None]
) -> Union[kdsl.storage.v1beta1.VolumeAttachmentSource, OmitEnum, None]:
    import kdsl.storage.v1beta1

    return (
        kdsl.storage.v1beta1.VolumeAttachmentSource(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_VolumeNodeResources(
    value: Union[kdsl.storage.v1beta1.VolumeNodeResourcesUnion, OmitEnum, None]
) -> Union[kdsl.storage.v1beta1.VolumeNodeResources, OmitEnum, None]:
    import kdsl.storage.v1beta1

    return (
        kdsl.storage.v1beta1.VolumeNodeResources(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_VolumeAttachmentStatus(
    value: Union[kdsl.storage.v1beta1.VolumeAttachmentStatusUnion, OmitEnum, None]
) -> Union[kdsl.storage.v1beta1.VolumeAttachmentStatus, OmitEnum, None]:
    import kdsl.storage.v1beta1

    return (
        kdsl.storage.v1beta1.VolumeAttachmentStatus(**value)
        if isinstance(value, dict)
        else value
    )


def required_mlist_converter_CSINodeDriverItem(
    value: Mapping[str, kdsl.storage.v1beta1.CSINodeDriverItemUnion]
) -> Mapping[str, kdsl.storage.v1beta1.CSINodeDriverItem]:
    return {k: required_converter_CSINodeDriverItem(v) for k, v in value.items()}


def required_converter_VolumeAttachmentStatus(
    value: kdsl.storage.v1beta1.VolumeAttachmentStatusUnion,
) -> kdsl.storage.v1beta1.VolumeAttachmentStatus:
    import kdsl.storage.v1beta1

    return (
        kdsl.storage.v1beta1.VolumeAttachmentStatus(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_CSINodeSpec(
    value: Union[kdsl.storage.v1beta1.CSINodeSpecUnion, OmitEnum, None]
) -> Union[kdsl.storage.v1beta1.CSINodeSpec, OmitEnum, None]:
    import kdsl.storage.v1beta1

    return (
        kdsl.storage.v1beta1.CSINodeSpec(**value) if isinstance(value, dict) else value
    )


def optional_converter_CSINodeDriverItem(
    value: Union[kdsl.storage.v1beta1.CSINodeDriverItemUnion, OmitEnum, None]
) -> Union[kdsl.storage.v1beta1.CSINodeDriverItem, OmitEnum, None]:
    import kdsl.storage.v1beta1

    return (
        kdsl.storage.v1beta1.CSINodeDriverItem(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_VolumeError(
    value: kdsl.storage.v1beta1.VolumeErrorUnion,
) -> kdsl.storage.v1beta1.VolumeError:
    import kdsl.storage.v1beta1

    return (
        kdsl.storage.v1beta1.VolumeError(**value) if isinstance(value, dict) else value
    )


def required_converter_VolumeAttachmentSpec(
    value: kdsl.storage.v1beta1.VolumeAttachmentSpecUnion,
) -> kdsl.storage.v1beta1.VolumeAttachmentSpec:
    import kdsl.storage.v1beta1

    return (
        kdsl.storage.v1beta1.VolumeAttachmentSpec(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_CSIDriverSpec(
    value: kdsl.storage.v1beta1.CSIDriverSpecUnion,
) -> kdsl.storage.v1beta1.CSIDriverSpec:
    import kdsl.storage.v1beta1

    return (
        kdsl.storage.v1beta1.CSIDriverSpec(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_VolumeAttachmentSource(
    value: kdsl.storage.v1beta1.VolumeAttachmentSourceUnion,
) -> kdsl.storage.v1beta1.VolumeAttachmentSource:
    import kdsl.storage.v1beta1

    return (
        kdsl.storage.v1beta1.VolumeAttachmentSource(**value)
        if isinstance(value, dict)
        else value
    )
