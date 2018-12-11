'''Tests for cli implementation.'''


import click
import pytest
import shutil
import os
from goto import cli
from goto import storage
import test_util


@test_util.custom_home
def test_add():
    '''Tests that add works with normal input.'''
    here = os.path.abspath('./')
    dirname = os.path.basename(here)
    cli.handle_add('./')
    assert storage.get_teleport_target(dirname) == here


@test_util.custom_home
def test_named_add():
    '''Tests that add works with input like A_NAME:PATH/DIR.'''
    cli.handle_add('testing:./')
    here = os.path.abspath('./')
    assert storage.get_teleport_target('testing') == here


@test_util.custom_home
def test_remove():
    '''Tests that removing works.'''
    cli.handle_add('testing-remove:./')
    assert len(storage.list_teleports()) > 0
    cli.handle_remove('testing-remove')
    assert len(storage.list_teleports()) == 0


@test_util.custom_home
def test_list(runner):
    '''Tests that listing works.'''
    with runner.isolation() as outstreams:
        cli.handle_add('testing-remove:/etc')
        cli.handle_add('test:/var')
        cli.handle_list()
        streams = outstreams[0].getvalue()
    lines = streams.decode('utf-8').split('\n')
    assert 'testing-remove' in lines[0] and '/etc' in lines[0]
    assert 'testing-remove' in lines[2] and '/etc' in lines[2]
    assert 'test' in lines[1] and '/var' in lines[1]
    assert 'test' in lines[3] and '/var' in lines[3]
    assert '=>' in lines[2] and '=>' in lines[3]

    # Both left sides of the arrow should be the same length so that smaller
    # texts are padded.
    assert len(lines[2].split('=>')[0]) == len(lines[3].split('=>')[0])


@test_util.custom_home
def test_profile():
    '''Tests that changing profile works.'''
    assert False


@test_util.custom_home
def test_list_profiles():
    '''Tests that listing profiles work.'''
    assert False

@test_util.custom_home
def test_remove_profile():
    '''Tests that removing profiles work.'''
    assert False




