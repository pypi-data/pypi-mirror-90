from __future__ import annotations
from typing import Sequence, Literal, Union
from kdsl.bases import OmitEnum, OMIT
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import kdsl.certificates.v1beta1


def required_converter_CertificateSigningRequestCondition(
    value: kdsl.certificates.v1beta1.CertificateSigningRequestConditionUnion,
) -> kdsl.certificates.v1beta1.CertificateSigningRequestCondition:
    import kdsl.certificates.v1beta1

    return (
        kdsl.certificates.v1beta1.CertificateSigningRequestCondition(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_CertificateSigningRequestSpec(
    value: kdsl.certificates.v1beta1.CertificateSigningRequestSpecUnion,
) -> kdsl.certificates.v1beta1.CertificateSigningRequestSpec:
    import kdsl.certificates.v1beta1

    return (
        kdsl.certificates.v1beta1.CertificateSigningRequestSpec(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_CertificateSigningRequestCondition(
    value: Union[
        kdsl.certificates.v1beta1.CertificateSigningRequestConditionUnion,
        OmitEnum,
        None,
    ]
) -> Union[
    kdsl.certificates.v1beta1.CertificateSigningRequestCondition, OmitEnum, None
]:
    import kdsl.certificates.v1beta1

    return (
        kdsl.certificates.v1beta1.CertificateSigningRequestCondition(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_CertificateSigningRequestSpec(
    value: Union[
        kdsl.certificates.v1beta1.CertificateSigningRequestSpecUnion, OmitEnum, None
    ]
) -> Union[kdsl.certificates.v1beta1.CertificateSigningRequestSpec, OmitEnum, None]:
    import kdsl.certificates.v1beta1

    return (
        kdsl.certificates.v1beta1.CertificateSigningRequestSpec(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_CertificateSigningRequestStatus(
    value: kdsl.certificates.v1beta1.CertificateSigningRequestStatusUnion,
) -> kdsl.certificates.v1beta1.CertificateSigningRequestStatus:
    import kdsl.certificates.v1beta1

    return (
        kdsl.certificates.v1beta1.CertificateSigningRequestStatus(**value)
        if isinstance(value, dict)
        else value
    )


def optional_list_converter_CertificateSigningRequestCondition(
    value: Union[
        Sequence[kdsl.certificates.v1beta1.CertificateSigningRequestConditionUnion],
        OmitEnum,
        None,
    ]
) -> Union[
    Sequence[kdsl.certificates.v1beta1.CertificateSigningRequestCondition],
    OmitEnum,
    None,
]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_CertificateSigningRequestCondition(x) for x in value]


def optional_converter_CertificateSigningRequestStatus(
    value: Union[
        kdsl.certificates.v1beta1.CertificateSigningRequestStatusUnion, OmitEnum, None
    ]
) -> Union[kdsl.certificates.v1beta1.CertificateSigningRequestStatus, OmitEnum, None]:
    import kdsl.certificates.v1beta1

    return (
        kdsl.certificates.v1beta1.CertificateSigningRequestStatus(**value)
        if isinstance(value, dict)
        else value
    )
