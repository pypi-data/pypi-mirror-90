from collections import OrderedDict
from functools import wraps


def memoize(fn):
    """
    A decorator that caches the last provided
    parameter for a function,
    until a new one is provided.

    Only works for function with a single positional param.

    !!! warning
        This method is most likely **not thread-safe** and
        is only recommended to be used for scripts that do not
        rely on `threading` or `multiprocessing`.

    Example:
        ````python
        @memoize
        def hello(name: str) -> None:
            print(f'Hello {name.capitalize().strip()}!')

        hello("Ben")
        hello()  # after the first run, we do not need to pass any params anymore
        ````
    """
    # use a dict for mutability
    cache = OrderedDict()

    @wraps(fn)
    def mem_f(arg=None):
        if arg:
            cache[0] = arg
        try:
            res = fn(cache[0])
        except KeyError:
            raise TypeError(
                f"Function {fn.__name__} missing positional argument."
            ) from None
        else:
            return res

    return mem_f


def resolve_super_auto_resolution(fn):
    """
    A decorator that fixes the issues
    with the parameterless super call,
    on instance methods of classes
    created with `type()`, or `types.new_class()`.

    See: <a href="https://bugs.python.org/issue29944" target="_blank">Issue 29944</a>

    Whether this is to be considered a bug or not
    is up to your use-case.

    This decorator however can override
    the functions closure cell to effectively 'patch'
    this issue in the local scope of each method.
    """

    @wraps(fn)
    def injector(self, *args, **kwargs):
        # if the `__class__` variable is in the unbound variables list
        # of the local function scope, that means it is an instance method,
        # otherwise this fix is not applicable.
        if "__class__" in (f := fn.__code__.co_freevars) and len(f) == 1:
            fn.__closure__[0].cell_contents = type(self)

        def injection_wrapper(slf, *a, **kw):
            return fn(slf, *a, **kw)

        return injection_wrapper(self, *args, **kwargs)

    return injector


__all__ = ["memoize", "resolve_super_auto_resolution"]
