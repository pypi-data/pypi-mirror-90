from __future__ import annotations
import kdsl.core.v1
import kdsl.core.v1_converters
import kdsl.rbac.v1_converters
import kdsl.rbac.v1
import attr
from typing import Mapping, ClassVar, Optional, Any, Sequence, TypedDict, Union
from kdsl.bases import OmitEnum, K8sObject, OMIT, K8sResource


@attr.s(kw_only=True)
class ClusterRole(K8sResource):
    apiVersion: ClassVar[str] = "rbac.authorization.k8s.io/v1"
    kind: ClassVar[str] = "ClusterRole"
    aggregationRule: Union[None, OmitEnum, kdsl.rbac.v1.AggregationRule] = attr.ib(
        metadata={"yaml_name": "aggregationRule"},
        converter=kdsl.rbac.v1_converters.optional_converter_AggregationRule,
        default=OMIT,
    )
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    rules: Union[None, OmitEnum, Sequence[kdsl.rbac.v1.PolicyRule]] = attr.ib(
        metadata={"yaml_name": "rules"},
        converter=kdsl.rbac.v1_converters.optional_list_converter_PolicyRule,
        default=OMIT,
    )


@attr.s(kw_only=True)
class RoleBinding(K8sResource):
    apiVersion: ClassVar[str] = "rbac.authorization.k8s.io/v1"
    kind: ClassVar[str] = "RoleBinding"
    roleRef: kdsl.rbac.v1.RoleRef = attr.ib(
        metadata={"yaml_name": "roleRef"},
        converter=kdsl.rbac.v1_converters.required_converter_RoleRef,
    )
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    subjects: Union[None, OmitEnum, Sequence[kdsl.rbac.v1.Subject]] = attr.ib(
        metadata={"yaml_name": "subjects"},
        converter=kdsl.rbac.v1_converters.optional_list_converter_Subject,
        default=OMIT,
    )


@attr.s(kw_only=True)
class PolicyRule(K8sObject):
    verbs: Sequence[str] = attr.ib(metadata={"yaml_name": "verbs"})
    apiGroups: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "apiGroups"}, default=OMIT
    )
    nonResourceURLs: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "nonResourceURLs"}, default=OMIT
    )
    resourceNames: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "resourceNames"}, default=OMIT
    )
    resources: Union[None, OmitEnum, Sequence[str]] = attr.ib(
        metadata={"yaml_name": "resources"}, default=OMIT
    )


class PolicyRuleOptionalTypedDict(TypedDict, total=(False)):
    apiGroups: Sequence[str]
    nonResourceURLs: Sequence[str]
    resourceNames: Sequence[str]
    resources: Sequence[str]


class PolicyRuleTypedDict(PolicyRuleOptionalTypedDict, total=(True)):
    verbs: Sequence[str]


PolicyRuleUnion = Union[PolicyRule, PolicyRuleTypedDict]


@attr.s(kw_only=True)
class RoleRef(K8sObject):
    apiGroup: str = attr.ib(metadata={"yaml_name": "apiGroup"})
    kind: str = attr.ib(metadata={"yaml_name": "kind"})
    name: str = attr.ib(metadata={"yaml_name": "name"})


class RoleRefTypedDict(TypedDict, total=(True)):
    apiGroup: str
    kind: str
    name: str


RoleRefUnion = Union[RoleRef, RoleRefTypedDict]


@attr.s(kw_only=True)
class Role(K8sResource):
    apiVersion: ClassVar[str] = "rbac.authorization.k8s.io/v1"
    kind: ClassVar[str] = "Role"
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    rules: Union[None, OmitEnum, Sequence[kdsl.rbac.v1.PolicyRule]] = attr.ib(
        metadata={"yaml_name": "rules"},
        converter=kdsl.rbac.v1_converters.optional_list_converter_PolicyRule,
        default=OMIT,
    )


@attr.s(kw_only=True)
class AggregationRule(K8sObject):
    clusterRoleSelectors: Union[
        None, OmitEnum, Sequence[kdsl.core.v1.LabelSelector]
    ] = attr.ib(
        metadata={"yaml_name": "clusterRoleSelectors"},
        converter=kdsl.core.v1_converters.optional_list_converter_LabelSelector,
        default=OMIT,
    )


class AggregationRuleTypedDict(TypedDict, total=(False)):
    clusterRoleSelectors: Sequence[kdsl.core.v1.LabelSelector]


AggregationRuleUnion = Union[AggregationRule, AggregationRuleTypedDict]


@attr.s(kw_only=True)
class ClusterRoleBinding(K8sResource):
    apiVersion: ClassVar[str] = "rbac.authorization.k8s.io/v1"
    kind: ClassVar[str] = "ClusterRoleBinding"
    roleRef: kdsl.rbac.v1.RoleRef = attr.ib(
        metadata={"yaml_name": "roleRef"},
        converter=kdsl.rbac.v1_converters.required_converter_RoleRef,
    )
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    subjects: Union[None, OmitEnum, Sequence[kdsl.rbac.v1.Subject]] = attr.ib(
        metadata={"yaml_name": "subjects"},
        converter=kdsl.rbac.v1_converters.optional_list_converter_Subject,
        default=OMIT,
    )


@attr.s(kw_only=True)
class Subject(K8sObject):
    kind: str = attr.ib(metadata={"yaml_name": "kind"})
    name: str = attr.ib(metadata={"yaml_name": "name"})
    apiGroup: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "apiGroup"}, default=OMIT
    )
    namespace: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "namespace"}, default=OMIT
    )


class SubjectOptionalTypedDict(TypedDict, total=(False)):
    apiGroup: str
    namespace: str


class SubjectTypedDict(SubjectOptionalTypedDict, total=(True)):
    kind: str
    name: str


SubjectUnion = Union[Subject, SubjectTypedDict]
