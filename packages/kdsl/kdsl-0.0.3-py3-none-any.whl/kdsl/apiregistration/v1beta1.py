from __future__ import annotations
import kdsl.core.v1_converters
import kdsl.core.v1
import kdsl.apiregistration.v1beta1
import kdsl.apiregistration.v1beta1_converters
import attr
from typing import Mapping, ClassVar, Optional, Any, Sequence, TypedDict, Union
from kdsl.bases import OmitEnum, K8sObject, OMIT, K8sResource


@attr.s(kw_only=True)
class APIServiceConditionItem(K8sObject):
    status: str = attr.ib(metadata={"yaml_name": "status"})
    lastTransitionTime: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "lastTransitionTime"}, default=OMIT
    )
    message: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "message"}, default=OMIT
    )
    reason: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "reason"}, default=OMIT
    )


class APIServiceConditionItemOptionalTypedDict(TypedDict, total=(False)):
    lastTransitionTime: str
    message: str
    reason: str


class APIServiceConditionItemTypedDict(
    APIServiceConditionItemOptionalTypedDict, total=(True)
):
    status: str


APIServiceConditionItemUnion = Union[
    APIServiceConditionItem, APIServiceConditionItemTypedDict
]


@attr.s(kw_only=True)
class ServiceReference(K8sObject):
    name: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "name"}, default=OMIT
    )
    namespace: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "namespace"}, default=OMIT
    )
    port: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "port"}, default=OMIT
    )


class ServiceReferenceTypedDict(TypedDict, total=(False)):
    name: str
    namespace: str
    port: int


ServiceReferenceUnion = Union[ServiceReference, ServiceReferenceTypedDict]


@attr.s(kw_only=True)
class APIServiceStatus(K8sObject):
    conditions: Union[
        None,
        OmitEnum,
        Mapping[str, kdsl.apiregistration.v1beta1.APIServiceConditionItem],
    ] = attr.ib(
        metadata={"yaml_name": "conditions", "mlist_key": "type"},
        converter=kdsl.apiregistration.v1beta1_converters.optional_mlist_converter_APIServiceConditionItem,
        default=OMIT,
    )


class APIServiceStatusTypedDict(TypedDict, total=(False)):
    conditions: Mapping[str, kdsl.apiregistration.v1beta1.APIServiceConditionItem]


APIServiceStatusUnion = Union[APIServiceStatus, APIServiceStatusTypedDict]


@attr.s(kw_only=True)
class APIServiceSpec(K8sObject):
    groupPriorityMinimum: int = attr.ib(metadata={"yaml_name": "groupPriorityMinimum"})
    service: kdsl.apiregistration.v1beta1.ServiceReference = attr.ib(
        metadata={"yaml_name": "service"},
        converter=kdsl.apiregistration.v1beta1_converters.required_converter_ServiceReference,
    )
    versionPriority: int = attr.ib(metadata={"yaml_name": "versionPriority"})
    caBundle: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "caBundle"}, default=OMIT
    )
    group: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "group"}, default=OMIT
    )
    insecureSkipTLSVerify: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "insecureSkipTLSVerify"}, default=OMIT
    )
    version: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "version"}, default=OMIT
    )


class APIServiceSpecOptionalTypedDict(TypedDict, total=(False)):
    caBundle: str
    group: str
    insecureSkipTLSVerify: bool
    version: str


class APIServiceSpecTypedDict(APIServiceSpecOptionalTypedDict, total=(True)):
    groupPriorityMinimum: int
    service: kdsl.apiregistration.v1beta1.ServiceReference
    versionPriority: int


APIServiceSpecUnion = Union[APIServiceSpec, APIServiceSpecTypedDict]


@attr.s(kw_only=True)
class APIService(K8sResource):
    apiVersion: ClassVar[str] = "apiregistration.k8s.io/v1beta1"
    kind: ClassVar[str] = "APIService"
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    spec: Union[None, OmitEnum, kdsl.apiregistration.v1beta1.APIServiceSpec] = attr.ib(
        metadata={"yaml_name": "spec"},
        converter=kdsl.apiregistration.v1beta1_converters.optional_converter_APIServiceSpec,
        default=OMIT,
    )
    status: Union[
        None, OmitEnum, kdsl.apiregistration.v1beta1.APIServiceStatus
    ] = attr.ib(
        metadata={"yaml_name": "status"},
        converter=kdsl.apiregistration.v1beta1_converters.optional_converter_APIServiceStatus,
        default=OMIT,
    )
