from __future__ import annotations
from typing import Literal, Union
from kdsl.bases import OmitEnum, OMIT
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import kdsl.batch.v2alpha1


def optional_converter_CronJobSpec(
    value: Union[kdsl.batch.v2alpha1.CronJobSpecUnion, OmitEnum, None]
) -> Union[kdsl.batch.v2alpha1.CronJobSpec, OmitEnum, None]:
    import kdsl.batch.v2alpha1

    return (
        kdsl.batch.v2alpha1.CronJobSpec(**value) if isinstance(value, dict) else value
    )


def optional_converter_JobTemplateSpec(
    value: Union[kdsl.batch.v2alpha1.JobTemplateSpecUnion, OmitEnum, None]
) -> Union[kdsl.batch.v2alpha1.JobTemplateSpec, OmitEnum, None]:
    import kdsl.batch.v2alpha1

    return (
        kdsl.batch.v2alpha1.JobTemplateSpec(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_CronJobStatus(
    value: Union[kdsl.batch.v2alpha1.CronJobStatusUnion, OmitEnum, None]
) -> Union[kdsl.batch.v2alpha1.CronJobStatus, OmitEnum, None]:
    import kdsl.batch.v2alpha1

    return (
        kdsl.batch.v2alpha1.CronJobStatus(**value) if isinstance(value, dict) else value
    )


def required_converter_CronJobSpec(
    value: kdsl.batch.v2alpha1.CronJobSpecUnion,
) -> kdsl.batch.v2alpha1.CronJobSpec:
    import kdsl.batch.v2alpha1

    return (
        kdsl.batch.v2alpha1.CronJobSpec(**value) if isinstance(value, dict) else value
    )


def required_converter_JobTemplateSpec(
    value: kdsl.batch.v2alpha1.JobTemplateSpecUnion,
) -> kdsl.batch.v2alpha1.JobTemplateSpec:
    import kdsl.batch.v2alpha1

    return (
        kdsl.batch.v2alpha1.JobTemplateSpec(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_CronJobStatus(
    value: kdsl.batch.v2alpha1.CronJobStatusUnion,
) -> kdsl.batch.v2alpha1.CronJobStatus:
    import kdsl.batch.v2alpha1

    return (
        kdsl.batch.v2alpha1.CronJobStatus(**value) if isinstance(value, dict) else value
    )
