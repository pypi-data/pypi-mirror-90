from __future__ import annotations
from typing import Literal, Sequence, Union
from kdsl.bases import OmitEnum, OMIT
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import kdsl.apiextensions.v1beta1


def optional_converter_CustomResourceDefinitionVersion(
    value: Union[
        kdsl.apiextensions.v1beta1.CustomResourceDefinitionVersionUnion, OmitEnum, None
    ]
) -> Union[kdsl.apiextensions.v1beta1.CustomResourceDefinitionVersion, OmitEnum, None]:
    import kdsl.apiextensions.v1beta1

    return (
        kdsl.apiextensions.v1beta1.CustomResourceDefinitionVersion(**value)
        if isinstance(value, dict)
        else value
    )


def optional_list_converter_CustomResourceDefinitionCondition(
    value: Union[
        Sequence[kdsl.apiextensions.v1beta1.CustomResourceDefinitionConditionUnion],
        OmitEnum,
        None,
    ]
) -> Union[
    Sequence[kdsl.apiextensions.v1beta1.CustomResourceDefinitionCondition],
    OmitEnum,
    None,
]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_CustomResourceDefinitionCondition(x) for x in value]


def required_converter_CustomResourceSubresourceScale(
    value: kdsl.apiextensions.v1beta1.CustomResourceSubresourceScaleUnion,
) -> kdsl.apiextensions.v1beta1.CustomResourceSubresourceScale:
    import kdsl.apiextensions.v1beta1

    return (
        kdsl.apiextensions.v1beta1.CustomResourceSubresourceScale(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_CustomResourceValidation(
    value: Union[
        kdsl.apiextensions.v1beta1.CustomResourceValidationUnion, OmitEnum, None
    ]
) -> Union[kdsl.apiextensions.v1beta1.CustomResourceValidation, OmitEnum, None]:
    import kdsl.apiextensions.v1beta1

    return (
        kdsl.apiextensions.v1beta1.CustomResourceValidation(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_CustomResourceDefinitionSpec(
    value: kdsl.apiextensions.v1beta1.CustomResourceDefinitionSpecUnion,
) -> kdsl.apiextensions.v1beta1.CustomResourceDefinitionSpec:
    import kdsl.apiextensions.v1beta1

    return (
        kdsl.apiextensions.v1beta1.CustomResourceDefinitionSpec(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_CustomResourceDefinitionCondition(
    value: kdsl.apiextensions.v1beta1.CustomResourceDefinitionConditionUnion,
) -> kdsl.apiextensions.v1beta1.CustomResourceDefinitionCondition:
    import kdsl.apiextensions.v1beta1

    return (
        kdsl.apiextensions.v1beta1.CustomResourceDefinitionCondition(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_CustomResourceConversion(
    value: kdsl.apiextensions.v1beta1.CustomResourceConversionUnion,
) -> kdsl.apiextensions.v1beta1.CustomResourceConversion:
    import kdsl.apiextensions.v1beta1

    return (
        kdsl.apiextensions.v1beta1.CustomResourceConversion(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_CustomResourceColumnDefinition(
    value: Union[
        kdsl.apiextensions.v1beta1.CustomResourceColumnDefinitionUnion, OmitEnum, None
    ]
) -> Union[kdsl.apiextensions.v1beta1.CustomResourceColumnDefinition, OmitEnum, None]:
    import kdsl.apiextensions.v1beta1

    return (
        kdsl.apiextensions.v1beta1.CustomResourceColumnDefinition(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_CustomResourceSubresources(
    value: kdsl.apiextensions.v1beta1.CustomResourceSubresourcesUnion,
) -> kdsl.apiextensions.v1beta1.CustomResourceSubresources:
    import kdsl.apiextensions.v1beta1

    return (
        kdsl.apiextensions.v1beta1.CustomResourceSubresources(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_CustomResourceDefinitionStatus(
    value: kdsl.apiextensions.v1beta1.CustomResourceDefinitionStatusUnion,
) -> kdsl.apiextensions.v1beta1.CustomResourceDefinitionStatus:
    import kdsl.apiextensions.v1beta1

    return (
        kdsl.apiextensions.v1beta1.CustomResourceDefinitionStatus(**value)
        if isinstance(value, dict)
        else value
    )


def optional_list_converter_CustomResourceDefinitionVersion(
    value: Union[
        Sequence[kdsl.apiextensions.v1beta1.CustomResourceDefinitionVersionUnion],
        OmitEnum,
        None,
    ]
) -> Union[
    Sequence[kdsl.apiextensions.v1beta1.CustomResourceDefinitionVersion], OmitEnum, None
]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_CustomResourceDefinitionVersion(x) for x in value]


def optional_converter_CustomResourceSubresourceScale(
    value: Union[
        kdsl.apiextensions.v1beta1.CustomResourceSubresourceScaleUnion, OmitEnum, None
    ]
) -> Union[kdsl.apiextensions.v1beta1.CustomResourceSubresourceScale, OmitEnum, None]:
    import kdsl.apiextensions.v1beta1

    return (
        kdsl.apiextensions.v1beta1.CustomResourceSubresourceScale(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_ServiceReference(
    value: kdsl.apiextensions.v1beta1.ServiceReferenceUnion,
) -> kdsl.apiextensions.v1beta1.ServiceReference:
    import kdsl.apiextensions.v1beta1

    return (
        kdsl.apiextensions.v1beta1.ServiceReference(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_CustomResourceDefinitionSpec(
    value: Union[
        kdsl.apiextensions.v1beta1.CustomResourceDefinitionSpecUnion, OmitEnum, None
    ]
) -> Union[kdsl.apiextensions.v1beta1.CustomResourceDefinitionSpec, OmitEnum, None]:
    import kdsl.apiextensions.v1beta1

    return (
        kdsl.apiextensions.v1beta1.CustomResourceDefinitionSpec(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_CustomResourceDefinitionCondition(
    value: Union[
        kdsl.apiextensions.v1beta1.CustomResourceDefinitionConditionUnion,
        OmitEnum,
        None,
    ]
) -> Union[
    kdsl.apiextensions.v1beta1.CustomResourceDefinitionCondition, OmitEnum, None
]:
    import kdsl.apiextensions.v1beta1

    return (
        kdsl.apiextensions.v1beta1.CustomResourceDefinitionCondition(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_WebhookClientConfig(
    value: kdsl.apiextensions.v1beta1.WebhookClientConfigUnion,
) -> kdsl.apiextensions.v1beta1.WebhookClientConfig:
    import kdsl.apiextensions.v1beta1

    return (
        kdsl.apiextensions.v1beta1.WebhookClientConfig(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_CustomResourceConversion(
    value: Union[
        kdsl.apiextensions.v1beta1.CustomResourceConversionUnion, OmitEnum, None
    ]
) -> Union[kdsl.apiextensions.v1beta1.CustomResourceConversion, OmitEnum, None]:
    import kdsl.apiextensions.v1beta1

    return (
        kdsl.apiextensions.v1beta1.CustomResourceConversion(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_CustomResourceDefinitionNames(
    value: kdsl.apiextensions.v1beta1.CustomResourceDefinitionNamesUnion,
) -> kdsl.apiextensions.v1beta1.CustomResourceDefinitionNames:
    import kdsl.apiextensions.v1beta1

    return (
        kdsl.apiextensions.v1beta1.CustomResourceDefinitionNames(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_CustomResourceDefinitionVersion(
    value: kdsl.apiextensions.v1beta1.CustomResourceDefinitionVersionUnion,
) -> kdsl.apiextensions.v1beta1.CustomResourceDefinitionVersion:
    import kdsl.apiextensions.v1beta1

    return (
        kdsl.apiextensions.v1beta1.CustomResourceDefinitionVersion(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_CustomResourceSubresources(
    value: Union[
        kdsl.apiextensions.v1beta1.CustomResourceSubresourcesUnion, OmitEnum, None
    ]
) -> Union[kdsl.apiextensions.v1beta1.CustomResourceSubresources, OmitEnum, None]:
    import kdsl.apiextensions.v1beta1

    return (
        kdsl.apiextensions.v1beta1.CustomResourceSubresources(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_ServiceReference(
    value: Union[kdsl.apiextensions.v1beta1.ServiceReferenceUnion, OmitEnum, None]
) -> Union[kdsl.apiextensions.v1beta1.ServiceReference, OmitEnum, None]:
    import kdsl.apiextensions.v1beta1

    return (
        kdsl.apiextensions.v1beta1.ServiceReference(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_CustomResourceDefinitionStatus(
    value: Union[
        kdsl.apiextensions.v1beta1.CustomResourceDefinitionStatusUnion, OmitEnum, None
    ]
) -> Union[kdsl.apiextensions.v1beta1.CustomResourceDefinitionStatus, OmitEnum, None]:
    import kdsl.apiextensions.v1beta1

    return (
        kdsl.apiextensions.v1beta1.CustomResourceDefinitionStatus(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_CustomResourceValidation(
    value: kdsl.apiextensions.v1beta1.CustomResourceValidationUnion,
) -> kdsl.apiextensions.v1beta1.CustomResourceValidation:
    import kdsl.apiextensions.v1beta1

    return (
        kdsl.apiextensions.v1beta1.CustomResourceValidation(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_WebhookClientConfig(
    value: Union[kdsl.apiextensions.v1beta1.WebhookClientConfigUnion, OmitEnum, None]
) -> Union[kdsl.apiextensions.v1beta1.WebhookClientConfig, OmitEnum, None]:
    import kdsl.apiextensions.v1beta1

    return (
        kdsl.apiextensions.v1beta1.WebhookClientConfig(**value)
        if isinstance(value, dict)
        else value
    )


def optional_list_converter_CustomResourceColumnDefinition(
    value: Union[
        Sequence[kdsl.apiextensions.v1beta1.CustomResourceColumnDefinitionUnion],
        OmitEnum,
        None,
    ]
) -> Union[
    Sequence[kdsl.apiextensions.v1beta1.CustomResourceColumnDefinition], OmitEnum, None
]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_CustomResourceColumnDefinition(x) for x in value]


def optional_converter_CustomResourceDefinitionNames(
    value: Union[
        kdsl.apiextensions.v1beta1.CustomResourceDefinitionNamesUnion, OmitEnum, None
    ]
) -> Union[kdsl.apiextensions.v1beta1.CustomResourceDefinitionNames, OmitEnum, None]:
    import kdsl.apiextensions.v1beta1

    return (
        kdsl.apiextensions.v1beta1.CustomResourceDefinitionNames(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_CustomResourceColumnDefinition(
    value: kdsl.apiextensions.v1beta1.CustomResourceColumnDefinitionUnion,
) -> kdsl.apiextensions.v1beta1.CustomResourceColumnDefinition:
    import kdsl.apiextensions.v1beta1

    return (
        kdsl.apiextensions.v1beta1.CustomResourceColumnDefinition(**value)
        if isinstance(value, dict)
        else value
    )
