from __future__ import annotations
from typing import Literal, Union
from kdsl.bases import OmitEnum, OMIT
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import kdsl.settings.v1alpha1


def optional_converter_PodPresetSpec(
    value: Union[kdsl.settings.v1alpha1.PodPresetSpecUnion, OmitEnum, None]
) -> Union[kdsl.settings.v1alpha1.PodPresetSpec, OmitEnum, None]:
    import kdsl.settings.v1alpha1

    return (
        kdsl.settings.v1alpha1.PodPresetSpec(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_PodPresetSpec(
    value: kdsl.settings.v1alpha1.PodPresetSpecUnion,
) -> kdsl.settings.v1alpha1.PodPresetSpec:
    import kdsl.settings.v1alpha1

    return (
        kdsl.settings.v1alpha1.PodPresetSpec(**value)
        if isinstance(value, dict)
        else value
    )
