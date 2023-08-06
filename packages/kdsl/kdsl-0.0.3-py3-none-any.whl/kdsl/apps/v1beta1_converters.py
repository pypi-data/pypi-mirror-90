from __future__ import annotations
from typing import Mapping, Literal, Union
from kdsl.bases import OmitEnum, OMIT
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import kdsl.apps.v1beta1


def optional_converter_RollingUpdateStatefulSetStrategy(
    value: Union[
        kdsl.apps.v1beta1.RollingUpdateStatefulSetStrategyUnion, OmitEnum, None
    ]
) -> Union[kdsl.apps.v1beta1.RollingUpdateStatefulSetStrategy, OmitEnum, None]:
    import kdsl.apps.v1beta1

    return (
        kdsl.apps.v1beta1.RollingUpdateStatefulSetStrategy(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_StatefulSetUpdateStrategy(
    value: Union[kdsl.apps.v1beta1.StatefulSetUpdateStrategyUnion, OmitEnum, None]
) -> Union[kdsl.apps.v1beta1.StatefulSetUpdateStrategy, OmitEnum, None]:
    import kdsl.apps.v1beta1

    return (
        kdsl.apps.v1beta1.StatefulSetUpdateStrategy(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_RollingUpdateDeployment(
    value: Union[kdsl.apps.v1beta1.RollingUpdateDeploymentUnion, OmitEnum, None]
) -> Union[kdsl.apps.v1beta1.RollingUpdateDeployment, OmitEnum, None]:
    import kdsl.apps.v1beta1

    return (
        kdsl.apps.v1beta1.RollingUpdateDeployment(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_StatefulSetConditionItem(
    value: kdsl.apps.v1beta1.StatefulSetConditionItemUnion,
) -> kdsl.apps.v1beta1.StatefulSetConditionItem:
    import kdsl.apps.v1beta1

    return (
        kdsl.apps.v1beta1.StatefulSetConditionItem(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_StatefulSetStatus(
    value: kdsl.apps.v1beta1.StatefulSetStatusUnion,
) -> kdsl.apps.v1beta1.StatefulSetStatus:
    import kdsl.apps.v1beta1

    return (
        kdsl.apps.v1beta1.StatefulSetStatus(**value)
        if isinstance(value, dict)
        else value
    )


def optional_mlist_converter_StatefulSetConditionItem(
    value: Union[
        Mapping[str, kdsl.apps.v1beta1.StatefulSetConditionItemUnion], OmitEnum, None
    ]
) -> Union[Mapping[str, kdsl.apps.v1beta1.StatefulSetConditionItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {
            k: required_converter_StatefulSetConditionItem(v) for k, v in value.items()
        }


def optional_mlist_converter_DeploymentConditionItem(
    value: Union[
        Mapping[str, kdsl.apps.v1beta1.DeploymentConditionItemUnion], OmitEnum, None
    ]
) -> Union[Mapping[str, kdsl.apps.v1beta1.DeploymentConditionItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {
            k: required_converter_DeploymentConditionItem(v) for k, v in value.items()
        }


def required_converter_StatefulSetSpec(
    value: kdsl.apps.v1beta1.StatefulSetSpecUnion,
) -> kdsl.apps.v1beta1.StatefulSetSpec:
    import kdsl.apps.v1beta1

    return (
        kdsl.apps.v1beta1.StatefulSetSpec(**value) if isinstance(value, dict) else value
    )


def required_converter_DeploymentSpec(
    value: kdsl.apps.v1beta1.DeploymentSpecUnion,
) -> kdsl.apps.v1beta1.DeploymentSpec:
    import kdsl.apps.v1beta1

    return (
        kdsl.apps.v1beta1.DeploymentSpec(**value) if isinstance(value, dict) else value
    )


def optional_converter_DeploymentConditionItem(
    value: Union[kdsl.apps.v1beta1.DeploymentConditionItemUnion, OmitEnum, None]
) -> Union[kdsl.apps.v1beta1.DeploymentConditionItem, OmitEnum, None]:
    import kdsl.apps.v1beta1

    return (
        kdsl.apps.v1beta1.DeploymentConditionItem(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_DeploymentStrategy(
    value: Union[kdsl.apps.v1beta1.DeploymentStrategyUnion, OmitEnum, None]
) -> Union[kdsl.apps.v1beta1.DeploymentStrategy, OmitEnum, None]:
    import kdsl.apps.v1beta1

    return (
        kdsl.apps.v1beta1.DeploymentStrategy(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_StatefulSetConditionItem(
    value: Union[kdsl.apps.v1beta1.StatefulSetConditionItemUnion, OmitEnum, None]
) -> Union[kdsl.apps.v1beta1.StatefulSetConditionItem, OmitEnum, None]:
    import kdsl.apps.v1beta1

    return (
        kdsl.apps.v1beta1.StatefulSetConditionItem(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_StatefulSetStatus(
    value: Union[kdsl.apps.v1beta1.StatefulSetStatusUnion, OmitEnum, None]
) -> Union[kdsl.apps.v1beta1.StatefulSetStatus, OmitEnum, None]:
    import kdsl.apps.v1beta1

    return (
        kdsl.apps.v1beta1.StatefulSetStatus(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_DeploymentStatus(
    value: kdsl.apps.v1beta1.DeploymentStatusUnion,
) -> kdsl.apps.v1beta1.DeploymentStatus:
    import kdsl.apps.v1beta1

    return (
        kdsl.apps.v1beta1.DeploymentStatus(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_StatefulSetSpec(
    value: Union[kdsl.apps.v1beta1.StatefulSetSpecUnion, OmitEnum, None]
) -> Union[kdsl.apps.v1beta1.StatefulSetSpec, OmitEnum, None]:
    import kdsl.apps.v1beta1

    return (
        kdsl.apps.v1beta1.StatefulSetSpec(**value) if isinstance(value, dict) else value
    )


def required_converter_RollbackConfig(
    value: kdsl.apps.v1beta1.RollbackConfigUnion,
) -> kdsl.apps.v1beta1.RollbackConfig:
    import kdsl.apps.v1beta1

    return (
        kdsl.apps.v1beta1.RollbackConfig(**value) if isinstance(value, dict) else value
    )


def optional_converter_DeploymentSpec(
    value: Union[kdsl.apps.v1beta1.DeploymentSpecUnion, OmitEnum, None]
) -> Union[kdsl.apps.v1beta1.DeploymentSpec, OmitEnum, None]:
    import kdsl.apps.v1beta1

    return (
        kdsl.apps.v1beta1.DeploymentSpec(**value) if isinstance(value, dict) else value
    )


def required_converter_RollingUpdateStatefulSetStrategy(
    value: kdsl.apps.v1beta1.RollingUpdateStatefulSetStrategyUnion,
) -> kdsl.apps.v1beta1.RollingUpdateStatefulSetStrategy:
    import kdsl.apps.v1beta1

    return (
        kdsl.apps.v1beta1.RollingUpdateStatefulSetStrategy(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_StatefulSetUpdateStrategy(
    value: kdsl.apps.v1beta1.StatefulSetUpdateStrategyUnion,
) -> kdsl.apps.v1beta1.StatefulSetUpdateStrategy:
    import kdsl.apps.v1beta1

    return (
        kdsl.apps.v1beta1.StatefulSetUpdateStrategy(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_RollingUpdateDeployment(
    value: kdsl.apps.v1beta1.RollingUpdateDeploymentUnion,
) -> kdsl.apps.v1beta1.RollingUpdateDeployment:
    import kdsl.apps.v1beta1

    return (
        kdsl.apps.v1beta1.RollingUpdateDeployment(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_DeploymentStatus(
    value: Union[kdsl.apps.v1beta1.DeploymentStatusUnion, OmitEnum, None]
) -> Union[kdsl.apps.v1beta1.DeploymentStatus, OmitEnum, None]:
    import kdsl.apps.v1beta1

    return (
        kdsl.apps.v1beta1.DeploymentStatus(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_RollbackConfig(
    value: Union[kdsl.apps.v1beta1.RollbackConfigUnion, OmitEnum, None]
) -> Union[kdsl.apps.v1beta1.RollbackConfig, OmitEnum, None]:
    import kdsl.apps.v1beta1

    return (
        kdsl.apps.v1beta1.RollbackConfig(**value) if isinstance(value, dict) else value
    )


def required_converter_DeploymentConditionItem(
    value: kdsl.apps.v1beta1.DeploymentConditionItemUnion,
) -> kdsl.apps.v1beta1.DeploymentConditionItem:
    import kdsl.apps.v1beta1

    return (
        kdsl.apps.v1beta1.DeploymentConditionItem(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_DeploymentStrategy(
    value: kdsl.apps.v1beta1.DeploymentStrategyUnion,
) -> kdsl.apps.v1beta1.DeploymentStrategy:
    import kdsl.apps.v1beta1

    return (
        kdsl.apps.v1beta1.DeploymentStrategy(**value)
        if isinstance(value, dict)
        else value
    )
