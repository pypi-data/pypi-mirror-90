from __future__ import annotations
import kdsl.core.v1
import kdsl.apiextensions.v1
import kdsl.core.v1_converters
import kdsl.apiextensions.v1_converters
import attr
from typing import Mapping, ClassVar, Optional, Any, Sequence, TypedDict, Union
from kdsl.bases import OmitEnum, K8sObject, OMIT, K8sResource


@attr.s(kw_only=True)
class CustomResourceColumnDefinition(K8sObject):
    jsonPath: str = attr.ib(metadata={"yaml_name": "jsonPath"})
    name: str = attr.ib(metadata={"yaml_name": "name"})
    type: str = attr.ib(metadata={"yaml_name": "type"})
    description: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "description"}, default=OMIT
    )
    format: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "format"}, default=OMIT
    )
    priority: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "priority"}, default=OMIT
    )


class CustomResourceColumnDefinitionOptionalTypedDict(TypedDict, total=(False)):
    description: str
    format: str
    priority: int


class CustomResourceColumnDefinitionTypedDict(
    CustomResourceColumnDefinitionOptionalTypedDict, total=(True)
):
    jsonPath: str
    name: str
    type: str


CustomResourceColumnDefinitionUnion = Union[
    CustomResourceColumnDefinition, CustomResourceColumnDefinitionTypedDict
]


@attr.s(kw_only=True)
class WebhookConversion(K8sObject):
    conversionReviewVersions: Sequence[str] = attr.ib(
        metadata={"yaml_name": "conversionReviewVersions"}
    )
    clientConfig: Union[
        None, OmitEnum, kdsl.apiextensions.v1.WebhookClientConfig
    ] = attr.ib(
        metadata={"yaml_name": "clientConfig"},
        converter=kdsl.apiextensions.v1_converters.optional_converter_WebhookClientConfig,
        default=OMIT,
    )


class WebhookConversionOptionalTypedDict(TypedDict, total=(False)):
    clientConfig: kdsl.apiextensions.v1.WebhookClientConfig


class WebhookConversionTypedDict(WebhookConversionOptionalTypedDict, total=(True)):
    conversionReviewVersions: Sequence[str]


WebhookConversionUnion = Union[WebhookConversion, WebhookConversionTypedDict]


@attr.s(kw_only=True)
class CustomResourceDefinitionNames(K8sObject):
    kind: str = attr.ib(metadata={"yaml_name": "kind"})
    plural: str = attr.ib(metadata={"yaml_name": "plural"})
    categories: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "categories"}, default=OMIT
    )
    listKind: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "listKind"}, default=OMIT
    )
    shortNames: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "shortNames"}, default=OMIT
    )
    singular: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "singular"}, default=OMIT
    )


class CustomResourceDefinitionNamesOptionalTypedDict(TypedDict, total=(False)):
    categories: Sequence[str]
    listKind: str
    shortNames: Sequence[str]
    singular: str


class CustomResourceDefinitionNamesTypedDict(
    CustomResourceDefinitionNamesOptionalTypedDict, total=(True)
):
    kind: str
    plural: str


CustomResourceDefinitionNamesUnion = Union[
    CustomResourceDefinitionNames, CustomResourceDefinitionNamesTypedDict
]


@attr.s(kw_only=True)
class CustomResourceValidation(K8sObject):
    openAPIV3Schema: Union[None, OmitEnum, Any] = attr.ib(
        metadata={"yaml_name": "openAPIV3Schema"}, default=OMIT
    )


class CustomResourceValidationTypedDict(TypedDict, total=(False)):
    openAPIV3Schema: Any


CustomResourceValidationUnion = Union[
    CustomResourceValidation, CustomResourceValidationTypedDict
]


@attr.s(kw_only=True)
class CustomResourceSubresources(K8sObject):
    scale: Union[
        None, OmitEnum, kdsl.apiextensions.v1.CustomResourceSubresourceScale
    ] = attr.ib(
        metadata={"yaml_name": "scale"},
        converter=kdsl.apiextensions.v1_converters.optional_converter_CustomResourceSubresourceScale,
        default=OMIT,
    )
    status: Union[None, OmitEnum, Mapping[str, Any]] = attr.ib(
        metadata={"yaml_name": "status"}, default=OMIT
    )


class CustomResourceSubresourcesTypedDict(TypedDict, total=(False)):
    scale: kdsl.apiextensions.v1.CustomResourceSubresourceScale
    status: Mapping[str, Any]


CustomResourceSubresourcesUnion = Union[
    CustomResourceSubresources, CustomResourceSubresourcesTypedDict
]


@attr.s(kw_only=True)
class CustomResourceDefinitionVersion(K8sObject):
    name: str = attr.ib(metadata={"yaml_name": "name"})
    served: bool = attr.ib(metadata={"yaml_name": "served"})
    storage: bool = attr.ib(metadata={"yaml_name": "storage"})
    additionalPrinterColumns: Union[
        None, OmitEnum, Sequence[kdsl.apiextensions.v1.CustomResourceColumnDefinition]
    ] = attr.ib(
        metadata={"yaml_name": "additionalPrinterColumns"},
        converter=kdsl.apiextensions.v1_converters.optional_list_converter_CustomResourceColumnDefinition,
        default=OMIT,
    )
    schema: Union[
        None, OmitEnum, kdsl.apiextensions.v1.CustomResourceValidation
    ] = attr.ib(
        metadata={"yaml_name": "schema"},
        converter=kdsl.apiextensions.v1_converters.optional_converter_CustomResourceValidation,
        default=OMIT,
    )
    subresources: Union[
        None, OmitEnum, kdsl.apiextensions.v1.CustomResourceSubresources
    ] = attr.ib(
        metadata={"yaml_name": "subresources"},
        converter=kdsl.apiextensions.v1_converters.optional_converter_CustomResourceSubresources,
        default=OMIT,
    )


class CustomResourceDefinitionVersionOptionalTypedDict(TypedDict, total=(False)):
    additionalPrinterColumns: Sequence[
        kdsl.apiextensions.v1.CustomResourceColumnDefinition
    ]
    schema: kdsl.apiextensions.v1.CustomResourceValidation
    subresources: kdsl.apiextensions.v1.CustomResourceSubresources


class CustomResourceDefinitionVersionTypedDict(
    CustomResourceDefinitionVersionOptionalTypedDict, total=(True)
):
    name: str
    served: bool
    storage: bool


CustomResourceDefinitionVersionUnion = Union[
    CustomResourceDefinitionVersion, CustomResourceDefinitionVersionTypedDict
]


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
class CustomResourceDefinitionSpec(K8sObject):
    group: str = attr.ib(metadata={"yaml_name": "group"})
    names: kdsl.apiextensions.v1.CustomResourceDefinitionNames = attr.ib(
        metadata={"yaml_name": "names"},
        converter=kdsl.apiextensions.v1_converters.required_converter_CustomResourceDefinitionNames,
    )
    scope: str = attr.ib(metadata={"yaml_name": "scope"})
    versions: Sequence[kdsl.apiextensions.v1.CustomResourceDefinitionVersion] = attr.ib(
        metadata={"yaml_name": "versions"},
        converter=kdsl.apiextensions.v1_converters.required_list_converter_CustomResourceDefinitionVersion,
    )
    conversion: Union[
        None, OmitEnum, kdsl.apiextensions.v1.CustomResourceConversion
    ] = attr.ib(
        metadata={"yaml_name": "conversion"},
        converter=kdsl.apiextensions.v1_converters.optional_converter_CustomResourceConversion,
        default=OMIT,
    )
    preserveUnknownFields: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "preserveUnknownFields"}, default=OMIT
    )


class CustomResourceDefinitionSpecOptionalTypedDict(TypedDict, total=(False)):
    conversion: kdsl.apiextensions.v1.CustomResourceConversion
    preserveUnknownFields: bool


class CustomResourceDefinitionSpecTypedDict(
    CustomResourceDefinitionSpecOptionalTypedDict, total=(True)
):
    group: str
    names: kdsl.apiextensions.v1.CustomResourceDefinitionNames
    scope: str
    versions: Sequence[kdsl.apiextensions.v1.CustomResourceDefinitionVersion]


CustomResourceDefinitionSpecUnion = Union[
    CustomResourceDefinitionSpec, CustomResourceDefinitionSpecTypedDict
]


@attr.s(kw_only=True)
class CustomResourceSubresourceScale(K8sObject):
    specReplicasPath: str = attr.ib(metadata={"yaml_name": "specReplicasPath"})
    statusReplicasPath: str = attr.ib(metadata={"yaml_name": "statusReplicasPath"})
    labelSelectorPath: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "labelSelectorPath"}, default=OMIT
    )


class CustomResourceSubresourceScaleOptionalTypedDict(TypedDict, total=(False)):
    labelSelectorPath: str


class CustomResourceSubresourceScaleTypedDict(
    CustomResourceSubresourceScaleOptionalTypedDict, total=(True)
):
    specReplicasPath: str
    statusReplicasPath: str


CustomResourceSubresourceScaleUnion = Union[
    CustomResourceSubresourceScale, CustomResourceSubresourceScaleTypedDict
]


@attr.s(kw_only=True)
class CustomResourceConversion(K8sObject):
    strategy: str = attr.ib(metadata={"yaml_name": "strategy"})
    webhook: Union[None, OmitEnum, kdsl.apiextensions.v1.WebhookConversion] = attr.ib(
        metadata={"yaml_name": "webhook"},
        converter=kdsl.apiextensions.v1_converters.optional_converter_WebhookConversion,
        default=OMIT,
    )


class CustomResourceConversionOptionalTypedDict(TypedDict, total=(False)):
    webhook: kdsl.apiextensions.v1.WebhookConversion


class CustomResourceConversionTypedDict(
    CustomResourceConversionOptionalTypedDict, total=(True)
):
    strategy: str


CustomResourceConversionUnion = Union[
    CustomResourceConversion, CustomResourceConversionTypedDict
]


@attr.s(kw_only=True)
class CustomResourceDefinition(K8sResource):
    apiVersion: ClassVar[str] = "apiextensions.k8s.io/v1"
    kind: ClassVar[str] = "CustomResourceDefinition"
    spec: kdsl.apiextensions.v1.CustomResourceDefinitionSpec = attr.ib(
        metadata={"yaml_name": "spec"},
        converter=kdsl.apiextensions.v1_converters.required_converter_CustomResourceDefinitionSpec,
    )
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    status: Union[
        None, OmitEnum, kdsl.apiextensions.v1.CustomResourceDefinitionStatus
    ] = attr.ib(
        metadata={"yaml_name": "status"},
        converter=kdsl.apiextensions.v1_converters.optional_converter_CustomResourceDefinitionStatus,
        default=OMIT,
    )


@attr.s(kw_only=True)
class WebhookClientConfig(K8sObject):
    caBundle: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "caBundle"}, default=OMIT
    )
    service: Union[None, OmitEnum, kdsl.apiextensions.v1.ServiceReference] = attr.ib(
        metadata={"yaml_name": "service"},
        converter=kdsl.apiextensions.v1_converters.optional_converter_ServiceReference,
        default=OMIT,
    )
    url: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "url"}, default=OMIT
    )


class WebhookClientConfigTypedDict(TypedDict, total=(False)):
    caBundle: str
    service: kdsl.apiextensions.v1.ServiceReference
    url: str


WebhookClientConfigUnion = Union[WebhookClientConfig, WebhookClientConfigTypedDict]


@attr.s(kw_only=True)
class CustomResourceDefinitionCondition(K8sObject):
    status: str = attr.ib(metadata={"yaml_name": "status"})
    type: str = attr.ib(metadata={"yaml_name": "type"})
    lastTransitionTime: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "lastTransitionTime"}, default=OMIT
    )
    message: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "message"}, default=OMIT
    )
    reason: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "reason"}, default=OMIT
    )


class CustomResourceDefinitionConditionOptionalTypedDict(TypedDict, total=(False)):
    lastTransitionTime: str
    message: str
    reason: str


class CustomResourceDefinitionConditionTypedDict(
    CustomResourceDefinitionConditionOptionalTypedDict, total=(True)
):
    status: str
    type: str


CustomResourceDefinitionConditionUnion = Union[
    CustomResourceDefinitionCondition, CustomResourceDefinitionConditionTypedDict
]


@attr.s(kw_only=True)
class CustomResourceDefinitionStatus(K8sObject):
    acceptedNames: kdsl.apiextensions.v1.CustomResourceDefinitionNames = attr.ib(
        metadata={"yaml_name": "acceptedNames"},
        converter=kdsl.apiextensions.v1_converters.required_converter_CustomResourceDefinitionNames,
    )
    storedVersions: Sequence[str] = attr.ib(metadata={"yaml_name": "storedVersions"})
    conditions: Union[
        None,
        OmitEnum,
        Sequence[kdsl.apiextensions.v1.CustomResourceDefinitionCondition],
    ] = attr.ib(
        metadata={"yaml_name": "conditions"},
        converter=kdsl.apiextensions.v1_converters.optional_list_converter_CustomResourceDefinitionCondition,
        default=OMIT,
    )


class CustomResourceDefinitionStatusOptionalTypedDict(TypedDict, total=(False)):
    conditions: Sequence[kdsl.apiextensions.v1.CustomResourceDefinitionCondition]


class CustomResourceDefinitionStatusTypedDict(
    CustomResourceDefinitionStatusOptionalTypedDict, total=(True)
):
    acceptedNames: kdsl.apiextensions.v1.CustomResourceDefinitionNames
    storedVersions: Sequence[str]


CustomResourceDefinitionStatusUnion = Union[
    CustomResourceDefinitionStatus, CustomResourceDefinitionStatusTypedDict
]
