from __future__ import annotations
import kdsl.admissionregistration.v1_converters
import kdsl.core.v1
import kdsl.core.v1_converters
import attr
import kdsl.admissionregistration.v1
from typing import Mapping, ClassVar, Optional, Any, Sequence, TypedDict, Union
from kdsl.bases import OmitEnum, K8sObject, OMIT, K8sResource


@attr.s(kw_only=True)
class ValidatingWebhookConfiguration(K8sResource):
    apiVersion: ClassVar[str] = "admissionregistration.k8s.io/v1"
    kind: ClassVar[str] = "ValidatingWebhookConfiguration"
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    webhooks: Union[
        None,
        OmitEnum,
        Mapping[str, kdsl.admissionregistration.v1.ValidatingWebhookItem],
    ] = attr.ib(
        metadata={"yaml_name": "webhooks", "mlist_key": "name"},
        converter=kdsl.admissionregistration.v1_converters.optional_mlist_converter_ValidatingWebhookItem,
        default=OMIT,
    )


@attr.s(kw_only=True)
class MutatingWebhookItem(K8sObject):
    admissionReviewVersions: Sequence[str] = attr.ib(
        metadata={"yaml_name": "admissionReviewVersions"}
    )
    clientConfig: kdsl.admissionregistration.v1.WebhookClientConfig = attr.ib(
        metadata={"yaml_name": "clientConfig"},
        converter=kdsl.admissionregistration.v1_converters.required_converter_WebhookClientConfig,
    )
    sideEffects: str = attr.ib(metadata={"yaml_name": "sideEffects"})
    failurePolicy: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "failurePolicy"}, default=OMIT
    )
    matchPolicy: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "matchPolicy"}, default=OMIT
    )
    namespaceSelector: Union[None, OmitEnum, kdsl.core.v1.LabelSelector] = attr.ib(
        metadata={"yaml_name": "namespaceSelector"},
        converter=kdsl.core.v1_converters.optional_converter_LabelSelector,
        default=OMIT,
    )
    objectSelector: Union[None, OmitEnum, kdsl.core.v1.LabelSelector] = attr.ib(
        metadata={"yaml_name": "objectSelector"},
        converter=kdsl.core.v1_converters.optional_converter_LabelSelector,
        default=OMIT,
    )
    reinvocationPolicy: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "reinvocationPolicy"}, default=OMIT
    )
    rules: Union[
        None, OmitEnum, Sequence[kdsl.admissionregistration.v1.RuleWithOperations]
    ] = attr.ib(
        metadata={"yaml_name": "rules"},
        converter=kdsl.admissionregistration.v1_converters.optional_list_converter_RuleWithOperations,
        default=OMIT,
    )
    timeoutSeconds: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "timeoutSeconds"}, default=OMIT
    )


class MutatingWebhookItemOptionalTypedDict(TypedDict, total=(False)):
    failurePolicy: str
    matchPolicy: str
    namespaceSelector: kdsl.core.v1.LabelSelector
    objectSelector: kdsl.core.v1.LabelSelector
    reinvocationPolicy: str
    rules: Sequence[kdsl.admissionregistration.v1.RuleWithOperations]
    timeoutSeconds: int


class MutatingWebhookItemTypedDict(MutatingWebhookItemOptionalTypedDict, total=(True)):
    admissionReviewVersions: Sequence[str]
    clientConfig: kdsl.admissionregistration.v1.WebhookClientConfig
    sideEffects: str


MutatingWebhookItemUnion = Union[MutatingWebhookItem, MutatingWebhookItemTypedDict]


@attr.s(kw_only=True)
class MutatingWebhookConfiguration(K8sResource):
    apiVersion: ClassVar[str] = "admissionregistration.k8s.io/v1"
    kind: ClassVar[str] = "MutatingWebhookConfiguration"
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    webhooks: Union[
        None, OmitEnum, Mapping[str, kdsl.admissionregistration.v1.MutatingWebhookItem]
    ] = attr.ib(
        metadata={"yaml_name": "webhooks", "mlist_key": "name"},
        converter=kdsl.admissionregistration.v1_converters.optional_mlist_converter_MutatingWebhookItem,
        default=OMIT,
    )


@attr.s(kw_only=True)
class WebhookClientConfig(K8sObject):
    caBundle: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "caBundle"}, default=OMIT
    )
    service: Union[
        None, OmitEnum, kdsl.admissionregistration.v1.ServiceReference
    ] = attr.ib(
        metadata={"yaml_name": "service"},
        converter=kdsl.admissionregistration.v1_converters.optional_converter_ServiceReference,
        default=OMIT,
    )
    url: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "url"}, default=OMIT
    )


class WebhookClientConfigTypedDict(TypedDict, total=(False)):
    caBundle: str
    service: kdsl.admissionregistration.v1.ServiceReference
    url: str


WebhookClientConfigUnion = Union[WebhookClientConfig, WebhookClientConfigTypedDict]


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
class ValidatingWebhookItem(K8sObject):
    admissionReviewVersions: Sequence[str] = attr.ib(
        metadata={"yaml_name": "admissionReviewVersions"}
    )
    clientConfig: kdsl.admissionregistration.v1.WebhookClientConfig = attr.ib(
        metadata={"yaml_name": "clientConfig"},
        converter=kdsl.admissionregistration.v1_converters.required_converter_WebhookClientConfig,
    )
    sideEffects: str = attr.ib(metadata={"yaml_name": "sideEffects"})
    failurePolicy: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "failurePolicy"}, default=OMIT
    )
    matchPolicy: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "matchPolicy"}, default=OMIT
    )
    namespaceSelector: Union[None, OmitEnum, kdsl.core.v1.LabelSelector] = attr.ib(
        metadata={"yaml_name": "namespaceSelector"},
        converter=kdsl.core.v1_converters.optional_converter_LabelSelector,
        default=OMIT,
    )
    objectSelector: Union[None, OmitEnum, kdsl.core.v1.LabelSelector] = attr.ib(
        metadata={"yaml_name": "objectSelector"},
        converter=kdsl.core.v1_converters.optional_converter_LabelSelector,
        default=OMIT,
    )
    rules: Union[
        None, OmitEnum, Sequence[kdsl.admissionregistration.v1.RuleWithOperations]
    ] = attr.ib(
        metadata={"yaml_name": "rules"},
        converter=kdsl.admissionregistration.v1_converters.optional_list_converter_RuleWithOperations,
        default=OMIT,
    )
    timeoutSeconds: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "timeoutSeconds"}, default=OMIT
    )


class ValidatingWebhookItemOptionalTypedDict(TypedDict, total=(False)):
    failurePolicy: str
    matchPolicy: str
    namespaceSelector: kdsl.core.v1.LabelSelector
    objectSelector: kdsl.core.v1.LabelSelector
    rules: Sequence[kdsl.admissionregistration.v1.RuleWithOperations]
    timeoutSeconds: int


class ValidatingWebhookItemTypedDict(
    ValidatingWebhookItemOptionalTypedDict, total=(True)
):
    admissionReviewVersions: Sequence[str]
    clientConfig: kdsl.admissionregistration.v1.WebhookClientConfig
    sideEffects: str


ValidatingWebhookItemUnion = Union[
    ValidatingWebhookItem, ValidatingWebhookItemTypedDict
]


@attr.s(kw_only=True)
class RuleWithOperations(K8sObject):
    apiGroups: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "apiGroups"}, default=OMIT
    )
    apiVersions: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "apiVersions"}, default=OMIT
    )
    operations: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "operations"}, default=OMIT
    )
    resources: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "resources"}, default=OMIT
    )
    scope: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "scope"}, default=OMIT
    )


class RuleWithOperationsTypedDict(TypedDict, total=(False)):
    apiGroups: Sequence[str]
    apiVersions: Sequence[str]
    operations: Sequence[str]
    resources: Sequence[str]
    scope: str


RuleWithOperationsUnion = Union[RuleWithOperations, RuleWithOperationsTypedDict]
