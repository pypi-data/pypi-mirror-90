from __future__ import annotations
from typing import Mapping, Sequence, Literal, Union
from kdsl.bases import OmitEnum, OMIT
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import kdsl.admissionregistration.v1


def optional_converter_ServiceReference(
    value: Union[kdsl.admissionregistration.v1.ServiceReferenceUnion, OmitEnum, None]
) -> Union[kdsl.admissionregistration.v1.ServiceReference, OmitEnum, None]:
    import kdsl.admissionregistration.v1

    return (
        kdsl.admissionregistration.v1.ServiceReference(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_MutatingWebhookItem(
    value: kdsl.admissionregistration.v1.MutatingWebhookItemUnion,
) -> kdsl.admissionregistration.v1.MutatingWebhookItem:
    import kdsl.admissionregistration.v1

    return (
        kdsl.admissionregistration.v1.MutatingWebhookItem(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_ValidatingWebhookItem(
    value: kdsl.admissionregistration.v1.ValidatingWebhookItemUnion,
) -> kdsl.admissionregistration.v1.ValidatingWebhookItem:
    import kdsl.admissionregistration.v1

    return (
        kdsl.admissionregistration.v1.ValidatingWebhookItem(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_RuleWithOperations(
    value: kdsl.admissionregistration.v1.RuleWithOperationsUnion,
) -> kdsl.admissionregistration.v1.RuleWithOperations:
    import kdsl.admissionregistration.v1

    return (
        kdsl.admissionregistration.v1.RuleWithOperations(**value)
        if isinstance(value, dict)
        else value
    )


def optional_mlist_converter_ValidatingWebhookItem(
    value: Union[
        Mapping[str, kdsl.admissionregistration.v1.ValidatingWebhookItemUnion],
        OmitEnum,
        None,
    ]
) -> Union[
    Mapping[str, kdsl.admissionregistration.v1.ValidatingWebhookItem], OmitEnum, None
]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {
            k: required_converter_ValidatingWebhookItem(v) for k, v in value.items()
        }


def optional_mlist_converter_MutatingWebhookItem(
    value: Union[
        Mapping[str, kdsl.admissionregistration.v1.MutatingWebhookItemUnion],
        OmitEnum,
        None,
    ]
) -> Union[
    Mapping[str, kdsl.admissionregistration.v1.MutatingWebhookItem], OmitEnum, None
]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {k: required_converter_MutatingWebhookItem(v) for k, v in value.items()}


def optional_converter_RuleWithOperations(
    value: Union[kdsl.admissionregistration.v1.RuleWithOperationsUnion, OmitEnum, None]
) -> Union[kdsl.admissionregistration.v1.RuleWithOperations, OmitEnum, None]:
    import kdsl.admissionregistration.v1

    return (
        kdsl.admissionregistration.v1.RuleWithOperations(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_ServiceReference(
    value: kdsl.admissionregistration.v1.ServiceReferenceUnion,
) -> kdsl.admissionregistration.v1.ServiceReference:
    import kdsl.admissionregistration.v1

    return (
        kdsl.admissionregistration.v1.ServiceReference(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_WebhookClientConfig(
    value: kdsl.admissionregistration.v1.WebhookClientConfigUnion,
) -> kdsl.admissionregistration.v1.WebhookClientConfig:
    import kdsl.admissionregistration.v1

    return (
        kdsl.admissionregistration.v1.WebhookClientConfig(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_MutatingWebhookItem(
    value: Union[kdsl.admissionregistration.v1.MutatingWebhookItemUnion, OmitEnum, None]
) -> Union[kdsl.admissionregistration.v1.MutatingWebhookItem, OmitEnum, None]:
    import kdsl.admissionregistration.v1

    return (
        kdsl.admissionregistration.v1.MutatingWebhookItem(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_ValidatingWebhookItem(
    value: Union[
        kdsl.admissionregistration.v1.ValidatingWebhookItemUnion, OmitEnum, None
    ]
) -> Union[kdsl.admissionregistration.v1.ValidatingWebhookItem, OmitEnum, None]:
    import kdsl.admissionregistration.v1

    return (
        kdsl.admissionregistration.v1.ValidatingWebhookItem(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_WebhookClientConfig(
    value: Union[kdsl.admissionregistration.v1.WebhookClientConfigUnion, OmitEnum, None]
) -> Union[kdsl.admissionregistration.v1.WebhookClientConfig, OmitEnum, None]:
    import kdsl.admissionregistration.v1

    return (
        kdsl.admissionregistration.v1.WebhookClientConfig(**value)
        if isinstance(value, dict)
        else value
    )


def optional_list_converter_RuleWithOperations(
    value: Union[
        Sequence[kdsl.admissionregistration.v1.RuleWithOperationsUnion], OmitEnum, None
    ]
) -> Union[Sequence[kdsl.admissionregistration.v1.RuleWithOperations], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_RuleWithOperations(x) for x in value]
