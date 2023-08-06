from __future__ import annotations
from typing import Mapping, Sequence, Literal, Union
from kdsl.bases import OmitEnum, OMIT
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import kdsl.extensions.v1beta1


def required_converter_ReplicaSetSpec(
    value: kdsl.extensions.v1beta1.ReplicaSetSpecUnion,
) -> kdsl.extensions.v1beta1.ReplicaSetSpec:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.ReplicaSetSpec(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_DeploymentConditionItem(
    value: kdsl.extensions.v1beta1.DeploymentConditionItemUnion,
) -> kdsl.extensions.v1beta1.DeploymentConditionItem:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.DeploymentConditionItem(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_DeploymentStrategy(
    value: kdsl.extensions.v1beta1.DeploymentStrategyUnion,
) -> kdsl.extensions.v1beta1.DeploymentStrategy:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.DeploymentStrategy(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_RuntimeClassStrategyOptions(
    value: kdsl.extensions.v1beta1.RuntimeClassStrategyOptionsUnion,
) -> kdsl.extensions.v1beta1.RuntimeClassStrategyOptions:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.RuntimeClassStrategyOptions(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_DaemonSetStatus(
    value: kdsl.extensions.v1beta1.DaemonSetStatusUnion,
) -> kdsl.extensions.v1beta1.DaemonSetStatus:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.DaemonSetStatus(**value)
        if isinstance(value, dict)
        else value
    )


def optional_list_converter_NetworkPolicyEgressRule(
    value: Union[
        Sequence[kdsl.extensions.v1beta1.NetworkPolicyEgressRuleUnion], OmitEnum, None
    ]
) -> Union[Sequence[kdsl.extensions.v1beta1.NetworkPolicyEgressRule], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_NetworkPolicyEgressRule(x) for x in value]


def optional_mlist_converter_DeploymentConditionItem(
    value: Union[
        Mapping[str, kdsl.extensions.v1beta1.DeploymentConditionItemUnion],
        OmitEnum,
        None,
    ]
) -> Union[
    Mapping[str, kdsl.extensions.v1beta1.DeploymentConditionItem], OmitEnum, None
]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {
            k: required_converter_DeploymentConditionItem(v) for k, v in value.items()
        }


def optional_converter_NetworkPolicySpec(
    value: Union[kdsl.extensions.v1beta1.NetworkPolicySpecUnion, OmitEnum, None]
) -> Union[kdsl.extensions.v1beta1.NetworkPolicySpec, OmitEnum, None]:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.NetworkPolicySpec(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_PodSecurityPolicySpec(
    value: Union[kdsl.extensions.v1beta1.PodSecurityPolicySpecUnion, OmitEnum, None]
) -> Union[kdsl.extensions.v1beta1.PodSecurityPolicySpec, OmitEnum, None]:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.PodSecurityPolicySpec(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_DaemonSetUpdateStrategy(
    value: kdsl.extensions.v1beta1.DaemonSetUpdateStrategyUnion,
) -> kdsl.extensions.v1beta1.DaemonSetUpdateStrategy:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.DaemonSetUpdateStrategy(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_RunAsUserStrategyOptions(
    value: kdsl.extensions.v1beta1.RunAsUserStrategyOptionsUnion,
) -> kdsl.extensions.v1beta1.RunAsUserStrategyOptions:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.RunAsUserStrategyOptions(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_DeploymentStatus(
    value: kdsl.extensions.v1beta1.DeploymentStatusUnion,
) -> kdsl.extensions.v1beta1.DeploymentStatus:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.DeploymentStatus(**value)
        if isinstance(value, dict)
        else value
    )


def optional_mlist_converter_DaemonSetConditionItem(
    value: Union[
        Mapping[str, kdsl.extensions.v1beta1.DaemonSetConditionItemUnion],
        OmitEnum,
        None,
    ]
) -> Union[
    Mapping[str, kdsl.extensions.v1beta1.DaemonSetConditionItem], OmitEnum, None
]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {
            k: required_converter_DaemonSetConditionItem(v) for k, v in value.items()
        }


def optional_converter_AllowedCSIDriver(
    value: Union[kdsl.extensions.v1beta1.AllowedCSIDriverUnion, OmitEnum, None]
) -> Union[kdsl.extensions.v1beta1.AllowedCSIDriver, OmitEnum, None]:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.AllowedCSIDriver(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_NetworkPolicyPeer(
    value: Union[kdsl.extensions.v1beta1.NetworkPolicyPeerUnion, OmitEnum, None]
) -> Union[kdsl.extensions.v1beta1.NetworkPolicyPeer, OmitEnum, None]:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.NetworkPolicyPeer(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_HostPortRange(
    value: Union[kdsl.extensions.v1beta1.HostPortRangeUnion, OmitEnum, None]
) -> Union[kdsl.extensions.v1beta1.HostPortRange, OmitEnum, None]:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.HostPortRange(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_HTTPIngressPath(
    value: Union[kdsl.extensions.v1beta1.HTTPIngressPathUnion, OmitEnum, None]
) -> Union[kdsl.extensions.v1beta1.HTTPIngressPath, OmitEnum, None]:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.HTTPIngressPath(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_RollingUpdateDaemonSet(
    value: kdsl.extensions.v1beta1.RollingUpdateDaemonSetUnion,
) -> kdsl.extensions.v1beta1.RollingUpdateDaemonSet:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.RollingUpdateDaemonSet(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_NetworkPolicyIngressRule(
    value: Union[kdsl.extensions.v1beta1.NetworkPolicyIngressRuleUnion, OmitEnum, None]
) -> Union[kdsl.extensions.v1beta1.NetworkPolicyIngressRule, OmitEnum, None]:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.NetworkPolicyIngressRule(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_IngressBackend(
    value: Union[kdsl.extensions.v1beta1.IngressBackendUnion, OmitEnum, None]
) -> Union[kdsl.extensions.v1beta1.IngressBackend, OmitEnum, None]:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.IngressBackend(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_NetworkPolicyPort(
    value: kdsl.extensions.v1beta1.NetworkPolicyPortUnion,
) -> kdsl.extensions.v1beta1.NetworkPolicyPort:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.NetworkPolicyPort(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_DaemonSetConditionItem(
    value: kdsl.extensions.v1beta1.DaemonSetConditionItemUnion,
) -> kdsl.extensions.v1beta1.DaemonSetConditionItem:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.DaemonSetConditionItem(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_ReplicaSetSpec(
    value: Union[kdsl.extensions.v1beta1.ReplicaSetSpecUnion, OmitEnum, None]
) -> Union[kdsl.extensions.v1beta1.ReplicaSetSpec, OmitEnum, None]:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.ReplicaSetSpec(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_RollingUpdateDeployment(
    value: kdsl.extensions.v1beta1.RollingUpdateDeploymentUnion,
) -> kdsl.extensions.v1beta1.RollingUpdateDeployment:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.RollingUpdateDeployment(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_DeploymentConditionItem(
    value: Union[kdsl.extensions.v1beta1.DeploymentConditionItemUnion, OmitEnum, None]
) -> Union[kdsl.extensions.v1beta1.DeploymentConditionItem, OmitEnum, None]:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.DeploymentConditionItem(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_IngressSpec(
    value: kdsl.extensions.v1beta1.IngressSpecUnion,
) -> kdsl.extensions.v1beta1.IngressSpec:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.IngressSpec(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_RuntimeClassStrategyOptions(
    value: Union[
        kdsl.extensions.v1beta1.RuntimeClassStrategyOptionsUnion, OmitEnum, None
    ]
) -> Union[kdsl.extensions.v1beta1.RuntimeClassStrategyOptions, OmitEnum, None]:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.RuntimeClassStrategyOptions(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_ReplicaSetConditionItem(
    value: kdsl.extensions.v1beta1.ReplicaSetConditionItemUnion,
) -> kdsl.extensions.v1beta1.ReplicaSetConditionItem:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.ReplicaSetConditionItem(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_IngressRule(
    value: kdsl.extensions.v1beta1.IngressRuleUnion,
) -> kdsl.extensions.v1beta1.IngressRule:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.IngressRule(**value)
        if isinstance(value, dict)
        else value
    )


def optional_list_converter_AllowedHostPath(
    value: Union[Sequence[kdsl.extensions.v1beta1.AllowedHostPathUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.extensions.v1beta1.AllowedHostPath], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_AllowedHostPath(x) for x in value]


def required_converter_SELinuxStrategyOptions(
    value: kdsl.extensions.v1beta1.SELinuxStrategyOptionsUnion,
) -> kdsl.extensions.v1beta1.SELinuxStrategyOptions:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.SELinuxStrategyOptions(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_NetworkPolicyEgressRule(
    value: Union[kdsl.extensions.v1beta1.NetworkPolicyEgressRuleUnion, OmitEnum, None]
) -> Union[kdsl.extensions.v1beta1.NetworkPolicyEgressRule, OmitEnum, None]:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.NetworkPolicyEgressRule(**value)
        if isinstance(value, dict)
        else value
    )


def optional_list_converter_IDRange(
    value: Union[Sequence[kdsl.extensions.v1beta1.IDRangeUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.extensions.v1beta1.IDRange], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_IDRange(x) for x in value]


def optional_converter_DaemonSetUpdateStrategy(
    value: Union[kdsl.extensions.v1beta1.DaemonSetUpdateStrategyUnion, OmitEnum, None]
) -> Union[kdsl.extensions.v1beta1.DaemonSetUpdateStrategy, OmitEnum, None]:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.DaemonSetUpdateStrategy(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_AllowedHostPath(
    value: kdsl.extensions.v1beta1.AllowedHostPathUnion,
) -> kdsl.extensions.v1beta1.AllowedHostPath:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.AllowedHostPath(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_IngressStatus(
    value: Union[kdsl.extensions.v1beta1.IngressStatusUnion, OmitEnum, None]
) -> Union[kdsl.extensions.v1beta1.IngressStatus, OmitEnum, None]:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.IngressStatus(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_RollbackConfig(
    value: kdsl.extensions.v1beta1.RollbackConfigUnion,
) -> kdsl.extensions.v1beta1.RollbackConfig:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.RollbackConfig(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_IDRange(
    value: kdsl.extensions.v1beta1.IDRangeUnion,
) -> kdsl.extensions.v1beta1.IDRange:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.IDRange(**value) if isinstance(value, dict) else value
    )


def optional_converter_ReplicaSetStatus(
    value: Union[kdsl.extensions.v1beta1.ReplicaSetStatusUnion, OmitEnum, None]
) -> Union[kdsl.extensions.v1beta1.ReplicaSetStatus, OmitEnum, None]:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.ReplicaSetStatus(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_DeploymentStatus(
    value: Union[kdsl.extensions.v1beta1.DeploymentStatusUnion, OmitEnum, None]
) -> Union[kdsl.extensions.v1beta1.DeploymentStatus, OmitEnum, None]:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.DeploymentStatus(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_FSGroupStrategyOptions(
    value: Union[kdsl.extensions.v1beta1.FSGroupStrategyOptionsUnion, OmitEnum, None]
) -> Union[kdsl.extensions.v1beta1.FSGroupStrategyOptions, OmitEnum, None]:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.FSGroupStrategyOptions(**value)
        if isinstance(value, dict)
        else value
    )


def required_list_converter_HTTPIngressPath(
    value: Sequence[kdsl.extensions.v1beta1.HTTPIngressPathUnion],
) -> Sequence[kdsl.extensions.v1beta1.HTTPIngressPath]:
    return [required_converter_HTTPIngressPath(x) for x in value]


def required_converter_SupplementalGroupsStrategyOptions(
    value: kdsl.extensions.v1beta1.SupplementalGroupsStrategyOptionsUnion,
) -> kdsl.extensions.v1beta1.SupplementalGroupsStrategyOptions:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.SupplementalGroupsStrategyOptions(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_IPBlock(
    value: kdsl.extensions.v1beta1.IPBlockUnion,
) -> kdsl.extensions.v1beta1.IPBlock:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.IPBlock(**value) if isinstance(value, dict) else value
    )


def optional_converter_DeploymentSpec(
    value: Union[kdsl.extensions.v1beta1.DeploymentSpecUnion, OmitEnum, None]
) -> Union[kdsl.extensions.v1beta1.DeploymentSpec, OmitEnum, None]:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.DeploymentSpec(**value)
        if isinstance(value, dict)
        else value
    )


def optional_list_converter_NetworkPolicyPort(
    value: Union[
        Sequence[kdsl.extensions.v1beta1.NetworkPolicyPortUnion], OmitEnum, None
    ]
) -> Union[Sequence[kdsl.extensions.v1beta1.NetworkPolicyPort], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_NetworkPolicyPort(x) for x in value]


def required_converter_IngressTLS(
    value: kdsl.extensions.v1beta1.IngressTLSUnion,
) -> kdsl.extensions.v1beta1.IngressTLS:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.IngressTLS(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_HTTPIngressRuleValue(
    value: kdsl.extensions.v1beta1.HTTPIngressRuleValueUnion,
) -> kdsl.extensions.v1beta1.HTTPIngressRuleValue:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.HTTPIngressRuleValue(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_RollingUpdateDaemonSet(
    value: Union[kdsl.extensions.v1beta1.RollingUpdateDaemonSetUnion, OmitEnum, None]
) -> Union[kdsl.extensions.v1beta1.RollingUpdateDaemonSet, OmitEnum, None]:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.RollingUpdateDaemonSet(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_RunAsGroupStrategyOptions(
    value: Union[kdsl.extensions.v1beta1.RunAsGroupStrategyOptionsUnion, OmitEnum, None]
) -> Union[kdsl.extensions.v1beta1.RunAsGroupStrategyOptions, OmitEnum, None]:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.RunAsGroupStrategyOptions(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_DaemonSetSpec(
    value: Union[kdsl.extensions.v1beta1.DaemonSetSpecUnion, OmitEnum, None]
) -> Union[kdsl.extensions.v1beta1.DaemonSetSpec, OmitEnum, None]:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.DaemonSetSpec(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_AllowedCSIDriver(
    value: kdsl.extensions.v1beta1.AllowedCSIDriverUnion,
) -> kdsl.extensions.v1beta1.AllowedCSIDriver:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.AllowedCSIDriver(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_NetworkPolicyPeer(
    value: kdsl.extensions.v1beta1.NetworkPolicyPeerUnion,
) -> kdsl.extensions.v1beta1.NetworkPolicyPeer:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.NetworkPolicyPeer(**value)
        if isinstance(value, dict)
        else value
    )


def optional_list_converter_IngressRule(
    value: Union[Sequence[kdsl.extensions.v1beta1.IngressRuleUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.extensions.v1beta1.IngressRule], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_IngressRule(x) for x in value]


def optional_converter_DeploymentStrategy(
    value: Union[kdsl.extensions.v1beta1.DeploymentStrategyUnion, OmitEnum, None]
) -> Union[kdsl.extensions.v1beta1.DeploymentStrategy, OmitEnum, None]:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.DeploymentStrategy(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_DaemonSetConditionItem(
    value: Union[kdsl.extensions.v1beta1.DaemonSetConditionItemUnion, OmitEnum, None]
) -> Union[kdsl.extensions.v1beta1.DaemonSetConditionItem, OmitEnum, None]:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.DaemonSetConditionItem(**value)
        if isinstance(value, dict)
        else value
    )


def optional_list_converter_AllowedFlexVolume(
    value: Union[
        Sequence[kdsl.extensions.v1beta1.AllowedFlexVolumeUnion], OmitEnum, None
    ]
) -> Union[Sequence[kdsl.extensions.v1beta1.AllowedFlexVolume], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_AllowedFlexVolume(x) for x in value]


def optional_converter_DaemonSetStatus(
    value: Union[kdsl.extensions.v1beta1.DaemonSetStatusUnion, OmitEnum, None]
) -> Union[kdsl.extensions.v1beta1.DaemonSetStatus, OmitEnum, None]:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.DaemonSetStatus(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_AllowedFlexVolume(
    value: kdsl.extensions.v1beta1.AllowedFlexVolumeUnion,
) -> kdsl.extensions.v1beta1.AllowedFlexVolume:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.AllowedFlexVolume(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_IngressSpec(
    value: Union[kdsl.extensions.v1beta1.IngressSpecUnion, OmitEnum, None]
) -> Union[kdsl.extensions.v1beta1.IngressSpec, OmitEnum, None]:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.IngressSpec(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_ReplicaSetConditionItem(
    value: Union[kdsl.extensions.v1beta1.ReplicaSetConditionItemUnion, OmitEnum, None]
) -> Union[kdsl.extensions.v1beta1.ReplicaSetConditionItem, OmitEnum, None]:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.ReplicaSetConditionItem(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_RunAsUserStrategyOptions(
    value: Union[kdsl.extensions.v1beta1.RunAsUserStrategyOptionsUnion, OmitEnum, None]
) -> Union[kdsl.extensions.v1beta1.RunAsUserStrategyOptions, OmitEnum, None]:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.RunAsUserStrategyOptions(**value)
        if isinstance(value, dict)
        else value
    )


def optional_list_converter_IngressTLS(
    value: Union[Sequence[kdsl.extensions.v1beta1.IngressTLSUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.extensions.v1beta1.IngressTLS], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_IngressTLS(x) for x in value]


def optional_converter_SELinuxStrategyOptions(
    value: Union[kdsl.extensions.v1beta1.SELinuxStrategyOptionsUnion, OmitEnum, None]
) -> Union[kdsl.extensions.v1beta1.SELinuxStrategyOptions, OmitEnum, None]:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.SELinuxStrategyOptions(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_NetworkPolicySpec(
    value: kdsl.extensions.v1beta1.NetworkPolicySpecUnion,
) -> kdsl.extensions.v1beta1.NetworkPolicySpec:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.NetworkPolicySpec(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_AllowedHostPath(
    value: Union[kdsl.extensions.v1beta1.AllowedHostPathUnion, OmitEnum, None]
) -> Union[kdsl.extensions.v1beta1.AllowedHostPath, OmitEnum, None]:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.AllowedHostPath(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_PodSecurityPolicySpec(
    value: kdsl.extensions.v1beta1.PodSecurityPolicySpecUnion,
) -> kdsl.extensions.v1beta1.PodSecurityPolicySpec:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.PodSecurityPolicySpec(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_RollbackConfig(
    value: Union[kdsl.extensions.v1beta1.RollbackConfigUnion, OmitEnum, None]
) -> Union[kdsl.extensions.v1beta1.RollbackConfig, OmitEnum, None]:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.RollbackConfig(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_IDRange(
    value: Union[kdsl.extensions.v1beta1.IDRangeUnion, OmitEnum, None]
) -> Union[kdsl.extensions.v1beta1.IDRange, OmitEnum, None]:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.IDRange(**value) if isinstance(value, dict) else value
    )


def optional_list_converter_AllowedCSIDriver(
    value: Union[
        Sequence[kdsl.extensions.v1beta1.AllowedCSIDriverUnion], OmitEnum, None
    ]
) -> Union[Sequence[kdsl.extensions.v1beta1.AllowedCSIDriver], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_AllowedCSIDriver(x) for x in value]


def optional_list_converter_NetworkPolicyPeer(
    value: Union[
        Sequence[kdsl.extensions.v1beta1.NetworkPolicyPeerUnion], OmitEnum, None
    ]
) -> Union[Sequence[kdsl.extensions.v1beta1.NetworkPolicyPeer], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_NetworkPolicyPeer(x) for x in value]


def optional_list_converter_HostPortRange(
    value: Union[Sequence[kdsl.extensions.v1beta1.HostPortRangeUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.extensions.v1beta1.HostPortRange], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_HostPortRange(x) for x in value]


def optional_converter_SupplementalGroupsStrategyOptions(
    value: Union[
        kdsl.extensions.v1beta1.SupplementalGroupsStrategyOptionsUnion, OmitEnum, None
    ]
) -> Union[kdsl.extensions.v1beta1.SupplementalGroupsStrategyOptions, OmitEnum, None]:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.SupplementalGroupsStrategyOptions(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_IPBlock(
    value: Union[kdsl.extensions.v1beta1.IPBlockUnion, OmitEnum, None]
) -> Union[kdsl.extensions.v1beta1.IPBlock, OmitEnum, None]:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.IPBlock(**value) if isinstance(value, dict) else value
    )


def required_converter_HostPortRange(
    value: kdsl.extensions.v1beta1.HostPortRangeUnion,
) -> kdsl.extensions.v1beta1.HostPortRange:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.HostPortRange(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_HTTPIngressPath(
    value: kdsl.extensions.v1beta1.HTTPIngressPathUnion,
) -> kdsl.extensions.v1beta1.HTTPIngressPath:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.HTTPIngressPath(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_IngressTLS(
    value: Union[kdsl.extensions.v1beta1.IngressTLSUnion, OmitEnum, None]
) -> Union[kdsl.extensions.v1beta1.IngressTLS, OmitEnum, None]:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.IngressTLS(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_NetworkPolicyEgressRule(
    value: kdsl.extensions.v1beta1.NetworkPolicyEgressRuleUnion,
) -> kdsl.extensions.v1beta1.NetworkPolicyEgressRule:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.NetworkPolicyEgressRule(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_HTTPIngressRuleValue(
    value: Union[kdsl.extensions.v1beta1.HTTPIngressRuleValueUnion, OmitEnum, None]
) -> Union[kdsl.extensions.v1beta1.HTTPIngressRuleValue, OmitEnum, None]:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.HTTPIngressRuleValue(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_IngressStatus(
    value: kdsl.extensions.v1beta1.IngressStatusUnion,
) -> kdsl.extensions.v1beta1.IngressStatus:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.IngressStatus(**value)
        if isinstance(value, dict)
        else value
    )


def optional_mlist_converter_ReplicaSetConditionItem(
    value: Union[
        Mapping[str, kdsl.extensions.v1beta1.ReplicaSetConditionItemUnion],
        OmitEnum,
        None,
    ]
) -> Union[
    Mapping[str, kdsl.extensions.v1beta1.ReplicaSetConditionItem], OmitEnum, None
]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {
            k: required_converter_ReplicaSetConditionItem(v) for k, v in value.items()
        }


def optional_converter_NetworkPolicyPort(
    value: Union[kdsl.extensions.v1beta1.NetworkPolicyPortUnion, OmitEnum, None]
) -> Union[kdsl.extensions.v1beta1.NetworkPolicyPort, OmitEnum, None]:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.NetworkPolicyPort(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_ReplicaSetStatus(
    value: kdsl.extensions.v1beta1.ReplicaSetStatusUnion,
) -> kdsl.extensions.v1beta1.ReplicaSetStatus:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.ReplicaSetStatus(**value)
        if isinstance(value, dict)
        else value
    )


def optional_list_converter_NetworkPolicyIngressRule(
    value: Union[
        Sequence[kdsl.extensions.v1beta1.NetworkPolicyIngressRuleUnion], OmitEnum, None
    ]
) -> Union[Sequence[kdsl.extensions.v1beta1.NetworkPolicyIngressRule], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_NetworkPolicyIngressRule(x) for x in value]


def required_converter_FSGroupStrategyOptions(
    value: kdsl.extensions.v1beta1.FSGroupStrategyOptionsUnion,
) -> kdsl.extensions.v1beta1.FSGroupStrategyOptions:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.FSGroupStrategyOptions(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_NetworkPolicyIngressRule(
    value: kdsl.extensions.v1beta1.NetworkPolicyIngressRuleUnion,
) -> kdsl.extensions.v1beta1.NetworkPolicyIngressRule:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.NetworkPolicyIngressRule(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_DeploymentSpec(
    value: kdsl.extensions.v1beta1.DeploymentSpecUnion,
) -> kdsl.extensions.v1beta1.DeploymentSpec:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.DeploymentSpec(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_IngressBackend(
    value: kdsl.extensions.v1beta1.IngressBackendUnion,
) -> kdsl.extensions.v1beta1.IngressBackend:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.IngressBackend(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_RollingUpdateDeployment(
    value: Union[kdsl.extensions.v1beta1.RollingUpdateDeploymentUnion, OmitEnum, None]
) -> Union[kdsl.extensions.v1beta1.RollingUpdateDeployment, OmitEnum, None]:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.RollingUpdateDeployment(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_RunAsGroupStrategyOptions(
    value: kdsl.extensions.v1beta1.RunAsGroupStrategyOptionsUnion,
) -> kdsl.extensions.v1beta1.RunAsGroupStrategyOptions:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.RunAsGroupStrategyOptions(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_DaemonSetSpec(
    value: kdsl.extensions.v1beta1.DaemonSetSpecUnion,
) -> kdsl.extensions.v1beta1.DaemonSetSpec:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.DaemonSetSpec(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_IngressRule(
    value: Union[kdsl.extensions.v1beta1.IngressRuleUnion, OmitEnum, None]
) -> Union[kdsl.extensions.v1beta1.IngressRule, OmitEnum, None]:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.IngressRule(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_AllowedFlexVolume(
    value: Union[kdsl.extensions.v1beta1.AllowedFlexVolumeUnion, OmitEnum, None]
) -> Union[kdsl.extensions.v1beta1.AllowedFlexVolume, OmitEnum, None]:
    import kdsl.extensions.v1beta1

    return (
        kdsl.extensions.v1beta1.AllowedFlexVolume(**value)
        if isinstance(value, dict)
        else value
    )
