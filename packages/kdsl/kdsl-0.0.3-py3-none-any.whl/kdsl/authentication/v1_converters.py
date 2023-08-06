from __future__ import annotations
from typing import Literal, Union
from kdsl.bases import OmitEnum, OMIT
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import kdsl.authentication.v1


def optional_converter_TokenReviewSpec(
    value: Union[kdsl.authentication.v1.TokenReviewSpecUnion, OmitEnum, None]
) -> Union[kdsl.authentication.v1.TokenReviewSpec, OmitEnum, None]:
    import kdsl.authentication.v1

    return (
        kdsl.authentication.v1.TokenReviewSpec(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_TokenReviewStatus(
    value: kdsl.authentication.v1.TokenReviewStatusUnion,
) -> kdsl.authentication.v1.TokenReviewStatus:
    import kdsl.authentication.v1

    return (
        kdsl.authentication.v1.TokenReviewStatus(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_UserInfo(
    value: kdsl.authentication.v1.UserInfoUnion,
) -> kdsl.authentication.v1.UserInfo:
    import kdsl.authentication.v1

    return (
        kdsl.authentication.v1.UserInfo(**value) if isinstance(value, dict) else value
    )


def optional_converter_BoundObjectReference(
    value: Union[kdsl.authentication.v1.BoundObjectReferenceUnion, OmitEnum, None]
) -> Union[kdsl.authentication.v1.BoundObjectReference, OmitEnum, None]:
    import kdsl.authentication.v1

    return (
        kdsl.authentication.v1.BoundObjectReference(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_TokenRequestSpec(
    value: Union[kdsl.authentication.v1.TokenRequestSpecUnion, OmitEnum, None]
) -> Union[kdsl.authentication.v1.TokenRequestSpec, OmitEnum, None]:
    import kdsl.authentication.v1

    return (
        kdsl.authentication.v1.TokenRequestSpec(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_UserInfo(
    value: Union[kdsl.authentication.v1.UserInfoUnion, OmitEnum, None]
) -> Union[kdsl.authentication.v1.UserInfo, OmitEnum, None]:
    import kdsl.authentication.v1

    return (
        kdsl.authentication.v1.UserInfo(**value) if isinstance(value, dict) else value
    )


def optional_converter_TokenReviewStatus(
    value: Union[kdsl.authentication.v1.TokenReviewStatusUnion, OmitEnum, None]
) -> Union[kdsl.authentication.v1.TokenReviewStatus, OmitEnum, None]:
    import kdsl.authentication.v1

    return (
        kdsl.authentication.v1.TokenReviewStatus(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_TokenReviewSpec(
    value: kdsl.authentication.v1.TokenReviewSpecUnion,
) -> kdsl.authentication.v1.TokenReviewSpec:
    import kdsl.authentication.v1

    return (
        kdsl.authentication.v1.TokenReviewSpec(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_TokenRequestStatus(
    value: kdsl.authentication.v1.TokenRequestStatusUnion,
) -> kdsl.authentication.v1.TokenRequestStatus:
    import kdsl.authentication.v1

    return (
        kdsl.authentication.v1.TokenRequestStatus(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_TokenRequestSpec(
    value: kdsl.authentication.v1.TokenRequestSpecUnion,
) -> kdsl.authentication.v1.TokenRequestSpec:
    import kdsl.authentication.v1

    return (
        kdsl.authentication.v1.TokenRequestSpec(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_TokenRequestStatus(
    value: Union[kdsl.authentication.v1.TokenRequestStatusUnion, OmitEnum, None]
) -> Union[kdsl.authentication.v1.TokenRequestStatus, OmitEnum, None]:
    import kdsl.authentication.v1

    return (
        kdsl.authentication.v1.TokenRequestStatus(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_BoundObjectReference(
    value: kdsl.authentication.v1.BoundObjectReferenceUnion,
) -> kdsl.authentication.v1.BoundObjectReference:
    import kdsl.authentication.v1

    return (
        kdsl.authentication.v1.BoundObjectReference(**value)
        if isinstance(value, dict)
        else value
    )
