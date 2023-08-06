from contextlib import contextmanager
from pathlib import Path

import pytest
from click.testing import CliRunner

from sym.cli.tests.helpers.sandbox import Sandbox


@pytest.fixture
def click_setup(sandbox):
    @contextmanager
    def context():
        runner = CliRunner()
        with runner.isolated_filesystem():
            with sandbox.push_xdg_config_home():
                yield runner

    return context


@pytest.fixture
def sandbox(tmp_path: Path) -> Sandbox:
    return Sandbox(tmp_path)
