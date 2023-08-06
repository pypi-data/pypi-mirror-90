from __future__ import annotations
import kdsl.coordination.v1_converters
import kdsl.core.v1
import kdsl.core.v1_converters
import kdsl.coordination.v1
import attr
from typing import Mapping, ClassVar, Optional, Any, Sequence, TypedDict, Union
from kdsl.bases import OmitEnum, K8sObject, OMIT, K8sResource


@attr.s(kw_only=True)
class Lease(K8sResource):
    apiVersion: ClassVar[str] = "coordination.k8s.io/v1"
    kind: ClassVar[str] = "Lease"
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    spec: Union[None, OmitEnum, kdsl.coordination.v1.LeaseSpec] = attr.ib(
        metadata={"yaml_name": "spec"},
        converter=kdsl.coordination.v1_converters.optional_converter_LeaseSpec,
        default=OMIT,
    )


@attr.s(kw_only=True)
class LeaseSpec(K8sObject):
    acquireTime: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "acquireTime"}, default=OMIT
    )
    holderIdentity: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "holderIdentity"}, default=OMIT
    )
    leaseDurationSeconds: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "leaseDurationSeconds"}, default=OMIT
    )
    leaseTransitions: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "leaseTransitions"}, default=OMIT
    )
    renewTime: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "renewTime"}, default=OMIT
    )


class LeaseSpecTypedDict(TypedDict, total=(False)):
    acquireTime: str
    holderIdentity: str
    leaseDurationSeconds: int
    leaseTransitions: int
    renewTime: str


LeaseSpecUnion = Union[LeaseSpec, LeaseSpecTypedDict]
