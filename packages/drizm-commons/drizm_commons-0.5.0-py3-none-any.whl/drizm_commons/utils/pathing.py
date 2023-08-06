import inspect
import os
import pathlib
import shutil
import sys
from inspect import FrameInfo
from typing import List
from typing import Optional, Union


def get_absolute_root_path() -> str:
    """ Return the absolute path to the project root directory. """
    caller_root_path = None

    # This is for apps like PyCharm, that by default,
    # inject the root path into PYTHONPATH
    if p := os.environ.get("PYTHONPATH"):
        return p.split(os.pathsep)[0]

    # The current module
    current_module = sys.path[0]

    # In an ideal world, sys.path[1] would be the project root path
    # but if utilities like Pydev are used, sys.path[1] may not be correct
    possible_root = sys.path[1]

    if current_module not in possible_root and "pydev" in possible_root:
        # Skip the first and second sys.path
        for path in sys.path[2:]:
            path_to_check = pathlib.Path(path)
            # Cut the reference path to the same length as the sys.path we are
            # currently checking, in case the reference path is above the current one
            current_module_cut_to_match = pathlib.Path(current_module).parts[
                : len(path_to_check.parts)
            ]

            # Return the first absolute path, that is a directory and contains
            # the reference path without containing pydev.
            # This is because pydev always contains the string 'pydev' and is often
            # from a completely different root path, which makes it easy to check for
            if (
                current_module_cut_to_match == path_to_check.parts
                and "pydev" not in path
            ):
                if not os.path.isfile(path) and os.path.isabs(path):
                    caller_root_path = path
                    break

    else:
        # stack trace history related to the call of this function
        frame_stack: List[FrameInfo] = inspect.stack()

        # get info about the module that has invoked this function
        # (
        #   index=0 is always this very module,
        #   index=1 is fine as long this function is not called by some other
        #   function in this module
        # )
        frame_info = frame_stack[1]

        # if there are multiple calls in the stacktrace of this module,
        # we have to skip those and take the first one which comes from another module
        if frame_info.filename == __file__:
            for frame in frame_stack:
                if frame.filename != __file__:
                    frame_info = frame
                    break

        # path of the module that has invoked this function
        caller_path: str = frame_info.filename

        # absolute path of the of the module that has invoked this function
        caller_absolute_path: str = os.path.abspath(caller_path)

        # get the top most directory path which contains the invoker module
        paths: List[str] = [p for p in sys.path if p in caller_absolute_path]
        paths.sort(key=lambda p: len(p))  # noqa shadows name from outer scope
        caller_root_path = paths[0]

        if not os.path.isabs(caller_path):
            # file name of the invoker module (eg: "mymodule.py")
            caller_module_name: str = pathlib.Path(caller_path).name

            # this piece represents a subpath in the project directory
            # (
            #   eg. if the root folder is "myproject"
            #   and this function has ben called from myproject/foo/bar/mymodule.py
            #   this will be "foo/bar"
            # )
            project_related_folders = caller_path.replace(
                os.sep + caller_module_name, ""
            )

            # fix root path by removing the undesired subpath
            caller_root_path = caller_root_path.replace(project_related_folders, "")

    root_path = pathlib.Path(caller_root_path)

    # This is the case for IDLE, where the root_path will be the path
    # to the system Python interpreter.
    interpreter_path = Path(sys.executable)
    if not interpreter_path.is_dir():
        interpreter_path = interpreter_path.parent

    if interpreter_path.parts == root_path.parts:
        root_path = pathlib.Path(sys.path[0])

    return str(root_path)


def get_root_path_dirname() -> str:
    """ Return the name of the project root directory. """
    return pathlib.Path(get_absolute_root_path()).name


# this is necessary because we can only subclass the concrete implementation
PATH_IMPL: Union[pathlib.WindowsPath, pathlib.PosixPath] = type(pathlib.Path())


class Path(PATH_IMPL):
    """
    A subclass of pathlib.Path.

    With the exception of the below listed, overridden methods,
    the behaviour is identical to that of its superclass.
    """

    def rmdir(self, recursive: Optional[bool] = True) -> None:
        """
        Remove this directory.
        By default, this method will recursively delete
        all contents of this directory.

        Arguments:
            recursive: If `False`, will only delete the directory
                if it is empty. Otherwise it will recursively
                delete its contents.
        """
        if recursive:
            shutil.rmtree(self)
        else:
            super(Path, self).rmdir()


__all__ = ["get_absolute_root_path", "get_root_path_dirname", "Path"]
