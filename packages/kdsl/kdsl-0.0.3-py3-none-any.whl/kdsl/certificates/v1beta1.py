from __future__ import annotations
import kdsl.certificates.v1beta1_converters
import kdsl.core.v1
import kdsl.certificates.v1beta1
import kdsl.core.v1_converters
import attr
from typing import Mapping, ClassVar, Optional, Any, Sequence, TypedDict, Union
from kdsl.bases import OmitEnum, K8sObject, OMIT, K8sResource


@attr.s(kw_only=True)
class CertificateSigningRequestStatus(K8sObject):
    certificate: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "certificate"}, default=OMIT
    )
    conditions: Union[
        None,
        OmitEnum,
        Sequence[kdsl.certificates.v1beta1.CertificateSigningRequestCondition],
    ] = attr.ib(
        metadata={"yaml_name": "conditions"},
        converter=kdsl.certificates.v1beta1_converters.optional_list_converter_CertificateSigningRequestCondition,
        default=OMIT,
    )


class CertificateSigningRequestStatusTypedDict(TypedDict, total=(False)):
    certificate: str
    conditions: Sequence[kdsl.certificates.v1beta1.CertificateSigningRequestCondition]


CertificateSigningRequestStatusUnion = Union[
    CertificateSigningRequestStatus, CertificateSigningRequestStatusTypedDict
]


@attr.s(kw_only=True)
class CertificateSigningRequestCondition(K8sObject):
    type: str = attr.ib(metadata={"yaml_name": "type"})
    lastUpdateTime: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "lastUpdateTime"}, default=OMIT
    )
    message: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "message"}, default=OMIT
    )
    reason: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "reason"}, default=OMIT
    )


class CertificateSigningRequestConditionOptionalTypedDict(TypedDict, total=(False)):
    lastUpdateTime: str
    message: str
    reason: str


class CertificateSigningRequestConditionTypedDict(
    CertificateSigningRequestConditionOptionalTypedDict, total=(True)
):
    type: str


CertificateSigningRequestConditionUnion = Union[
    CertificateSigningRequestCondition, CertificateSigningRequestConditionTypedDict
]


@attr.s(kw_only=True)
class CertificateSigningRequest(K8sResource):
    apiVersion: ClassVar[str] = "certificates.k8s.io/v1beta1"
    kind: ClassVar[str] = "CertificateSigningRequest"
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    spec: Union[
        None, OmitEnum, kdsl.certificates.v1beta1.CertificateSigningRequestSpec
    ] = attr.ib(
        metadata={"yaml_name": "spec"},
        converter=kdsl.certificates.v1beta1_converters.optional_converter_CertificateSigningRequestSpec,
        default=OMIT,
    )
    status: Union[
        None, OmitEnum, kdsl.certificates.v1beta1.CertificateSigningRequestStatus
    ] = attr.ib(
        metadata={"yaml_name": "status"},
        converter=kdsl.certificates.v1beta1_converters.optional_converter_CertificateSigningRequestStatus,
        default=OMIT,
    )


@attr.s(kw_only=True)
class CertificateSigningRequestSpec(K8sObject):
    request: str = attr.ib(metadata={"yaml_name": "request"})
    extra: Union[None, OmitEnum, Mapping[str, Sequence[str]]] = attr.ib(
        metadata={"yaml_name": "extra"}, default=OMIT
    )
    groups: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "groups"}, default=OMIT
    )
    uid: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "uid"}, default=OMIT
    )
    usages: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "usages"}, default=OMIT
    )
    username: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "username"}, default=OMIT
    )


class CertificateSigningRequestSpecOptionalTypedDict(TypedDict, total=(False)):
    extra: Mapping[str, Sequence[str]]
    groups: Sequence[str]
    uid: str
    usages: Sequence[str]
    username: str


class CertificateSigningRequestSpecTypedDict(
    CertificateSigningRequestSpecOptionalTypedDict, total=(True)
):
    request: str


CertificateSigningRequestSpecUnion = Union[
    CertificateSigningRequestSpec, CertificateSigningRequestSpecTypedDict
]
