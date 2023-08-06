from __future__ import annotations
import kdsl.core.v1
import kdsl.networking.v1beta1
import kdsl.core.v1_converters
import kdsl.networking.v1beta1_converters
import attr
from typing import Mapping, ClassVar, Optional, Any, Sequence, TypedDict, Union
from kdsl.bases import OmitEnum, K8sObject, OMIT, K8sResource


@attr.s(kw_only=True)
class IngressStatus(K8sObject):
    loadBalancer: Union[None, OmitEnum, kdsl.core.v1.LoadBalancerStatus] = attr.ib(
        metadata={"yaml_name": "loadBalancer"},
        converter=kdsl.core.v1_converters.optional_converter_LoadBalancerStatus,
        default=OMIT,
    )


class IngressStatusTypedDict(TypedDict, total=(False)):
    loadBalancer: kdsl.core.v1.LoadBalancerStatus


IngressStatusUnion = Union[IngressStatus, IngressStatusTypedDict]


@attr.s(kw_only=True)
class HTTPIngressRuleValue(K8sObject):
    paths: Sequence[kdsl.networking.v1beta1.HTTPIngressPath] = attr.ib(
        metadata={"yaml_name": "paths"},
        converter=kdsl.networking.v1beta1_converters.required_list_converter_HTTPIngressPath,
    )


class HTTPIngressRuleValueTypedDict(TypedDict, total=(True)):
    paths: Sequence[kdsl.networking.v1beta1.HTTPIngressPath]


HTTPIngressRuleValueUnion = Union[HTTPIngressRuleValue, HTTPIngressRuleValueTypedDict]


@attr.s(kw_only=True)
class Ingress(K8sResource):
    apiVersion: ClassVar[str] = "networking.k8s.io/v1beta1"
    kind: ClassVar[str] = "Ingress"
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    spec: Union[None, OmitEnum, kdsl.networking.v1beta1.IngressSpec] = attr.ib(
        metadata={"yaml_name": "spec"},
        converter=kdsl.networking.v1beta1_converters.optional_converter_IngressSpec,
        default=OMIT,
    )
    status: Union[None, OmitEnum, kdsl.networking.v1beta1.IngressStatus] = attr.ib(
        metadata={"yaml_name": "status"},
        converter=kdsl.networking.v1beta1_converters.optional_converter_IngressStatus,
        default=OMIT,
    )


@attr.s(kw_only=True)
class IngressBackend(K8sObject):
    serviceName: str = attr.ib(metadata={"yaml_name": "serviceName"})
    servicePort: Union[int, str] = attr.ib(metadata={"yaml_name": "servicePort"})


class IngressBackendTypedDict(TypedDict, total=(True)):
    serviceName: str
    servicePort: Union[int, str]


IngressBackendUnion = Union[IngressBackend, IngressBackendTypedDict]


@attr.s(kw_only=True)
class IngressRule(K8sObject):
    host: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "host"}, default=OMIT
    )
    http: Union[None, OmitEnum, kdsl.networking.v1beta1.HTTPIngressRuleValue] = attr.ib(
        metadata={"yaml_name": "http"},
        converter=kdsl.networking.v1beta1_converters.optional_converter_HTTPIngressRuleValue,
        default=OMIT,
    )


class IngressRuleTypedDict(TypedDict, total=(False)):
    host: str
    http: kdsl.networking.v1beta1.HTTPIngressRuleValue


IngressRuleUnion = Union[IngressRule, IngressRuleTypedDict]


@attr.s(kw_only=True)
class HTTPIngressPath(K8sObject):
    backend: kdsl.networking.v1beta1.IngressBackend = attr.ib(
        metadata={"yaml_name": "backend"},
        converter=kdsl.networking.v1beta1_converters.required_converter_IngressBackend,
    )
    path: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "path"}, default=OMIT
    )


class HTTPIngressPathOptionalTypedDict(TypedDict, total=(False)):
    path: str


class HTTPIngressPathTypedDict(HTTPIngressPathOptionalTypedDict, total=(True)):
    backend: kdsl.networking.v1beta1.IngressBackend


HTTPIngressPathUnion = Union[HTTPIngressPath, HTTPIngressPathTypedDict]


@attr.s(kw_only=True)
class IngressSpec(K8sObject):
    backend: Union[None, OmitEnum, kdsl.networking.v1beta1.IngressBackend] = attr.ib(
        metadata={"yaml_name": "backend"},
        converter=kdsl.networking.v1beta1_converters.optional_converter_IngressBackend,
        default=OMIT,
    )
    rules: Union[
        None, OmitEnum, Sequence[kdsl.networking.v1beta1.IngressRule]
    ] = attr.ib(
        metadata={"yaml_name": "rules"},
        converter=kdsl.networking.v1beta1_converters.optional_list_converter_IngressRule,
        default=OMIT,
    )
    tls: Union[None, OmitEnum, Sequence[kdsl.networking.v1beta1.IngressTLS]] = attr.ib(
        metadata={"yaml_name": "tls"},
        converter=kdsl.networking.v1beta1_converters.optional_list_converter_IngressTLS,
        default=OMIT,
    )


class IngressSpecTypedDict(TypedDict, total=(False)):
    backend: kdsl.networking.v1beta1.IngressBackend
    rules: Sequence[kdsl.networking.v1beta1.IngressRule]
    tls: Sequence[kdsl.networking.v1beta1.IngressTLS]


IngressSpecUnion = Union[IngressSpec, IngressSpecTypedDict]


@attr.s(kw_only=True)
class IngressTLS(K8sObject):
    hosts: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "hosts"}, default=OMIT
    )
    secretName: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "secretName"}, default=OMIT
    )


class IngressTLSTypedDict(TypedDict, total=(False)):
    hosts: Sequence[str]
    secretName: str


IngressTLSUnion = Union[IngressTLS, IngressTLSTypedDict]
