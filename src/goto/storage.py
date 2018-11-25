'''Storage functions for accessing configuration.'''
import os
import os.path
import toml
try:
  from pathlib import Path
except ImportError:
  from pathlib2 import Path

def get_config_home():
    '''Returns the home folder of the configurations. Makes sure the directory exists.'''
    xdg_home = os.environ.get('XDG_CONFIG_HOME')
    if xdg_home and Path(xdg_home).exists():
        return xdg_home
    if Path(os.path.expanduser('~'), '.config').exists():
        return os.path.join(os.path.expanduser('~'), '.config')
    path = os.path.join(os.path.expanduser('~'), '.goto-cd')
    touch_directory(path)
    return path


def touch_directory(dirpath):
    '''Makes sure the whole directory path exists.'''
    Path(dirpath).mkdir(exist_ok=True)


def _touch_config_file(fpath):
    '''Makes sure the file exists.'''
    with open(fpath, 'a') as f:
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


def get_named_profile(name, public_file=False):
    '''Returns the data of the specified profile.'''
    if public_file and name.startswith('_'):
        raise Exception('{} is an invalid name. Cannot start with "_"'.format(name))
    fpath = _retrieve_config('{}.toml'.format(name))
    try:
        data = _read_config_file(fpath)
        return toml.loads(data)
    except IOError:
        write_file(fpath, dict())
        return {}

