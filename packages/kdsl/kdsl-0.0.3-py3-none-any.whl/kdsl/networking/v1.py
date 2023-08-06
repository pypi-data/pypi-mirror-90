from __future__ import annotations
import kdsl.networking.v1
import kdsl.core.v1_converters
import kdsl.core.v1
import attr
import kdsl.networking.v1_converters
from typing import Mapping, ClassVar, Optional, Any, Sequence, TypedDict, Union
from kdsl.bases import OmitEnum, K8sObject, OMIT, K8sResource


@attr.s(kw_only=True)
class NetworkPolicyPeer(K8sObject):
    ipBlock: Union[None, OmitEnum, kdsl.networking.v1.IPBlock] = attr.ib(
        metadata={"yaml_name": "ipBlock"},
        converter=kdsl.networking.v1_converters.optional_converter_IPBlock,
        default=OMIT,
    )
    namespaceSelector: Union[None, OmitEnum, kdsl.core.v1.LabelSelector] = attr.ib(
        metadata={"yaml_name": "namespaceSelector"},
        converter=kdsl.core.v1_converters.optional_converter_LabelSelector,
        default=OMIT,
    )
    podSelector: Union[None, OmitEnum, kdsl.core.v1.LabelSelector] = attr.ib(
        metadata={"yaml_name": "podSelector"},
        converter=kdsl.core.v1_converters.optional_converter_LabelSelector,
        default=OMIT,
    )


class NetworkPolicyPeerTypedDict(TypedDict, total=(False)):
    ipBlock: kdsl.networking.v1.IPBlock
    namespaceSelector: kdsl.core.v1.LabelSelector
    podSelector: kdsl.core.v1.LabelSelector


NetworkPolicyPeerUnion = Union[NetworkPolicyPeer, NetworkPolicyPeerTypedDict]


@attr.s(kw_only=True)
class NetworkPolicySpec(K8sObject):
    podSelector: kdsl.core.v1.LabelSelector = attr.ib(
        metadata={"yaml_name": "podSelector"},
        converter=kdsl.core.v1_converters.required_converter_LabelSelector,
    )
    egress: Union[
        None, OmitEnum, Sequence[kdsl.networking.v1.NetworkPolicyEgressRule]
    ] = attr.ib(
        metadata={"yaml_name": "egress"},
        converter=kdsl.networking.v1_converters.optional_list_converter_NetworkPolicyEgressRule,
        default=OMIT,
    )
    ingress: Union[
        None, OmitEnum, Sequence[kdsl.networking.v1.NetworkPolicyIngressRule]
    ] = attr.ib(
        metadata={"yaml_name": "ingress"},
        converter=kdsl.networking.v1_converters.optional_list_converter_NetworkPolicyIngressRule,
        default=OMIT,
    )
    policyTypes: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "policyTypes"}, default=OMIT
    )


class NetworkPolicySpecOptionalTypedDict(TypedDict, total=(False)):
    egress: Sequence[kdsl.networking.v1.NetworkPolicyEgressRule]
    ingress: Sequence[kdsl.networking.v1.NetworkPolicyIngressRule]
    policyTypes: Sequence[str]


class NetworkPolicySpecTypedDict(NetworkPolicySpecOptionalTypedDict, total=(True)):
    podSelector: kdsl.core.v1.LabelSelector


NetworkPolicySpecUnion = Union[NetworkPolicySpec, NetworkPolicySpecTypedDict]


@attr.s(kw_only=True)
class NetworkPolicyPort(K8sObject):
    port: Union[None, OmitEnum, Union[int, str]] = attr.ib(
        metadata={"yaml_name": "port"}, default=OMIT
    )
    protocol: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "protocol"}, default=OMIT
    )


class NetworkPolicyPortTypedDict(TypedDict, total=(False)):
    port: Union[int, str]
    protocol: str


NetworkPolicyPortUnion = Union[NetworkPolicyPort, NetworkPolicyPortTypedDict]


@attr.s(kw_only=True)
class IPBlock(K8sObject):
    cidr: str = attr.ib(metadata={"yaml_name": "cidr"})
    except_: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "except"}, default=OMIT
    )


class IPBlockOptionalTypedDict(TypedDict, total=(False)):
    except_: Sequence[str]


class IPBlockTypedDict(IPBlockOptionalTypedDict, total=(True)):
    cidr: str


IPBlockUnion = Union[IPBlock, IPBlockTypedDict]


@attr.s(kw_only=True)
class NetworkPolicyIngressRule(K8sObject):
    from_: Union[
        None, OmitEnum, Sequence[kdsl.networking.v1.NetworkPolicyPeer]
    ] = attr.ib(
        metadata={"yaml_name": "from"},
        converter=kdsl.networking.v1_converters.optional_list_converter_NetworkPolicyPeer,
        default=OMIT,
    )
    ports: Union[
        None, OmitEnum, Sequence[kdsl.networking.v1.NetworkPolicyPort]
    ] = attr.ib(
        metadata={"yaml_name": "ports"},
        converter=kdsl.networking.v1_converters.optional_list_converter_NetworkPolicyPort,
        default=OMIT,
    )


class NetworkPolicyIngressRuleTypedDict(TypedDict, total=(False)):
    from_: Sequence[kdsl.networking.v1.NetworkPolicyPeer]
    ports: Sequence[kdsl.networking.v1.NetworkPolicyPort]


NetworkPolicyIngressRuleUnion = Union[
    NetworkPolicyIngressRule, NetworkPolicyIngressRuleTypedDict
]


@attr.s(kw_only=True)
class NetworkPolicy(K8sResource):
    apiVersion: ClassVar[str] = "networking.k8s.io/v1"
    kind: ClassVar[str] = "NetworkPolicy"
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    spec: Union[None, OmitEnum, kdsl.networking.v1.NetworkPolicySpec] = attr.ib(
        metadata={"yaml_name": "spec"},
        converter=kdsl.networking.v1_converters.optional_converter_NetworkPolicySpec,
        default=OMIT,
    )


@attr.s(kw_only=True)
class NetworkPolicyEgressRule(K8sObject):
    ports: Union[
        None, OmitEnum, Sequence[kdsl.networking.v1.NetworkPolicyPort]
    ] = attr.ib(
        metadata={"yaml_name": "ports"},
        converter=kdsl.networking.v1_converters.optional_list_converter_NetworkPolicyPort,
        default=OMIT,
    )
    to: Union[None, OmitEnum, Sequence[kdsl.networking.v1.NetworkPolicyPeer]] = attr.ib(
        metadata={"yaml_name": "to"},
        converter=kdsl.networking.v1_converters.optional_list_converter_NetworkPolicyPeer,
        default=OMIT,
    )


class NetworkPolicyEgressRuleTypedDict(TypedDict, total=(False)):
    ports: Sequence[kdsl.networking.v1.NetworkPolicyPort]
    to: Sequence[kdsl.networking.v1.NetworkPolicyPeer]


NetworkPolicyEgressRuleUnion = Union[
    NetworkPolicyEgressRule, NetworkPolicyEgressRuleTypedDict
]
