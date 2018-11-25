'''Tests for storage functions'''

import os
import os.path
import goto
import pytest
try:
  from pathlib import Path
except ImportError:
  from pathlib2 import Path

import test_util

@test_util.custom_home
def test_get_home_config():
    '''Test that GetHomeConfig returns a valid directory structure.'''
    home_directory = goto.storage.get_config_home()
    assert isinstance(home_directory, str)

@test_util.custom_home
def test_touch_directory_structure():
    '''Test that touch directory can create a directory.'''
    target_directory = goto.storage.get_config_home()
    assert isinstance(target_directory, str)
    goto.storage.touch_directory(target_directory)
    assert os.path.isdir(target_directory)


@test_util.custom_home
def test_get_default_profile_with_nothing():
    data = goto.storage.get_default_profile()
    assert data == dict()


@test_util.custom_home
def test_get_updated_profile():
    pre_data = goto.storage.get_default_profile()
    goto.storage.update_default_profile({ 'test': 'abcd' })
    post_data = goto.storage.get_default_profile()
    assert pre_data != post_data
    assert post_data == { 'test': 'abcd' }

@test_util.custom_home
def test_no_such_file():
    data = goto.storage.get_named_profile('nosuchprofile')
    assert data == dict()
    does_exist = Path(os.environ['XDG_CONFIG_HOME'], 'goto-cd', 'nosuchprofile.toml').exists()
    assert does_exist

@test_util.custom_home
def test_private_files():
    with pytest.raises(goto.storage.StorageException):
        goto.storage.get_named_profile('_notokay', public_file=True)
