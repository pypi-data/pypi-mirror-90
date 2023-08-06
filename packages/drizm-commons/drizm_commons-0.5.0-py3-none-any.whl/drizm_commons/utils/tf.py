"""
A wrapper around a .tfvars file.

````python
from drizm_commons.utils.tf import Tfvars
````
"""
from pathlib import Path
from typing import Union


class _TfvarsParser:
    """ A parser class for *.tfvars files. """

    def __init__(self, path: Path) -> None:
        self.path = path

    def read(self) -> dict:
        with open(self.path, "r") as fin:
            c = [
                line for line in fin.readlines() if not self._ignore_line(line) and line
            ]

        attrs = {
            l[0]: self._guess_type(l[1])
            for l in [[e.strip() for e in line.split("=")] for line in c]
        }
        return attrs

    # noinspection PyMethodMayBeStatic
    def _ignore_line(self, line: str) -> bool:
        # Case for comments
        if line.strip().startswith(("/", "*", "#")):
            return True

        # Cannot be a key value block if there is no '='
        if "=" not in line:
            return True

        return False

    # noinspection PyMethodMayBeStatic
    def _guess_type(self, val: str) -> Union[str, int, float]:
        if val.isdigit():
            return int(val)
        else:
            try:
                return float(val)
            except ValueError:
                pass
        if any(v in val for v in ["'", '"']):
            return val[1:-1]
        return val


class Tfvars:
    """ Wrapper for a parsed *.tfvars file. """

    def __init__(self, /, path: Union[str, Path]) -> None:
        from .type import AttrDict

        if not isinstance(path, Path):
            path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"The directory {path} does not exist")
        self.path = path
        self.vars = AttrDict(**_TfvarsParser(path).read())


__all__ = ["Tfvars"]
