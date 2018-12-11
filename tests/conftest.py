from click.testing import CliRunner
import pytest

@pytest.fixture
def runner():
    '''Fixture for handling output from click.'''
    return CliRunner()
