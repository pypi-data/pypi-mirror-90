from __future__ import annotations
import kdsl.flowcontrol.v1alpha1_converters
import kdsl.core.v1
import kdsl.core.v1_converters
import attr
import kdsl.flowcontrol.v1alpha1
from typing import Mapping, ClassVar, Optional, Any, Sequence, TypedDict, Union
from kdsl.bases import OmitEnum, K8sObject, OMIT, K8sResource


@attr.s(kw_only=True)
class PriorityLevelConfigurationSpec(K8sObject):
    type: str = attr.ib(metadata={"yaml_name": "type"})
    limited: Union[
        None, OmitEnum, kdsl.flowcontrol.v1alpha1.LimitedPriorityLevelConfiguration
    ] = attr.ib(
        metadata={"yaml_name": "limited"},
        converter=kdsl.flowcontrol.v1alpha1_converters.optional_converter_LimitedPriorityLevelConfiguration,
        default=OMIT,
    )


class PriorityLevelConfigurationSpecOptionalTypedDict(TypedDict, total=(False)):
    limited: kdsl.flowcontrol.v1alpha1.LimitedPriorityLevelConfiguration


class PriorityLevelConfigurationSpecTypedDict(
    PriorityLevelConfigurationSpecOptionalTypedDict, total=(True)
):
    type: str


PriorityLevelConfigurationSpecUnion = Union[
    PriorityLevelConfigurationSpec, PriorityLevelConfigurationSpecTypedDict
]


@attr.s(kw_only=True)
class GroupSubject(K8sObject):
    name: str = attr.ib(metadata={"yaml_name": "name"})


class GroupSubjectTypedDict(TypedDict, total=(True)):
    name: str


GroupSubjectUnion = Union[GroupSubject, GroupSubjectTypedDict]


@attr.s(kw_only=True)
class FlowSchemaSpec(K8sObject):
    priorityLevelConfiguration: kdsl.flowcontrol.v1alpha1.PriorityLevelConfigurationReference = attr.ib(
        metadata={"yaml_name": "priorityLevelConfiguration"},
        converter=kdsl.flowcontrol.v1alpha1_converters.required_converter_PriorityLevelConfigurationReference,
    )
    distinguisherMethod: Union[
        None, OmitEnum, kdsl.flowcontrol.v1alpha1.FlowDistinguisherMethod
    ] = attr.ib(
        metadata={"yaml_name": "distinguisherMethod"},
        converter=kdsl.flowcontrol.v1alpha1_converters.optional_converter_FlowDistinguisherMethod,
        default=OMIT,
    )
    matchingPrecedence: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "matchingPrecedence"}, default=OMIT
    )
    rules: Union[
        None, OmitEnum, Sequence[kdsl.flowcontrol.v1alpha1.PolicyRulesWithSubjects]
    ] = attr.ib(
        metadata={"yaml_name": "rules"},
        converter=kdsl.flowcontrol.v1alpha1_converters.optional_list_converter_PolicyRulesWithSubjects,
        default=OMIT,
    )


class FlowSchemaSpecOptionalTypedDict(TypedDict, total=(False)):
    distinguisherMethod: kdsl.flowcontrol.v1alpha1.FlowDistinguisherMethod
    matchingPrecedence: int
    rules: Sequence[kdsl.flowcontrol.v1alpha1.PolicyRulesWithSubjects]


class FlowSchemaSpecTypedDict(FlowSchemaSpecOptionalTypedDict, total=(True)):
    priorityLevelConfiguration: kdsl.flowcontrol.v1alpha1.PriorityLevelConfigurationReference


FlowSchemaSpecUnion = Union[FlowSchemaSpec, FlowSchemaSpecTypedDict]


@attr.s(kw_only=True)
class FlowSchema(K8sResource):
    apiVersion: ClassVar[str] = "flowcontrol.apiserver.k8s.io/v1alpha1"
    kind: ClassVar[str] = "FlowSchema"
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    spec: Union[None, OmitEnum, kdsl.flowcontrol.v1alpha1.FlowSchemaSpec] = attr.ib(
        metadata={"yaml_name": "spec"},
        converter=kdsl.flowcontrol.v1alpha1_converters.optional_converter_FlowSchemaSpec,
        default=OMIT,
    )
    status: Union[None, OmitEnum, kdsl.flowcontrol.v1alpha1.FlowSchemaStatus] = attr.ib(
        metadata={"yaml_name": "status"},
        converter=kdsl.flowcontrol.v1alpha1_converters.optional_converter_FlowSchemaStatus,
        default=OMIT,
    )


@attr.s(kw_only=True)
class PriorityLevelConfiguration(K8sResource):
    apiVersion: ClassVar[str] = "flowcontrol.apiserver.k8s.io/v1alpha1"
    kind: ClassVar[str] = "PriorityLevelConfiguration"
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    spec: Union[
        None, OmitEnum, kdsl.flowcontrol.v1alpha1.PriorityLevelConfigurationSpec
    ] = attr.ib(
        metadata={"yaml_name": "spec"},
        converter=kdsl.flowcontrol.v1alpha1_converters.optional_converter_PriorityLevelConfigurationSpec,
        default=OMIT,
    )
    status: Union[
        None, OmitEnum, kdsl.flowcontrol.v1alpha1.PriorityLevelConfigurationStatus
    ] = attr.ib(
        metadata={"yaml_name": "status"},
        converter=kdsl.flowcontrol.v1alpha1_converters.optional_converter_PriorityLevelConfigurationStatus,
        default=OMIT,
    )


@attr.s(kw_only=True)
class Subject(K8sObject):
    kind: str = attr.ib(metadata={"yaml_name": "kind"})
    group: Union[None, OmitEnum, kdsl.flowcontrol.v1alpha1.GroupSubject] = attr.ib(
        metadata={"yaml_name": "group"},
        converter=kdsl.flowcontrol.v1alpha1_converters.optional_converter_GroupSubject,
        default=OMIT,
    )
    serviceAccount: Union[
        None, OmitEnum, kdsl.flowcontrol.v1alpha1.ServiceAccountSubject
    ] = attr.ib(
        metadata={"yaml_name": "serviceAccount"},
        converter=kdsl.flowcontrol.v1alpha1_converters.optional_converter_ServiceAccountSubject,
        default=OMIT,
    )
    user: Union[None, OmitEnum, kdsl.flowcontrol.v1alpha1.UserSubject] = attr.ib(
        metadata={"yaml_name": "user"},
        converter=kdsl.flowcontrol.v1alpha1_converters.optional_converter_UserSubject,
        default=OMIT,
    )


class SubjectOptionalTypedDict(TypedDict, total=(False)):
    group: kdsl.flowcontrol.v1alpha1.GroupSubject
    serviceAccount: kdsl.flowcontrol.v1alpha1.ServiceAccountSubject
    user: kdsl.flowcontrol.v1alpha1.UserSubject


class SubjectTypedDict(SubjectOptionalTypedDict, total=(True)):
    kind: str


SubjectUnion = Union[Subject, SubjectTypedDict]


@attr.s(kw_only=True)
class ResourcePolicyRule(K8sObject):
    apiGroups: Sequence[str] = attr.ib(metadata={"yaml_name": "apiGroups"})
    resources: Sequence[str] = attr.ib(metadata={"yaml_name": "resources"})
    verbs: Sequence[str] = attr.ib(metadata={"yaml_name": "verbs"})
    clusterScope: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "clusterScope"}, default=OMIT
    )
    namespaces: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "namespaces"}, default=OMIT
    )


class ResourcePolicyRuleOptionalTypedDict(TypedDict, total=(False)):
    clusterScope: bool
    namespaces: Sequence[str]


class ResourcePolicyRuleTypedDict(ResourcePolicyRuleOptionalTypedDict, total=(True)):
    apiGroups: Sequence[str]
    resources: Sequence[str]
    verbs: Sequence[str]


ResourcePolicyRuleUnion = Union[ResourcePolicyRule, ResourcePolicyRuleTypedDict]


@attr.s(kw_only=True)
class FlowSchemaCondition(K8sObject):
    lastTransitionTime: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "lastTransitionTime"}, default=OMIT
    )
    message: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "message"}, default=OMIT
    )
    reason: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "reason"}, default=OMIT
    )
    status: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "status"}, default=OMIT
    )
    type: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "type"}, default=OMIT
    )


class FlowSchemaConditionTypedDict(TypedDict, total=(False)):
    lastTransitionTime: str
    message: str
    reason: str
    status: str
    type: str


FlowSchemaConditionUnion = Union[FlowSchemaCondition, FlowSchemaConditionTypedDict]


@attr.s(kw_only=True)
class LimitedPriorityLevelConfiguration(K8sObject):
    assuredConcurrencyShares: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "assuredConcurrencyShares"}, default=OMIT
    )
    limitResponse: Union[
        None, OmitEnum, kdsl.flowcontrol.v1alpha1.LimitResponse
    ] = attr.ib(
        metadata={"yaml_name": "limitResponse"},
        converter=kdsl.flowcontrol.v1alpha1_converters.optional_converter_LimitResponse,
        default=OMIT,
    )


class LimitedPriorityLevelConfigurationTypedDict(TypedDict, total=(False)):
    assuredConcurrencyShares: int
    limitResponse: kdsl.flowcontrol.v1alpha1.LimitResponse


LimitedPriorityLevelConfigurationUnion = Union[
    LimitedPriorityLevelConfiguration, LimitedPriorityLevelConfigurationTypedDict
]


@attr.s(kw_only=True)
class ServiceAccountSubject(K8sObject):
    name: str = attr.ib(metadata={"yaml_name": "name"})
    namespace: str = attr.ib(metadata={"yaml_name": "namespace"})


class ServiceAccountSubjectTypedDict(TypedDict, total=(True)):
    name: str
    namespace: str


ServiceAccountSubjectUnion = Union[
    ServiceAccountSubject, ServiceAccountSubjectTypedDict
]


@attr.s(kw_only=True)
class QueuingConfiguration(K8sObject):
    handSize: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "handSize"}, default=OMIT
    )
    queueLengthLimit: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "queueLengthLimit"}, default=OMIT
    )
    queues: Union[None, OmitEnum, int] = attr.ib(
        metadata={"yaml_name": "queues"}, default=OMIT
    )


class QueuingConfigurationTypedDict(TypedDict, total=(False)):
    handSize: int
    queueLengthLimit: int
    queues: int


QueuingConfigurationUnion = Union[QueuingConfiguration, QueuingConfigurationTypedDict]


@attr.s(kw_only=True)
class PriorityLevelConfigurationCondition(K8sObject):
    lastTransitionTime: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "lastTransitionTime"}, default=OMIT
    )
    message: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "message"}, default=OMIT
    )
    reason: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "reason"}, default=OMIT
    )
    status: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "status"}, default=OMIT
    )
    type: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "type"}, default=OMIT
    )


class PriorityLevelConfigurationConditionTypedDict(TypedDict, total=(False)):
    lastTransitionTime: str
    message: str
    reason: str
    status: str
    type: str


PriorityLevelConfigurationConditionUnion = Union[
    PriorityLevelConfigurationCondition, PriorityLevelConfigurationConditionTypedDict
]


@attr.s(kw_only=True)
class PriorityLevelConfigurationReference(K8sObject):
    name: str = attr.ib(metadata={"yaml_name": "name"})


class PriorityLevelConfigurationReferenceTypedDict(TypedDict, total=(True)):
    name: str


PriorityLevelConfigurationReferenceUnion = Union[
    PriorityLevelConfigurationReference, PriorityLevelConfigurationReferenceTypedDict
]


@attr.s(kw_only=True)
class NonResourcePolicyRule(K8sObject):
    nonResourceURLs: Sequence[str] = attr.ib(metadata={"yaml_name": "nonResourceURLs"})
    verbs: Sequence[str] = attr.ib(metadata={"yaml_name": "verbs"})


class NonResourcePolicyRuleTypedDict(TypedDict, total=(True)):
    nonResourceURLs: Sequence[str]
    verbs: Sequence[str]


NonResourcePolicyRuleUnion = Union[
    NonResourcePolicyRule, NonResourcePolicyRuleTypedDict
]


@attr.s(kw_only=True)
class LimitResponse(K8sObject):
    type: str = attr.ib(metadata={"yaml_name": "type"})
    queuing: Union[
        None, OmitEnum, kdsl.flowcontrol.v1alpha1.QueuingConfiguration
    ] = attr.ib(
        metadata={"yaml_name": "queuing"},
        converter=kdsl.flowcontrol.v1alpha1_converters.optional_converter_QueuingConfiguration,
        default=OMIT,
    )


class LimitResponseOptionalTypedDict(TypedDict, total=(False)):
    queuing: kdsl.flowcontrol.v1alpha1.QueuingConfiguration


class LimitResponseTypedDict(LimitResponseOptionalTypedDict, total=(True)):
    type: str


LimitResponseUnion = Union[LimitResponse, LimitResponseTypedDict]


@attr.s(kw_only=True)
class PriorityLevelConfigurationStatus(K8sObject):
    conditions: Union[
        None,
        OmitEnum,
        Sequence[kdsl.flowcontrol.v1alpha1.PriorityLevelConfigurationCondition],
    ] = attr.ib(
        metadata={"yaml_name": "conditions"},
        converter=kdsl.flowcontrol.v1alpha1_converters.optional_list_converter_PriorityLevelConfigurationCondition,
        default=OMIT,
    )


class PriorityLevelConfigurationStatusTypedDict(TypedDict, total=(False)):
    conditions: Sequence[kdsl.flowcontrol.v1alpha1.PriorityLevelConfigurationCondition]


PriorityLevelConfigurationStatusUnion = Union[
    PriorityLevelConfigurationStatus, PriorityLevelConfigurationStatusTypedDict
]


@attr.s(kw_only=True)
class FlowDistinguisherMethod(K8sObject):
    type: str = attr.ib(metadata={"yaml_name": "type"})


class FlowDistinguisherMethodTypedDict(TypedDict, total=(True)):
    type: str


FlowDistinguisherMethodUnion = Union[
    FlowDistinguisherMethod, FlowDistinguisherMethodTypedDict
]


@attr.s(kw_only=True)
class FlowSchemaStatus(K8sObject):
    conditions: Union[
        None, OmitEnum, Sequence[kdsl.flowcontrol.v1alpha1.FlowSchemaCondition]
    ] = attr.ib(
        metadata={"yaml_name": "conditions"},
        converter=kdsl.flowcontrol.v1alpha1_converters.optional_list_converter_FlowSchemaCondition,
        default=OMIT,
    )


class FlowSchemaStatusTypedDict(TypedDict, total=(False)):
    conditions: Sequence[kdsl.flowcontrol.v1alpha1.FlowSchemaCondition]


FlowSchemaStatusUnion = Union[FlowSchemaStatus, FlowSchemaStatusTypedDict]


@attr.s(kw_only=True)
class PolicyRulesWithSubjects(K8sObject):
    subjects: Sequence[kdsl.flowcontrol.v1alpha1.Subject] = attr.ib(
        metadata={"yaml_name": "subjects"},
        converter=kdsl.flowcontrol.v1alpha1_converters.required_list_converter_Subject,
    )
    nonResourceRules: Union[
        None, OmitEnum, Sequence[kdsl.flowcontrol.v1alpha1.NonResourcePolicyRule]
    ] = attr.ib(
        metadata={"yaml_name": "nonResourceRules"},
        converter=kdsl.flowcontrol.v1alpha1_converters.optional_list_converter_NonResourcePolicyRule,
        default=OMIT,
    )
    resourceRules: Union[
        None, OmitEnum, Sequence[kdsl.flowcontrol.v1alpha1.ResourcePolicyRule]
    ] = attr.ib(
        metadata={"yaml_name": "resourceRules"},
        converter=kdsl.flowcontrol.v1alpha1_converters.optional_list_converter_ResourcePolicyRule,
        default=OMIT,
    )


class PolicyRulesWithSubjectsOptionalTypedDict(TypedDict, total=(False)):
    nonResourceRules: Sequence[kdsl.flowcontrol.v1alpha1.NonResourcePolicyRule]
    resourceRules: Sequence[kdsl.flowcontrol.v1alpha1.ResourcePolicyRule]


class PolicyRulesWithSubjectsTypedDict(
    PolicyRulesWithSubjectsOptionalTypedDict, total=(True)
):
    subjects: Sequence[kdsl.flowcontrol.v1alpha1.Subject]


PolicyRulesWithSubjectsUnion = Union[
    PolicyRulesWithSubjects, PolicyRulesWithSubjectsTypedDict
]


@attr.s(kw_only=True)
class UserSubject(K8sObject):
    name: str = attr.ib(metadata={"yaml_name": "name"})


class UserSubjectTypedDict(TypedDict, total=(True)):
    name: str


UserSubjectUnion = Union[UserSubject, UserSubjectTypedDict]
