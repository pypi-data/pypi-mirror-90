from __future__ import annotations
import kdsl.core.v1_converters
import kdsl.settings.v1alpha1_converters
import kdsl.settings.v1alpha1
import kdsl.core.v1
import attr
from typing import Mapping, ClassVar, Optional, Any, Sequence, TypedDict, Union
from kdsl.bases import OmitEnum, K8sObject, OMIT, K8sResource


@attr.s(kw_only=True)
class PodPresetSpec(K8sObject):
    env: Union[None, OmitEnum, Sequence[kdsl.core.v1.EnvVar]] = attr.ib(
        metadata={"yaml_name": "env"},
        converter=kdsl.core.v1_converters.optional_list_converter_EnvVar,
        default=OMIT,
    )
    envFrom: Union[None, OmitEnum, Sequence[kdsl.core.v1.EnvFromSource]] = attr.ib(
        metadata={"yaml_name": "envFrom"},
        converter=kdsl.core.v1_converters.optional_list_converter_EnvFromSource,
        default=OMIT,
    )
    selector: Union[None, OmitEnum, kdsl.core.v1.LabelSelector] = attr.ib(
        metadata={"yaml_name": "selector"},
        converter=kdsl.core.v1_converters.optional_converter_LabelSelector,
        default=OMIT,
    )
    volumeMounts: Union[None, OmitEnum, Sequence[kdsl.core.v1.VolumeMount]] = attr.ib(
        metadata={"yaml_name": "volumeMounts"},
        converter=kdsl.core.v1_converters.optional_list_converter_VolumeMount,
        default=OMIT,
    )
    volumes: Union[None, OmitEnum, Sequence[kdsl.core.v1.Volume]] = attr.ib(
        metadata={"yaml_name": "volumes"},
        converter=kdsl.core.v1_converters.optional_list_converter_Volume,
        default=OMIT,
    )


class PodPresetSpecTypedDict(TypedDict, total=(False)):
    env: Sequence[kdsl.core.v1.EnvVar]
    envFrom: Sequence[kdsl.core.v1.EnvFromSource]
    selector: kdsl.core.v1.LabelSelector
    volumeMounts: Sequence[kdsl.core.v1.VolumeMount]
    volumes: Sequence[kdsl.core.v1.Volume]


PodPresetSpecUnion = Union[PodPresetSpec, PodPresetSpecTypedDict]


@attr.s(kw_only=True)
class PodPreset(K8sResource):
    apiVersion: ClassVar[str] = "settings.k8s.io/v1alpha1"
    kind: ClassVar[str] = "PodPreset"
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    spec: Union[None, OmitEnum, kdsl.settings.v1alpha1.PodPresetSpec] = attr.ib(
        metadata={"yaml_name": "spec"},
        converter=kdsl.settings.v1alpha1_converters.optional_converter_PodPresetSpec,
        default=OMIT,
    )
