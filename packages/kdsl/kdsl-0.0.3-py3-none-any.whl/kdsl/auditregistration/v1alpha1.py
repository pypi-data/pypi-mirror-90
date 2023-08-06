from __future__ import annotations
import kdsl.core.v1_converters
import kdsl.auditregistration.v1alpha1
import kdsl.core.v1
import attr
import kdsl.auditregistration.v1alpha1_converters
from typing import Mapping, ClassVar, Optional, Any, Sequence, TypedDict, Union
from kdsl.bases import OmitEnum, K8sObject, OMIT, K8sResource


@attr.s(kw_only=True)
class WebhookClientConfig(K8sObject):
    caBundle: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "caBundle"}, default=OMIT
    )
    service: Union[
        None, OmitEnum, kdsl.auditregistration.v1alpha1.ServiceReference
    ] = attr.ib(
        metadata={"yaml_name": "service"},
        converter=kdsl.auditregistration.v1alpha1_converters.optional_converter_ServiceReference,
        default=OMIT,
    )
    url: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "url"}, default=OMIT
    )


class WebhookClientConfigTypedDict(TypedDict, total=(False)):
    caBundle: str
    service: kdsl.auditregistration.v1alpha1.ServiceReference
    url: str


WebhookClientConfigUnion = Union[WebhookClientConfig, WebhookClientConfigTypedDict]


@attr.s(kw_only=True)
class WebhookThrottleConfig(K8sObject):
    burst: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "burst"}, default=OMIT
    )
    qps: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "qps"}, default=OMIT
    )


class WebhookThrottleConfigTypedDict(TypedDict, total=(False)):
    burst: int
    qps: int


WebhookThrottleConfigUnion = Union[
    WebhookThrottleConfig, WebhookThrottleConfigTypedDict
]


@attr.s(kw_only=True)
class Webhook(K8sObject):
    clientConfig: kdsl.auditregistration.v1alpha1.WebhookClientConfig = attr.ib(
        metadata={"yaml_name": "clientConfig"},
        converter=kdsl.auditregistration.v1alpha1_converters.required_converter_WebhookClientConfig,
    )
    throttle: Union[
        None, OmitEnum, kdsl.auditregistration.v1alpha1.WebhookThrottleConfig
    ] = attr.ib(
        metadata={"yaml_name": "throttle"},
        converter=kdsl.auditregistration.v1alpha1_converters.optional_converter_WebhookThrottleConfig,
        default=OMIT,
    )


class WebhookOptionalTypedDict(TypedDict, total=(False)):
    throttle: kdsl.auditregistration.v1alpha1.WebhookThrottleConfig


class WebhookTypedDict(WebhookOptionalTypedDict, total=(True)):
    clientConfig: kdsl.auditregistration.v1alpha1.WebhookClientConfig


WebhookUnion = Union[Webhook, WebhookTypedDict]


@attr.s(kw_only=True)
class ServiceReference(K8sObject):
    name: str = attr.ib(metadata={"yaml_name": "name"})
    namespace: str = attr.ib(metadata={"yaml_name": "namespace"})
    path: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "path"}, default=OMIT
    )
    port: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "port"}, default=OMIT
    )


class ServiceReferenceOptionalTypedDict(TypedDict, total=(False)):
    path: str
    port: int


class ServiceReferenceTypedDict(ServiceReferenceOptionalTypedDict, total=(True)):
    name: str
    namespace: str


ServiceReferenceUnion = Union[ServiceReference, ServiceReferenceTypedDict]


@attr.s(kw_only=True)
class AuditSinkSpec(K8sObject):
    policy: kdsl.auditregistration.v1alpha1.Policy = attr.ib(
        metadata={"yaml_name": "policy"},
        converter=kdsl.auditregistration.v1alpha1_converters.required_converter_Policy,
    )
    webhook: kdsl.auditregistration.v1alpha1.Webhook = attr.ib(
        metadata={"yaml_name": "webhook"},
        converter=kdsl.auditregistration.v1alpha1_converters.required_converter_Webhook,
    )


class AuditSinkSpecTypedDict(TypedDict, total=(True)):
    policy: kdsl.auditregistration.v1alpha1.Policy
    webhook: kdsl.auditregistration.v1alpha1.Webhook


AuditSinkSpecUnion = Union[AuditSinkSpec, AuditSinkSpecTypedDict]


@attr.s(kw_only=True)
class Policy(K8sObject):
    level: str = attr.ib(metadata={"yaml_name": "level"})
    stages: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "stages"}, default=OMIT
    )


class PolicyOptionalTypedDict(TypedDict, total=(False)):
    stages: Sequence[str]


class PolicyTypedDict(PolicyOptionalTypedDict, total=(True)):
    level: str


PolicyUnion = Union[Policy, PolicyTypedDict]


@attr.s(kw_only=True)
class AuditSink(K8sResource):
    apiVersion: ClassVar[str] = "auditregistration.k8s.io/v1alpha1"
    kind: ClassVar[str] = "AuditSink"
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    spec: Union[
        None, OmitEnum, kdsl.auditregistration.v1alpha1.AuditSinkSpec
    ] = attr.ib(
        metadata={"yaml_name": "spec"},
        converter=kdsl.auditregistration.v1alpha1_converters.optional_converter_AuditSinkSpec,
        default=OMIT,
    )
