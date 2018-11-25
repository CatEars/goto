'''Storage functions for accessing configuration.'''
import os
import os.path
import toml
try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

from . import util

class StorageException(Exception):
    '''Exception with the storage engine of goto.'''
    pass

def get_config_home():
    '''Returns the home folder of the configurations.'''
    xdg_home = os.environ.get('XDG_CONFIG_HOME')
    dot_config = os.path.join(os.path.expanduser('~'), '.config')
    dot_goto = os.path.join(os.path.expanduser('~'), '.goto-cd')

    join = os.path.join
    home_path = util.cond((
        (xdg_home, join(xdg_home, 'goto-cd')),
        (Path(dot_config).exists(), join(dot_config, 'goto-cd')),
        (True, dot_goto)
    ))()

    touch_directory(home_path)
    return home_path


def touch_directory(dirpath):
    '''Makes sure the whole directory path exists.'''
    Path(dirpath).mkdir(exist_ok=True)


def _touch_config_file(fpath):
    '''Makes sure the file exists.'''
    with open(fpath, 'a') as _:
        pass


def _retrieve_config(fname):
    '''Retrieves a config file, if it does not exist, creates it.'''
    touch_directory(get_config_home())
    fpath = os.path.join(get_config_home(), fname)
    _touch_config_file(fpath)
    return fpath


def _read_config_file(fpath):
    '''Reads the content of a file and returns it.'''
    with open(fpath, 'r') as f:
        data = f.read()
    return data


def write_file(fpath, data):
    '''Writes the data to file.'''
    with open(fpath, 'w') as f:
        toml.dump(data, f)


def get_default_profile():
    '''Returns the contents of the default profile.'''
    return get_named_profile('default')


def update_default_profile(data):
    '''Updates the default profile.'''
    update_named_profile('default', data)


def update_named_profile(name, data):
    config_path = os.path.join(get_config_home(), '{}.toml'.format(name))
    write_file(config_path, data)


def get_named_profile(name, public_file=True):
    '''Returns the data of the specified profile.'''
    if public_file and name.startswith('_'):
        raise StorageException('{} is an invalid name. Cannot start with "_"'.format(name))
    fpath = _retrieve_config('{}.toml'.format(name))
    try:
        data = _read_config_file(fpath)
        return toml.loads(data)
    except IOError:
        write_file(fpath, {})
        return {}
