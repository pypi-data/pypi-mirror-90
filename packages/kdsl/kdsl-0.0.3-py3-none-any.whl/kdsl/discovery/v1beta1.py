from __future__ import annotations
import kdsl.core.v1
import kdsl.core.v1_converters
import kdsl.discovery.v1beta1
import kdsl.discovery.v1beta1_converters
import attr
from typing import Mapping, ClassVar, Optional, Any, Sequence, TypedDict, Union
from kdsl.bases import OmitEnum, K8sObject, OMIT, K8sResource


@attr.s(kw_only=True)
class EndpointConditions(K8sObject):
    ready: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "ready"}, default=OMIT
    )


class EndpointConditionsTypedDict(TypedDict, total=(False)):
    ready: bool


EndpointConditionsUnion = Union[EndpointConditions, EndpointConditionsTypedDict]


@attr.s(kw_only=True)
class EndpointSlice(K8sResource):
    apiVersion: ClassVar[str] = "discovery.k8s.io/v1beta1"
    kind: ClassVar[str] = "EndpointSlice"
    addressType: str = attr.ib(metadata={"yaml_name": "addressType"})
    endpoints: Sequence[kdsl.discovery.v1beta1.Endpoint] = attr.ib(
        metadata={"yaml_name": "endpoints"},
        converter=kdsl.discovery.v1beta1_converters.required_list_converter_Endpoint,
    )
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    ports: Union[
        None, OmitEnum, Sequence[kdsl.discovery.v1beta1.EndpointPort]
    ] = attr.ib(
        metadata={"yaml_name": "ports"},
        converter=kdsl.discovery.v1beta1_converters.optional_list_converter_EndpointPort,
        default=OMIT,
    )


@attr.s(kw_only=True)
class Endpoint(K8sObject):
    addresses: Sequence[str] = attr.ib(metadata={"yaml_name": "addresses"})
    conditions: Union[
        None, OmitEnum, kdsl.discovery.v1beta1.EndpointConditions
    ] = attr.ib(
        metadata={"yaml_name": "conditions"},
        converter=kdsl.discovery.v1beta1_converters.optional_converter_EndpointConditions,
        default=OMIT,
    )
    hostname: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "hostname"}, default=OMIT
    )
    targetRef: Union[None, OmitEnum, kdsl.core.v1.ObjectReference] = attr.ib(
        metadata={"yaml_name": "targetRef"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectReference,
        default=OMIT,
    )
    topology: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(
        metadata={"yaml_name": "topology"}, default=OMIT
    )


class EndpointOptionalTypedDict(TypedDict, total=(False)):
    conditions: kdsl.discovery.v1beta1.EndpointConditions
    hostname: str
    targetRef: kdsl.core.v1.ObjectReference
    topology: Mapping[str, str]


class EndpointTypedDict(EndpointOptionalTypedDict, total=(True)):
    addresses: Sequence[str]


EndpointUnion = Union[Endpoint, EndpointTypedDict]


@attr.s(kw_only=True)
class EndpointPort(K8sObject):
    appProtocol: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "appProtocol"}, default=OMIT
    )
    name: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "name"}, default=OMIT
    )
    port: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "port"}, default=OMIT
    )
    protocol: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "protocol"}, default=OMIT
    )


class EndpointPortTypedDict(TypedDict, total=(False)):
    appProtocol: str
    name: str
    port: int
    protocol: str


EndpointPortUnion = Union[EndpointPort, EndpointPortTypedDict]
