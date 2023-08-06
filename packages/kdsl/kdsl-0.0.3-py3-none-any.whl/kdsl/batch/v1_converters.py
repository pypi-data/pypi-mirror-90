from __future__ import annotations
from typing import Mapping, Literal, Union
from kdsl.bases import OmitEnum, OMIT
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import kdsl.batch.v1


def required_converter_JobSpec(
    value: kdsl.batch.v1.JobSpecUnion,
) -> kdsl.batch.v1.JobSpec:
    import kdsl.batch.v1

    return kdsl.batch.v1.JobSpec(**value) if isinstance(value, dict) else value


def required_converter_JobConditionItem(
    value: kdsl.batch.v1.JobConditionItemUnion,
) -> kdsl.batch.v1.JobConditionItem:
    import kdsl.batch.v1

    return kdsl.batch.v1.JobConditionItem(**value) if isinstance(value, dict) else value


def required_converter_JobStatus(
    value: kdsl.batch.v1.JobStatusUnion,
) -> kdsl.batch.v1.JobStatus:
    import kdsl.batch.v1

    return kdsl.batch.v1.JobStatus(**value) if isinstance(value, dict) else value


def optional_converter_JobSpec(
    value: Union[kdsl.batch.v1.JobSpecUnion, OmitEnum, None]
) -> Union[kdsl.batch.v1.JobSpec, OmitEnum, None]:
    import kdsl.batch.v1

    return kdsl.batch.v1.JobSpec(**value) if isinstance(value, dict) else value


def optional_converter_JobStatus(
    value: Union[kdsl.batch.v1.JobStatusUnion, OmitEnum, None]
) -> Union[kdsl.batch.v1.JobStatus, OmitEnum, None]:
    import kdsl.batch.v1

    return kdsl.batch.v1.JobStatus(**value) if isinstance(value, dict) else value


def optional_converter_JobConditionItem(
    value: Union[kdsl.batch.v1.JobConditionItemUnion, OmitEnum, None]
) -> Union[kdsl.batch.v1.JobConditionItem, OmitEnum, None]:
    import kdsl.batch.v1

    return kdsl.batch.v1.JobConditionItem(**value) if isinstance(value, dict) else value


def optional_mlist_converter_JobConditionItem(
    value: Union[Mapping[str, kdsl.batch.v1.JobConditionItemUnion], OmitEnum, None]
) -> Union[Mapping[str, kdsl.batch.v1.JobConditionItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {k: required_converter_JobConditionItem(v) for k, v in value.items()}
