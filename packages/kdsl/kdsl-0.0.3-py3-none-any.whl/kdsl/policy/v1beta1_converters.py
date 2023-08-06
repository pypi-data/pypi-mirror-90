from __future__ import annotations
from typing import Sequence, Literal, Union
from kdsl.bases import OmitEnum, OMIT
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import kdsl.policy.v1beta1


def required_converter_SupplementalGroupsStrategyOptions(
    value: kdsl.policy.v1beta1.SupplementalGroupsStrategyOptionsUnion,
) -> kdsl.policy.v1beta1.SupplementalGroupsStrategyOptions:
    import kdsl.policy.v1beta1

    return (
        kdsl.policy.v1beta1.SupplementalGroupsStrategyOptions(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_HostPortRange(
    value: kdsl.policy.v1beta1.HostPortRangeUnion,
) -> kdsl.policy.v1beta1.HostPortRange:
    import kdsl.policy.v1beta1

    return (
        kdsl.policy.v1beta1.HostPortRange(**value) if isinstance(value, dict) else value
    )


def required_converter_IDRange(
    value: kdsl.policy.v1beta1.IDRangeUnion,
) -> kdsl.policy.v1beta1.IDRange:
    import kdsl.policy.v1beta1

    return kdsl.policy.v1beta1.IDRange(**value) if isinstance(value, dict) else value


def required_converter_FSGroupStrategyOptions(
    value: kdsl.policy.v1beta1.FSGroupStrategyOptionsUnion,
) -> kdsl.policy.v1beta1.FSGroupStrategyOptions:
    import kdsl.policy.v1beta1

    return (
        kdsl.policy.v1beta1.FSGroupStrategyOptions(**value)
        if isinstance(value, dict)
        else value
    )


def optional_list_converter_AllowedFlexVolume(
    value: Union[Sequence[kdsl.policy.v1beta1.AllowedFlexVolumeUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.policy.v1beta1.AllowedFlexVolume], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_AllowedFlexVolume(x) for x in value]


def required_converter_RuntimeClassStrategyOptions(
    value: kdsl.policy.v1beta1.RuntimeClassStrategyOptionsUnion,
) -> kdsl.policy.v1beta1.RuntimeClassStrategyOptions:
    import kdsl.policy.v1beta1

    return (
        kdsl.policy.v1beta1.RuntimeClassStrategyOptions(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_PodDisruptionBudgetStatus(
    value: Union[kdsl.policy.v1beta1.PodDisruptionBudgetStatusUnion, OmitEnum, None]
) -> Union[kdsl.policy.v1beta1.PodDisruptionBudgetStatus, OmitEnum, None]:
    import kdsl.policy.v1beta1

    return (
        kdsl.policy.v1beta1.PodDisruptionBudgetStatus(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_SELinuxStrategyOptions(
    value: Union[kdsl.policy.v1beta1.SELinuxStrategyOptionsUnion, OmitEnum, None]
) -> Union[kdsl.policy.v1beta1.SELinuxStrategyOptions, OmitEnum, None]:
    import kdsl.policy.v1beta1

    return (
        kdsl.policy.v1beta1.SELinuxStrategyOptions(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_RunAsUserStrategyOptions(
    value: kdsl.policy.v1beta1.RunAsUserStrategyOptionsUnion,
) -> kdsl.policy.v1beta1.RunAsUserStrategyOptions:
    import kdsl.policy.v1beta1

    return (
        kdsl.policy.v1beta1.RunAsUserStrategyOptions(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_RunAsGroupStrategyOptions(
    value: kdsl.policy.v1beta1.RunAsGroupStrategyOptionsUnion,
) -> kdsl.policy.v1beta1.RunAsGroupStrategyOptions:
    import kdsl.policy.v1beta1

    return (
        kdsl.policy.v1beta1.RunAsGroupStrategyOptions(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_SupplementalGroupsStrategyOptions(
    value: Union[
        kdsl.policy.v1beta1.SupplementalGroupsStrategyOptionsUnion, OmitEnum, None
    ]
) -> Union[kdsl.policy.v1beta1.SupplementalGroupsStrategyOptions, OmitEnum, None]:
    import kdsl.policy.v1beta1

    return (
        kdsl.policy.v1beta1.SupplementalGroupsStrategyOptions(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_HostPortRange(
    value: Union[kdsl.policy.v1beta1.HostPortRangeUnion, OmitEnum, None]
) -> Union[kdsl.policy.v1beta1.HostPortRange, OmitEnum, None]:
    import kdsl.policy.v1beta1

    return (
        kdsl.policy.v1beta1.HostPortRange(**value) if isinstance(value, dict) else value
    )


def required_converter_AllowedFlexVolume(
    value: kdsl.policy.v1beta1.AllowedFlexVolumeUnion,
) -> kdsl.policy.v1beta1.AllowedFlexVolume:
    import kdsl.policy.v1beta1

    return (
        kdsl.policy.v1beta1.AllowedFlexVolume(**value)
        if isinstance(value, dict)
        else value
    )


def optional_list_converter_AllowedCSIDriver(
    value: Union[Sequence[kdsl.policy.v1beta1.AllowedCSIDriverUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.policy.v1beta1.AllowedCSIDriver], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_AllowedCSIDriver(x) for x in value]


def optional_converter_IDRange(
    value: Union[kdsl.policy.v1beta1.IDRangeUnion, OmitEnum, None]
) -> Union[kdsl.policy.v1beta1.IDRange, OmitEnum, None]:
    import kdsl.policy.v1beta1

    return kdsl.policy.v1beta1.IDRange(**value) if isinstance(value, dict) else value


def optional_list_converter_AllowedHostPath(
    value: Union[Sequence[kdsl.policy.v1beta1.AllowedHostPathUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.policy.v1beta1.AllowedHostPath], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_AllowedHostPath(x) for x in value]


def required_converter_AllowedCSIDriver(
    value: kdsl.policy.v1beta1.AllowedCSIDriverUnion,
) -> kdsl.policy.v1beta1.AllowedCSIDriver:
    import kdsl.policy.v1beta1

    return (
        kdsl.policy.v1beta1.AllowedCSIDriver(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_AllowedHostPath(
    value: kdsl.policy.v1beta1.AllowedHostPathUnion,
) -> kdsl.policy.v1beta1.AllowedHostPath:
    import kdsl.policy.v1beta1

    return (
        kdsl.policy.v1beta1.AllowedHostPath(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_RuntimeClassStrategyOptions(
    value: Union[kdsl.policy.v1beta1.RuntimeClassStrategyOptionsUnion, OmitEnum, None]
) -> Union[kdsl.policy.v1beta1.RuntimeClassStrategyOptions, OmitEnum, None]:
    import kdsl.policy.v1beta1

    return (
        kdsl.policy.v1beta1.RuntimeClassStrategyOptions(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_FSGroupStrategyOptions(
    value: Union[kdsl.policy.v1beta1.FSGroupStrategyOptionsUnion, OmitEnum, None]
) -> Union[kdsl.policy.v1beta1.FSGroupStrategyOptions, OmitEnum, None]:
    import kdsl.policy.v1beta1

    return (
        kdsl.policy.v1beta1.FSGroupStrategyOptions(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_PodDisruptionBudgetSpec(
    value: kdsl.policy.v1beta1.PodDisruptionBudgetSpecUnion,
) -> kdsl.policy.v1beta1.PodDisruptionBudgetSpec:
    import kdsl.policy.v1beta1

    return (
        kdsl.policy.v1beta1.PodDisruptionBudgetSpec(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_PodSecurityPolicySpec(
    value: kdsl.policy.v1beta1.PodSecurityPolicySpecUnion,
) -> kdsl.policy.v1beta1.PodSecurityPolicySpec:
    import kdsl.policy.v1beta1

    return (
        kdsl.policy.v1beta1.PodSecurityPolicySpec(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_RunAsUserStrategyOptions(
    value: Union[kdsl.policy.v1beta1.RunAsUserStrategyOptionsUnion, OmitEnum, None]
) -> Union[kdsl.policy.v1beta1.RunAsUserStrategyOptions, OmitEnum, None]:
    import kdsl.policy.v1beta1

    return (
        kdsl.policy.v1beta1.RunAsUserStrategyOptions(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_RunAsGroupStrategyOptions(
    value: Union[kdsl.policy.v1beta1.RunAsGroupStrategyOptionsUnion, OmitEnum, None]
) -> Union[kdsl.policy.v1beta1.RunAsGroupStrategyOptions, OmitEnum, None]:
    import kdsl.policy.v1beta1

    return (
        kdsl.policy.v1beta1.RunAsGroupStrategyOptions(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_AllowedFlexVolume(
    value: Union[kdsl.policy.v1beta1.AllowedFlexVolumeUnion, OmitEnum, None]
) -> Union[kdsl.policy.v1beta1.AllowedFlexVolume, OmitEnum, None]:
    import kdsl.policy.v1beta1

    return (
        kdsl.policy.v1beta1.AllowedFlexVolume(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_AllowedCSIDriver(
    value: Union[kdsl.policy.v1beta1.AllowedCSIDriverUnion, OmitEnum, None]
) -> Union[kdsl.policy.v1beta1.AllowedCSIDriver, OmitEnum, None]:
    import kdsl.policy.v1beta1

    return (
        kdsl.policy.v1beta1.AllowedCSIDriver(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_PodDisruptionBudgetSpec(
    value: Union[kdsl.policy.v1beta1.PodDisruptionBudgetSpecUnion, OmitEnum, None]
) -> Union[kdsl.policy.v1beta1.PodDisruptionBudgetSpec, OmitEnum, None]:
    import kdsl.policy.v1beta1

    return (
        kdsl.policy.v1beta1.PodDisruptionBudgetSpec(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_AllowedHostPath(
    value: Union[kdsl.policy.v1beta1.AllowedHostPathUnion, OmitEnum, None]
) -> Union[kdsl.policy.v1beta1.AllowedHostPath, OmitEnum, None]:
    import kdsl.policy.v1beta1

    return (
        kdsl.policy.v1beta1.AllowedHostPath(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_PodSecurityPolicySpec(
    value: Union[kdsl.policy.v1beta1.PodSecurityPolicySpecUnion, OmitEnum, None]
) -> Union[kdsl.policy.v1beta1.PodSecurityPolicySpec, OmitEnum, None]:
    import kdsl.policy.v1beta1

    return (
        kdsl.policy.v1beta1.PodSecurityPolicySpec(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_PodDisruptionBudgetStatus(
    value: kdsl.policy.v1beta1.PodDisruptionBudgetStatusUnion,
) -> kdsl.policy.v1beta1.PodDisruptionBudgetStatus:
    import kdsl.policy.v1beta1

    return (
        kdsl.policy.v1beta1.PodDisruptionBudgetStatus(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_SELinuxStrategyOptions(
    value: kdsl.policy.v1beta1.SELinuxStrategyOptionsUnion,
) -> kdsl.policy.v1beta1.SELinuxStrategyOptions:
    import kdsl.policy.v1beta1

    return (
        kdsl.policy.v1beta1.SELinuxStrategyOptions(**value)
        if isinstance(value, dict)
        else value
    )


def optional_list_converter_HostPortRange(
    value: Union[Sequence[kdsl.policy.v1beta1.HostPortRangeUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.policy.v1beta1.HostPortRange], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_HostPortRange(x) for x in value]


def optional_list_converter_IDRange(
    value: Union[Sequence[kdsl.policy.v1beta1.IDRangeUnion], OmitEnum, None]
) -> Union[Sequence[kdsl.policy.v1beta1.IDRange], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_IDRange(x) for x in value]
