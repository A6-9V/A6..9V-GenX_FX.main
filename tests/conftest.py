import os
import pytest


def pytest_sessionstart(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """
    os.environ["EXNESS_LOGIN"] = "123456"
    os.environ["EXNESS_PASSWORD"] = "password"
    os.environ["EXNESS_SERVER"] = "exness-mt5"
