"""Performance profiling utilities."""

import cProfile
import functools
import os
import pstats
from io import StringIO
from typing import Callable, TypeVar

F = TypeVar("F", bound=Callable)


def profile_if_enabled(func: F) -> F:
    """Wrap a function to profile it if MELLEA_PROFILE env var is set.

    Set MELLEA_PROFILE=1 to enable cProfile profiling of the command.
    Profiling results (top 40 functions by cumulative time) are printed
    to stdout after the command completes.

    Example:
        MELLEA_PROFILE=1 mellea-skills-compiler compile spec.yaml
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not os.environ.get("MELLEA_PROFILE"):
            return func(*args, **kwargs)

        pr = cProfile.Profile()
        pr.enable()
        try:
            result = func(*args, **kwargs)
        finally:
            pr.disable()
            stream = StringIO()
            stats = pstats.Stats(pr, stream=stream).sort_stats("cumulative")
            stats.print_stats(40)
            print("\n" + "=" * 80)
            print("PROFILING RESULTS (MELLEA_PROFILE=1)")
            print("=" * 80)
            print(stream.getvalue())
        return result
    return wrapper
