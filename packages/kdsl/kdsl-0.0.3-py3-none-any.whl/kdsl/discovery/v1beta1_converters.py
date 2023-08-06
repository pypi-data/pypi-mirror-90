from __future__ import annotations
from typing import Literal, Sequence, Union
from kdsl.bases import OmitEnum, OMIT
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import kdsl.discovery.v1beta1


def optional_list_converter_EndpointPort(
    value: Union[Sequence[kdsl.discovery.v1beta1.EndpointPortUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.discovery.v1beta1.EndpointPort], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_EndpointPort(x) for x in value]


def required_converter_EndpointPort(
    value: kdsl.discovery.v1beta1.EndpointPortUnion,
) -> kdsl.discovery.v1beta1.EndpointPort:
    import kdsl.discovery.v1beta1

    return (
        kdsl.discovery.v1beta1.EndpointPort(**value)
        if isinstance(value, dict)
        else value
    )


def required_list_converter_Endpoint(
    value: Sequence[kdsl.discovery.v1beta1.EndpointUnion],
) -> Sequence[kdsl.discovery.v1beta1.Endpoint]:
    return [required_converter_Endpoint(x) for x in value]


def required_converter_EndpointConditions(
    value: kdsl.discovery.v1beta1.EndpointConditionsUnion,
) -> kdsl.discovery.v1beta1.EndpointConditions:
    import kdsl.discovery.v1beta1

    return (
        kdsl.discovery.v1beta1.EndpointConditions(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_Endpoint(
    value: kdsl.discovery.v1beta1.EndpointUnion,
) -> kdsl.discovery.v1beta1.Endpoint:
    import kdsl.discovery.v1beta1

    return (
        kdsl.discovery.v1beta1.Endpoint(**value) if isinstance(value, dict) else value
    )


def optional_converter_EndpointPort(
    value: Union[kdsl.discovery.v1beta1.EndpointPortUnion, OmitEnum, None]
) -> Union[kdsl.discovery.v1beta1.EndpointPort, OmitEnum, None]:
    import kdsl.discovery.v1beta1

    return (
        kdsl.discovery.v1beta1.EndpointPort(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_EndpointConditions(
    value: Union[kdsl.discovery.v1beta1.EndpointConditionsUnion, OmitEnum, None]
) -> Union[kdsl.discovery.v1beta1.EndpointConditions, OmitEnum, None]:
    import kdsl.discovery.v1beta1

    return (
        kdsl.discovery.v1beta1.EndpointConditions(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_Endpoint(
    value: Union[kdsl.discovery.v1beta1.EndpointUnion, OmitEnum, None]
) -> Union[kdsl.discovery.v1beta1.Endpoint, OmitEnum, None]:
    import kdsl.discovery.v1beta1

    return (
        kdsl.discovery.v1beta1.Endpoint(**value) if isinstance(value, dict) else value
    )
