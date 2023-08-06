from envparse import env  # type: ignore
from typing import Sequence, Mapping, List, Dict, TypeVar, Callable, Union


recipe_string: str = env.str("RECIPE")
recipe: Sequence[str] = recipe_string.split("+")


A = TypeVar("A")


ValueOrCallable = Union[A, Callable[[], A]]


def resolve_callable(v: ValueOrCallable) -> A:
    return v() if callable(v) else v


def choice(**values: ValueOrCallable) -> A:
    """
    Use the most local value
    """
    for r in reversed(recipe):
        try:
            value = values[r]
        except KeyError:
            pass
        else:
            return resolve_callable(value)

    raise RuntimeError(
        "No choice for recipe\n" f"recipe: {recipe}\n" f"choices: {values}"
    )


def overlay(**overlays: Mapping[str, ValueOrCallable]) -> Mapping[str, A]:
    """
    Use the most local values from overlays
    """
    ret: Dict[str, ValueOrCallable] = {}

    for r in recipe:
        try:
            ret.update(overlays[r])
        except KeyError:
            pass

    return {k: resolve_callable(v) for k, v in ret.items()}


ValueSeqOrCallable = Union[Sequence[A], Callable[[], Sequence[A]]]


def resolve_seq_callable(v: ValueSeqOrCallable) -> Sequence[A]:
    return v() if callable(v) else v


def collection(**collections: ValueSeqOrCallable) -> Sequence[A]:
    """
    Collect values from all subcollections
    """
    found: bool = False
    ret: List[A] = []

    for r in recipe:
        try:
            raw = collections[r]
        except KeyError:
            pass
        else:
            ret += resolve_seq_callable(raw)

    return ret
