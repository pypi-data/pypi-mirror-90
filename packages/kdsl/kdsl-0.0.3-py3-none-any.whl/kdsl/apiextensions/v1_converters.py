from __future__ import annotations
from typing import Literal, Sequence, Union
from kdsl.bases import OmitEnum, OMIT
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import kdsl.apiextensions.v1


def optional_list_converter_CustomResourceDefinitionCondition(
    value: Union[
        Sequence[kdsl.apiextensions.v1.CustomResourceDefinitionConditionUnion],
        OmitEnum,
        None,
    ]
) -> Union[
    Sequence[kdsl.apiextensions.v1.CustomResourceDefinitionCondition], OmitEnum, None
]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_CustomResourceDefinitionCondition(x) for x in value]


def required_list_converter_CustomResourceDefinitionVersion(
    value: Sequence[kdsl.apiextensions.v1.CustomResourceDefinitionVersionUnion],
) -> Sequence[kdsl.apiextensions.v1.CustomResourceDefinitionVersion]:
    return [required_converter_CustomResourceDefinitionVersion(x) for x in value]


def required_converter_CustomResourceDefinitionStatus(
    value: kdsl.apiextensions.v1.CustomResourceDefinitionStatusUnion,
) -> kdsl.apiextensions.v1.CustomResourceDefinitionStatus:
    import kdsl.apiextensions.v1

    return (
        kdsl.apiextensions.v1.CustomResourceDefinitionStatus(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_CustomResourceDefinitionNames(
    value: Union[
        kdsl.apiextensions.v1.CustomResourceDefinitionNamesUnion, OmitEnum, None
    ]
) -> Union[kdsl.apiextensions.v1.CustomResourceDefinitionNames, OmitEnum, None]:
    import kdsl.apiextensions.v1

    return (
        kdsl.apiextensions.v1.CustomResourceDefinitionNames(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_CustomResourceDefinitionCondition(
    value: kdsl.apiextensions.v1.CustomResourceDefinitionConditionUnion,
) -> kdsl.apiextensions.v1.CustomResourceDefinitionCondition:
    import kdsl.apiextensions.v1

    return (
        kdsl.apiextensions.v1.CustomResourceDefinitionCondition(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_CustomResourceColumnDefinition(
    value: Union[
        kdsl.apiextensions.v1.CustomResourceColumnDefinitionUnion, OmitEnum, None
    ]
) -> Union[kdsl.apiextensions.v1.CustomResourceColumnDefinition, OmitEnum, None]:
    import kdsl.apiextensions.v1

    return (
        kdsl.apiextensions.v1.CustomResourceColumnDefinition(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_CustomResourceSubresources(
    value: Union[kdsl.apiextensions.v1.CustomResourceSubresourcesUnion, OmitEnum, None]
) -> Union[kdsl.apiextensions.v1.CustomResourceSubresources, OmitEnum, None]:
    import kdsl.apiextensions.v1

    return (
        kdsl.apiextensions.v1.CustomResourceSubresources(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_CustomResourceSubresourceScale(
    value: Union[
        kdsl.apiextensions.v1.CustomResourceSubresourceScaleUnion, OmitEnum, None
    ]
) -> Union[kdsl.apiextensions.v1.CustomResourceSubresourceScale, OmitEnum, None]:
    import kdsl.apiextensions.v1

    return (
        kdsl.apiextensions.v1.CustomResourceSubresourceScale(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_CustomResourceConversion(
    value: Union[kdsl.apiextensions.v1.CustomResourceConversionUnion, OmitEnum, None]
) -> Union[kdsl.apiextensions.v1.CustomResourceConversion, OmitEnum, None]:
    import kdsl.apiextensions.v1

    return (
        kdsl.apiextensions.v1.CustomResourceConversion(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_CustomResourceDefinitionSpec(
    value: Union[
        kdsl.apiextensions.v1.CustomResourceDefinitionSpecUnion, OmitEnum, None
    ]
) -> Union[kdsl.apiextensions.v1.CustomResourceDefinitionSpec, OmitEnum, None]:
    import kdsl.apiextensions.v1

    return (
        kdsl.apiextensions.v1.CustomResourceDefinitionSpec(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_CustomResourceDefinitionStatus(
    value: Union[
        kdsl.apiextensions.v1.CustomResourceDefinitionStatusUnion, OmitEnum, None
    ]
) -> Union[kdsl.apiextensions.v1.CustomResourceDefinitionStatus, OmitEnum, None]:
    import kdsl.apiextensions.v1

    return (
        kdsl.apiextensions.v1.CustomResourceDefinitionStatus(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_CustomResourceDefinitionCondition(
    value: Union[
        kdsl.apiextensions.v1.CustomResourceDefinitionConditionUnion, OmitEnum, None
    ]
) -> Union[kdsl.apiextensions.v1.CustomResourceDefinitionCondition, OmitEnum, None]:
    import kdsl.apiextensions.v1

    return (
        kdsl.apiextensions.v1.CustomResourceDefinitionCondition(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_CustomResourceDefinitionVersion(
    value: kdsl.apiextensions.v1.CustomResourceDefinitionVersionUnion,
) -> kdsl.apiextensions.v1.CustomResourceDefinitionVersion:
    import kdsl.apiextensions.v1

    return (
        kdsl.apiextensions.v1.CustomResourceDefinitionVersion(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_WebhookClientConfig(
    value: kdsl.apiextensions.v1.WebhookClientConfigUnion,
) -> kdsl.apiextensions.v1.WebhookClientConfig:
    import kdsl.apiextensions.v1

    return (
        kdsl.apiextensions.v1.WebhookClientConfig(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_ServiceReference(
    value: kdsl.apiextensions.v1.ServiceReferenceUnion,
) -> kdsl.apiextensions.v1.ServiceReference:
    import kdsl.apiextensions.v1

    return (
        kdsl.apiextensions.v1.ServiceReference(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_CustomResourceValidation(
    value: kdsl.apiextensions.v1.CustomResourceValidationUnion,
) -> kdsl.apiextensions.v1.CustomResourceValidation:
    import kdsl.apiextensions.v1

    return (
        kdsl.apiextensions.v1.CustomResourceValidation(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_WebhookConversion(
    value: kdsl.apiextensions.v1.WebhookConversionUnion,
) -> kdsl.apiextensions.v1.WebhookConversion:
    import kdsl.apiextensions.v1

    return (
        kdsl.apiextensions.v1.WebhookConversion(**value)
        if isinstance(value, dict)
        else value
    )


def optional_list_converter_CustomResourceColumnDefinition(
    value: Union[
        Sequence[kdsl.apiextensions.v1.CustomResourceColumnDefinitionUnion],
        OmitEnum,
        None,
    ]
) -> Union[
    Sequence[kdsl.apiextensions.v1.CustomResourceColumnDefinition], OmitEnum, None
]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_CustomResourceColumnDefinition(x) for x in value]


def required_converter_CustomResourceColumnDefinition(
    value: kdsl.apiextensions.v1.CustomResourceColumnDefinitionUnion,
) -> kdsl.apiextensions.v1.CustomResourceColumnDefinition:
    import kdsl.apiextensions.v1

    return (
        kdsl.apiextensions.v1.CustomResourceColumnDefinition(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_CustomResourceDefinitionVersion(
    value: Union[
        kdsl.apiextensions.v1.CustomResourceDefinitionVersionUnion, OmitEnum, None
    ]
) -> Union[kdsl.apiextensions.v1.CustomResourceDefinitionVersion, OmitEnum, None]:
    import kdsl.apiextensions.v1

    return (
        kdsl.apiextensions.v1.CustomResourceDefinitionVersion(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_CustomResourceSubresourceScale(
    value: kdsl.apiextensions.v1.CustomResourceSubresourceScaleUnion,
) -> kdsl.apiextensions.v1.CustomResourceSubresourceScale:
    import kdsl.apiextensions.v1

    return (
        kdsl.apiextensions.v1.CustomResourceSubresourceScale(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_WebhookClientConfig(
    value: Union[kdsl.apiextensions.v1.WebhookClientConfigUnion, OmitEnum, None]
) -> Union[kdsl.apiextensions.v1.WebhookClientConfig, OmitEnum, None]:
    import kdsl.apiextensions.v1

    return (
        kdsl.apiextensions.v1.WebhookClientConfig(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_CustomResourceDefinitionNames(
    value: kdsl.apiextensions.v1.CustomResourceDefinitionNamesUnion,
) -> kdsl.apiextensions.v1.CustomResourceDefinitionNames:
    import kdsl.apiextensions.v1

    return (
        kdsl.apiextensions.v1.CustomResourceDefinitionNames(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_CustomResourceSubresources(
    value: kdsl.apiextensions.v1.CustomResourceSubresourcesUnion,
) -> kdsl.apiextensions.v1.CustomResourceSubresources:
    import kdsl.apiextensions.v1

    return (
        kdsl.apiextensions.v1.CustomResourceSubresources(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_CustomResourceConversion(
    value: kdsl.apiextensions.v1.CustomResourceConversionUnion,
) -> kdsl.apiextensions.v1.CustomResourceConversion:
    import kdsl.apiextensions.v1

    return (
        kdsl.apiextensions.v1.CustomResourceConversion(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_ServiceReference(
    value: Union[kdsl.apiextensions.v1.ServiceReferenceUnion, OmitEnum, None]
) -> Union[kdsl.apiextensions.v1.ServiceReference, OmitEnum, None]:
    import kdsl.apiextensions.v1

    return (
        kdsl.apiextensions.v1.ServiceReference(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_CustomResourceValidation(
    value: Union[kdsl.apiextensions.v1.CustomResourceValidationUnion, OmitEnum, None]
) -> Union[kdsl.apiextensions.v1.CustomResourceValidation, OmitEnum, None]:
    import kdsl.apiextensions.v1

    return (
        kdsl.apiextensions.v1.CustomResourceValidation(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_CustomResourceDefinitionSpec(
    value: kdsl.apiextensions.v1.CustomResourceDefinitionSpecUnion,
) -> kdsl.apiextensions.v1.CustomResourceDefinitionSpec:
    import kdsl.apiextensions.v1

    return (
        kdsl.apiextensions.v1.CustomResourceDefinitionSpec(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_WebhookConversion(
    value: Union[kdsl.apiextensions.v1.WebhookConversionUnion, OmitEnum, None]
) -> Union[kdsl.apiextensions.v1.WebhookConversion, OmitEnum, None]:
    import kdsl.apiextensions.v1

    return (
        kdsl.apiextensions.v1.WebhookConversion(**value)
        if isinstance(value, dict)
        else value
    )
