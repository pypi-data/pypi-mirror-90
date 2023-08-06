from __future__ import annotations
from typing import Literal, Sequence, Union
from kdsl.bases import OmitEnum, OMIT
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import kdsl.networking.v1beta1


def required_converter_HTTPIngressRuleValue(
    value: kdsl.networking.v1beta1.HTTPIngressRuleValueUnion,
) -> kdsl.networking.v1beta1.HTTPIngressRuleValue:
    import kdsl.networking.v1beta1

    return (
        kdsl.networking.v1beta1.HTTPIngressRuleValue(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_IngressBackend(
    value: Union[kdsl.networking.v1beta1.IngressBackendUnion, OmitEnum, None]
) -> Union[kdsl.networking.v1beta1.IngressBackend, OmitEnum, None]:
    import kdsl.networking.v1beta1

    return (
        kdsl.networking.v1beta1.IngressBackend(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_IngressStatus(
    value: kdsl.networking.v1beta1.IngressStatusUnion,
) -> kdsl.networking.v1beta1.IngressStatus:
    import kdsl.networking.v1beta1

    return (
        kdsl.networking.v1beta1.IngressStatus(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_HTTPIngressPath(
    value: Union[kdsl.networking.v1beta1.HTTPIngressPathUnion, OmitEnum, None]
) -> Union[kdsl.networking.v1beta1.HTTPIngressPath, OmitEnum, None]:
    import kdsl.networking.v1beta1

    return (
        kdsl.networking.v1beta1.HTTPIngressPath(**value)
        if isinstance(value, dict)
        else value
    )


def optional_list_converter_IngressRule(
    value: Union[Sequence[kdsl.networking.v1beta1.IngressRuleUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.networking.v1beta1.IngressRule], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_IngressRule(x) for x in value]


def optional_converter_HTTPIngressRuleValue(
    value: Union[kdsl.networking.v1beta1.HTTPIngressRuleValueUnion, OmitEnum, None]
) -> Union[kdsl.networking.v1beta1.HTTPIngressRuleValue, OmitEnum, None]:
    import kdsl.networking.v1beta1

    return (
        kdsl.networking.v1beta1.HTTPIngressRuleValue(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_IngressBackend(
    value: kdsl.networking.v1beta1.IngressBackendUnion,
) -> kdsl.networking.v1beta1.IngressBackend:
    import kdsl.networking.v1beta1

    return (
        kdsl.networking.v1beta1.IngressBackend(**value)
        if isinstance(value, dict)
        else value
    )


def required_list_converter_HTTPIngressPath(
    value: Sequence[kdsl.networking.v1beta1.HTTPIngressPathUnion],
) -> Sequence[kdsl.networking.v1beta1.HTTPIngressPath]:
    return [required_converter_HTTPIngressPath(x) for x in value]


def required_converter_IngressSpec(
    value: kdsl.networking.v1beta1.IngressSpecUnion,
) -> kdsl.networking.v1beta1.IngressSpec:
    import kdsl.networking.v1beta1

    return (
        kdsl.networking.v1beta1.IngressSpec(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_IngressStatus(
    value: Union[kdsl.networking.v1beta1.IngressStatusUnion, OmitEnum, None]
) -> Union[kdsl.networking.v1beta1.IngressStatus, OmitEnum, None]:
    import kdsl.networking.v1beta1

    return (
        kdsl.networking.v1beta1.IngressStatus(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_IngressTLS(
    value: Union[kdsl.networking.v1beta1.IngressTLSUnion, OmitEnum, None]
) -> Union[kdsl.networking.v1beta1.IngressTLS, OmitEnum, None]:
    import kdsl.networking.v1beta1

    return (
        kdsl.networking.v1beta1.IngressTLS(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_IngressRule(
    value: kdsl.networking.v1beta1.IngressRuleUnion,
) -> kdsl.networking.v1beta1.IngressRule:
    import kdsl.networking.v1beta1

    return (
        kdsl.networking.v1beta1.IngressRule(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_IngressSpec(
    value: Union[kdsl.networking.v1beta1.IngressSpecUnion, OmitEnum, None]
) -> Union[kdsl.networking.v1beta1.IngressSpec, OmitEnum, None]:
    import kdsl.networking.v1beta1

    return (
        kdsl.networking.v1beta1.IngressSpec(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_IngressRule(
    value: Union[kdsl.networking.v1beta1.IngressRuleUnion, OmitEnum, None]
) -> Union[kdsl.networking.v1beta1.IngressRule, OmitEnum, None]:
    import kdsl.networking.v1beta1

    return (
        kdsl.networking.v1beta1.IngressRule(**value)
        if isinstance(value, dict)
        else value
    )


def optional_list_converter_IngressTLS(
    value: Union[Sequence[kdsl.networking.v1beta1.IngressTLSUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.networking.v1beta1.IngressTLS], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_IngressTLS(x) for x in value]


def required_converter_HTTPIngressPath(
    value: kdsl.networking.v1beta1.HTTPIngressPathUnion,
) -> kdsl.networking.v1beta1.HTTPIngressPath:
    import kdsl.networking.v1beta1

    return (
        kdsl.networking.v1beta1.HTTPIngressPath(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_IngressTLS(
    value: kdsl.networking.v1beta1.IngressTLSUnion,
) -> kdsl.networking.v1beta1.IngressTLS:
    import kdsl.networking.v1beta1

    return (
        kdsl.networking.v1beta1.IngressTLS(**value)
        if isinstance(value, dict)
        else value
    )
