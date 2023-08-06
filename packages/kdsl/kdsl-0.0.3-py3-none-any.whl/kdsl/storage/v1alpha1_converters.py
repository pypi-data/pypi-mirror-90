from __future__ import annotations
from typing import Literal, Union
from kdsl.bases import OmitEnum, OMIT
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import kdsl.storage.v1alpha1


def optional_converter_VolumeAttachmentStatus(
    value: Union[kdsl.storage.v1alpha1.VolumeAttachmentStatusUnion, OmitEnum, None]
) -> Union[kdsl.storage.v1alpha1.VolumeAttachmentStatus, OmitEnum, None]:
    import kdsl.storage.v1alpha1

    return (
        kdsl.storage.v1alpha1.VolumeAttachmentStatus(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_VolumeAttachmentSpec(
    value: Union[kdsl.storage.v1alpha1.VolumeAttachmentSpecUnion, OmitEnum, None]
) -> Union[kdsl.storage.v1alpha1.VolumeAttachmentSpec, OmitEnum, None]:
    import kdsl.storage.v1alpha1

    return (
        kdsl.storage.v1alpha1.VolumeAttachmentSpec(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_VolumeAttachmentSource(
    value: kdsl.storage.v1alpha1.VolumeAttachmentSourceUnion,
) -> kdsl.storage.v1alpha1.VolumeAttachmentSource:
    import kdsl.storage.v1alpha1

    return (
        kdsl.storage.v1alpha1.VolumeAttachmentSource(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_VolumeAttachmentSource(
    value: Union[kdsl.storage.v1alpha1.VolumeAttachmentSourceUnion, OmitEnum, None]
) -> Union[kdsl.storage.v1alpha1.VolumeAttachmentSource, OmitEnum, None]:
    import kdsl.storage.v1alpha1

    return (
        kdsl.storage.v1alpha1.VolumeAttachmentSource(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_VolumeError(
    value: kdsl.storage.v1alpha1.VolumeErrorUnion,
) -> kdsl.storage.v1alpha1.VolumeError:
    import kdsl.storage.v1alpha1

    return (
        kdsl.storage.v1alpha1.VolumeError(**value) if isinstance(value, dict) else value
    )


def required_converter_VolumeAttachmentStatus(
    value: kdsl.storage.v1alpha1.VolumeAttachmentStatusUnion,
) -> kdsl.storage.v1alpha1.VolumeAttachmentStatus:
    import kdsl.storage.v1alpha1

    return (
        kdsl.storage.v1alpha1.VolumeAttachmentStatus(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_VolumeError(
    value: Union[kdsl.storage.v1alpha1.VolumeErrorUnion, OmitEnum, None]
) -> Union[kdsl.storage.v1alpha1.VolumeError, OmitEnum, None]:
    import kdsl.storage.v1alpha1

    return (
        kdsl.storage.v1alpha1.VolumeError(**value) if isinstance(value, dict) else value
    )


def required_converter_VolumeAttachmentSpec(
    value: kdsl.storage.v1alpha1.VolumeAttachmentSpecUnion,
) -> kdsl.storage.v1alpha1.VolumeAttachmentSpec:
    import kdsl.storage.v1alpha1

    return (
        kdsl.storage.v1alpha1.VolumeAttachmentSpec(**value)
        if isinstance(value, dict)
        else value
    )
