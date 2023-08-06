from __future__ import annotations
from typing import Mapping, Sequence, Literal, Union
from kdsl.bases import OmitEnum, OMIT
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import kdsl.core.v1


def optional_converter_SecretEnvSource(
    value: Union[kdsl.core.v1.SecretEnvSourceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.SecretEnvSource, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.SecretEnvSource(**value) if isinstance(value, dict) else value


def optional_converter_PersistentVolumeSpec(
    value: Union[kdsl.core.v1.PersistentVolumeSpecUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.PersistentVolumeSpec, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.PersistentVolumeSpec(**value) if isinstance(value, dict) else value
    )


def optional_mlist_converter_VolumeMountItem(
    value: Union[Mapping[str, kdsl.core.v1.VolumeMountItemUnion], OmitEnum, None]
) -> Union[Mapping[str, kdsl.core.v1.VolumeMountItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {k: required_converter_VolumeMountItem(v) for k, v in value.items()}


def required_converter_ReplicationControllerSpec(
    value: kdsl.core.v1.ReplicationControllerSpecUnion,
) -> kdsl.core.v1.ReplicationControllerSpec:
    import kdsl.core.v1

    return (
        kdsl.core.v1.ReplicationControllerSpec(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_CSIPersistentVolumeSource(
    value: kdsl.core.v1.CSIPersistentVolumeSourceUnion,
) -> kdsl.core.v1.CSIPersistentVolumeSource:
    import kdsl.core.v1

    return (
        kdsl.core.v1.CSIPersistentVolumeSource(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_AzureDiskVolumeSource(
    value: Union[kdsl.core.v1.AzureDiskVolumeSourceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.AzureDiskVolumeSource, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.AzureDiskVolumeSource(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_LocalVolumeSource(
    value: Union[kdsl.core.v1.LocalVolumeSourceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.LocalVolumeSource, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.LocalVolumeSource(**value) if isinstance(value, dict) else value


def required_converter_DeleteOptions(
    value: kdsl.core.v1.DeleteOptionsUnion,
) -> kdsl.core.v1.DeleteOptions:
    import kdsl.core.v1

    return kdsl.core.v1.DeleteOptions(**value) if isinstance(value, dict) else value


def optional_converter_PodConditionItem(
    value: Union[kdsl.core.v1.PodConditionItemUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.PodConditionItem, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.PodConditionItem(**value) if isinstance(value, dict) else value


def optional_converter_ResourceQuotaSpec(
    value: Union[kdsl.core.v1.ResourceQuotaSpecUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.ResourceQuotaSpec, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.ResourceQuotaSpec(**value) if isinstance(value, dict) else value


def required_converter_NodeSystemInfo(
    value: kdsl.core.v1.NodeSystemInfoUnion,
) -> kdsl.core.v1.NodeSystemInfo:
    import kdsl.core.v1

    return kdsl.core.v1.NodeSystemInfo(**value) if isinstance(value, dict) else value


def optional_list_converter_PodDNSConfigOption(
    value: Union[Sequence[kdsl.core.v1.PodDNSConfigOptionUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.core.v1.PodDNSConfigOption], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_PodDNSConfigOption(x) for x in value]


def optional_converter_NamespaceSpec(
    value: Union[kdsl.core.v1.NamespaceSpecUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.NamespaceSpec, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.NamespaceSpec(**value) if isinstance(value, dict) else value


def optional_converter_LabelSelectorRequirement(
    value: Union[kdsl.core.v1.LabelSelectorRequirementUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.LabelSelectorRequirement, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.LabelSelectorRequirement(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_TCPSocketAction(
    value: Union[kdsl.core.v1.TCPSocketActionUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.TCPSocketAction, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.TCPSocketAction(**value) if isinstance(value, dict) else value


def optional_mlist_converter_NodeAddressItem(
    value: Union[Mapping[str, kdsl.core.v1.NodeAddressItemUnion], OmitEnum, None]
) -> Union[Mapping[str, kdsl.core.v1.NodeAddressItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {k: required_converter_NodeAddressItem(v) for k, v in value.items()}


def required_converter_DownwardAPIProjection(
    value: kdsl.core.v1.DownwardAPIProjectionUnion,
) -> kdsl.core.v1.DownwardAPIProjection:
    import kdsl.core.v1

    return (
        kdsl.core.v1.DownwardAPIProjection(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_ConfigMapVolumeSource(
    value: Union[kdsl.core.v1.ConfigMapVolumeSourceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.ConfigMapVolumeSource, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.ConfigMapVolumeSource(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_VolumeDeviceItem(
    value: kdsl.core.v1.VolumeDeviceItemUnion,
) -> kdsl.core.v1.VolumeDeviceItem:
    import kdsl.core.v1

    return kdsl.core.v1.VolumeDeviceItem(**value) if isinstance(value, dict) else value


def optional_converter_ObjectReferenceItem(
    value: Union[kdsl.core.v1.ObjectReferenceItemUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.ObjectReferenceItem, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.ObjectReferenceItem(**value) if isinstance(value, dict) else value
    )


def required_converter_NodeSelector(
    value: kdsl.core.v1.NodeSelectorUnion,
) -> kdsl.core.v1.NodeSelector:
    import kdsl.core.v1

    return kdsl.core.v1.NodeSelector(**value) if isinstance(value, dict) else value


def required_converter_Handler(
    value: kdsl.core.v1.HandlerUnion,
) -> kdsl.core.v1.Handler:
    import kdsl.core.v1

    return kdsl.core.v1.Handler(**value) if isinstance(value, dict) else value


def optional_converter_HostAliasItem(
    value: Union[kdsl.core.v1.HostAliasItemUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.HostAliasItem, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.HostAliasItem(**value) if isinstance(value, dict) else value


def optional_converter_ResourceRequirements(
    value: Union[kdsl.core.v1.ResourceRequirementsUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.ResourceRequirements, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.ResourceRequirements(**value) if isinstance(value, dict) else value
    )


def optional_converter_PodDNSConfigOption(
    value: Union[kdsl.core.v1.PodDNSConfigOptionUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.PodDNSConfigOption, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.PodDNSConfigOption(**value) if isinstance(value, dict) else value
    )


def required_converter_ProjectedVolumeSource(
    value: kdsl.core.v1.ProjectedVolumeSourceUnion,
) -> kdsl.core.v1.ProjectedVolumeSource:
    import kdsl.core.v1

    return (
        kdsl.core.v1.ProjectedVolumeSource(**value)
        if isinstance(value, dict)
        else value
    )


def optional_list_converter_HTTPHeader(
    value: Union[Sequence[kdsl.core.v1.HTTPHeaderUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.core.v1.HTTPHeader], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_HTTPHeader(x) for x in value]


def optional_converter_VolumeProjection(
    value: Union[kdsl.core.v1.VolumeProjectionUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.VolumeProjection, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.VolumeProjection(**value) if isinstance(value, dict) else value


def optional_converter_ISCSIVolumeSource(
    value: Union[kdsl.core.v1.ISCSIVolumeSourceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.ISCSIVolumeSource, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.ISCSIVolumeSource(**value) if isinstance(value, dict) else value


def optional_mlist_converter_NodeConditionItem(
    value: Union[Mapping[str, kdsl.core.v1.NodeConditionItemUnion], OmitEnum, None]
) -> Union[Mapping[str, kdsl.core.v1.NodeConditionItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {k: required_converter_NodeConditionItem(v) for k, v in value.items()}


def required_converter_HTTPGetAction(
    value: kdsl.core.v1.HTTPGetActionUnion,
) -> kdsl.core.v1.HTTPGetAction:
    import kdsl.core.v1

    return kdsl.core.v1.HTTPGetAction(**value) if isinstance(value, dict) else value


def required_converter_WindowsSecurityContextOptions(
    value: kdsl.core.v1.WindowsSecurityContextOptionsUnion,
) -> kdsl.core.v1.WindowsSecurityContextOptions:
    import kdsl.core.v1

    return (
        kdsl.core.v1.WindowsSecurityContextOptions(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_Preconditions(
    value: Union[kdsl.core.v1.PreconditionsUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.Preconditions, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.Preconditions(**value) if isinstance(value, dict) else value


def optional_mlist_converter_VolumeDeviceItem(
    value: Union[Mapping[str, kdsl.core.v1.VolumeDeviceItemUnion], OmitEnum, None]
) -> Union[Mapping[str, kdsl.core.v1.VolumeDeviceItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {k: required_converter_VolumeDeviceItem(v) for k, v in value.items()}


def optional_mlist_converter_ObjectReferenceItem(
    value: Union[Mapping[str, kdsl.core.v1.ObjectReferenceItemUnion], OmitEnum, None]
) -> Union[Mapping[str, kdsl.core.v1.ObjectReferenceItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {k: required_converter_ObjectReferenceItem(v) for k, v in value.items()}


def optional_converter_ExecAction(
    value: Union[kdsl.core.v1.ExecActionUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.ExecAction, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.ExecAction(**value) if isinstance(value, dict) else value


def optional_converter_RBDPersistentVolumeSource(
    value: Union[kdsl.core.v1.RBDPersistentVolumeSourceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.RBDPersistentVolumeSource, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.RBDPersistentVolumeSource(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_NodeSpec(
    value: kdsl.core.v1.NodeSpecUnion,
) -> kdsl.core.v1.NodeSpec:
    import kdsl.core.v1

    return kdsl.core.v1.NodeSpec(**value) if isinstance(value, dict) else value


def required_converter_StorageOSVolumeSource(
    value: kdsl.core.v1.StorageOSVolumeSourceUnion,
) -> kdsl.core.v1.StorageOSVolumeSource:
    import kdsl.core.v1

    return (
        kdsl.core.v1.StorageOSVolumeSource(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_ServiceAccountTokenProjection(
    value: kdsl.core.v1.ServiceAccountTokenProjectionUnion,
) -> kdsl.core.v1.ServiceAccountTokenProjection:
    import kdsl.core.v1

    return (
        kdsl.core.v1.ServiceAccountTokenProjection(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_PodTemplateSpec(
    value: Union[kdsl.core.v1.PodTemplateSpecUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.PodTemplateSpec, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.PodTemplateSpec(**value) if isinstance(value, dict) else value


def optional_converter_NodeAffinity(
    value: Union[kdsl.core.v1.NodeAffinityUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.NodeAffinity, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.NodeAffinity(**value) if isinstance(value, dict) else value


def required_converter_ScopeSelector(
    value: kdsl.core.v1.ScopeSelectorUnion,
) -> kdsl.core.v1.ScopeSelector:
    import kdsl.core.v1

    return kdsl.core.v1.ScopeSelector(**value) if isinstance(value, dict) else value


def required_converter_EnvVarItem(
    value: kdsl.core.v1.EnvVarItemUnion,
) -> kdsl.core.v1.EnvVarItem:
    import kdsl.core.v1

    return kdsl.core.v1.EnvVarItem(**value) if isinstance(value, dict) else value


def optional_converter_DownwardAPIVolumeSource(
    value: Union[kdsl.core.v1.DownwardAPIVolumeSourceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.DownwardAPIVolumeSource, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.DownwardAPIVolumeSource(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_ConfigMapEnvSource(
    value: Union[kdsl.core.v1.ConfigMapEnvSourceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.ConfigMapEnvSource, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.ConfigMapEnvSource(**value) if isinstance(value, dict) else value
    )


def optional_list_converter_ContainerImage(
    value: Union[Sequence[kdsl.core.v1.ContainerImageUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.core.v1.ContainerImage], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_ContainerImage(x) for x in value]


def required_converter_ContainerImage(
    value: kdsl.core.v1.ContainerImageUnion,
) -> kdsl.core.v1.ContainerImage:
    import kdsl.core.v1

    return kdsl.core.v1.ContainerImage(**value) if isinstance(value, dict) else value


def required_converter_ContainerPortItem(
    value: kdsl.core.v1.ContainerPortItemUnion,
) -> kdsl.core.v1.ContainerPortItem:
    import kdsl.core.v1

    return kdsl.core.v1.ContainerPortItem(**value) if isinstance(value, dict) else value


def optional_converter_DownwardAPIProjection(
    value: Union[kdsl.core.v1.DownwardAPIProjectionUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.DownwardAPIProjection, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.DownwardAPIProjection(**value)
        if isinstance(value, dict)
        else value
    )


def required_list_converter_LimitRangeItem(
    value: Sequence[kdsl.core.v1.LimitRangeItemUnion],
) -> Sequence[kdsl.core.v1.LimitRangeItem]:
    return [required_converter_LimitRangeItem(x) for x in value]


def optional_converter_VolumeDeviceItem(
    value: Union[kdsl.core.v1.VolumeDeviceItemUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.VolumeDeviceItem, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.VolumeDeviceItem(**value) if isinstance(value, dict) else value


def required_converter_FCVolumeSource(
    value: kdsl.core.v1.FCVolumeSourceUnion,
) -> kdsl.core.v1.FCVolumeSource:
    import kdsl.core.v1

    return kdsl.core.v1.FCVolumeSource(**value) if isinstance(value, dict) else value


def required_converter_PortworxVolumeSource(
    value: kdsl.core.v1.PortworxVolumeSourceUnion,
) -> kdsl.core.v1.PortworxVolumeSource:
    import kdsl.core.v1

    return (
        kdsl.core.v1.PortworxVolumeSource(**value) if isinstance(value, dict) else value
    )


def required_converter_PodReadinessGate(
    value: kdsl.core.v1.PodReadinessGateUnion,
) -> kdsl.core.v1.PodReadinessGate:
    import kdsl.core.v1

    return kdsl.core.v1.PodReadinessGate(**value) if isinstance(value, dict) else value


def required_converter_ContainerStateTerminated(
    value: kdsl.core.v1.ContainerStateTerminatedUnion,
) -> kdsl.core.v1.ContainerStateTerminated:
    import kdsl.core.v1

    return (
        kdsl.core.v1.ContainerStateTerminated(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_ContainerState(
    value: Union[kdsl.core.v1.ContainerStateUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.ContainerState, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.ContainerState(**value) if isinstance(value, dict) else value


def required_converter_ContainerStateWaiting(
    value: kdsl.core.v1.ContainerStateWaitingUnion,
) -> kdsl.core.v1.ContainerStateWaiting:
    import kdsl.core.v1

    return (
        kdsl.core.v1.ContainerStateWaiting(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_Handler(
    value: Union[kdsl.core.v1.HandlerUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.Handler, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.Handler(**value) if isinstance(value, dict) else value


def optional_mlist_converter_HostAliasItem(
    value: Union[Mapping[str, kdsl.core.v1.HostAliasItemUnion], OmitEnum, None]
) -> Union[Mapping[str, kdsl.core.v1.HostAliasItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {k: required_converter_HostAliasItem(v) for k, v in value.items()}


def optional_converter_HTTPGetAction(
    value: Union[kdsl.core.v1.HTTPGetActionUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.HTTPGetAction, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.HTTPGetAction(**value) if isinstance(value, dict) else value


def optional_converter_HTTPHeader(
    value: Union[kdsl.core.v1.HTTPHeaderUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.HTTPHeader, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.HTTPHeader(**value) if isinstance(value, dict) else value


def optional_converter_NodeSpec(
    value: Union[kdsl.core.v1.NodeSpecUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.NodeSpec, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.NodeSpec(**value) if isinstance(value, dict) else value


def optional_converter_CephFSPersistentVolumeSource(
    value: Union[kdsl.core.v1.CephFSPersistentVolumeSourceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.CephFSPersistentVolumeSource, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.CephFSPersistentVolumeSource(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_ServicePortItem(
    value: kdsl.core.v1.ServicePortItemUnion,
) -> kdsl.core.v1.ServicePortItem:
    import kdsl.core.v1

    return kdsl.core.v1.ServicePortItem(**value) if isinstance(value, dict) else value


def required_converter_FlexVolumeSource(
    value: kdsl.core.v1.FlexVolumeSourceUnion,
) -> kdsl.core.v1.FlexVolumeSource:
    import kdsl.core.v1

    return kdsl.core.v1.FlexVolumeSource(**value) if isinstance(value, dict) else value


def optional_converter_EnvVarItem(
    value: Union[kdsl.core.v1.EnvVarItemUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.EnvVarItem, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.EnvVarItem(**value) if isinstance(value, dict) else value


def required_converter_ResourceFieldSelector(
    value: kdsl.core.v1.ResourceFieldSelectorUnion,
) -> kdsl.core.v1.ResourceFieldSelector:
    import kdsl.core.v1

    return (
        kdsl.core.v1.ResourceFieldSelector(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_SessionAffinityConfig(
    value: kdsl.core.v1.SessionAffinityConfigUnion,
) -> kdsl.core.v1.SessionAffinityConfig:
    import kdsl.core.v1

    return (
        kdsl.core.v1.SessionAffinityConfig(**value)
        if isinstance(value, dict)
        else value
    )


def optional_list_converter_TopologySelectorLabelRequirement(
    value: Union[
        Sequence[kdsl.core.v1.TopologySelectorLabelRequirementUnion], OmitEnum, None
    ]
) -> Union[Sequence[kdsl.core.v1.TopologySelectorLabelRequirement], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_TopologySelectorLabelRequirement(x) for x in value]


def required_converter_EventSource(
    value: kdsl.core.v1.EventSourceUnion,
) -> kdsl.core.v1.EventSource:
    import kdsl.core.v1

    return kdsl.core.v1.EventSource(**value) if isinstance(value, dict) else value


def optional_converter_NodeDaemonEndpoints(
    value: Union[kdsl.core.v1.NodeDaemonEndpointsUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.NodeDaemonEndpoints, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.NodeDaemonEndpoints(**value) if isinstance(value, dict) else value
    )


def required_converter_EnvVar(value: kdsl.core.v1.EnvVarUnion) -> kdsl.core.v1.EnvVar:
    import kdsl.core.v1

    return kdsl.core.v1.EnvVar(**value) if isinstance(value, dict) else value


def required_converter_PodAntiAffinity(
    value: kdsl.core.v1.PodAntiAffinityUnion,
) -> kdsl.core.v1.PodAntiAffinity:
    import kdsl.core.v1

    return kdsl.core.v1.PodAntiAffinity(**value) if isinstance(value, dict) else value


def optional_converter_ContainerImage(
    value: Union[kdsl.core.v1.ContainerImageUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.ContainerImage, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.ContainerImage(**value) if isinstance(value, dict) else value


def optional_mlist_converter_PersistentVolumeClaimConditionItem(
    value: Union[
        Mapping[str, kdsl.core.v1.PersistentVolumeClaimConditionItemUnion],
        OmitEnum,
        None,
    ]
) -> Union[
    Mapping[str, kdsl.core.v1.PersistentVolumeClaimConditionItem], OmitEnum, None
]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {
            k: required_converter_PersistentVolumeClaimConditionItem(v)
            for k, v in value.items()
        }


def optional_list_converter_KeyToPath(
    value: Union[Sequence[kdsl.core.v1.KeyToPathUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.core.v1.KeyToPath], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_KeyToPath(x) for x in value]


def optional_list_converter_EndpointPort(
    value: Union[Sequence[kdsl.core.v1.EndpointPortUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.core.v1.EndpointPort], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_EndpointPort(x) for x in value]


def optional_converter_ContainerPortItem(
    value: Union[kdsl.core.v1.ContainerPortItemUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.ContainerPortItem, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.ContainerPortItem(**value) if isinstance(value, dict) else value


def optional_converter_ReplicationControllerStatus(
    value: Union[kdsl.core.v1.ReplicationControllerStatusUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.ReplicationControllerStatus, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.ReplicationControllerStatus(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_ObjectMeta(
    value: Union[kdsl.core.v1.ObjectMetaUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.ObjectMeta, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.ObjectMeta(**value) if isinstance(value, dict) else value


def optional_list_converter_EndpointSubset(
    value: Union[Sequence[kdsl.core.v1.EndpointSubsetUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.core.v1.EndpointSubset], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_EndpointSubset(x) for x in value]


def optional_list_converter_LocalObjectReference(
    value: Union[Sequence[kdsl.core.v1.LocalObjectReferenceUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.core.v1.LocalObjectReference], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_LocalObjectReference(x) for x in value]


def required_converter_ScaleIOPersistentVolumeSource(
    value: kdsl.core.v1.ScaleIOPersistentVolumeSourceUnion,
) -> kdsl.core.v1.ScaleIOPersistentVolumeSource:
    import kdsl.core.v1

    return (
        kdsl.core.v1.ScaleIOPersistentVolumeSource(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_PortworxVolumeSource(
    value: Union[kdsl.core.v1.PortworxVolumeSourceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.PortworxVolumeSource, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.PortworxVolumeSource(**value) if isinstance(value, dict) else value
    )


def required_converter_LabelSelector(
    value: kdsl.core.v1.LabelSelectorUnion,
) -> kdsl.core.v1.LabelSelector:
    import kdsl.core.v1

    return kdsl.core.v1.LabelSelector(**value) if isinstance(value, dict) else value


def required_converter_LimitRangeItem(
    value: kdsl.core.v1.LimitRangeItemUnion,
) -> kdsl.core.v1.LimitRangeItem:
    import kdsl.core.v1

    return kdsl.core.v1.LimitRangeItem(**value) if isinstance(value, dict) else value


def optional_converter_ContainerStateTerminated(
    value: Union[kdsl.core.v1.ContainerStateTerminatedUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.ContainerStateTerminated, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.ContainerStateTerminated(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_ContainerStateWaiting(
    value: Union[kdsl.core.v1.ContainerStateWaitingUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.ContainerStateWaiting, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.ContainerStateWaiting(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_ScopedResourceSelectorRequirement(
    value: kdsl.core.v1.ScopedResourceSelectorRequirementUnion,
) -> kdsl.core.v1.ScopedResourceSelectorRequirement:
    import kdsl.core.v1

    return (
        kdsl.core.v1.ScopedResourceSelectorRequirement(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_AWSElasticBlockStoreVolumeSource(
    value: kdsl.core.v1.AWSElasticBlockStoreVolumeSourceUnion,
) -> kdsl.core.v1.AWSElasticBlockStoreVolumeSource:
    import kdsl.core.v1

    return (
        kdsl.core.v1.AWSElasticBlockStoreVolumeSource(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_QuobyteVolumeSource(
    value: kdsl.core.v1.QuobyteVolumeSourceUnion,
) -> kdsl.core.v1.QuobyteVolumeSource:
    import kdsl.core.v1

    return (
        kdsl.core.v1.QuobyteVolumeSource(**value) if isinstance(value, dict) else value
    )


def required_converter_RBDVolumeSource(
    value: kdsl.core.v1.RBDVolumeSourceUnion,
) -> kdsl.core.v1.RBDVolumeSource:
    import kdsl.core.v1

    return kdsl.core.v1.RBDVolumeSource(**value) if isinstance(value, dict) else value


def required_converter_SecretProjection(
    value: kdsl.core.v1.SecretProjectionUnion,
) -> kdsl.core.v1.SecretProjection:
    import kdsl.core.v1

    return kdsl.core.v1.SecretProjection(**value) if isinstance(value, dict) else value


def required_converter_ContainerStatus(
    value: kdsl.core.v1.ContainerStatusUnion,
) -> kdsl.core.v1.ContainerStatus:
    import kdsl.core.v1

    return kdsl.core.v1.ContainerStatus(**value) if isinstance(value, dict) else value


def required_converter_SELinuxOptions(
    value: kdsl.core.v1.SELinuxOptionsUnion,
) -> kdsl.core.v1.SELinuxOptions:
    import kdsl.core.v1

    return kdsl.core.v1.SELinuxOptions(**value) if isinstance(value, dict) else value


def optional_converter_Affinity(
    value: Union[kdsl.core.v1.AffinityUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.Affinity, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.Affinity(**value) if isinstance(value, dict) else value


def optional_converter_EphemeralContainerItem(
    value: Union[kdsl.core.v1.EphemeralContainerItemUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.EphemeralContainerItem, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.EphemeralContainerItem(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_GCEPersistentDiskVolumeSource(
    value: kdsl.core.v1.GCEPersistentDiskVolumeSourceUnion,
) -> kdsl.core.v1.GCEPersistentDiskVolumeSource:
    import kdsl.core.v1

    return (
        kdsl.core.v1.GCEPersistentDiskVolumeSource(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_ScaleIOVolumeSource(
    value: kdsl.core.v1.ScaleIOVolumeSourceUnion,
) -> kdsl.core.v1.ScaleIOVolumeSource:
    import kdsl.core.v1

    return (
        kdsl.core.v1.ScaleIOVolumeSource(**value) if isinstance(value, dict) else value
    )


def optional_list_converter_Taint(
    value: Union[Sequence[kdsl.core.v1.TaintUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.core.v1.Taint], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_Taint(x) for x in value]


def optional_converter_FlexVolumeSource(
    value: Union[kdsl.core.v1.FlexVolumeSourceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.FlexVolumeSource, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.FlexVolumeSource(**value) if isinstance(value, dict) else value


def optional_converter_ServicePortItem(
    value: Union[kdsl.core.v1.ServicePortItemUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.ServicePortItem, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.ServicePortItem(**value) if isinstance(value, dict) else value


def optional_converter_ResourceFieldSelector(
    value: Union[kdsl.core.v1.ResourceFieldSelectorUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.ResourceFieldSelector, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.ResourceFieldSelector(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_SessionAffinityConfig(
    value: Union[kdsl.core.v1.SessionAffinityConfigUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.SessionAffinityConfig, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.SessionAffinityConfig(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_Taint(value: kdsl.core.v1.TaintUnion) -> kdsl.core.v1.Taint:
    import kdsl.core.v1

    return kdsl.core.v1.Taint(**value) if isinstance(value, dict) else value


def optional_converter_NFSVolumeSource(
    value: Union[kdsl.core.v1.NFSVolumeSourceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.NFSVolumeSource, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.NFSVolumeSource(**value) if isinstance(value, dict) else value


def optional_converter_EventSource(
    value: Union[kdsl.core.v1.EventSourceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.EventSource, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.EventSource(**value) if isinstance(value, dict) else value


def optional_converter_TopologySelectorLabelRequirement(
    value: Union[kdsl.core.v1.TopologySelectorLabelRequirementUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.TopologySelectorLabelRequirement, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.TopologySelectorLabelRequirement(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_PodAntiAffinity(
    value: Union[kdsl.core.v1.PodAntiAffinityUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.PodAntiAffinity, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.PodAntiAffinity(**value) if isinstance(value, dict) else value


def required_converter_ServiceSpec(
    value: kdsl.core.v1.ServiceSpecUnion,
) -> kdsl.core.v1.ServiceSpec:
    import kdsl.core.v1

    return kdsl.core.v1.ServiceSpec(**value) if isinstance(value, dict) else value


def required_converter_GitRepoVolumeSource(
    value: kdsl.core.v1.GitRepoVolumeSourceUnion,
) -> kdsl.core.v1.GitRepoVolumeSource:
    import kdsl.core.v1

    return (
        kdsl.core.v1.GitRepoVolumeSource(**value) if isinstance(value, dict) else value
    )


def required_converter_ConfigMapNodeConfigSource(
    value: kdsl.core.v1.ConfigMapNodeConfigSourceUnion,
) -> kdsl.core.v1.ConfigMapNodeConfigSource:
    import kdsl.core.v1

    return (
        kdsl.core.v1.ConfigMapNodeConfigSource(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_OwnerReferenceItem(
    value: kdsl.core.v1.OwnerReferenceItemUnion,
) -> kdsl.core.v1.OwnerReferenceItem:
    import kdsl.core.v1

    return (
        kdsl.core.v1.OwnerReferenceItem(**value) if isinstance(value, dict) else value
    )


def optional_converter_KeyToPath(
    value: Union[kdsl.core.v1.KeyToPathUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.KeyToPath, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.KeyToPath(**value) if isinstance(value, dict) else value


def optional_converter_EndpointPort(
    value: Union[kdsl.core.v1.EndpointPortUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.EndpointPort, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.EndpointPort(**value) if isinstance(value, dict) else value


def optional_converter_EndpointSubset(
    value: Union[kdsl.core.v1.EndpointSubsetUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.EndpointSubset, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.EndpointSubset(**value) if isinstance(value, dict) else value


def optional_list_converter_ObjectReference(
    value: Union[Sequence[kdsl.core.v1.ObjectReferenceUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.core.v1.ObjectReference], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_ObjectReference(x) for x in value]


def optional_mlist_converter_ContainerItem(
    value: Union[Mapping[str, kdsl.core.v1.ContainerItemUnion], OmitEnum, None]
) -> Union[Mapping[str, kdsl.core.v1.ContainerItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {k: required_converter_ContainerItem(v) for k, v in value.items()}


def optional_converter_LabelSelector(
    value: Union[kdsl.core.v1.LabelSelectorUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.LabelSelector, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.LabelSelector(**value) if isinstance(value, dict) else value


def optional_converter_LimitRangeItem(
    value: Union[kdsl.core.v1.LimitRangeItemUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.LimitRangeItem, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.LimitRangeItem(**value) if isinstance(value, dict) else value


def optional_converter_ScopedResourceSelectorRequirement(
    value: Union[kdsl.core.v1.ScopedResourceSelectorRequirementUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.ScopedResourceSelectorRequirement, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.ScopedResourceSelectorRequirement(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_CephFSVolumeSource(
    value: kdsl.core.v1.CephFSVolumeSourceUnion,
) -> kdsl.core.v1.CephFSVolumeSource:
    import kdsl.core.v1

    return (
        kdsl.core.v1.CephFSVolumeSource(**value) if isinstance(value, dict) else value
    )


def optional_converter_QuobyteVolumeSource(
    value: Union[kdsl.core.v1.QuobyteVolumeSourceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.QuobyteVolumeSource, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.QuobyteVolumeSource(**value) if isinstance(value, dict) else value
    )


def optional_converter_VolumeItem(
    value: Union[kdsl.core.v1.VolumeItemUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.VolumeItem, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.VolumeItem(**value) if isinstance(value, dict) else value


def required_converter_NodeConditionItem(
    value: kdsl.core.v1.NodeConditionItemUnion,
) -> kdsl.core.v1.NodeConditionItem:
    import kdsl.core.v1

    return kdsl.core.v1.NodeConditionItem(**value) if isinstance(value, dict) else value


def required_converter_PersistentVolumeClaimStatus(
    value: kdsl.core.v1.PersistentVolumeClaimStatusUnion,
) -> kdsl.core.v1.PersistentVolumeClaimStatus:
    import kdsl.core.v1

    return (
        kdsl.core.v1.PersistentVolumeClaimStatus(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_RBDVolumeSource(
    value: Union[kdsl.core.v1.RBDVolumeSourceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.RBDVolumeSource, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.RBDVolumeSource(**value) if isinstance(value, dict) else value


def required_converter_CinderPersistentVolumeSource(
    value: kdsl.core.v1.CinderPersistentVolumeSourceUnion,
) -> kdsl.core.v1.CinderPersistentVolumeSource:
    import kdsl.core.v1

    return (
        kdsl.core.v1.CinderPersistentVolumeSource(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_NodeStatus(
    value: kdsl.core.v1.NodeStatusUnion,
) -> kdsl.core.v1.NodeStatus:
    import kdsl.core.v1

    return kdsl.core.v1.NodeStatus(**value) if isinstance(value, dict) else value


def optional_list_converter_Toleration(
    value: Union[Sequence[kdsl.core.v1.TolerationUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.core.v1.Toleration], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_Toleration(x) for x in value]


def optional_list_converter_EmbeddedPersistentVolumeClaim(
    value: Union[
        Sequence[kdsl.core.v1.EmbeddedPersistentVolumeClaimUnion], OmitEnum, None
    ]
) -> Union[Sequence[kdsl.core.v1.EmbeddedPersistentVolumeClaim], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_EmbeddedPersistentVolumeClaim(x) for x in value]


def required_converter_PersistentVolumeClaimVolumeSource(
    value: kdsl.core.v1.PersistentVolumeClaimVolumeSourceUnion,
) -> kdsl.core.v1.PersistentVolumeClaimVolumeSource:
    import kdsl.core.v1

    return (
        kdsl.core.v1.PersistentVolumeClaimVolumeSource(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_EmbeddedPersistentVolumeClaim(
    value: kdsl.core.v1.EmbeddedPersistentVolumeClaimUnion,
) -> kdsl.core.v1.EmbeddedPersistentVolumeClaim:
    import kdsl.core.v1

    return (
        kdsl.core.v1.EmbeddedPersistentVolumeClaim(**value)
        if isinstance(value, dict)
        else value
    )


def optional_list_converter_Sysctl(
    value: Union[Sequence[kdsl.core.v1.SysctlUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.core.v1.Sysctl], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_Sysctl(x) for x in value]


def required_converter_VolumeNodeAffinity(
    value: kdsl.core.v1.VolumeNodeAffinityUnion,
) -> kdsl.core.v1.VolumeNodeAffinity:
    import kdsl.core.v1

    return (
        kdsl.core.v1.VolumeNodeAffinity(**value) if isinstance(value, dict) else value
    )


def optional_converter_GlusterfsPersistentVolumeSource(
    value: Union[kdsl.core.v1.GlusterfsPersistentVolumeSourceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.GlusterfsPersistentVolumeSource, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.GlusterfsPersistentVolumeSource(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_NamespaceConditionItem(
    value: kdsl.core.v1.NamespaceConditionItemUnion,
) -> kdsl.core.v1.NamespaceConditionItem:
    import kdsl.core.v1

    return (
        kdsl.core.v1.NamespaceConditionItem(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_Sysctl(value: kdsl.core.v1.SysctlUnion) -> kdsl.core.v1.Sysctl:
    import kdsl.core.v1

    return kdsl.core.v1.Sysctl(**value) if isinstance(value, dict) else value


def optional_converter_Taint(
    value: Union[kdsl.core.v1.TaintUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.Taint, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.Taint(**value) if isinstance(value, dict) else value


def required_converter_HostPathVolumeSource(
    value: kdsl.core.v1.HostPathVolumeSourceUnion,
) -> kdsl.core.v1.HostPathVolumeSource:
    import kdsl.core.v1

    return (
        kdsl.core.v1.HostPathVolumeSource(**value) if isinstance(value, dict) else value
    )


def required_converter_EndpointAddress(
    value: kdsl.core.v1.EndpointAddressUnion,
) -> kdsl.core.v1.EndpointAddress:
    import kdsl.core.v1

    return kdsl.core.v1.EndpointAddress(**value) if isinstance(value, dict) else value


def optional_converter_Toleration(
    value: Union[kdsl.core.v1.TolerationUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.Toleration, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.Toleration(**value) if isinstance(value, dict) else value


def required_converter_GlusterfsVolumeSource(
    value: kdsl.core.v1.GlusterfsVolumeSourceUnion,
) -> kdsl.core.v1.GlusterfsVolumeSource:
    import kdsl.core.v1

    return (
        kdsl.core.v1.GlusterfsVolumeSource(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_ConfigMapNodeConfigSource(
    value: Union[kdsl.core.v1.ConfigMapNodeConfigSourceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.ConfigMapNodeConfigSource, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.ConfigMapNodeConfigSource(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_ClientIPConfig(
    value: kdsl.core.v1.ClientIPConfigUnion,
) -> kdsl.core.v1.ClientIPConfig:
    import kdsl.core.v1

    return kdsl.core.v1.ClientIPConfig(**value) if isinstance(value, dict) else value


def optional_converter_LimitRangeSpec(
    value: Union[kdsl.core.v1.LimitRangeSpecUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.LimitRangeSpec, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.LimitRangeSpec(**value) if isinstance(value, dict) else value


def optional_converter_NodeAddressItem(
    value: Union[kdsl.core.v1.NodeAddressItemUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.NodeAddressItem, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.NodeAddressItem(**value) if isinstance(value, dict) else value


def optional_converter_ConfigMapKeySelector(
    value: Union[kdsl.core.v1.ConfigMapKeySelectorUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.ConfigMapKeySelector, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.ConfigMapKeySelector(**value) if isinstance(value, dict) else value
    )


def required_converter_DaemonEndpoint(
    value: kdsl.core.v1.DaemonEndpointUnion,
) -> kdsl.core.v1.DaemonEndpoint:
    import kdsl.core.v1

    return kdsl.core.v1.DaemonEndpoint(**value) if isinstance(value, dict) else value


def optional_converter_CephFSVolumeSource(
    value: Union[kdsl.core.v1.CephFSVolumeSourceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.CephFSVolumeSource, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.CephFSVolumeSource(**value) if isinstance(value, dict) else value
    )


def optional_converter_ObjectReference(
    value: Union[kdsl.core.v1.ObjectReferenceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.ObjectReference, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.ObjectReference(**value) if isinstance(value, dict) else value


def optional_converter_NodeConditionItem(
    value: Union[kdsl.core.v1.NodeConditionItemUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.NodeConditionItem, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.NodeConditionItem(**value) if isinstance(value, dict) else value


def optional_converter_PersistentVolumeClaimStatus(
    value: Union[kdsl.core.v1.PersistentVolumeClaimStatusUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.PersistentVolumeClaimStatus, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.PersistentVolumeClaimStatus(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_TopologySpreadConstraintItem(
    value: kdsl.core.v1.TopologySpreadConstraintItemUnion,
) -> kdsl.core.v1.TopologySpreadConstraintItem:
    import kdsl.core.v1

    return (
        kdsl.core.v1.TopologySpreadConstraintItem(**value)
        if isinstance(value, dict)
        else value
    )


def optional_list_converter_DownwardAPIVolumeFile(
    value: Union[Sequence[kdsl.core.v1.DownwardAPIVolumeFileUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.core.v1.DownwardAPIVolumeFile], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_DownwardAPIVolumeFile(x) for x in value]


def optional_converter_CinderPersistentVolumeSource(
    value: Union[kdsl.core.v1.CinderPersistentVolumeSourceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.CinderPersistentVolumeSource, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.CinderPersistentVolumeSource(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_ReplicationControllerSpec(
    value: Union[kdsl.core.v1.ReplicationControllerSpecUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.ReplicationControllerSpec, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.ReplicationControllerSpec(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_CSIPersistentVolumeSource(
    value: Union[kdsl.core.v1.CSIPersistentVolumeSourceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.CSIPersistentVolumeSource, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.CSIPersistentVolumeSource(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_DownwardAPIVolumeFile(
    value: kdsl.core.v1.DownwardAPIVolumeFileUnion,
) -> kdsl.core.v1.DownwardAPIVolumeFile:
    import kdsl.core.v1

    return (
        kdsl.core.v1.DownwardAPIVolumeFile(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_PhotonPersistentDiskVolumeSource(
    value: kdsl.core.v1.PhotonPersistentDiskVolumeSourceUnion,
) -> kdsl.core.v1.PhotonPersistentDiskVolumeSource:
    import kdsl.core.v1

    return (
        kdsl.core.v1.PhotonPersistentDiskVolumeSource(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_NamespaceStatus(
    value: kdsl.core.v1.NamespaceStatusUnion,
) -> kdsl.core.v1.NamespaceStatus:
    import kdsl.core.v1

    return kdsl.core.v1.NamespaceStatus(**value) if isinstance(value, dict) else value


def required_converter_LoadBalancerStatus(
    value: kdsl.core.v1.LoadBalancerStatusUnion,
) -> kdsl.core.v1.LoadBalancerStatus:
    import kdsl.core.v1

    return (
        kdsl.core.v1.LoadBalancerStatus(**value) if isinstance(value, dict) else value
    )


def optional_converter_PersistentVolumeClaimVolumeSource(
    value: Union[kdsl.core.v1.PersistentVolumeClaimVolumeSourceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.PersistentVolumeClaimVolumeSource, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.PersistentVolumeClaimVolumeSource(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_EmbeddedPersistentVolumeClaim(
    value: Union[kdsl.core.v1.EmbeddedPersistentVolumeClaimUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.EmbeddedPersistentVolumeClaim, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.EmbeddedPersistentVolumeClaim(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_DeleteOptions(
    value: Union[kdsl.core.v1.DeleteOptionsUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.DeleteOptions, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.DeleteOptions(**value) if isinstance(value, dict) else value


def optional_converter_NamespaceConditionItem(
    value: Union[kdsl.core.v1.NamespaceConditionItemUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.NamespaceConditionItem, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.NamespaceConditionItem(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_Sysctl(
    value: Union[kdsl.core.v1.SysctlUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.Sysctl, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.Sysctl(**value) if isinstance(value, dict) else value


def optional_converter_HostPathVolumeSource(
    value: Union[kdsl.core.v1.HostPathVolumeSourceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.HostPathVolumeSource, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.HostPathVolumeSource(**value) if isinstance(value, dict) else value
    )


def required_converter_SecretReference(
    value: kdsl.core.v1.SecretReferenceUnion,
) -> kdsl.core.v1.SecretReference:
    import kdsl.core.v1

    return kdsl.core.v1.SecretReference(**value) if isinstance(value, dict) else value


def optional_converter_NodeSystemInfo(
    value: Union[kdsl.core.v1.NodeSystemInfoUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.NodeSystemInfo, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.NodeSystemInfo(**value) if isinstance(value, dict) else value


def optional_converter_EndpointAddress(
    value: Union[kdsl.core.v1.EndpointAddressUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.EndpointAddress, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.EndpointAddress(**value) if isinstance(value, dict) else value


def optional_list_converter_PodReadinessGate(
    value: Union[Sequence[kdsl.core.v1.PodReadinessGateUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.core.v1.PodReadinessGate], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_PodReadinessGate(x) for x in value]


def required_converter_NodeConfigStatus(
    value: kdsl.core.v1.NodeConfigStatusUnion,
) -> kdsl.core.v1.NodeConfigStatus:
    import kdsl.core.v1

    return kdsl.core.v1.NodeConfigStatus(**value) if isinstance(value, dict) else value


def optional_converter_ClientIPConfig(
    value: Union[kdsl.core.v1.ClientIPConfigUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.ClientIPConfig, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.ClientIPConfig(**value) if isinstance(value, dict) else value


def required_list_converter_NodeSelectorTerm(
    value: Sequence[kdsl.core.v1.NodeSelectorTermUnion],
) -> Sequence[kdsl.core.v1.NodeSelectorTerm]:
    return [required_converter_NodeSelectorTerm(x) for x in value]


def optional_converter_NodeSelector(
    value: Union[kdsl.core.v1.NodeSelectorUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.NodeSelector, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.NodeSelector(**value) if isinstance(value, dict) else value


def required_converter_ServiceStatus(
    value: kdsl.core.v1.ServiceStatusUnion,
) -> kdsl.core.v1.ServiceStatus:
    import kdsl.core.v1

    return kdsl.core.v1.ServiceStatus(**value) if isinstance(value, dict) else value


def required_converter_SecurityContext(
    value: kdsl.core.v1.SecurityContextUnion,
) -> kdsl.core.v1.SecurityContext:
    import kdsl.core.v1

    return kdsl.core.v1.SecurityContext(**value) if isinstance(value, dict) else value


def optional_converter_ProjectedVolumeSource(
    value: Union[kdsl.core.v1.ProjectedVolumeSourceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.ProjectedVolumeSource, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.ProjectedVolumeSource(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_PersistentVolumeClaimSpec(
    value: kdsl.core.v1.PersistentVolumeClaimSpecUnion,
) -> kdsl.core.v1.PersistentVolumeClaimSpec:
    import kdsl.core.v1

    return (
        kdsl.core.v1.PersistentVolumeClaimSpec(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_WindowsSecurityContextOptions(
    value: Union[kdsl.core.v1.WindowsSecurityContextOptionsUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.WindowsSecurityContextOptions, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.WindowsSecurityContextOptions(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_TopologySpreadConstraintItem(
    value: Union[kdsl.core.v1.TopologySpreadConstraintItemUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.TopologySpreadConstraintItem, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.TopologySpreadConstraintItem(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_PodSpec(
    value: kdsl.core.v1.PodSpecUnion,
) -> kdsl.core.v1.PodSpec:
    import kdsl.core.v1

    return kdsl.core.v1.PodSpec(**value) if isinstance(value, dict) else value


def optional_converter_StorageOSVolumeSource(
    value: Union[kdsl.core.v1.StorageOSVolumeSourceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.StorageOSVolumeSource, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.StorageOSVolumeSource(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_ServiceAccountTokenProjection(
    value: Union[kdsl.core.v1.ServiceAccountTokenProjectionUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.ServiceAccountTokenProjection, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.ServiceAccountTokenProjection(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_DownwardAPIVolumeFile(
    value: Union[kdsl.core.v1.DownwardAPIVolumeFileUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.DownwardAPIVolumeFile, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.DownwardAPIVolumeFile(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_PhotonPersistentDiskVolumeSource(
    value: Union[kdsl.core.v1.PhotonPersistentDiskVolumeSourceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.PhotonPersistentDiskVolumeSource, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.PhotonPersistentDiskVolumeSource(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_NamespaceStatus(
    value: Union[kdsl.core.v1.NamespaceStatusUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.NamespaceStatus, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.NamespaceStatus(**value) if isinstance(value, dict) else value


def optional_converter_ScopeSelector(
    value: Union[kdsl.core.v1.ScopeSelectorUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.ScopeSelector, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.ScopeSelector(**value) if isinstance(value, dict) else value


def required_converter_FlockerVolumeSource(
    value: kdsl.core.v1.FlockerVolumeSourceUnion,
) -> kdsl.core.v1.FlockerVolumeSource:
    import kdsl.core.v1

    return (
        kdsl.core.v1.FlockerVolumeSource(**value) if isinstance(value, dict) else value
    )


def required_converter_Capabilities(
    value: kdsl.core.v1.CapabilitiesUnion,
) -> kdsl.core.v1.Capabilities:
    import kdsl.core.v1

    return kdsl.core.v1.Capabilities(**value) if isinstance(value, dict) else value


def required_converter_ConfigMapProjection(
    value: kdsl.core.v1.ConfigMapProjectionUnion,
) -> kdsl.core.v1.ConfigMapProjection:
    import kdsl.core.v1

    return (
        kdsl.core.v1.ConfigMapProjection(**value) if isinstance(value, dict) else value
    )


def optional_converter_SecretReference(
    value: Union[kdsl.core.v1.SecretReferenceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.SecretReference, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.SecretReference(**value) if isinstance(value, dict) else value


def required_converter_PodIP(value: kdsl.core.v1.PodIPUnion) -> kdsl.core.v1.PodIP:
    import kdsl.core.v1

    return kdsl.core.v1.PodIP(**value) if isinstance(value, dict) else value


def required_converter_PodAffinity(
    value: kdsl.core.v1.PodAffinityUnion,
) -> kdsl.core.v1.PodAffinity:
    import kdsl.core.v1

    return kdsl.core.v1.PodAffinity(**value) if isinstance(value, dict) else value


def required_converter_ObjectFieldSelector(
    value: kdsl.core.v1.ObjectFieldSelectorUnion,
) -> kdsl.core.v1.ObjectFieldSelector:
    import kdsl.core.v1

    return (
        kdsl.core.v1.ObjectFieldSelector(**value) if isinstance(value, dict) else value
    )


def required_converter_PodSecurityContext(
    value: kdsl.core.v1.PodSecurityContextUnion,
) -> kdsl.core.v1.PodSecurityContext:
    import kdsl.core.v1

    return (
        kdsl.core.v1.PodSecurityContext(**value) if isinstance(value, dict) else value
    )


def required_converter_ISCSIPersistentVolumeSource(
    value: kdsl.core.v1.ISCSIPersistentVolumeSourceUnion,
) -> kdsl.core.v1.ISCSIPersistentVolumeSource:
    import kdsl.core.v1

    return (
        kdsl.core.v1.ISCSIPersistentVolumeSource(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_ResourceQuotaStatus(
    value: kdsl.core.v1.ResourceQuotaStatusUnion,
) -> kdsl.core.v1.ResourceQuotaStatus:
    import kdsl.core.v1

    return (
        kdsl.core.v1.ResourceQuotaStatus(**value) if isinstance(value, dict) else value
    )


def required_converter_SecretVolumeSource(
    value: kdsl.core.v1.SecretVolumeSourceUnion,
) -> kdsl.core.v1.SecretVolumeSource:
    import kdsl.core.v1

    return (
        kdsl.core.v1.SecretVolumeSource(**value) if isinstance(value, dict) else value
    )


def optional_list_converter_LabelSelector(
    value: Union[Sequence[kdsl.core.v1.LabelSelectorUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.core.v1.LabelSelector], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_LabelSelector(x) for x in value]


def required_converter_CinderVolumeSource(
    value: kdsl.core.v1.CinderVolumeSourceUnion,
) -> kdsl.core.v1.CinderVolumeSource:
    import kdsl.core.v1

    return (
        kdsl.core.v1.CinderVolumeSource(**value) if isinstance(value, dict) else value
    )


def optional_converter_FCVolumeSource(
    value: Union[kdsl.core.v1.FCVolumeSourceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.FCVolumeSource, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.FCVolumeSource(**value) if isinstance(value, dict) else value


def optional_list_converter_ScopedResourceSelectorRequirement(
    value: Union[
        Sequence[kdsl.core.v1.ScopedResourceSelectorRequirementUnion], OmitEnum, None
    ]
) -> Union[Sequence[kdsl.core.v1.ScopedResourceSelectorRequirement], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_ScopedResourceSelectorRequirement(x) for x in value]


def optional_mlist_converter_EnvVarItem(
    value: Union[Mapping[str, kdsl.core.v1.EnvVarItemUnion], OmitEnum, None]
) -> Union[Mapping[str, kdsl.core.v1.EnvVarItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {k: required_converter_EnvVarItem(v) for k, v in value.items()}


def optional_converter_NodeConfigStatus(
    value: Union[kdsl.core.v1.NodeConfigStatusUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.NodeConfigStatus, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.NodeConfigStatus(**value) if isinstance(value, dict) else value


def optional_converter_PodReadinessGate(
    value: Union[kdsl.core.v1.PodReadinessGateUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.PodReadinessGate, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.PodReadinessGate(**value) if isinstance(value, dict) else value


def required_converter_ContainerPort(
    value: kdsl.core.v1.ContainerPortUnion,
) -> kdsl.core.v1.ContainerPort:
    import kdsl.core.v1

    return kdsl.core.v1.ContainerPort(**value) if isinstance(value, dict) else value


def required_converter_Probe(value: kdsl.core.v1.ProbeUnion) -> kdsl.core.v1.Probe:
    import kdsl.core.v1

    return kdsl.core.v1.Probe(**value) if isinstance(value, dict) else value


def optional_mlist_converter_EphemeralContainerItem(
    value: Union[Mapping[str, kdsl.core.v1.EphemeralContainerItemUnion], OmitEnum, None]
) -> Union[Mapping[str, kdsl.core.v1.EphemeralContainerItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {
            k: required_converter_EphemeralContainerItem(v) for k, v in value.items()
        }


def required_converter_NodeSelectorTerm(
    value: kdsl.core.v1.NodeSelectorTermUnion,
) -> kdsl.core.v1.NodeSelectorTerm:
    import kdsl.core.v1

    return kdsl.core.v1.NodeSelectorTerm(**value) if isinstance(value, dict) else value


def optional_converter_ServiceStatus(
    value: Union[kdsl.core.v1.ServiceStatusUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.ServiceStatus, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.ServiceStatus(**value) if isinstance(value, dict) else value


def required_converter_ContainerStateRunning(
    value: kdsl.core.v1.ContainerStateRunningUnion,
) -> kdsl.core.v1.ContainerStateRunning:
    import kdsl.core.v1

    return (
        kdsl.core.v1.ContainerStateRunning(**value)
        if isinstance(value, dict)
        else value
    )


def optional_list_converter_ContainerStatus(
    value: Union[Sequence[kdsl.core.v1.ContainerStatusUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.core.v1.ContainerStatus], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_ContainerStatus(x) for x in value]


def optional_converter_SecurityContext(
    value: Union[kdsl.core.v1.SecurityContextUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.SecurityContext, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.SecurityContext(**value) if isinstance(value, dict) else value


def optional_list_converter_EnvVar(
    value: Union[Sequence[kdsl.core.v1.EnvVarUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.core.v1.EnvVar], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_EnvVar(x) for x in value]


def required_converter_ContainerItem(
    value: kdsl.core.v1.ContainerItemUnion,
) -> kdsl.core.v1.ContainerItem:
    import kdsl.core.v1

    return kdsl.core.v1.ContainerItem(**value) if isinstance(value, dict) else value


def optional_converter_PodSpec(
    value: Union[kdsl.core.v1.PodSpecUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.PodSpec, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.PodSpec(**value) if isinstance(value, dict) else value


def optional_list_converter_Volume(
    value: Union[Sequence[kdsl.core.v1.VolumeUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.core.v1.Volume], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_Volume(x) for x in value]


def optional_mlist_converter_ServicePortItem(
    value: Union[Mapping[int, kdsl.core.v1.ServicePortItemUnion], OmitEnum, None]
) -> Union[Mapping[int, kdsl.core.v1.ServicePortItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {k: required_converter_ServicePortItem(v) for k, v in value.items()}


def required_converter_FlexPersistentVolumeSource(
    value: kdsl.core.v1.FlexPersistentVolumeSourceUnion,
) -> kdsl.core.v1.FlexPersistentVolumeSource:
    import kdsl.core.v1

    return (
        kdsl.core.v1.FlexPersistentVolumeSource(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_FlockerVolumeSource(
    value: Union[kdsl.core.v1.FlockerVolumeSourceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.FlockerVolumeSource, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.FlockerVolumeSource(**value) if isinstance(value, dict) else value
    )


def optional_converter_Capabilities(
    value: Union[kdsl.core.v1.CapabilitiesUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.Capabilities, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.Capabilities(**value) if isinstance(value, dict) else value


def required_converter_WeightedPodAffinityTerm(
    value: kdsl.core.v1.WeightedPodAffinityTermUnion,
) -> kdsl.core.v1.WeightedPodAffinityTerm:
    import kdsl.core.v1

    return (
        kdsl.core.v1.WeightedPodAffinityTerm(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_EnvVar(
    value: Union[kdsl.core.v1.EnvVarUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.EnvVar, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.EnvVar(**value) if isinstance(value, dict) else value


def required_converter_NodeSelectorRequirement(
    value: kdsl.core.v1.NodeSelectorRequirementUnion,
) -> kdsl.core.v1.NodeSelectorRequirement:
    import kdsl.core.v1

    return (
        kdsl.core.v1.NodeSelectorRequirement(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_ConfigMapProjection(
    value: Union[kdsl.core.v1.ConfigMapProjectionUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.ConfigMapProjection, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.ConfigMapProjection(**value) if isinstance(value, dict) else value
    )


def required_converter_AzureFilePersistentVolumeSource(
    value: kdsl.core.v1.AzureFilePersistentVolumeSourceUnion,
) -> kdsl.core.v1.AzureFilePersistentVolumeSource:
    import kdsl.core.v1

    return (
        kdsl.core.v1.AzureFilePersistentVolumeSource(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_Volume(value: kdsl.core.v1.VolumeUnion) -> kdsl.core.v1.Volume:
    import kdsl.core.v1

    return kdsl.core.v1.Volume(**value) if isinstance(value, dict) else value


def required_converter_EventSeries(
    value: kdsl.core.v1.EventSeriesUnion,
) -> kdsl.core.v1.EventSeries:
    import kdsl.core.v1

    return kdsl.core.v1.EventSeries(**value) if isinstance(value, dict) else value


def optional_converter_PodIP(
    value: Union[kdsl.core.v1.PodIPUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.PodIP, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.PodIP(**value) if isinstance(value, dict) else value


def optional_converter_PodAffinity(
    value: Union[kdsl.core.v1.PodAffinityUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.PodAffinity, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.PodAffinity(**value) if isinstance(value, dict) else value


def optional_converter_ObjectFieldSelector(
    value: Union[kdsl.core.v1.ObjectFieldSelectorUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.ObjectFieldSelector, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.ObjectFieldSelector(**value) if isinstance(value, dict) else value
    )


def required_converter_VolumeMount(
    value: kdsl.core.v1.VolumeMountUnion,
) -> kdsl.core.v1.VolumeMount:
    import kdsl.core.v1

    return kdsl.core.v1.VolumeMount(**value) if isinstance(value, dict) else value


def optional_converter_ISCSIPersistentVolumeSource(
    value: Union[kdsl.core.v1.ISCSIPersistentVolumeSourceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.ISCSIPersistentVolumeSource, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.ISCSIPersistentVolumeSource(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_ResourceQuotaStatus(
    value: Union[kdsl.core.v1.ResourceQuotaStatusUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.ResourceQuotaStatus, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.ResourceQuotaStatus(**value) if isinstance(value, dict) else value
    )


def optional_converter_CinderVolumeSource(
    value: Union[kdsl.core.v1.CinderVolumeSourceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.CinderVolumeSource, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.CinderVolumeSource(**value) if isinstance(value, dict) else value
    )


def optional_converter_SecretVolumeSource(
    value: Union[kdsl.core.v1.SecretVolumeSourceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.SecretVolumeSource, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.SecretVolumeSource(**value) if isinstance(value, dict) else value
    )


def optional_converter_ScaleIOPersistentVolumeSource(
    value: Union[kdsl.core.v1.ScaleIOPersistentVolumeSourceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.ScaleIOPersistentVolumeSource, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.ScaleIOPersistentVolumeSource(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_AzureDiskVolumeSource(
    value: kdsl.core.v1.AzureDiskVolumeSourceUnion,
) -> kdsl.core.v1.AzureDiskVolumeSource:
    import kdsl.core.v1

    return (
        kdsl.core.v1.AzureDiskVolumeSource(**value)
        if isinstance(value, dict)
        else value
    )


def optional_mlist_converter_ContainerPortItem(
    value: Union[Mapping[int, kdsl.core.v1.ContainerPortItemUnion], OmitEnum, None]
) -> Union[Mapping[int, kdsl.core.v1.ContainerPortItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {k: required_converter_ContainerPortItem(v) for k, v in value.items()}


def optional_converter_ContainerPort(
    value: Union[kdsl.core.v1.ContainerPortUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.ContainerPort, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.ContainerPort(**value) if isinstance(value, dict) else value


def required_converter_SecretKeySelector(
    value: kdsl.core.v1.SecretKeySelectorUnion,
) -> kdsl.core.v1.SecretKeySelector:
    import kdsl.core.v1

    return kdsl.core.v1.SecretKeySelector(**value) if isinstance(value, dict) else value


def optional_converter_Probe(
    value: Union[kdsl.core.v1.ProbeUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.Probe, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.Probe(**value) if isinstance(value, dict) else value


def optional_converter_NodeSelectorTerm(
    value: Union[kdsl.core.v1.NodeSelectorTermUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.NodeSelectorTerm, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.NodeSelectorTerm(**value) if isinstance(value, dict) else value


def optional_converter_AWSElasticBlockStoreVolumeSource(
    value: Union[kdsl.core.v1.AWSElasticBlockStoreVolumeSourceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.AWSElasticBlockStoreVolumeSource, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.AWSElasticBlockStoreVolumeSource(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_ContainerStateRunning(
    value: Union[kdsl.core.v1.ContainerStateRunningUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.ContainerStateRunning, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.ContainerStateRunning(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_ReplicationControllerConditionItem(
    value: kdsl.core.v1.ReplicationControllerConditionItemUnion,
) -> kdsl.core.v1.ReplicationControllerConditionItem:
    import kdsl.core.v1

    return (
        kdsl.core.v1.ReplicationControllerConditionItem(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_SecretProjection(
    value: Union[kdsl.core.v1.SecretProjectionUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.SecretProjection, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.SecretProjection(**value) if isinstance(value, dict) else value


def optional_converter_ContainerStatus(
    value: Union[kdsl.core.v1.ContainerStatusUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.ContainerStatus, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.ContainerStatus(**value) if isinstance(value, dict) else value


def optional_converter_ContainerItem(
    value: Union[kdsl.core.v1.ContainerItemUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.ContainerItem, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.ContainerItem(**value) if isinstance(value, dict) else value


def optional_converter_SELinuxOptions(
    value: Union[kdsl.core.v1.SELinuxOptionsUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.SELinuxOptions, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.SELinuxOptions(**value) if isinstance(value, dict) else value


def required_converter_NamespaceSpec(
    value: kdsl.core.v1.NamespaceSpecUnion,
) -> kdsl.core.v1.NamespaceSpec:
    import kdsl.core.v1

    return kdsl.core.v1.NamespaceSpec(**value) if isinstance(value, dict) else value


def required_converter_TCPSocketAction(
    value: kdsl.core.v1.TCPSocketActionUnion,
) -> kdsl.core.v1.TCPSocketAction:
    import kdsl.core.v1

    return kdsl.core.v1.TCPSocketAction(**value) if isinstance(value, dict) else value


def optional_list_converter_AttachedVolume(
    value: Union[Sequence[kdsl.core.v1.AttachedVolumeUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.core.v1.AttachedVolume], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_AttachedVolume(x) for x in value]


def optional_converter_GCEPersistentDiskVolumeSource(
    value: Union[kdsl.core.v1.GCEPersistentDiskVolumeSourceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.GCEPersistentDiskVolumeSource, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.GCEPersistentDiskVolumeSource(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_ManagedFieldsEntry(
    value: kdsl.core.v1.ManagedFieldsEntryUnion,
) -> kdsl.core.v1.ManagedFieldsEntry:
    import kdsl.core.v1

    return (
        kdsl.core.v1.ManagedFieldsEntry(**value) if isinstance(value, dict) else value
    )


def optional_mlist_converter_TopologySpreadConstraintItem(
    value: Union[
        Mapping[str, kdsl.core.v1.TopologySpreadConstraintItemUnion], OmitEnum, None
    ]
) -> Union[Mapping[str, kdsl.core.v1.TopologySpreadConstraintItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {
            k: required_converter_TopologySpreadConstraintItem(v)
            for k, v in value.items()
        }


def optional_converter_FlexPersistentVolumeSource(
    value: Union[kdsl.core.v1.FlexPersistentVolumeSourceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.FlexPersistentVolumeSource, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.FlexPersistentVolumeSource(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_ScaleIOVolumeSource(
    value: Union[kdsl.core.v1.ScaleIOVolumeSourceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.ScaleIOVolumeSource, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.ScaleIOVolumeSource(**value) if isinstance(value, dict) else value
    )


def required_converter_AttachedVolume(
    value: kdsl.core.v1.AttachedVolumeUnion,
) -> kdsl.core.v1.AttachedVolume:
    import kdsl.core.v1

    return kdsl.core.v1.AttachedVolume(**value) if isinstance(value, dict) else value


def required_converter_ObjectReferenceItem(
    value: kdsl.core.v1.ObjectReferenceItemUnion,
) -> kdsl.core.v1.ObjectReferenceItem:
    import kdsl.core.v1

    return (
        kdsl.core.v1.ObjectReferenceItem(**value) if isinstance(value, dict) else value
    )


def required_converter_PreferredSchedulingTerm(
    value: kdsl.core.v1.PreferredSchedulingTermUnion,
) -> kdsl.core.v1.PreferredSchedulingTerm:
    import kdsl.core.v1

    return (
        kdsl.core.v1.PreferredSchedulingTerm(**value)
        if isinstance(value, dict)
        else value
    )


def optional_list_converter_EndpointAddress(
    value: Union[Sequence[kdsl.core.v1.EndpointAddressUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.core.v1.EndpointAddress], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_EndpointAddress(x) for x in value]


def required_converter_HostAliasItem(
    value: kdsl.core.v1.HostAliasItemUnion,
) -> kdsl.core.v1.HostAliasItem:
    import kdsl.core.v1

    return kdsl.core.v1.HostAliasItem(**value) if isinstance(value, dict) else value


def optional_converter_NodeSelectorRequirement(
    value: Union[kdsl.core.v1.NodeSelectorRequirementUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.NodeSelectorRequirement, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.NodeSelectorRequirement(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_ResourceRequirements(
    value: kdsl.core.v1.ResourceRequirementsUnion,
) -> kdsl.core.v1.ResourceRequirements:
    import kdsl.core.v1

    return (
        kdsl.core.v1.ResourceRequirements(**value) if isinstance(value, dict) else value
    )


def optional_converter_AzureFilePersistentVolumeSource(
    value: Union[kdsl.core.v1.AzureFilePersistentVolumeSourceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.AzureFilePersistentVolumeSource, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.AzureFilePersistentVolumeSource(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_Volume(
    value: Union[kdsl.core.v1.VolumeUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.Volume, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.Volume(**value) if isinstance(value, dict) else value


def optional_mlist_converter_OwnerReferenceItem(
    value: Union[Mapping[str, kdsl.core.v1.OwnerReferenceItemUnion], OmitEnum, None]
) -> Union[Mapping[str, kdsl.core.v1.OwnerReferenceItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {k: required_converter_OwnerReferenceItem(v) for k, v in value.items()}


def optional_converter_ServiceSpec(
    value: Union[kdsl.core.v1.ServiceSpecUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.ServiceSpec, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.ServiceSpec(**value) if isinstance(value, dict) else value


def optional_converter_EventSeries(
    value: Union[kdsl.core.v1.EventSeriesUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.EventSeries, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.EventSeries(**value) if isinstance(value, dict) else value


def optional_converter_GitRepoVolumeSource(
    value: Union[kdsl.core.v1.GitRepoVolumeSourceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.GitRepoVolumeSource, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.GitRepoVolumeSource(**value) if isinstance(value, dict) else value
    )


def required_converter_ISCSIVolumeSource(
    value: kdsl.core.v1.ISCSIVolumeSourceUnion,
) -> kdsl.core.v1.ISCSIVolumeSource:
    import kdsl.core.v1

    return kdsl.core.v1.ISCSIVolumeSource(**value) if isinstance(value, dict) else value


def optional_converter_OwnerReferenceItem(
    value: Union[kdsl.core.v1.OwnerReferenceItemUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.OwnerReferenceItem, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.OwnerReferenceItem(**value) if isinstance(value, dict) else value
    )


def required_converter_RBDPersistentVolumeSource(
    value: kdsl.core.v1.RBDPersistentVolumeSourceUnion,
) -> kdsl.core.v1.RBDPersistentVolumeSource:
    import kdsl.core.v1

    return (
        kdsl.core.v1.RBDPersistentVolumeSource(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_PodTemplateSpec(
    value: kdsl.core.v1.PodTemplateSpecUnion,
) -> kdsl.core.v1.PodTemplateSpec:
    import kdsl.core.v1

    return kdsl.core.v1.PodTemplateSpec(**value) if isinstance(value, dict) else value


def required_converter_NodeAffinity(
    value: kdsl.core.v1.NodeAffinityUnion,
) -> kdsl.core.v1.NodeAffinity:
    import kdsl.core.v1

    return kdsl.core.v1.NodeAffinity(**value) if isinstance(value, dict) else value


def required_converter_VolumeMountItem(
    value: kdsl.core.v1.VolumeMountItemUnion,
) -> kdsl.core.v1.VolumeMountItem:
    import kdsl.core.v1

    return kdsl.core.v1.VolumeMountItem(**value) if isinstance(value, dict) else value


def optional_list_converter_ManagedFieldsEntry(
    value: Union[Sequence[kdsl.core.v1.ManagedFieldsEntryUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.core.v1.ManagedFieldsEntry], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_ManagedFieldsEntry(x) for x in value]


def optional_converter_SecretKeySelector(
    value: Union[kdsl.core.v1.SecretKeySelectorUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.SecretKeySelector, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.SecretKeySelector(**value) if isinstance(value, dict) else value


def optional_list_converter_EnvFromSource(
    value: Union[Sequence[kdsl.core.v1.EnvFromSourceUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.core.v1.EnvFromSource], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_EnvFromSource(x) for x in value]


def required_converter_DownwardAPIVolumeSource(
    value: kdsl.core.v1.DownwardAPIVolumeSourceUnion,
) -> kdsl.core.v1.DownwardAPIVolumeSource:
    import kdsl.core.v1

    return (
        kdsl.core.v1.DownwardAPIVolumeSource(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_ConfigMapEnvSource(
    value: kdsl.core.v1.ConfigMapEnvSourceUnion,
) -> kdsl.core.v1.ConfigMapEnvSource:
    import kdsl.core.v1

    return (
        kdsl.core.v1.ConfigMapEnvSource(**value) if isinstance(value, dict) else value
    )


def required_converter_EnvFromSource(
    value: kdsl.core.v1.EnvFromSourceUnion,
) -> kdsl.core.v1.EnvFromSource:
    import kdsl.core.v1

    return kdsl.core.v1.EnvFromSource(**value) if isinstance(value, dict) else value


def required_mlist_converter_ContainerItem(
    value: Mapping[str, kdsl.core.v1.ContainerItemUnion]
) -> Mapping[str, kdsl.core.v1.ContainerItem]:
    return {k: required_converter_ContainerItem(v) for k, v in value.items()}


def optional_converter_ReplicationControllerConditionItem(
    value: Union[kdsl.core.v1.ReplicationControllerConditionItemUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.ReplicationControllerConditionItem, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.ReplicationControllerConditionItem(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_EnvVarSource(
    value: kdsl.core.v1.EnvVarSourceUnion,
) -> kdsl.core.v1.EnvVarSource:
    import kdsl.core.v1

    return kdsl.core.v1.EnvVarSource(**value) if isinstance(value, dict) else value


def optional_converter_NodeStatus(
    value: Union[kdsl.core.v1.NodeStatusUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.NodeStatus, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.NodeStatus(**value) if isinstance(value, dict) else value


def optional_converter_ManagedFieldsEntry(
    value: Union[kdsl.core.v1.ManagedFieldsEntryUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.ManagedFieldsEntry, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.ManagedFieldsEntry(**value) if isinstance(value, dict) else value
    )


def optional_converter_AttachedVolume(
    value: Union[kdsl.core.v1.AttachedVolumeUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.AttachedVolume, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.AttachedVolume(**value) if isinstance(value, dict) else value


def optional_converter_VolumeNodeAffinity(
    value: Union[kdsl.core.v1.VolumeNodeAffinityUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.VolumeNodeAffinity, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.VolumeNodeAffinity(**value) if isinstance(value, dict) else value
    )


def optional_list_converter_PodAffinityTerm(
    value: Union[Sequence[kdsl.core.v1.PodAffinityTermUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.core.v1.PodAffinityTerm], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_PodAffinityTerm(x) for x in value]


def optional_converter_PreferredSchedulingTerm(
    value: Union[kdsl.core.v1.PreferredSchedulingTermUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.PreferredSchedulingTerm, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.PreferredSchedulingTerm(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_ContainerState(
    value: kdsl.core.v1.ContainerStateUnion,
) -> kdsl.core.v1.ContainerState:
    import kdsl.core.v1

    return kdsl.core.v1.ContainerState(**value) if isinstance(value, dict) else value


def required_converter_PodAffinityTerm(
    value: kdsl.core.v1.PodAffinityTermUnion,
) -> kdsl.core.v1.PodAffinityTerm:
    import kdsl.core.v1

    return kdsl.core.v1.PodAffinityTerm(**value) if isinstance(value, dict) else value


def optional_mlist_converter_PodConditionItem(
    value: Union[Mapping[str, kdsl.core.v1.PodConditionItemUnion], OmitEnum, None]
) -> Union[Mapping[str, kdsl.core.v1.PodConditionItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {k: required_converter_PodConditionItem(v) for k, v in value.items()}


def optional_converter_GlusterfsVolumeSource(
    value: Union[kdsl.core.v1.GlusterfsVolumeSourceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.GlusterfsVolumeSource, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.GlusterfsVolumeSource(**value)
        if isinstance(value, dict)
        else value
    )


def optional_mlist_converter_NamespaceConditionItem(
    value: Union[Mapping[str, kdsl.core.v1.NamespaceConditionItemUnion], OmitEnum, None]
) -> Union[Mapping[str, kdsl.core.v1.NamespaceConditionItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {
            k: required_converter_NamespaceConditionItem(v) for k, v in value.items()
        }


def required_converter_StorageOSPersistentVolumeSource(
    value: kdsl.core.v1.StorageOSPersistentVolumeSourceUnion,
) -> kdsl.core.v1.StorageOSPersistentVolumeSource:
    import kdsl.core.v1

    return (
        kdsl.core.v1.StorageOSPersistentVolumeSource(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_VsphereVirtualDiskVolumeSource(
    value: kdsl.core.v1.VsphereVirtualDiskVolumeSourceUnion,
) -> kdsl.core.v1.VsphereVirtualDiskVolumeSource:
    import kdsl.core.v1

    return (
        kdsl.core.v1.VsphereVirtualDiskVolumeSource(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_HTTPHeader(
    value: kdsl.core.v1.HTTPHeaderUnion,
) -> kdsl.core.v1.HTTPHeader:
    import kdsl.core.v1

    return kdsl.core.v1.HTTPHeader(**value) if isinstance(value, dict) else value


def required_converter_CephFSPersistentVolumeSource(
    value: kdsl.core.v1.CephFSPersistentVolumeSourceUnion,
) -> kdsl.core.v1.CephFSPersistentVolumeSource:
    import kdsl.core.v1

    return (
        kdsl.core.v1.CephFSPersistentVolumeSource(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_VolumeMountItem(
    value: Union[kdsl.core.v1.VolumeMountItemUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.VolumeMountItem, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.VolumeMountItem(**value) if isinstance(value, dict) else value


def optional_converter_DaemonEndpoint(
    value: Union[kdsl.core.v1.DaemonEndpointUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.DaemonEndpoint, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.DaemonEndpoint(**value) if isinstance(value, dict) else value


def optional_converter_EnvFromSource(
    value: Union[kdsl.core.v1.EnvFromSourceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.EnvFromSource, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.EnvFromSource(**value) if isinstance(value, dict) else value


def required_converter_NodeDaemonEndpoints(
    value: kdsl.core.v1.NodeDaemonEndpointsUnion,
) -> kdsl.core.v1.NodeDaemonEndpoints:
    import kdsl.core.v1

    return (
        kdsl.core.v1.NodeDaemonEndpoints(**value) if isinstance(value, dict) else value
    )


def optional_converter_EnvVarSource(
    value: Union[kdsl.core.v1.EnvVarSourceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.EnvVarSource, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.EnvVarSource(**value) if isinstance(value, dict) else value


def required_converter_CSIVolumeSource(
    value: kdsl.core.v1.CSIVolumeSourceUnion,
) -> kdsl.core.v1.CSIVolumeSource:
    import kdsl.core.v1

    return kdsl.core.v1.CSIVolumeSource(**value) if isinstance(value, dict) else value


def required_converter_AzureFileVolumeSource(
    value: kdsl.core.v1.AzureFileVolumeSourceUnion,
) -> kdsl.core.v1.AzureFileVolumeSource:
    import kdsl.core.v1

    return (
        kdsl.core.v1.AzureFileVolumeSource(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_TypedLocalObjectReference(
    value: kdsl.core.v1.TypedLocalObjectReferenceUnion,
) -> kdsl.core.v1.TypedLocalObjectReference:
    import kdsl.core.v1

    return (
        kdsl.core.v1.TypedLocalObjectReference(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_ObjectMeta(
    value: kdsl.core.v1.ObjectMetaUnion,
) -> kdsl.core.v1.ObjectMeta:
    import kdsl.core.v1

    return kdsl.core.v1.ObjectMeta(**value) if isinstance(value, dict) else value


def required_converter_ReplicationControllerStatus(
    value: kdsl.core.v1.ReplicationControllerStatusUnion,
) -> kdsl.core.v1.ReplicationControllerStatus:
    import kdsl.core.v1

    return (
        kdsl.core.v1.ReplicationControllerStatus(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_LoadBalancerStatus(
    value: Union[kdsl.core.v1.LoadBalancerStatusUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.LoadBalancerStatus, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.LoadBalancerStatus(**value) if isinstance(value, dict) else value
    )


def optional_list_converter_PodIP(
    value: Union[Sequence[kdsl.core.v1.PodIPUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.core.v1.PodIP], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_PodIP(x) for x in value]


def optional_converter_PodAffinityTerm(
    value: Union[kdsl.core.v1.PodAffinityTermUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.PodAffinityTerm, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.PodAffinityTerm(**value) if isinstance(value, dict) else value


def required_converter_PersistentVolumeClaimConditionItem(
    value: kdsl.core.v1.PersistentVolumeClaimConditionItemUnion,
) -> kdsl.core.v1.PersistentVolumeClaimConditionItem:
    import kdsl.core.v1

    return (
        kdsl.core.v1.PersistentVolumeClaimConditionItem(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_PodDNSConfig(
    value: kdsl.core.v1.PodDNSConfigUnion,
) -> kdsl.core.v1.PodDNSConfig:
    import kdsl.core.v1

    return kdsl.core.v1.PodDNSConfig(**value) if isinstance(value, dict) else value


def optional_converter_StorageOSPersistentVolumeSource(
    value: Union[kdsl.core.v1.StorageOSPersistentVolumeSourceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.StorageOSPersistentVolumeSource, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.StorageOSPersistentVolumeSource(**value)
        if isinstance(value, dict)
        else value
    )


def optional_list_converter_ContainerPort(
    value: Union[Sequence[kdsl.core.v1.ContainerPortUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.core.v1.ContainerPort], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_ContainerPort(x) for x in value]


def optional_converter_VsphereVirtualDiskVolumeSource(
    value: Union[kdsl.core.v1.VsphereVirtualDiskVolumeSourceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.VsphereVirtualDiskVolumeSource, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.VsphereVirtualDiskVolumeSource(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_Affinity(
    value: kdsl.core.v1.AffinityUnion,
) -> kdsl.core.v1.Affinity:
    import kdsl.core.v1

    return kdsl.core.v1.Affinity(**value) if isinstance(value, dict) else value


def required_converter_EphemeralContainerItem(
    value: kdsl.core.v1.EphemeralContainerItemUnion,
) -> kdsl.core.v1.EphemeralContainerItem:
    import kdsl.core.v1

    return (
        kdsl.core.v1.EphemeralContainerItem(**value)
        if isinstance(value, dict)
        else value
    )


def optional_mlist_converter_ReplicationControllerConditionItem(
    value: Union[
        Mapping[str, kdsl.core.v1.ReplicationControllerConditionItemUnion],
        OmitEnum,
        None,
    ]
) -> Union[
    Mapping[str, kdsl.core.v1.ReplicationControllerConditionItem], OmitEnum, None
]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {
            k: required_converter_ReplicationControllerConditionItem(v)
            for k, v in value.items()
        }


def required_converter_EmptyDirVolumeSource(
    value: kdsl.core.v1.EmptyDirVolumeSourceUnion,
) -> kdsl.core.v1.EmptyDirVolumeSource:
    import kdsl.core.v1

    return (
        kdsl.core.v1.EmptyDirVolumeSource(**value) if isinstance(value, dict) else value
    )


def required_converter_PersistentVolumeStatus(
    value: kdsl.core.v1.PersistentVolumeStatusUnion,
) -> kdsl.core.v1.PersistentVolumeStatus:
    import kdsl.core.v1

    return (
        kdsl.core.v1.PersistentVolumeStatus(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_NFSVolumeSource(
    value: kdsl.core.v1.NFSVolumeSourceUnion,
) -> kdsl.core.v1.NFSVolumeSource:
    import kdsl.core.v1

    return kdsl.core.v1.NFSVolumeSource(**value) if isinstance(value, dict) else value


def optional_list_converter_LoadBalancerIngress(
    value: Union[Sequence[kdsl.core.v1.LoadBalancerIngressUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.core.v1.LoadBalancerIngress], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_LoadBalancerIngress(x) for x in value]


def optional_converter_PersistentVolumeClaimSpec(
    value: Union[kdsl.core.v1.PersistentVolumeClaimSpecUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.PersistentVolumeClaimSpec, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.PersistentVolumeClaimSpec(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_TopologySelectorLabelRequirement(
    value: kdsl.core.v1.TopologySelectorLabelRequirementUnion,
) -> kdsl.core.v1.TopologySelectorLabelRequirement:
    import kdsl.core.v1

    return (
        kdsl.core.v1.TopologySelectorLabelRequirement(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_Lifecycle(
    value: kdsl.core.v1.LifecycleUnion,
) -> kdsl.core.v1.Lifecycle:
    import kdsl.core.v1

    return kdsl.core.v1.Lifecycle(**value) if isinstance(value, dict) else value


def required_converter_PodStatus(
    value: kdsl.core.v1.PodStatusUnion,
) -> kdsl.core.v1.PodStatus:
    import kdsl.core.v1

    return kdsl.core.v1.PodStatus(**value) if isinstance(value, dict) else value


def optional_converter_CSIVolumeSource(
    value: Union[kdsl.core.v1.CSIVolumeSourceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.CSIVolumeSource, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.CSIVolumeSource(**value) if isinstance(value, dict) else value


def optional_converter_AzureFileVolumeSource(
    value: Union[kdsl.core.v1.AzureFileVolumeSourceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.AzureFileVolumeSource, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.AzureFileVolumeSource(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_LoadBalancerIngress(
    value: kdsl.core.v1.LoadBalancerIngressUnion,
) -> kdsl.core.v1.LoadBalancerIngress:
    import kdsl.core.v1

    return (
        kdsl.core.v1.LoadBalancerIngress(**value) if isinstance(value, dict) else value
    )


def optional_converter_TypedLocalObjectReference(
    value: Union[kdsl.core.v1.TypedLocalObjectReferenceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.TypedLocalObjectReference, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.TypedLocalObjectReference(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_NodeConfigSource(
    value: kdsl.core.v1.NodeConfigSourceUnion,
) -> kdsl.core.v1.NodeConfigSource:
    import kdsl.core.v1

    return kdsl.core.v1.NodeConfigSource(**value) if isinstance(value, dict) else value


def required_converter_KeyToPath(
    value: kdsl.core.v1.KeyToPathUnion,
) -> kdsl.core.v1.KeyToPath:
    import kdsl.core.v1

    return kdsl.core.v1.KeyToPath(**value) if isinstance(value, dict) else value


def required_converter_EndpointPort(
    value: kdsl.core.v1.EndpointPortUnion,
) -> kdsl.core.v1.EndpointPort:
    import kdsl.core.v1

    return kdsl.core.v1.EndpointPort(**value) if isinstance(value, dict) else value


def optional_list_converter_WeightedPodAffinityTerm(
    value: Union[Sequence[kdsl.core.v1.WeightedPodAffinityTermUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.core.v1.WeightedPodAffinityTerm], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_WeightedPodAffinityTerm(x) for x in value]


def optional_list_converter_NodeSelectorRequirement(
    value: Union[Sequence[kdsl.core.v1.NodeSelectorRequirementUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.core.v1.NodeSelectorRequirement], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_NodeSelectorRequirement(x) for x in value]


def optional_list_converter_TopologySelectorTerm(
    value: Union[Sequence[kdsl.core.v1.TopologySelectorTermUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.core.v1.TopologySelectorTerm], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_TopologySelectorTerm(x) for x in value]


def optional_mlist_converter_VolumeItem(
    value: Union[Mapping[str, kdsl.core.v1.VolumeItemUnion], OmitEnum, None]
) -> Union[Mapping[str, kdsl.core.v1.VolumeItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {k: required_converter_VolumeItem(v) for k, v in value.items()}


def required_converter_EndpointSubset(
    value: kdsl.core.v1.EndpointSubsetUnion,
) -> kdsl.core.v1.EndpointSubset:
    import kdsl.core.v1

    return kdsl.core.v1.EndpointSubset(**value) if isinstance(value, dict) else value


def required_converter_LocalObjectReference(
    value: kdsl.core.v1.LocalObjectReferenceUnion,
) -> kdsl.core.v1.LocalObjectReference:
    import kdsl.core.v1

    return (
        kdsl.core.v1.LocalObjectReference(**value) if isinstance(value, dict) else value
    )


def required_converter_TopologySelectorTerm(
    value: kdsl.core.v1.TopologySelectorTermUnion,
) -> kdsl.core.v1.TopologySelectorTerm:
    import kdsl.core.v1

    return (
        kdsl.core.v1.TopologySelectorTerm(**value) if isinstance(value, dict) else value
    )


def required_list_converter_VolumeProjection(
    value: Sequence[kdsl.core.v1.VolumeProjectionUnion],
) -> Sequence[kdsl.core.v1.VolumeProjection]:
    return [required_converter_VolumeProjection(x) for x in value]


def optional_list_converter_VolumeMount(
    value: Union[Sequence[kdsl.core.v1.VolumeMountUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.core.v1.VolumeMount], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_VolumeMount(x) for x in value]


def required_converter_VolumeItem(
    value: kdsl.core.v1.VolumeItemUnion,
) -> kdsl.core.v1.VolumeItem:
    import kdsl.core.v1

    return kdsl.core.v1.VolumeItem(**value) if isinstance(value, dict) else value


def optional_converter_PersistentVolumeClaimConditionItem(
    value: Union[kdsl.core.v1.PersistentVolumeClaimConditionItemUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.PersistentVolumeClaimConditionItem, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.PersistentVolumeClaimConditionItem(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_PodDNSConfig(
    value: Union[kdsl.core.v1.PodDNSConfigUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.PodDNSConfig, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.PodDNSConfig(**value) if isinstance(value, dict) else value


def optional_converter_PodSecurityContext(
    value: Union[kdsl.core.v1.PodSecurityContextUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.PodSecurityContext, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.PodSecurityContext(**value) if isinstance(value, dict) else value
    )


def required_converter_SecretEnvSource(
    value: kdsl.core.v1.SecretEnvSourceUnion,
) -> kdsl.core.v1.SecretEnvSource:
    import kdsl.core.v1

    return kdsl.core.v1.SecretEnvSource(**value) if isinstance(value, dict) else value


def required_converter_PersistentVolumeSpec(
    value: kdsl.core.v1.PersistentVolumeSpecUnion,
) -> kdsl.core.v1.PersistentVolumeSpec:
    import kdsl.core.v1

    return (
        kdsl.core.v1.PersistentVolumeSpec(**value) if isinstance(value, dict) else value
    )


def required_converter_LocalVolumeSource(
    value: kdsl.core.v1.LocalVolumeSourceUnion,
) -> kdsl.core.v1.LocalVolumeSource:
    import kdsl.core.v1

    return kdsl.core.v1.LocalVolumeSource(**value) if isinstance(value, dict) else value


def required_converter_GlusterfsPersistentVolumeSource(
    value: kdsl.core.v1.GlusterfsPersistentVolumeSourceUnion,
) -> kdsl.core.v1.GlusterfsPersistentVolumeSource:
    import kdsl.core.v1

    return (
        kdsl.core.v1.GlusterfsPersistentVolumeSource(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_PodConditionItem(
    value: kdsl.core.v1.PodConditionItemUnion,
) -> kdsl.core.v1.PodConditionItem:
    import kdsl.core.v1

    return kdsl.core.v1.PodConditionItem(**value) if isinstance(value, dict) else value


def optional_converter_EmptyDirVolumeSource(
    value: Union[kdsl.core.v1.EmptyDirVolumeSourceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.EmptyDirVolumeSource, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.EmptyDirVolumeSource(**value) if isinstance(value, dict) else value
    )


def required_converter_ResourceQuotaSpec(
    value: kdsl.core.v1.ResourceQuotaSpecUnion,
) -> kdsl.core.v1.ResourceQuotaSpec:
    import kdsl.core.v1

    return kdsl.core.v1.ResourceQuotaSpec(**value) if isinstance(value, dict) else value


def optional_converter_PersistentVolumeStatus(
    value: Union[kdsl.core.v1.PersistentVolumeStatusUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.PersistentVolumeStatus, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.PersistentVolumeStatus(**value)
        if isinstance(value, dict)
        else value
    )


def optional_list_converter_LabelSelectorRequirement(
    value: Union[Sequence[kdsl.core.v1.LabelSelectorRequirementUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.core.v1.LabelSelectorRequirement], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_LabelSelectorRequirement(x) for x in value]


def optional_converter_Lifecycle(
    value: Union[kdsl.core.v1.LifecycleUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.Lifecycle, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.Lifecycle(**value) if isinstance(value, dict) else value


def optional_converter_PodStatus(
    value: Union[kdsl.core.v1.PodStatusUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.PodStatus, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.PodStatus(**value) if isinstance(value, dict) else value


def required_converter_LabelSelectorRequirement(
    value: kdsl.core.v1.LabelSelectorRequirementUnion,
) -> kdsl.core.v1.LabelSelectorRequirement:
    import kdsl.core.v1

    return (
        kdsl.core.v1.LabelSelectorRequirement(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_Toleration(
    value: kdsl.core.v1.TolerationUnion,
) -> kdsl.core.v1.Toleration:
    import kdsl.core.v1

    return kdsl.core.v1.Toleration(**value) if isinstance(value, dict) else value


def optional_converter_LoadBalancerIngress(
    value: Union[kdsl.core.v1.LoadBalancerIngressUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.LoadBalancerIngress, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.LoadBalancerIngress(**value) if isinstance(value, dict) else value
    )


def required_converter_ConfigMapVolumeSource(
    value: kdsl.core.v1.ConfigMapVolumeSourceUnion,
) -> kdsl.core.v1.ConfigMapVolumeSource:
    import kdsl.core.v1

    return (
        kdsl.core.v1.ConfigMapVolumeSource(**value)
        if isinstance(value, dict)
        else value
    )


def optional_list_converter_PreferredSchedulingTerm(
    value: Union[Sequence[kdsl.core.v1.PreferredSchedulingTermUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.core.v1.PreferredSchedulingTerm], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_PreferredSchedulingTerm(x) for x in value]


def optional_converter_NodeConfigSource(
    value: Union[kdsl.core.v1.NodeConfigSourceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.NodeConfigSource, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.NodeConfigSource(**value) if isinstance(value, dict) else value


def required_converter_LimitRangeSpec(
    value: kdsl.core.v1.LimitRangeSpecUnion,
) -> kdsl.core.v1.LimitRangeSpec:
    import kdsl.core.v1

    return kdsl.core.v1.LimitRangeSpec(**value) if isinstance(value, dict) else value


def required_converter_NodeAddressItem(
    value: kdsl.core.v1.NodeAddressItemUnion,
) -> kdsl.core.v1.NodeAddressItem:
    import kdsl.core.v1

    return kdsl.core.v1.NodeAddressItem(**value) if isinstance(value, dict) else value


def optional_converter_WeightedPodAffinityTerm(
    value: Union[kdsl.core.v1.WeightedPodAffinityTermUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.WeightedPodAffinityTerm, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.WeightedPodAffinityTerm(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_LocalObjectReference(
    value: Union[kdsl.core.v1.LocalObjectReferenceUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.LocalObjectReference, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.LocalObjectReference(**value) if isinstance(value, dict) else value
    )


def required_converter_ConfigMapKeySelector(
    value: kdsl.core.v1.ConfigMapKeySelectorUnion,
) -> kdsl.core.v1.ConfigMapKeySelector:
    import kdsl.core.v1

    return (
        kdsl.core.v1.ConfigMapKeySelector(**value) if isinstance(value, dict) else value
    )


def optional_converter_TopologySelectorTerm(
    value: Union[kdsl.core.v1.TopologySelectorTermUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.TopologySelectorTerm, OmitEnum, None]:
    import kdsl.core.v1

    return (
        kdsl.core.v1.TopologySelectorTerm(**value) if isinstance(value, dict) else value
    )


def required_converter_PodDNSConfigOption(
    value: kdsl.core.v1.PodDNSConfigOptionUnion,
) -> kdsl.core.v1.PodDNSConfigOption:
    import kdsl.core.v1

    return (
        kdsl.core.v1.PodDNSConfigOption(**value) if isinstance(value, dict) else value
    )


def required_converter_ObjectReference(
    value: kdsl.core.v1.ObjectReferenceUnion,
) -> kdsl.core.v1.ObjectReference:
    import kdsl.core.v1

    return kdsl.core.v1.ObjectReference(**value) if isinstance(value, dict) else value


def required_converter_VolumeProjection(
    value: kdsl.core.v1.VolumeProjectionUnion,
) -> kdsl.core.v1.VolumeProjection:
    import kdsl.core.v1

    return kdsl.core.v1.VolumeProjection(**value) if isinstance(value, dict) else value


def required_converter_Preconditions(
    value: kdsl.core.v1.PreconditionsUnion,
) -> kdsl.core.v1.Preconditions:
    import kdsl.core.v1

    return kdsl.core.v1.Preconditions(**value) if isinstance(value, dict) else value


def optional_converter_VolumeMount(
    value: Union[kdsl.core.v1.VolumeMountUnion, OmitEnum, None]
) -> Union[kdsl.core.v1.VolumeMount, OmitEnum, None]:
    import kdsl.core.v1

    return kdsl.core.v1.VolumeMount(**value) if isinstance(value, dict) else value


def required_converter_ExecAction(
    value: kdsl.core.v1.ExecActionUnion,
) -> kdsl.core.v1.ExecAction:
    import kdsl.core.v1

    return kdsl.core.v1.ExecAction(**value) if isinstance(value, dict) else value
