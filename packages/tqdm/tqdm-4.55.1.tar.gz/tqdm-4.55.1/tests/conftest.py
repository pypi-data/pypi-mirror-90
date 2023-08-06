"""Shared pytest config."""
import sys
from tqdm import tqdm
from pytest import fixture


@fixture(autouse=True)
def pretest_posttest():
    """Fixture for all tests ensuring environment cleanup"""
    try:
        sys.setswitchinterval(1)
    except AttributeError:
        sys.setcheckinterval(100)  # deprecated

    if getattr(tqdm, "_instances", False):
        n = len(tqdm._instances)
        if n:
            tqdm._instances.clear()
            raise EnvironmentError(
                "{0} `tqdm` instances still in existence PRE-test".format(n))
    yield
    if getattr(tqdm, "_instances", False):
        n = len(tqdm._instances)
        if n:
            tqdm._instances.clear()
            raise EnvironmentError(
                "{0} `tqdm` instances still in existence POST-test".format(n))
