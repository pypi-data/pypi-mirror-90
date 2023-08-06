from __future__ import annotations
import kdsl.node.v1beta1
import kdsl.node.v1beta1_converters
import kdsl.core.v1
import kdsl.core.v1_converters
import attr
from typing import Mapping, ClassVar, Optional, Any, Sequence, TypedDict, Union
from kdsl.bases import OmitEnum, K8sObject, OMIT, K8sResource


@attr.s(kw_only=True)
class Overhead(K8sObject):
    podFixed: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(
        metadata={"yaml_name": "podFixed"}, default=OMIT
    )


class OverheadTypedDict(TypedDict, total=(False)):
    podFixed: Mapping[str, str]


OverheadUnion = Union[Overhead, OverheadTypedDict]


@attr.s(kw_only=True)
class RuntimeClass(K8sResource):
    apiVersion: ClassVar[str] = "node.k8s.io/v1beta1"
    kind: ClassVar[str] = "RuntimeClass"
    handler: str = attr.ib(metadata={"yaml_name": "handler"})
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    overhead: Union[None, OmitEnum, kdsl.node.v1beta1.Overhead] = attr.ib(
        metadata={"yaml_name": "overhead"},
        converter=kdsl.node.v1beta1_converters.optional_converter_Overhead,
        default=OMIT,
    )
    scheduling: Union[None, OmitEnum, kdsl.node.v1beta1.Scheduling] = attr.ib(
        metadata={"yaml_name": "scheduling"},
        converter=kdsl.node.v1beta1_converters.optional_converter_Scheduling,
        default=OMIT,
    )


@attr.s(kw_only=True)
class Scheduling(K8sObject):
    nodeSelector: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(
        metadata={"yaml_name": "nodeSelector"}, default=OMIT
    )
    tolerations: Union[None, OmitEnum, Sequence[kdsl.core.v1.Toleration]] = attr.ib(
        metadata={"yaml_name": "tolerations"},
        converter=kdsl.core.v1_converters.optional_list_converter_Toleration,
        default=OMIT,
    )


class SchedulingTypedDict(TypedDict, total=(False)):
    nodeSelector: Mapping[str, str]
    tolerations: Sequence[kdsl.core.v1.Toleration]


SchedulingUnion = Union[Scheduling, SchedulingTypedDict]
