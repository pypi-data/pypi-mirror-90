from __future__ import annotations
from typing import Mapping, Literal, Union
from kdsl.bases import OmitEnum, OMIT
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import kdsl.apiregistration.v1


def required_converter_ServiceReference(
    value: kdsl.apiregistration.v1.ServiceReferenceUnion,
) -> kdsl.apiregistration.v1.ServiceReference:
    import kdsl.apiregistration.v1

    return (
        kdsl.apiregistration.v1.ServiceReference(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_APIServiceStatus(
    value: kdsl.apiregistration.v1.APIServiceStatusUnion,
) -> kdsl.apiregistration.v1.APIServiceStatus:
    import kdsl.apiregistration.v1

    return (
        kdsl.apiregistration.v1.APIServiceStatus(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_APIServiceConditionItem(
    value: Union[kdsl.apiregistration.v1.APIServiceConditionItemUnion, OmitEnum, None]
) -> Union[kdsl.apiregistration.v1.APIServiceConditionItem, OmitEnum, None]:
    import kdsl.apiregistration.v1

    return (
        kdsl.apiregistration.v1.APIServiceConditionItem(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_ServiceReference(
    value: Union[kdsl.apiregistration.v1.ServiceReferenceUnion, OmitEnum, None]
) -> Union[kdsl.apiregistration.v1.ServiceReference, OmitEnum, None]:
    import kdsl.apiregistration.v1

    return (
        kdsl.apiregistration.v1.ServiceReference(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_APIServiceStatus(
    value: Union[kdsl.apiregistration.v1.APIServiceStatusUnion, OmitEnum, None]
) -> Union[kdsl.apiregistration.v1.APIServiceStatus, OmitEnum, None]:
    import kdsl.apiregistration.v1

    return (
        kdsl.apiregistration.v1.APIServiceStatus(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_APIServiceSpec(
    value: kdsl.apiregistration.v1.APIServiceSpecUnion,
) -> kdsl.apiregistration.v1.APIServiceSpec:
    import kdsl.apiregistration.v1

    return (
        kdsl.apiregistration.v1.APIServiceSpec(**value)
        if isinstance(value, dict)
        else value
    )


def optional_mlist_converter_APIServiceConditionItem(
    value: Union[
        Mapping[str, kdsl.apiregistration.v1.APIServiceConditionItemUnion],
        OmitEnum,
        None,
    ]
) -> Union[
    Mapping[str, kdsl.apiregistration.v1.APIServiceConditionItem], OmitEnum, None
]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {
            k: required_converter_APIServiceConditionItem(v) for k, v in value.items()
        }


def optional_converter_APIServiceSpec(
    value: Union[kdsl.apiregistration.v1.APIServiceSpecUnion, OmitEnum, None]
) -> Union[kdsl.apiregistration.v1.APIServiceSpec, OmitEnum, None]:
    import kdsl.apiregistration.v1

    return (
        kdsl.apiregistration.v1.APIServiceSpec(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_APIServiceConditionItem(
    value: kdsl.apiregistration.v1.APIServiceConditionItemUnion,
) -> kdsl.apiregistration.v1.APIServiceConditionItem:
    import kdsl.apiregistration.v1

    return (
        kdsl.apiregistration.v1.APIServiceConditionItem(**value)
        if isinstance(value, dict)
        else value
    )
