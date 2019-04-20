'''Tests for storage functions'''

import os
import os.path
import shutil

import pytest

import goto

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

import test_util

def home_path(fpath):
    '''Returns the path, with a slash at the end.'''
    fpath = test_util.home_path(fpath)
    if not fpath.endswith(os.sep):
        return '{}{}'.format(fpath, os.sep)
    return fpath


def make_local_dirs(fpath):
    '''Creates directories like mkdir -p in the home_path of custom_home.'''
    Path(home_path(fpath)).mkdir(parents=True, exist_ok=True)

def touch_file(fpath):
    '''Creates an empty file. Similar to `touch` UNIX command.'''
    fpath = home_path(fpath)[:-1] # Remove trailing slash
    with open(fpath, 'w') as _:
        pass

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
def test_get_default_profile_empty():
    '''Test that default profile is empty if nothing has happened.'''
    data = goto.storage.get_default_profile()
    assert data == dict()


@test_util.custom_home
def test_get_updated_profile():
    '''Test that a simple update to profile is visible.'''
    pre_data = goto.storage.get_default_profile()
    goto.storage.update_default_profile({'test': 'abcd'})
    post_data = goto.storage.get_default_profile()
    assert pre_data != post_data
    assert post_data == {'test': 'abcd'}

@test_util.custom_home
def test_no_such_file():
    '''Test that a named profile is created if it does not exist.'''
    data = goto.storage.get_named_profile('nosuchprofile')
    assert data == dict()
    does_exist = Path(os.environ['XDG_CONFIG_HOME'], 'goto-cd', 'nosuchprofile.toml').exists()
    assert does_exist

@test_util.custom_home
def test_private_files():
    '''Test that an exception is raised if underscore files are accessed.'''
    with pytest.raises(goto.storage.StorageException):
        goto.storage.get_named_profile('_notokay', public_file=True)


@test_util.custom_home
def test_add_profiles():
    '''Test adding a profile makes it listable.'''
    profiles = goto.storage.list_profiles()
    assert profiles == ['default']
    goto.storage.add_profile('abcd')
    profiles = goto.storage.list_profiles()
    assert set(profiles) == set(['default', 'abcd'])


@test_util.custom_home
def test_add_profiles_throws():
    '''Test different exceptions for storage.'''
    with pytest.raises(goto.storage.StorageException):
        goto.storage.add_profile('_notallowed')
    goto.storage.add_profile('somerandomprofile')
    with pytest.raises(goto.storage.StorageException):
        goto.storage.add_profile('somerandomprofile')
    with pytest.raises(goto.storage.StorageException):
        goto.storage.add_profile('default')


@test_util.custom_home
def test_remove_profile():
    '''Test removing profile.'''
    files = lambda: os.listdir(goto.storage.get_config_home())
    goto.storage.add_profile('abcd')
    profiles = goto.storage.list_profiles()
    assert set(profiles) == set(['default', 'abcd'])
    assert set(files()) == set(['default.toml', '_setting.toml', 'abcd.toml'])
    goto.storage.remove_profile('abcd')
    profiles = goto.storage.list_profiles()
    assert set(profiles) == set(['default'])
    assert set(files()) == set(['default.toml', '_setting.toml'])


@test_util.custom_home
def test_profile_with_teleport():
    '''Test that adding a teleport to a profile works.'''
    files = lambda: os.listdir(goto.storage.get_config_home())
    goto.storage.add_profile('abcd')
    assert set(files()) == set(['default.toml', '_setting.toml', 'abcd.toml'])
    goto.storage.set_teleport('teleport', './')
    assert goto.storage.get_teleport_target('teleport') == os.path.abspath('./')
    goto.storage.remove_profile('abcd')
    assert set(files()) == set(['default.toml', '_setting.toml'])


@test_util.custom_home
def test_remove_profile_throws():
    '''Tests exceptions in remove profile.'''
    with pytest.raises(goto.storage.StorageException):
        goto.storage.remove_profile('nonexistant')

@test_util.custom_home
def test_remove_default_throws():
    '''Tests that removing the default profile throws.'''
    with pytest.raises(goto.storage.StorageException):
        goto.storage.remove_profile('default')

@test_util.custom_home
def test_get_active_profile():
    '''Test getting the active profile.'''
    assert goto.storage.get_active_profile_name() == 'default'
    goto.storage.add_profile('abcd')
    goto.storage.set_active_profile('abcd')
    assert goto.storage.get_active_profile_name() == 'abcd'


@test_util.custom_home
def test_set_active_profile_throws():
    '''Test that setting active profile has to be an existing profile.'''
    with pytest.raises(goto.storage.StorageException):
        goto.storage.set_active_profile('nonexistant')


@test_util.custom_home
def test_set_teleport():
    '''Test basic set teleport functionality.'''
    assert goto.storage.list_teleports() == []
    actual_directory = './'
    goto.storage.set_teleport('thisdir', actual_directory)
    assert goto.storage.list_teleports() == ['thisdir']

@test_util.custom_home
def test_remove_teleport():
    '''Test removing teleport works.'''
    actual_directory = './'
    goto.storage.set_teleport('thisdir', actual_directory)
    assert goto.storage.list_teleports() == ['thisdir']
    goto.storage.remove_teleport('thisdir')
    assert goto.storage.list_teleports() == []

@test_util.custom_home
def test_get_matching_teleports():
    '''Test getting matching teleports work'''
    added_teleports = [
        ('a', test_util.home_path('./a')),
        ('abcd', test_util.home_path('./abcd')),
        ('b', test_util.home_path('./b'))
    ]
    try:
        for name, target in added_teleports:
            os.mkdir(target)
            goto.storage.set_teleport(name, target)
        assert set(goto.storage.list_teleports()) == set(['a', 'abcd', 'b'])
        assert set(goto.storage.get_matching_teleports('a')) == set(['a', 'abcd'])
        assert set(goto.storage.get_matching_teleports('b')) == set(['b'])
        assert set(goto.storage.get_matching_teleports('')) == set(['a', 'b', 'abcd'])
    finally:
        for _, target in added_teleports:
            if os.path.exists(target):
                shutil.rmtree(target)

@test_util.custom_home
def test_set_teleport_throws():
    '''Test exceptions are raised for setting teleport.'''
    with pytest.raises(goto.storage.StorageException):
        goto.storage.set_teleport('abcd', './notanexistantdirectory')
    with pytest.raises(goto.storage.StorageException):
        goto.storage.set_teleport('', './')

@test_util.custom_home
def test_remove_teleport_throws():
    '''Test removing nonexistant teleport throws.'''
    with pytest.raises(goto.storage.StorageException):
        goto.storage.remove_teleport('abcd')

@test_util.custom_home
def test_get_teleport_target():
    '''Test getting teleport target works.'''
    abspath = os.path.abspath('./')
    goto.storage.set_teleport('abcd', './')
    assert goto.storage.get_teleport_target('abcd') == abspath


@test_util.custom_home
def test_get_teleport_target_throws():
    '''Test that getting nonexistant teleport target throws.'''
    with pytest.raises(goto.storage.StorageException):
        goto.storage.get_teleport_target('abcd')


@test_util.custom_home
def test_home_folder_expands():
    '''Test that home folder is expanded correctly for teleports.'''
    goto.storage.set_teleport('home', '~')
    home = os.path.expanduser('~')
    assert home == goto.storage.get_teleport_target('home')


@test_util.custom_home
def test_starts_with_teleport():
    '''Tests that we can determine when a path starts with a teleport.'''
    goto.storage.set_teleport('abcd', './')
    goto.storage.set_teleport('abc', './')
    fails = [
        'zxcv',
        'abcdd/',
        'ab'
    ]
    corrects = [
        'abc',
        'abcd',
        'abc/',
        'abcd/',
        'abc/s',
        'abcd/s',
        'abcd/s/s/s/s'
    ]

    for fail in fails:
        assert not goto.storage.starts_with_teleport(fail)
    for correct in corrects:
        assert goto.storage.starts_with_teleport(correct)

@test_util.custom_home
def test_prefix_determined():
    '''Tests that we can determine when there is exact 1 prefix'''
    goto.storage.set_teleport('abcd', './')
    goto.storage.set_teleport('abc', './')

    fails = [
        'ab', 'a', 'z', 'abc'
    ]
    corrects = [
        'abcd'
    ]

    for fail in fails:
        assert not goto.storage.prefix_can_be_determined(fail)

    for correct in corrects:
        assert goto.storage.prefix_can_be_determined(correct)


@test_util.custom_home
def test_expand_teleport_path():
    '''Test that a teleport is expanded correctly'''
    goto.storage.set_teleport('abcd', home_path('.'))
    make_local_dirs('a/b/c/d')
    make_local_dirs('a/b/x/zqw')
    make_local_dirs('q/w')

    cases = [
        (home_path(''), 'abcd'),
        (home_path('a'), 'abcd/a'),
        (home_path('a/b'), 'abcd/a/b'),
        (home_path('a/b/c'), 'abcd/a/b/c'),
        (home_path('a/b/c/d'), 'abcd/a/b/c/d'),
        (home_path('a/b/x'), 'abcd/a/b/x'),
        (home_path('a/b/x/zqw'), 'abcd/a/b/x/zqw'),
        (home_path('q'), 'abcd/q'),
        (home_path('q/w'), 'abcd/q/w'),
    ]

    for expected, teleport in cases:
        actual = goto.storage.expand_teleport_path(teleport)
        assert expected == actual
        with_trailing_slash = '{}{}'.format(teleport, os.sep)
        actual = goto.storage.expand_teleport_path(with_trailing_slash)
        assert expected == actual

    fpath = home_path('a/b/x/zq')
    if fpath.endswith(os.sep):
        fpath = fpath[:-1]
    teleport = 'abcd/a/b/x/zq'
    result = goto.storage.expand_teleport_path(teleport)
    assert result == fpath


@test_util.custom_home
def test_expand_raises():
    '''Tests that nonexistant teleports raise errors when expanded.'''
    with pytest.raises(goto.storage.StorageException):
        goto.storage.expand_teleport_path('abcd')


@test_util.custom_home
def test_no_expansion():
    '''Test when no expansion is available and no subpath exists.

    This is a bit of a relic from older times, when goto was just supposed to
    take you directly to the repo and not expand to subfolders.

    '''
    corrects = [
        '',
        'a',
        'b',
        'abcd',
        'zxcv'
    ]
    fails = [
        os.path.join('ab', os.sep),
        os.path.join('a', 'b'),
        os.path.join('a', 'b', os.sep),
        os.path.join('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'),
        os.path.join('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', os.sep)
    ]

    for correct in corrects:
        assert goto.storage.is_no_expansion(correct)
    for fail in fails:
        assert not goto.storage.is_no_expansion(fail)


@test_util.custom_home
def test_expands_to_directory():
    '''Tests when expansion is expanded to a directory.'''
    make_local_dirs('abc/a')
    make_local_dirs('abc/aaa')
    make_local_dirs('abc/b')
    make_local_dirs('abc/c')
    make_local_dirs('abc/xxx/y/z')
    goto.storage.set_teleport('abcd', home_path('abc'))

    corrects = [
        'abcd/aaa',
        'abcd/b',
        'abcd/c',
        'abcd/xxx',
        'abcd/xxx/y',
        'abcd/xxx/y/z'
    ]
    fails = [
        'abcd/',
        'abcd',
        'abcd/a',
        '',
        'abcd/d',
        'abcd/xx',
        'abcd/xxx/z'
    ]

    for correct in corrects:
        assert goto.storage.is_directory_expansion(correct)
    for fail in fails:
        assert not goto.storage.is_directory_expansion(fail)


@test_util.custom_home
def test_expands_to_prefix():
    '''Tests when an expansion has subpaths and is a prefix (not a directory).'''
    make_local_dirs('abc/a/bb/cc')
    make_local_dirs('abc/b')
    make_local_dirs('abc/c')
    make_local_dirs('abc/xxx/y/z')
    goto.storage.set_teleport('abcd', home_path('abc'))

    corrects = [
        'abcd/',
        'abcd/xx',
        'abcd/a/b',
        'abcd/a/bb/c'
    ]
    fails = [
        'abcd/a',
        'abcd/b',
        'abcd/c',
        'abcd/xxx',
        'abcd/xxx/y',
        'abcd/xxx/y/z'
    ]

    for correct in corrects:
        assert goto.storage.is_prefix_expansion(correct)
    for fail in fails:
        assert not goto.storage.is_prefix_expansion(fail)


@test_util.custom_home
def test_list_subprefixes():
    '''Tests that we filter subfolders for a teleport.'''
    make_local_dirs('abc/bbax')
    make_local_dirs('abc/bbaz')
    make_local_dirs('abc/bboo')
    make_local_dirs('abc/xyz')
    touch_file('abc/bbbb')
    touch_file('abc/bbay')
    touch_file('abc/bbaq')
    goto.storage.set_teleport('abcd', home_path('abc'))

    cases = [
        ('abcd/bb', ['bbax', 'bbaz', 'bboo']),
        ('abcd/bba', ['bbax', 'bbaz']),
        ('abcd/x', ['xyz'])
    ]

    for teleport, expected in cases:
        actual = goto.storage.list_subprefixes(teleport)
        assert set(expected) == set(actual)

@test_util.custom_home
def test_list_subfolders():
    '''Tests that we can list subfolders for a teleport.'''

    goto.storage.set_teleport('abcd', home_path('.'))
    make_local_dirs('a/b/c/d')
    make_local_dirs('a/b/xyz/zyx')
    make_local_dirs('q/w')
    touch_file('a/bbb')
    touch_file('a/.gitignore')
    touch_file('a/b/xyz/.gitignore')

    cases = [
        (home_path('./a'), 'abcd/a', ['b']),
        (home_path('./a/b'), 'abcd/a/b', ['c', 'xyz']),
        (home_path('./a/b/c'), 'abcd/a/b/c', ['d']),
        (home_path('./a/b/c/d'), 'abcd/a/b/c/d', []),
        (home_path('./a/b/xyz'), 'abcd/a/b/xyz', ['zyx']),
        (home_path('./a/b/xyz/zyx'), 'abcd/a/b/xyz/zyx', []),
        (home_path('./q'), 'abcd/q', ['w']),
        (home_path('./q/w'), 'abcd/q/w', []),
    ]

    for fpath, teleport, expected in cases:
        actual = goto.storage.list_subfolders(teleport)
        assert set(actual) == set(expected)
        listing = os.listdir(fpath)
        listing = [x for x in listing if os.path.isdir(os.path.join(fpath, x))]
        assert set(actual) == set(listing)

@test_util.custom_home
def test_get_directory_expansions():
    '''Tests that we can get directory expansions.'''
    goto.storage.set_teleport('abcd', home_path('.'))
    make_local_dirs('a/b/c')
    make_local_dirs('a/xyz/zyx')
    touch_file('a/xyzxxx')
    touch_file('a/.gitignore')

    cases = [
        ('abcd/a', ['abcd/a/b/', 'abcd/a/xyz/']),
        ('abcd/a/b', ['abcd/a/b/c/']),
        ('abcd/a/b/c', []),
        ('abcd/a/xyz', ['abcd/a/xyz/zyx/']),
        ('abcd/a/xyz/zyx', [])
    ]

    for teleport, expected in cases:
        actual = goto.storage.get_directory_expansions(teleport)
        assert set(expected) == set(actual)

@test_util.custom_home
def test_get_prefix_expansions():
    '''Tests that we can get prefix expansions.'''
    goto.storage.set_teleport('abcd', home_path('.'))
    make_local_dirs('a/xyzxyz')
    make_local_dirs('a/xyz/xyz')
    touch_file('a/xyzxxx')
    touch_file('a/.gitignore')

    cases = [
        ('abcd/a/x', ['abcd/a/xyz/', 'abcd/a/xyzxyz/']),
        ('abcd/a/xyzx', ['abcd/a/xyzxyz/']),
        ('abcd/a/xyz/x', ['abcd/a/xyz/xyz/'])
    ]

    for teleport, expected in cases:
        actual = goto.storage.get_prefix_expansions(teleport)
        assert set(actual) == set(expected)
