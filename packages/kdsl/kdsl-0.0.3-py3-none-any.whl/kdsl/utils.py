import yaml
import sys

from .bases import K8sEntries


def render_to_stdout(entries: K8sEntries):
    rendered = [x.__asyaml__() for x in entries]
    yaml.safe_dump_all(rendered, stream=sys.stdout)
