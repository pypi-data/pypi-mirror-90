from __future__ import annotations
from typing import Literal, Union
from kdsl.bases import OmitEnum, OMIT
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import kdsl.auditregistration.v1alpha1


def required_converter_Policy(
    value: kdsl.auditregistration.v1alpha1.PolicyUnion,
) -> kdsl.auditregistration.v1alpha1.Policy:
    import kdsl.auditregistration.v1alpha1

    return (
        kdsl.auditregistration.v1alpha1.Policy(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_Policy(
    value: Union[kdsl.auditregistration.v1alpha1.PolicyUnion, OmitEnum, None]
) -> Union[kdsl.auditregistration.v1alpha1.Policy, OmitEnum, None]:
    import kdsl.auditregistration.v1alpha1

    return (
        kdsl.auditregistration.v1alpha1.Policy(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_ServiceReference(
    value: kdsl.auditregistration.v1alpha1.ServiceReferenceUnion,
) -> kdsl.auditregistration.v1alpha1.ServiceReference:
    import kdsl.auditregistration.v1alpha1

    return (
        kdsl.auditregistration.v1alpha1.ServiceReference(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_WebhookClientConfig(
    value: kdsl.auditregistration.v1alpha1.WebhookClientConfigUnion,
) -> kdsl.auditregistration.v1alpha1.WebhookClientConfig:
    import kdsl.auditregistration.v1alpha1

    return (
        kdsl.auditregistration.v1alpha1.WebhookClientConfig(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_WebhookThrottleConfig(
    value: Union[
        kdsl.auditregistration.v1alpha1.WebhookThrottleConfigUnion, OmitEnum, None
    ]
) -> Union[kdsl.auditregistration.v1alpha1.WebhookThrottleConfig, OmitEnum, None]:
    import kdsl.auditregistration.v1alpha1

    return (
        kdsl.auditregistration.v1alpha1.WebhookThrottleConfig(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_AuditSinkSpec(
    value: kdsl.auditregistration.v1alpha1.AuditSinkSpecUnion,
) -> kdsl.auditregistration.v1alpha1.AuditSinkSpec:
    import kdsl.auditregistration.v1alpha1

    return (
        kdsl.auditregistration.v1alpha1.AuditSinkSpec(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_WebhookClientConfig(
    value: Union[
        kdsl.auditregistration.v1alpha1.WebhookClientConfigUnion, OmitEnum, None
    ]
) -> Union[kdsl.auditregistration.v1alpha1.WebhookClientConfig, OmitEnum, None]:
    import kdsl.auditregistration.v1alpha1

    return (
        kdsl.auditregistration.v1alpha1.WebhookClientConfig(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_ServiceReference(
    value: Union[kdsl.auditregistration.v1alpha1.ServiceReferenceUnion, OmitEnum, None]
) -> Union[kdsl.auditregistration.v1alpha1.ServiceReference, OmitEnum, None]:
    import kdsl.auditregistration.v1alpha1

    return (
        kdsl.auditregistration.v1alpha1.ServiceReference(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_AuditSinkSpec(
    value: Union[kdsl.auditregistration.v1alpha1.AuditSinkSpecUnion, OmitEnum, None]
) -> Union[kdsl.auditregistration.v1alpha1.AuditSinkSpec, OmitEnum, None]:
    import kdsl.auditregistration.v1alpha1

    return (
        kdsl.auditregistration.v1alpha1.AuditSinkSpec(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_Webhook(
    value: kdsl.auditregistration.v1alpha1.WebhookUnion,
) -> kdsl.auditregistration.v1alpha1.Webhook:
    import kdsl.auditregistration.v1alpha1

    return (
        kdsl.auditregistration.v1alpha1.Webhook(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_Webhook(
    value: Union[kdsl.auditregistration.v1alpha1.WebhookUnion, OmitEnum, None]
) -> Union[kdsl.auditregistration.v1alpha1.Webhook, OmitEnum, None]:
    import kdsl.auditregistration.v1alpha1

    return (
        kdsl.auditregistration.v1alpha1.Webhook(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_WebhookThrottleConfig(
    value: kdsl.auditregistration.v1alpha1.WebhookThrottleConfigUnion,
) -> kdsl.auditregistration.v1alpha1.WebhookThrottleConfig:
    import kdsl.auditregistration.v1alpha1

    return (
        kdsl.auditregistration.v1alpha1.WebhookThrottleConfig(**value)
        if isinstance(value, dict)
        else value
    )
