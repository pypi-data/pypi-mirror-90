from __future__ import annotations
from typing import Mapping, Literal, Union
from kdsl.bases import OmitEnum, OMIT
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import kdsl.apps.v1


def required_converter_StatefulSetSpec(
    value: kdsl.apps.v1.StatefulSetSpecUnion,
) -> kdsl.apps.v1.StatefulSetSpec:
    import kdsl.apps.v1

    return kdsl.apps.v1.StatefulSetSpec(**value) if isinstance(value, dict) else value


def required_converter_DeploymentStatus(
    value: kdsl.apps.v1.DeploymentStatusUnion,
) -> kdsl.apps.v1.DeploymentStatus:
    import kdsl.apps.v1

    return kdsl.apps.v1.DeploymentStatus(**value) if isinstance(value, dict) else value


def optional_converter_DaemonSetStatus(
    value: Union[kdsl.apps.v1.DaemonSetStatusUnion, OmitEnum, None]
) -> Union[kdsl.apps.v1.DaemonSetStatus, OmitEnum, None]:
    import kdsl.apps.v1

    return kdsl.apps.v1.DaemonSetStatus(**value) if isinstance(value, dict) else value


def optional_converter_RollingUpdateDeployment(
    value: Union[kdsl.apps.v1.RollingUpdateDeploymentUnion, OmitEnum, None]
) -> Union[kdsl.apps.v1.RollingUpdateDeployment, OmitEnum, None]:
    import kdsl.apps.v1

    return (
        kdsl.apps.v1.RollingUpdateDeployment(**value)
        if isinstance(value, dict)
        else value
    )


def optional_mlist_converter_StatefulSetConditionItem(
    value: Union[
        Mapping[str, kdsl.apps.v1.StatefulSetConditionItemUnion], OmitEnum, None
    ]
) -> Union[Mapping[str, kdsl.apps.v1.StatefulSetConditionItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {
            k: required_converter_StatefulSetConditionItem(v) for k, v in value.items()
        }


def required_converter_RollingUpdateDaemonSet(
    value: kdsl.apps.v1.RollingUpdateDaemonSetUnion,
) -> kdsl.apps.v1.RollingUpdateDaemonSet:
    import kdsl.apps.v1

    return (
        kdsl.apps.v1.RollingUpdateDaemonSet(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_ReplicaSetStatus(
    value: Union[kdsl.apps.v1.ReplicaSetStatusUnion, OmitEnum, None]
) -> Union[kdsl.apps.v1.ReplicaSetStatus, OmitEnum, None]:
    import kdsl.apps.v1

    return kdsl.apps.v1.ReplicaSetStatus(**value) if isinstance(value, dict) else value


def optional_converter_DeploymentSpec(
    value: Union[kdsl.apps.v1.DeploymentSpecUnion, OmitEnum, None]
) -> Union[kdsl.apps.v1.DeploymentSpec, OmitEnum, None]:
    import kdsl.apps.v1

    return kdsl.apps.v1.DeploymentSpec(**value) if isinstance(value, dict) else value


def required_converter_DaemonSetSpec(
    value: kdsl.apps.v1.DaemonSetSpecUnion,
) -> kdsl.apps.v1.DaemonSetSpec:
    import kdsl.apps.v1

    return kdsl.apps.v1.DaemonSetSpec(**value) if isinstance(value, dict) else value


def required_converter_StatefulSetUpdateStrategy(
    value: kdsl.apps.v1.StatefulSetUpdateStrategyUnion,
) -> kdsl.apps.v1.StatefulSetUpdateStrategy:
    import kdsl.apps.v1

    return (
        kdsl.apps.v1.StatefulSetUpdateStrategy(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_StatefulSetStatus(
    value: Union[kdsl.apps.v1.StatefulSetStatusUnion, OmitEnum, None]
) -> Union[kdsl.apps.v1.StatefulSetStatus, OmitEnum, None]:
    import kdsl.apps.v1

    return kdsl.apps.v1.StatefulSetStatus(**value) if isinstance(value, dict) else value


def optional_converter_DaemonSetUpdateStrategy(
    value: Union[kdsl.apps.v1.DaemonSetUpdateStrategyUnion, OmitEnum, None]
) -> Union[kdsl.apps.v1.DaemonSetUpdateStrategy, OmitEnum, None]:
    import kdsl.apps.v1

    return (
        kdsl.apps.v1.DaemonSetUpdateStrategy(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_ReplicaSetSpec(
    value: Union[kdsl.apps.v1.ReplicaSetSpecUnion, OmitEnum, None]
) -> Union[kdsl.apps.v1.ReplicaSetSpec, OmitEnum, None]:
    import kdsl.apps.v1

    return kdsl.apps.v1.ReplicaSetSpec(**value) if isinstance(value, dict) else value


def required_converter_ReplicaSetConditionItem(
    value: kdsl.apps.v1.ReplicaSetConditionItemUnion,
) -> kdsl.apps.v1.ReplicaSetConditionItem:
    import kdsl.apps.v1

    return (
        kdsl.apps.v1.ReplicaSetConditionItem(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_DaemonSetConditionItem(
    value: kdsl.apps.v1.DaemonSetConditionItemUnion,
) -> kdsl.apps.v1.DaemonSetConditionItem:
    import kdsl.apps.v1

    return (
        kdsl.apps.v1.DaemonSetConditionItem(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_StatefulSetSpec(
    value: Union[kdsl.apps.v1.StatefulSetSpecUnion, OmitEnum, None]
) -> Union[kdsl.apps.v1.StatefulSetSpec, OmitEnum, None]:
    import kdsl.apps.v1

    return kdsl.apps.v1.StatefulSetSpec(**value) if isinstance(value, dict) else value


def optional_converter_DeploymentStatus(
    value: Union[kdsl.apps.v1.DeploymentStatusUnion, OmitEnum, None]
) -> Union[kdsl.apps.v1.DeploymentStatus, OmitEnum, None]:
    import kdsl.apps.v1

    return kdsl.apps.v1.DeploymentStatus(**value) if isinstance(value, dict) else value


def required_converter_DeploymentStrategy(
    value: kdsl.apps.v1.DeploymentStrategyUnion,
) -> kdsl.apps.v1.DeploymentStrategy:
    import kdsl.apps.v1

    return (
        kdsl.apps.v1.DeploymentStrategy(**value) if isinstance(value, dict) else value
    )


def optional_converter_RollingUpdateDaemonSet(
    value: Union[kdsl.apps.v1.RollingUpdateDaemonSetUnion, OmitEnum, None]
) -> Union[kdsl.apps.v1.RollingUpdateDaemonSet, OmitEnum, None]:
    import kdsl.apps.v1

    return (
        kdsl.apps.v1.RollingUpdateDaemonSet(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_DaemonSetSpec(
    value: Union[kdsl.apps.v1.DaemonSetSpecUnion, OmitEnum, None]
) -> Union[kdsl.apps.v1.DaemonSetSpec, OmitEnum, None]:
    import kdsl.apps.v1

    return kdsl.apps.v1.DaemonSetSpec(**value) if isinstance(value, dict) else value


def optional_converter_StatefulSetUpdateStrategy(
    value: Union[kdsl.apps.v1.StatefulSetUpdateStrategyUnion, OmitEnum, None]
) -> Union[kdsl.apps.v1.StatefulSetUpdateStrategy, OmitEnum, None]:
    import kdsl.apps.v1

    return (
        kdsl.apps.v1.StatefulSetUpdateStrategy(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_RollingUpdateStatefulSetStrategy(
    value: kdsl.apps.v1.RollingUpdateStatefulSetStrategyUnion,
) -> kdsl.apps.v1.RollingUpdateStatefulSetStrategy:
    import kdsl.apps.v1

    return (
        kdsl.apps.v1.RollingUpdateStatefulSetStrategy(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_ReplicaSetConditionItem(
    value: Union[kdsl.apps.v1.ReplicaSetConditionItemUnion, OmitEnum, None]
) -> Union[kdsl.apps.v1.ReplicaSetConditionItem, OmitEnum, None]:
    import kdsl.apps.v1

    return (
        kdsl.apps.v1.ReplicaSetConditionItem(**value)
        if isinstance(value, dict)
        else value
    )


def optional_mlist_converter_ReplicaSetConditionItem(
    value: Union[
        Mapping[str, kdsl.apps.v1.ReplicaSetConditionItemUnion], OmitEnum, None
    ]
) -> Union[Mapping[str, kdsl.apps.v1.ReplicaSetConditionItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {
            k: required_converter_ReplicaSetConditionItem(v) for k, v in value.items()
        }


def required_converter_DeploymentConditionItem(
    value: kdsl.apps.v1.DeploymentConditionItemUnion,
) -> kdsl.apps.v1.DeploymentConditionItem:
    import kdsl.apps.v1

    return (
        kdsl.apps.v1.DeploymentConditionItem(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_StatefulSetConditionItem(
    value: kdsl.apps.v1.StatefulSetConditionItemUnion,
) -> kdsl.apps.v1.StatefulSetConditionItem:
    import kdsl.apps.v1

    return (
        kdsl.apps.v1.StatefulSetConditionItem(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_DaemonSetConditionItem(
    value: Union[kdsl.apps.v1.DaemonSetConditionItemUnion, OmitEnum, None]
) -> Union[kdsl.apps.v1.DaemonSetConditionItem, OmitEnum, None]:
    import kdsl.apps.v1

    return (
        kdsl.apps.v1.DaemonSetConditionItem(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_DaemonSetStatus(
    value: kdsl.apps.v1.DaemonSetStatusUnion,
) -> kdsl.apps.v1.DaemonSetStatus:
    import kdsl.apps.v1

    return kdsl.apps.v1.DaemonSetStatus(**value) if isinstance(value, dict) else value


def required_converter_RollingUpdateDeployment(
    value: kdsl.apps.v1.RollingUpdateDeploymentUnion,
) -> kdsl.apps.v1.RollingUpdateDeployment:
    import kdsl.apps.v1

    return (
        kdsl.apps.v1.RollingUpdateDeployment(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_DeploymentStrategy(
    value: Union[kdsl.apps.v1.DeploymentStrategyUnion, OmitEnum, None]
) -> Union[kdsl.apps.v1.DeploymentStrategy, OmitEnum, None]:
    import kdsl.apps.v1

    return (
        kdsl.apps.v1.DeploymentStrategy(**value) if isinstance(value, dict) else value
    )


def required_converter_ReplicaSetStatus(
    value: kdsl.apps.v1.ReplicaSetStatusUnion,
) -> kdsl.apps.v1.ReplicaSetStatus:
    import kdsl.apps.v1

    return kdsl.apps.v1.ReplicaSetStatus(**value) if isinstance(value, dict) else value


def optional_mlist_converter_DeploymentConditionItem(
    value: Union[
        Mapping[str, kdsl.apps.v1.DeploymentConditionItemUnion], OmitEnum, None
    ]
) -> Union[Mapping[str, kdsl.apps.v1.DeploymentConditionItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {
            k: required_converter_DeploymentConditionItem(v) for k, v in value.items()
        }


def required_converter_DeploymentSpec(
    value: kdsl.apps.v1.DeploymentSpecUnion,
) -> kdsl.apps.v1.DeploymentSpec:
    import kdsl.apps.v1

    return kdsl.apps.v1.DeploymentSpec(**value) if isinstance(value, dict) else value


def optional_converter_DeploymentConditionItem(
    value: Union[kdsl.apps.v1.DeploymentConditionItemUnion, OmitEnum, None]
) -> Union[kdsl.apps.v1.DeploymentConditionItem, OmitEnum, None]:
    import kdsl.apps.v1

    return (
        kdsl.apps.v1.DeploymentConditionItem(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_RollingUpdateStatefulSetStrategy(
    value: Union[kdsl.apps.v1.RollingUpdateStatefulSetStrategyUnion, OmitEnum, None]
) -> Union[kdsl.apps.v1.RollingUpdateStatefulSetStrategy, OmitEnum, None]:
    import kdsl.apps.v1

    return (
        kdsl.apps.v1.RollingUpdateStatefulSetStrategy(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_StatefulSetStatus(
    value: kdsl.apps.v1.StatefulSetStatusUnion,
) -> kdsl.apps.v1.StatefulSetStatus:
    import kdsl.apps.v1

    return kdsl.apps.v1.StatefulSetStatus(**value) if isinstance(value, dict) else value


def required_converter_DaemonSetUpdateStrategy(
    value: kdsl.apps.v1.DaemonSetUpdateStrategyUnion,
) -> kdsl.apps.v1.DaemonSetUpdateStrategy:
    import kdsl.apps.v1

    return (
        kdsl.apps.v1.DaemonSetUpdateStrategy(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_ReplicaSetSpec(
    value: kdsl.apps.v1.ReplicaSetSpecUnion,
) -> kdsl.apps.v1.ReplicaSetSpec:
    import kdsl.apps.v1

    return kdsl.apps.v1.ReplicaSetSpec(**value) if isinstance(value, dict) else value


def optional_mlist_converter_DaemonSetConditionItem(
    value: Union[Mapping[str, kdsl.apps.v1.DaemonSetConditionItemUnion], OmitEnum, None]
) -> Union[Mapping[str, kdsl.apps.v1.DaemonSetConditionItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {
            k: required_converter_DaemonSetConditionItem(v) for k, v in value.items()
        }


def optional_converter_StatefulSetConditionItem(
    value: Union[kdsl.apps.v1.StatefulSetConditionItemUnion, OmitEnum, None]
) -> Union[kdsl.apps.v1.StatefulSetConditionItem, OmitEnum, None]:
    import kdsl.apps.v1

    return (
        kdsl.apps.v1.StatefulSetConditionItem(**value)
        if isinstance(value, dict)
        else value
    )
