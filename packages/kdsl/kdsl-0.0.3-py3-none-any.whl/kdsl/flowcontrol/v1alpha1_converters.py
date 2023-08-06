from __future__ import annotations
from typing import Literal, Sequence, Union
from kdsl.bases import OmitEnum, OMIT
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import kdsl.flowcontrol.v1alpha1


def optional_converter_ServiceAccountSubject(
    value: Union[kdsl.flowcontrol.v1alpha1.ServiceAccountSubjectUnion, OmitEnum, None]
) -> Union[kdsl.flowcontrol.v1alpha1.ServiceAccountSubject, OmitEnum, None]:
    import kdsl.flowcontrol.v1alpha1

    return (
        kdsl.flowcontrol.v1alpha1.ServiceAccountSubject(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_PriorityLevelConfigurationReference(
    value: kdsl.flowcontrol.v1alpha1.PriorityLevelConfigurationReferenceUnion,
) -> kdsl.flowcontrol.v1alpha1.PriorityLevelConfigurationReference:
    import kdsl.flowcontrol.v1alpha1

    return (
        kdsl.flowcontrol.v1alpha1.PriorityLevelConfigurationReference(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_GroupSubject(
    value: kdsl.flowcontrol.v1alpha1.GroupSubjectUnion,
) -> kdsl.flowcontrol.v1alpha1.GroupSubject:
    import kdsl.flowcontrol.v1alpha1

    return (
        kdsl.flowcontrol.v1alpha1.GroupSubject(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_UserSubject(
    value: Union[kdsl.flowcontrol.v1alpha1.UserSubjectUnion, OmitEnum, None]
) -> Union[kdsl.flowcontrol.v1alpha1.UserSubject, OmitEnum, None]:
    import kdsl.flowcontrol.v1alpha1

    return (
        kdsl.flowcontrol.v1alpha1.UserSubject(**value)
        if isinstance(value, dict)
        else value
    )


def optional_list_converter_NonResourcePolicyRule(
    value: Union[
        Sequence[kdsl.flowcontrol.v1alpha1.NonResourcePolicyRuleUnion], OmitEnum, None
    ]
) -> Union[Sequence[kdsl.flowcontrol.v1alpha1.NonResourcePolicyRule], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_NonResourcePolicyRule(x) for x in value]


def optional_converter_PolicyRulesWithSubjects(
    value: Union[kdsl.flowcontrol.v1alpha1.PolicyRulesWithSubjectsUnion, OmitEnum, None]
) -> Union[kdsl.flowcontrol.v1alpha1.PolicyRulesWithSubjects, OmitEnum, None]:
    import kdsl.flowcontrol.v1alpha1

    return (
        kdsl.flowcontrol.v1alpha1.PolicyRulesWithSubjects(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_Subject(
    value: kdsl.flowcontrol.v1alpha1.SubjectUnion,
) -> kdsl.flowcontrol.v1alpha1.Subject:
    import kdsl.flowcontrol.v1alpha1

    return (
        kdsl.flowcontrol.v1alpha1.Subject(**value) if isinstance(value, dict) else value
    )


def required_converter_LimitResponse(
    value: kdsl.flowcontrol.v1alpha1.LimitResponseUnion,
) -> kdsl.flowcontrol.v1alpha1.LimitResponse:
    import kdsl.flowcontrol.v1alpha1

    return (
        kdsl.flowcontrol.v1alpha1.LimitResponse(**value)
        if isinstance(value, dict)
        else value
    )


def optional_list_converter_FlowSchemaCondition(
    value: Union[
        Sequence[kdsl.flowcontrol.v1alpha1.FlowSchemaConditionUnion], OmitEnum, None
    ]
) -> Union[Sequence[kdsl.flowcontrol.v1alpha1.FlowSchemaCondition], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_FlowSchemaCondition(x) for x in value]


def optional_converter_FlowDistinguisherMethod(
    value: Union[kdsl.flowcontrol.v1alpha1.FlowDistinguisherMethodUnion, OmitEnum, None]
) -> Union[kdsl.flowcontrol.v1alpha1.FlowDistinguisherMethod, OmitEnum, None]:
    import kdsl.flowcontrol.v1alpha1

    return (
        kdsl.flowcontrol.v1alpha1.FlowDistinguisherMethod(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_PriorityLevelConfigurationReference(
    value: Union[
        kdsl.flowcontrol.v1alpha1.PriorityLevelConfigurationReferenceUnion,
        OmitEnum,
        None,
    ]
) -> Union[
    kdsl.flowcontrol.v1alpha1.PriorityLevelConfigurationReference, OmitEnum, None
]:
    import kdsl.flowcontrol.v1alpha1

    return (
        kdsl.flowcontrol.v1alpha1.PriorityLevelConfigurationReference(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_FlowSchemaCondition(
    value: kdsl.flowcontrol.v1alpha1.FlowSchemaConditionUnion,
) -> kdsl.flowcontrol.v1alpha1.FlowSchemaCondition:
    import kdsl.flowcontrol.v1alpha1

    return (
        kdsl.flowcontrol.v1alpha1.FlowSchemaCondition(**value)
        if isinstance(value, dict)
        else value
    )


def optional_list_converter_ResourcePolicyRule(
    value: Union[
        Sequence[kdsl.flowcontrol.v1alpha1.ResourcePolicyRuleUnion], OmitEnum, None
    ]
) -> Union[Sequence[kdsl.flowcontrol.v1alpha1.ResourcePolicyRule], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_ResourcePolicyRule(x) for x in value]


def required_converter_QueuingConfiguration(
    value: kdsl.flowcontrol.v1alpha1.QueuingConfigurationUnion,
) -> kdsl.flowcontrol.v1alpha1.QueuingConfiguration:
    import kdsl.flowcontrol.v1alpha1

    return (
        kdsl.flowcontrol.v1alpha1.QueuingConfiguration(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_PriorityLevelConfigurationStatus(
    value: kdsl.flowcontrol.v1alpha1.PriorityLevelConfigurationStatusUnion,
) -> kdsl.flowcontrol.v1alpha1.PriorityLevelConfigurationStatus:
    import kdsl.flowcontrol.v1alpha1

    return (
        kdsl.flowcontrol.v1alpha1.PriorityLevelConfigurationStatus(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_NonResourcePolicyRule(
    value: kdsl.flowcontrol.v1alpha1.NonResourcePolicyRuleUnion,
) -> kdsl.flowcontrol.v1alpha1.NonResourcePolicyRule:
    import kdsl.flowcontrol.v1alpha1

    return (
        kdsl.flowcontrol.v1alpha1.NonResourcePolicyRule(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_ResourcePolicyRule(
    value: kdsl.flowcontrol.v1alpha1.ResourcePolicyRuleUnion,
) -> kdsl.flowcontrol.v1alpha1.ResourcePolicyRule:
    import kdsl.flowcontrol.v1alpha1

    return (
        kdsl.flowcontrol.v1alpha1.ResourcePolicyRule(**value)
        if isinstance(value, dict)
        else value
    )


def optional_list_converter_PriorityLevelConfigurationCondition(
    value: Union[
        Sequence[kdsl.flowcontrol.v1alpha1.PriorityLevelConfigurationConditionUnion],
        OmitEnum,
        None,
    ]
) -> Union[
    Sequence[kdsl.flowcontrol.v1alpha1.PriorityLevelConfigurationCondition],
    OmitEnum,
    None,
]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [
            required_converter_PriorityLevelConfigurationCondition(x) for x in value
        ]


def optional_converter_GroupSubject(
    value: Union[kdsl.flowcontrol.v1alpha1.GroupSubjectUnion, OmitEnum, None]
) -> Union[kdsl.flowcontrol.v1alpha1.GroupSubject, OmitEnum, None]:
    import kdsl.flowcontrol.v1alpha1

    return (
        kdsl.flowcontrol.v1alpha1.GroupSubject(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_FlowSchemaStatus(
    value: kdsl.flowcontrol.v1alpha1.FlowSchemaStatusUnion,
) -> kdsl.flowcontrol.v1alpha1.FlowSchemaStatus:
    import kdsl.flowcontrol.v1alpha1

    return (
        kdsl.flowcontrol.v1alpha1.FlowSchemaStatus(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_PriorityLevelConfigurationSpec(
    value: kdsl.flowcontrol.v1alpha1.PriorityLevelConfigurationSpecUnion,
) -> kdsl.flowcontrol.v1alpha1.PriorityLevelConfigurationSpec:
    import kdsl.flowcontrol.v1alpha1

    return (
        kdsl.flowcontrol.v1alpha1.PriorityLevelConfigurationSpec(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_LimitedPriorityLevelConfiguration(
    value: kdsl.flowcontrol.v1alpha1.LimitedPriorityLevelConfigurationUnion,
) -> kdsl.flowcontrol.v1alpha1.LimitedPriorityLevelConfiguration:
    import kdsl.flowcontrol.v1alpha1

    return (
        kdsl.flowcontrol.v1alpha1.LimitedPriorityLevelConfiguration(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_PriorityLevelConfigurationCondition(
    value: kdsl.flowcontrol.v1alpha1.PriorityLevelConfigurationConditionUnion,
) -> kdsl.flowcontrol.v1alpha1.PriorityLevelConfigurationCondition:
    import kdsl.flowcontrol.v1alpha1

    return (
        kdsl.flowcontrol.v1alpha1.PriorityLevelConfigurationCondition(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_FlowSchemaSpec(
    value: kdsl.flowcontrol.v1alpha1.FlowSchemaSpecUnion,
) -> kdsl.flowcontrol.v1alpha1.FlowSchemaSpec:
    import kdsl.flowcontrol.v1alpha1

    return (
        kdsl.flowcontrol.v1alpha1.FlowSchemaSpec(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_Subject(
    value: Union[kdsl.flowcontrol.v1alpha1.SubjectUnion, OmitEnum, None]
) -> Union[kdsl.flowcontrol.v1alpha1.Subject, OmitEnum, None]:
    import kdsl.flowcontrol.v1alpha1

    return (
        kdsl.flowcontrol.v1alpha1.Subject(**value) if isinstance(value, dict) else value
    )


def optional_converter_LimitResponse(
    value: Union[kdsl.flowcontrol.v1alpha1.LimitResponseUnion, OmitEnum, None]
) -> Union[kdsl.flowcontrol.v1alpha1.LimitResponse, OmitEnum, None]:
    import kdsl.flowcontrol.v1alpha1

    return (
        kdsl.flowcontrol.v1alpha1.LimitResponse(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_QueuingConfiguration(
    value: Union[kdsl.flowcontrol.v1alpha1.QueuingConfigurationUnion, OmitEnum, None]
) -> Union[kdsl.flowcontrol.v1alpha1.QueuingConfiguration, OmitEnum, None]:
    import kdsl.flowcontrol.v1alpha1

    return (
        kdsl.flowcontrol.v1alpha1.QueuingConfiguration(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_FlowSchemaCondition(
    value: Union[kdsl.flowcontrol.v1alpha1.FlowSchemaConditionUnion, OmitEnum, None]
) -> Union[kdsl.flowcontrol.v1alpha1.FlowSchemaCondition, OmitEnum, None]:
    import kdsl.flowcontrol.v1alpha1

    return (
        kdsl.flowcontrol.v1alpha1.FlowSchemaCondition(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_NonResourcePolicyRule(
    value: Union[kdsl.flowcontrol.v1alpha1.NonResourcePolicyRuleUnion, OmitEnum, None]
) -> Union[kdsl.flowcontrol.v1alpha1.NonResourcePolicyRule, OmitEnum, None]:
    import kdsl.flowcontrol.v1alpha1

    return (
        kdsl.flowcontrol.v1alpha1.NonResourcePolicyRule(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_ServiceAccountSubject(
    value: kdsl.flowcontrol.v1alpha1.ServiceAccountSubjectUnion,
) -> kdsl.flowcontrol.v1alpha1.ServiceAccountSubject:
    import kdsl.flowcontrol.v1alpha1

    return (
        kdsl.flowcontrol.v1alpha1.ServiceAccountSubject(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_PriorityLevelConfigurationStatus(
    value: Union[
        kdsl.flowcontrol.v1alpha1.PriorityLevelConfigurationStatusUnion, OmitEnum, None
    ]
) -> Union[kdsl.flowcontrol.v1alpha1.PriorityLevelConfigurationStatus, OmitEnum, None]:
    import kdsl.flowcontrol.v1alpha1

    return (
        kdsl.flowcontrol.v1alpha1.PriorityLevelConfigurationStatus(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_ResourcePolicyRule(
    value: Union[kdsl.flowcontrol.v1alpha1.ResourcePolicyRuleUnion, OmitEnum, None]
) -> Union[kdsl.flowcontrol.v1alpha1.ResourcePolicyRule, OmitEnum, None]:
    import kdsl.flowcontrol.v1alpha1

    return (
        kdsl.flowcontrol.v1alpha1.ResourcePolicyRule(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_PriorityLevelConfigurationSpec(
    value: Union[
        kdsl.flowcontrol.v1alpha1.PriorityLevelConfigurationSpecUnion, OmitEnum, None
    ]
) -> Union[kdsl.flowcontrol.v1alpha1.PriorityLevelConfigurationSpec, OmitEnum, None]:
    import kdsl.flowcontrol.v1alpha1

    return (
        kdsl.flowcontrol.v1alpha1.PriorityLevelConfigurationSpec(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_LimitedPriorityLevelConfiguration(
    value: Union[
        kdsl.flowcontrol.v1alpha1.LimitedPriorityLevelConfigurationUnion, OmitEnum, None
    ]
) -> Union[kdsl.flowcontrol.v1alpha1.LimitedPriorityLevelConfiguration, OmitEnum, None]:
    import kdsl.flowcontrol.v1alpha1

    return (
        kdsl.flowcontrol.v1alpha1.LimitedPriorityLevelConfiguration(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_FlowSchemaStatus(
    value: Union[kdsl.flowcontrol.v1alpha1.FlowSchemaStatusUnion, OmitEnum, None]
) -> Union[kdsl.flowcontrol.v1alpha1.FlowSchemaStatus, OmitEnum, None]:
    import kdsl.flowcontrol.v1alpha1

    return (
        kdsl.flowcontrol.v1alpha1.FlowSchemaStatus(**value)
        if isinstance(value, dict)
        else value
    )


def optional_list_converter_PolicyRulesWithSubjects(
    value: Union[
        Sequence[kdsl.flowcontrol.v1alpha1.PolicyRulesWithSubjectsUnion], OmitEnum, None
    ]
) -> Union[Sequence[kdsl.flowcontrol.v1alpha1.PolicyRulesWithSubjects], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_PolicyRulesWithSubjects(x) for x in value]


def optional_converter_FlowSchemaSpec(
    value: Union[kdsl.flowcontrol.v1alpha1.FlowSchemaSpecUnion, OmitEnum, None]
) -> Union[kdsl.flowcontrol.v1alpha1.FlowSchemaSpec, OmitEnum, None]:
    import kdsl.flowcontrol.v1alpha1

    return (
        kdsl.flowcontrol.v1alpha1.FlowSchemaSpec(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_UserSubject(
    value: kdsl.flowcontrol.v1alpha1.UserSubjectUnion,
) -> kdsl.flowcontrol.v1alpha1.UserSubject:
    import kdsl.flowcontrol.v1alpha1

    return (
        kdsl.flowcontrol.v1alpha1.UserSubject(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_PriorityLevelConfigurationCondition(
    value: Union[
        kdsl.flowcontrol.v1alpha1.PriorityLevelConfigurationConditionUnion,
        OmitEnum,
        None,
    ]
) -> Union[
    kdsl.flowcontrol.v1alpha1.PriorityLevelConfigurationCondition, OmitEnum, None
]:
    import kdsl.flowcontrol.v1alpha1

    return (
        kdsl.flowcontrol.v1alpha1.PriorityLevelConfigurationCondition(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_PolicyRulesWithSubjects(
    value: kdsl.flowcontrol.v1alpha1.PolicyRulesWithSubjectsUnion,
) -> kdsl.flowcontrol.v1alpha1.PolicyRulesWithSubjects:
    import kdsl.flowcontrol.v1alpha1

    return (
        kdsl.flowcontrol.v1alpha1.PolicyRulesWithSubjects(**value)
        if isinstance(value, dict)
        else value
    )


def required_list_converter_Subject(
    value: Sequence[kdsl.flowcontrol.v1alpha1.SubjectUnion],
) -> Sequence[kdsl.flowcontrol.v1alpha1.Subject]:
    return [required_converter_Subject(x) for x in value]


def required_converter_FlowDistinguisherMethod(
    value: kdsl.flowcontrol.v1alpha1.FlowDistinguisherMethodUnion,
) -> kdsl.flowcontrol.v1alpha1.FlowDistinguisherMethod:
    import kdsl.flowcontrol.v1alpha1

    return (
        kdsl.flowcontrol.v1alpha1.FlowDistinguisherMethod(**value)
        if isinstance(value, dict)
        else value
    )
