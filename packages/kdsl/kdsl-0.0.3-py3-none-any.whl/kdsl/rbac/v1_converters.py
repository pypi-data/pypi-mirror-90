from __future__ import annotations
from typing import Literal, Sequence, Union
from kdsl.bases import OmitEnum, OMIT
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import kdsl.rbac.v1


def optional_list_converter_Subject(
    value: Union[Sequence[kdsl.rbac.v1.SubjectUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.rbac.v1.Subject], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_Subject(x) for x in value]


def required_converter_RoleRef(
    value: kdsl.rbac.v1.RoleRefUnion,
) -> kdsl.rbac.v1.RoleRef:
    import kdsl.rbac.v1

    return kdsl.rbac.v1.RoleRef(**value) if isinstance(value, dict) else value


def required_converter_PolicyRule(
    value: kdsl.rbac.v1.PolicyRuleUnion,
) -> kdsl.rbac.v1.PolicyRule:
    import kdsl.rbac.v1

    return kdsl.rbac.v1.PolicyRule(**value) if isinstance(value, dict) else value


def optional_converter_RoleRef(
    value: Union[kdsl.rbac.v1.RoleRefUnion, OmitEnum, None]
) -> Union[kdsl.rbac.v1.RoleRef, OmitEnum, None]:
    import kdsl.rbac.v1

    return kdsl.rbac.v1.RoleRef(**value) if isinstance(value, dict) else value


def required_converter_AggregationRule(
    value: kdsl.rbac.v1.AggregationRuleUnion,
) -> kdsl.rbac.v1.AggregationRule:
    import kdsl.rbac.v1

    return kdsl.rbac.v1.AggregationRule(**value) if isinstance(value, dict) else value


def optional_list_converter_PolicyRule(
    value: Union[Sequence[kdsl.rbac.v1.PolicyRuleUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.rbac.v1.PolicyRule], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_PolicyRule(x) for x in value]


def required_converter_Subject(
    value: kdsl.rbac.v1.SubjectUnion,
) -> kdsl.rbac.v1.Subject:
    import kdsl.rbac.v1

    return kdsl.rbac.v1.Subject(**value) if isinstance(value, dict) else value


def optional_converter_PolicyRule(
    value: Union[kdsl.rbac.v1.PolicyRuleUnion, OmitEnum, None]
) -> Union[kdsl.rbac.v1.PolicyRule, OmitEnum, None]:
    import kdsl.rbac.v1

    return kdsl.rbac.v1.PolicyRule(**value) if isinstance(value, dict) else value


def optional_converter_Subject(
    value: Union[kdsl.rbac.v1.SubjectUnion, OmitEnum, None]
) -> Union[kdsl.rbac.v1.Subject, OmitEnum, None]:
    import kdsl.rbac.v1

    return kdsl.rbac.v1.Subject(**value) if isinstance(value, dict) else value


def optional_converter_AggregationRule(
    value: Union[kdsl.rbac.v1.AggregationRuleUnion, OmitEnum, None]
) -> Union[kdsl.rbac.v1.AggregationRule, OmitEnum, None]:
    import kdsl.rbac.v1

    return kdsl.rbac.v1.AggregationRule(**value) if isinstance(value, dict) else value
