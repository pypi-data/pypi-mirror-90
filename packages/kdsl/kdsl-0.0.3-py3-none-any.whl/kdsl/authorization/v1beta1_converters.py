from __future__ import annotations
from typing import Literal, Sequence, Union
from kdsl.bases import OmitEnum, OMIT
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import kdsl.authorization.v1beta1


def optional_converter_NonResourceAttributes(
    value: Union[kdsl.authorization.v1beta1.NonResourceAttributesUnion, OmitEnum, None]
) -> Union[kdsl.authorization.v1beta1.NonResourceAttributes, OmitEnum, None]:
    import kdsl.authorization.v1beta1

    return (
        kdsl.authorization.v1beta1.NonResourceAttributes(**value)
        if isinstance(value, dict)
        else value
    )


def required_list_converter_NonResourceRule(
    value: Sequence[kdsl.authorization.v1beta1.NonResourceRuleUnion],
) -> Sequence[kdsl.authorization.v1beta1.NonResourceRule]:
    return [required_converter_NonResourceRule(x) for x in value]


def required_converter_SelfSubjectRulesReviewSpec(
    value: kdsl.authorization.v1beta1.SelfSubjectRulesReviewSpecUnion,
) -> kdsl.authorization.v1beta1.SelfSubjectRulesReviewSpec:
    import kdsl.authorization.v1beta1

    return (
        kdsl.authorization.v1beta1.SelfSubjectRulesReviewSpec(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_SubjectAccessReviewSpec(
    value: Union[
        kdsl.authorization.v1beta1.SubjectAccessReviewSpecUnion, OmitEnum, None
    ]
) -> Union[kdsl.authorization.v1beta1.SubjectAccessReviewSpec, OmitEnum, None]:
    import kdsl.authorization.v1beta1

    return (
        kdsl.authorization.v1beta1.SubjectAccessReviewSpec(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_ResourceRule(
    value: Union[kdsl.authorization.v1beta1.ResourceRuleUnion, OmitEnum, None]
) -> Union[kdsl.authorization.v1beta1.ResourceRule, OmitEnum, None]:
    import kdsl.authorization.v1beta1

    return (
        kdsl.authorization.v1beta1.ResourceRule(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_SubjectRulesReviewStatus(
    value: Union[
        kdsl.authorization.v1beta1.SubjectRulesReviewStatusUnion, OmitEnum, None
    ]
) -> Union[kdsl.authorization.v1beta1.SubjectRulesReviewStatus, OmitEnum, None]:
    import kdsl.authorization.v1beta1

    return (
        kdsl.authorization.v1beta1.SubjectRulesReviewStatus(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_SelfSubjectAccessReviewSpec(
    value: kdsl.authorization.v1beta1.SelfSubjectAccessReviewSpecUnion,
) -> kdsl.authorization.v1beta1.SelfSubjectAccessReviewSpec:
    import kdsl.authorization.v1beta1

    return (
        kdsl.authorization.v1beta1.SelfSubjectAccessReviewSpec(**value)
        if isinstance(value, dict)
        else value
    )


def required_list_converter_ResourceRule(
    value: Sequence[kdsl.authorization.v1beta1.ResourceRuleUnion],
) -> Sequence[kdsl.authorization.v1beta1.ResourceRule]:
    return [required_converter_ResourceRule(x) for x in value]


def optional_converter_SelfSubjectRulesReviewSpec(
    value: Union[
        kdsl.authorization.v1beta1.SelfSubjectRulesReviewSpecUnion, OmitEnum, None
    ]
) -> Union[kdsl.authorization.v1beta1.SelfSubjectRulesReviewSpec, OmitEnum, None]:
    import kdsl.authorization.v1beta1

    return (
        kdsl.authorization.v1beta1.SelfSubjectRulesReviewSpec(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_ResourceAttributes(
    value: kdsl.authorization.v1beta1.ResourceAttributesUnion,
) -> kdsl.authorization.v1beta1.ResourceAttributes:
    import kdsl.authorization.v1beta1

    return (
        kdsl.authorization.v1beta1.ResourceAttributes(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_NonResourceRule(
    value: kdsl.authorization.v1beta1.NonResourceRuleUnion,
) -> kdsl.authorization.v1beta1.NonResourceRule:
    import kdsl.authorization.v1beta1

    return (
        kdsl.authorization.v1beta1.NonResourceRule(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_SubjectAccessReviewStatus(
    value: kdsl.authorization.v1beta1.SubjectAccessReviewStatusUnion,
) -> kdsl.authorization.v1beta1.SubjectAccessReviewStatus:
    import kdsl.authorization.v1beta1

    return (
        kdsl.authorization.v1beta1.SubjectAccessReviewStatus(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_SelfSubjectAccessReviewSpec(
    value: Union[
        kdsl.authorization.v1beta1.SelfSubjectAccessReviewSpecUnion, OmitEnum, None
    ]
) -> Union[kdsl.authorization.v1beta1.SelfSubjectAccessReviewSpec, OmitEnum, None]:
    import kdsl.authorization.v1beta1

    return (
        kdsl.authorization.v1beta1.SelfSubjectAccessReviewSpec(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_NonResourceAttributes(
    value: kdsl.authorization.v1beta1.NonResourceAttributesUnion,
) -> kdsl.authorization.v1beta1.NonResourceAttributes:
    import kdsl.authorization.v1beta1

    return (
        kdsl.authorization.v1beta1.NonResourceAttributes(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_ResourceAttributes(
    value: Union[kdsl.authorization.v1beta1.ResourceAttributesUnion, OmitEnum, None]
) -> Union[kdsl.authorization.v1beta1.ResourceAttributes, OmitEnum, None]:
    import kdsl.authorization.v1beta1

    return (
        kdsl.authorization.v1beta1.ResourceAttributes(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_NonResourceRule(
    value: Union[kdsl.authorization.v1beta1.NonResourceRuleUnion, OmitEnum, None]
) -> Union[kdsl.authorization.v1beta1.NonResourceRule, OmitEnum, None]:
    import kdsl.authorization.v1beta1

    return (
        kdsl.authorization.v1beta1.NonResourceRule(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_ResourceRule(
    value: kdsl.authorization.v1beta1.ResourceRuleUnion,
) -> kdsl.authorization.v1beta1.ResourceRule:
    import kdsl.authorization.v1beta1

    return (
        kdsl.authorization.v1beta1.ResourceRule(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_SubjectRulesReviewStatus(
    value: kdsl.authorization.v1beta1.SubjectRulesReviewStatusUnion,
) -> kdsl.authorization.v1beta1.SubjectRulesReviewStatus:
    import kdsl.authorization.v1beta1

    return (
        kdsl.authorization.v1beta1.SubjectRulesReviewStatus(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_SubjectAccessReviewSpec(
    value: kdsl.authorization.v1beta1.SubjectAccessReviewSpecUnion,
) -> kdsl.authorization.v1beta1.SubjectAccessReviewSpec:
    import kdsl.authorization.v1beta1

    return (
        kdsl.authorization.v1beta1.SubjectAccessReviewSpec(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_SubjectAccessReviewStatus(
    value: Union[
        kdsl.authorization.v1beta1.SubjectAccessReviewStatusUnion, OmitEnum, None
    ]
) -> Union[kdsl.authorization.v1beta1.SubjectAccessReviewStatus, OmitEnum, None]:
    import kdsl.authorization.v1beta1

    return (
        kdsl.authorization.v1beta1.SubjectAccessReviewStatus(**value)
        if isinstance(value, dict)
        else value
    )
