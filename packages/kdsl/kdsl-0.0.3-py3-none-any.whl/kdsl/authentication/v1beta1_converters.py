from __future__ import annotations
from typing import Literal, Union
from kdsl.bases import OmitEnum, OMIT
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import kdsl.authentication.v1beta1


def required_converter_TokenReviewSpec(
    value: kdsl.authentication.v1beta1.TokenReviewSpecUnion,
) -> kdsl.authentication.v1beta1.TokenReviewSpec:
    import kdsl.authentication.v1beta1

    return (
        kdsl.authentication.v1beta1.TokenReviewSpec(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_UserInfo(
    value: Union[kdsl.authentication.v1beta1.UserInfoUnion, OmitEnum, None]
) -> Union[kdsl.authentication.v1beta1.UserInfo, OmitEnum, None]:
    import kdsl.authentication.v1beta1

    return (
        kdsl.authentication.v1beta1.UserInfo(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_TokenReviewStatus(
    value: Union[kdsl.authentication.v1beta1.TokenReviewStatusUnion, OmitEnum, None]
) -> Union[kdsl.authentication.v1beta1.TokenReviewStatus, OmitEnum, None]:
    import kdsl.authentication.v1beta1

    return (
        kdsl.authentication.v1beta1.TokenReviewStatus(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_TokenReviewSpec(
    value: Union[kdsl.authentication.v1beta1.TokenReviewSpecUnion, OmitEnum, None]
) -> Union[kdsl.authentication.v1beta1.TokenReviewSpec, OmitEnum, None]:
    import kdsl.authentication.v1beta1

    return (
        kdsl.authentication.v1beta1.TokenReviewSpec(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_UserInfo(
    value: kdsl.authentication.v1beta1.UserInfoUnion,
) -> kdsl.authentication.v1beta1.UserInfo:
    import kdsl.authentication.v1beta1

    return (
        kdsl.authentication.v1beta1.UserInfo(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_TokenReviewStatus(
    value: kdsl.authentication.v1beta1.TokenReviewStatusUnion,
) -> kdsl.authentication.v1beta1.TokenReviewStatus:
    import kdsl.authentication.v1beta1

    return (
        kdsl.authentication.v1beta1.TokenReviewStatus(**value)
        if isinstance(value, dict)
        else value
    )
