from __future__ import annotations
from typing import Literal, Sequence, Union
from kdsl.bases import OmitEnum, OMIT
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import kdsl.networking.v1


def optional_converter_NetworkPolicyIngressRule(
    value: Union[kdsl.networking.v1.NetworkPolicyIngressRuleUnion, OmitEnum, None]
) -> Union[kdsl.networking.v1.NetworkPolicyIngressRule, OmitEnum, None]:
    import kdsl.networking.v1

    return (
        kdsl.networking.v1.NetworkPolicyIngressRule(**value)
        if isinstance(value, dict)
        else value
    )


def optional_list_converter_NetworkPolicyPeer(
    value: Union[Sequence[kdsl.networking.v1.NetworkPolicyPeerUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.networking.v1.NetworkPolicyPeer], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_NetworkPolicyPeer(x) for x in value]


def optional_converter_NetworkPolicyPort(
    value: Union[kdsl.networking.v1.NetworkPolicyPortUnion, OmitEnum, None]
) -> Union[kdsl.networking.v1.NetworkPolicyPort, OmitEnum, None]:
    import kdsl.networking.v1

    return (
        kdsl.networking.v1.NetworkPolicyPort(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_NetworkPolicyEgressRule(
    value: Union[kdsl.networking.v1.NetworkPolicyEgressRuleUnion, OmitEnum, None]
) -> Union[kdsl.networking.v1.NetworkPolicyEgressRule, OmitEnum, None]:
    import kdsl.networking.v1

    return (
        kdsl.networking.v1.NetworkPolicyEgressRule(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_NetworkPolicySpec(
    value: kdsl.networking.v1.NetworkPolicySpecUnion,
) -> kdsl.networking.v1.NetworkPolicySpec:
    import kdsl.networking.v1

    return (
        kdsl.networking.v1.NetworkPolicySpec(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_NetworkPolicyPeer(
    value: kdsl.networking.v1.NetworkPolicyPeerUnion,
) -> kdsl.networking.v1.NetworkPolicyPeer:
    import kdsl.networking.v1

    return (
        kdsl.networking.v1.NetworkPolicyPeer(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_IPBlock(
    value: kdsl.networking.v1.IPBlockUnion,
) -> kdsl.networking.v1.IPBlock:
    import kdsl.networking.v1

    return kdsl.networking.v1.IPBlock(**value) if isinstance(value, dict) else value


def optional_list_converter_NetworkPolicyPort(
    value: Union[Sequence[kdsl.networking.v1.NetworkPolicyPortUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.networking.v1.NetworkPolicyPort], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_NetworkPolicyPort(x) for x in value]


def optional_list_converter_NetworkPolicyEgressRule(
    value: Union[
        Sequence[kdsl.networking.v1.NetworkPolicyEgressRuleUnion], OmitEnum, None
    ]
) -> Union[Sequence[kdsl.networking.v1.NetworkPolicyEgressRule], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_NetworkPolicyEgressRule(x) for x in value]


def optional_converter_IPBlock(
    value: Union[kdsl.networking.v1.IPBlockUnion, OmitEnum, None]
) -> Union[kdsl.networking.v1.IPBlock, OmitEnum, None]:
    import kdsl.networking.v1

    return kdsl.networking.v1.IPBlock(**value) if isinstance(value, dict) else value


def optional_list_converter_NetworkPolicyIngressRule(
    value: Union[
        Sequence[kdsl.networking.v1.NetworkPolicyIngressRuleUnion], OmitEnum, None
    ]
) -> Union[Sequence[kdsl.networking.v1.NetworkPolicyIngressRule], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_NetworkPolicyIngressRule(x) for x in value]


def required_converter_NetworkPolicyPort(
    value: kdsl.networking.v1.NetworkPolicyPortUnion,
) -> kdsl.networking.v1.NetworkPolicyPort:
    import kdsl.networking.v1

    return (
        kdsl.networking.v1.NetworkPolicyPort(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_NetworkPolicyEgressRule(
    value: kdsl.networking.v1.NetworkPolicyEgressRuleUnion,
) -> kdsl.networking.v1.NetworkPolicyEgressRule:
    import kdsl.networking.v1

    return (
        kdsl.networking.v1.NetworkPolicyEgressRule(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_NetworkPolicySpec(
    value: Union[kdsl.networking.v1.NetworkPolicySpecUnion, OmitEnum, None]
) -> Union[kdsl.networking.v1.NetworkPolicySpec, OmitEnum, None]:
    import kdsl.networking.v1

    return (
        kdsl.networking.v1.NetworkPolicySpec(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_NetworkPolicyPeer(
    value: Union[kdsl.networking.v1.NetworkPolicyPeerUnion, OmitEnum, None]
) -> Union[kdsl.networking.v1.NetworkPolicyPeer, OmitEnum, None]:
    import kdsl.networking.v1

    return (
        kdsl.networking.v1.NetworkPolicyPeer(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_NetworkPolicyIngressRule(
    value: kdsl.networking.v1.NetworkPolicyIngressRuleUnion,
) -> kdsl.networking.v1.NetworkPolicyIngressRule:
    import kdsl.networking.v1

    return (
        kdsl.networking.v1.NetworkPolicyIngressRule(**value)
        if isinstance(value, dict)
        else value
    )
