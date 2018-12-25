'''Tests for cli implementation.'''

import os

import pytest
import test_util

from goto import cli
from goto import storage


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
    assert storage.list_teleports()
    cli.handle_remove('testing-remove')
    assert not storage.list_teleports()


@test_util.custom_home
def test_list(runner):
    '''Tests that listing works.'''
    cli.handle_add('testing-remove:/etc')
    cli.handle_add('test:/var')

    with runner.isolation() as outstreams:
        cli.handle_list()
        streams = outstreams[0].getvalue()

    lines = sorted(streams.decode('utf-8').split('\n'))
    lines = [x for x in lines if x]
    assert len(lines) == 2
    assert 'test' in lines[0] and '/var' in lines[0]
    assert 'testing-remove' in lines[1] and '/etc' in lines[1]

    # Both left sides of the arrow should be the same length so that smaller
    # texts are padded.
    assert len(lines[0].split('=>')[0]) == len(lines[1].split('=>')[0])


@test_util.custom_home
def test_profile():
    '''Tests that changing profile works.'''
    assert storage.get_active_profile_name() == 'default'
    cli.handle_profile('test_profile')
    assert storage.get_active_profile_name() == 'test_profile'


@test_util.custom_home
def test_get(runner):
    '''Tests that changing profile works.'''
    cli.handle_add('a:/etc')
    cli.handle_add('abc:/var')
    cli.handle_add('b:/bin')

    with runner.isolation() as outstreams:
        cli.handle_get('a')
        cli.handle_get('abc')
        cli.handle_get('b')
        streams = outstreams[0].getvalue()
    lines = streams.decode('utf-8').strip().split('\n')
    assert len(lines) == 3
    assert lines[0].strip() == '/etc'
    assert lines[1].strip() == '/var'
    assert lines[2].strip() == '/bin'


@test_util.custom_home
def test_prefix(runner):
    '''Tests that changing profile works.'''
    cli.handle_add('a:/etc')
    cli.handle_add('abc:/etc')
    cli.handle_add('b:/etc')

    with runner.isolation() as outstreams:
        cli.handle_prefix('a')
        streams = outstreams[0].getvalue()
    line = streams.decode('utf-8').strip()
    assert line == 'a abc' or line == 'abc a'

    with runner.isolation() as outstreams:
        cli.handle_prefix('')
        streams = outstreams[0].getvalue()
    line = streams.decode('utf-8').strip()
    assert set(line.split(' ')) == set(['a', 'b', 'abc'])


@test_util.custom_home
def test_list_profiles(runner):
    '''Tests that listing profiles work.'''
    cli.handle_profile('other')

    with runner.isolation() as outstreams:
        cli.handle_profiles()
        streams = outstreams[0].getvalue()
    lines = streams.decode('utf-8').strip().split('\n')
    lines = [line.strip() for line in lines]
    assert '> other' in lines
    assert 'default' in lines


@test_util.custom_home
def test_remove_profile():
    '''Tests that removing profiles work.'''
    cli.handle_profile('other')
    cli.handle_profile('default')
    assert set(storage.list_profiles()) == set(['default', 'other'])
    cli.handle_rmprofile('other')
    assert set(storage.list_profiles()) == set(['default'])
