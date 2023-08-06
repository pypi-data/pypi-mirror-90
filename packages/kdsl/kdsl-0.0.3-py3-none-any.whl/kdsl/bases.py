from typing import TypeVar, Union, Sequence
from enum import Enum


def ensure_dict(value):
    if isinstance(value, K8sObject):
        return value.__asyaml__()

    if isinstance(value, dict):
        return {k: ensure_dict(v) for k, v in value.items()}

    if isinstance(value, list):
        return [ensure_dict(x) for x in value]

    return value


class OmitEnum(Enum):
    OMIT = "OMIT"


OMIT = OmitEnum.OMIT


class K8sObject:
    def __asyaml__(self):
        ret = {}

        for a in self.__attrs_attrs__:
            meta = a.metadata
            if (yaml_name := meta["yaml_name"]) is not None:
                if (value := getattr(self, a.name)) is not OMIT:
                    value = ensure_dict(value)

                    if "mlist_key" in meta and isinstance(value, dict):
                        mlist_key = meta["mlist_key"]
                        value = [{mlist_key: k, **v} for k, v in value.items()]

                    ret[yaml_name] = value

        return ret


class K8sResource(K8sObject):
    def __asyaml__(self):
        return {
            "apiVersion": self.apiVersion,
            "kind": self.kind,
            **super().__asyaml__(),
        }


K8sEntries = Sequence[K8sResource]
