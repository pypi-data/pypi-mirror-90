from __future__ import annotations
import kdsl.authentication.v1beta1_converters
import kdsl.core.v1_converters
import kdsl.core.v1
import kdsl.authentication.v1beta1
import attr
from typing import Mapping, ClassVar, Optional, Any, Sequence, TypedDict, Union
from kdsl.bases import OmitEnum, K8sObject, OMIT, K8sResource


@attr.s(kw_only=True)
class TokenReviewSpec(K8sObject):
    audiences: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "audiences"}, default=OMIT
    )
    token: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "token"}, default=OMIT
    )


class TokenReviewSpecTypedDict(TypedDict, total=(False)):
    audiences: Sequence[str]
    token: str


TokenReviewSpecUnion = Union[TokenReviewSpec, TokenReviewSpecTypedDict]


@attr.s(kw_only=True)
class TokenReviewStatus(K8sObject):
    audiences: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "audiences"}, default=OMIT
    )
    authenticated: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "authenticated"}, default=OMIT
    )
    error: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "error"}, default=OMIT
    )
    user: Union[None, OmitEnum, kdsl.authentication.v1beta1.UserInfo] = attr.ib(
        metadata={"yaml_name": "user"},
        converter=kdsl.authentication.v1beta1_converters.optional_converter_UserInfo,
        default=OMIT,
    )


class TokenReviewStatusTypedDict(TypedDict, total=(False)):
    audiences: Sequence[str]
    authenticated: bool
    error: str
    user: kdsl.authentication.v1beta1.UserInfo


TokenReviewStatusUnion = Union[TokenReviewStatus, TokenReviewStatusTypedDict]


@attr.s(kw_only=True)
class UserInfo(K8sObject):
    extra: Union[None, OmitEnum, Mapping[str, Sequence[str]]] = attr.ib(
        metadata={"yaml_name": "extra"}, default=OMIT
    )
    groups: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "groups"}, default=OMIT
    )
    uid: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "uid"}, default=OMIT
    )
    username: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "username"}, default=OMIT
    )


class UserInfoTypedDict(TypedDict, total=(False)):
    extra: Mapping[str, Sequence[str]]
    groups: Sequence[str]
    uid: str
    username: str


UserInfoUnion = Union[UserInfo, UserInfoTypedDict]


@attr.s(kw_only=True)
class TokenReview(K8sResource):
    apiVersion: ClassVar[str] = "authentication.k8s.io/v1beta1"
    kind: ClassVar[str] = "TokenReview"
    spec: kdsl.authentication.v1beta1.TokenReviewSpec = attr.ib(
        metadata={"yaml_name": "spec"},
        converter=kdsl.authentication.v1beta1_converters.required_converter_TokenReviewSpec,
    )
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    status: Union[
        None, OmitEnum, kdsl.authentication.v1beta1.TokenReviewStatus
    ] = attr.ib(
        metadata={"yaml_name": "status"},
        converter=kdsl.authentication.v1beta1_converters.optional_converter_TokenReviewStatus,
        default=OMIT,
    )
