'''Storage functions for accessing configuration.'''
import os
import os.path
import toml


def _get_xdg_config_home():
    '''Returns XDG_CONFIG_HOME variable.'''
    return os.environ.get('XDG_CONFIG_HOME')


def get_config_home():
    '''Returns the home folder of the configurations.'''
    if _get_xdg_config_home():
        return os.path.join(_get_xdg_config_home(), 'goto-cd')
    return os.path.join(os.path.expanduser('~'), '.goto-cd')


def touch_directory(dirpath):
    '''Makes sure the whole directory path exists.'''
    os.makedirs(dirpath, exist_ok=True)


def _touch_config_file(fpath):
    '''Makes sure the file exists.'''
    with open(fpath, 'a') as f:
        pass


def _retrieve_config(fname):
    '''Retrieves a config file, if it does not exist, creates it.'''
    touch_directory(get_config_home())
    fpath = os.path.join(get_config_home(), fname)
    touch_config_file(fpath)
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


def get_named_profile(name):
    '''Returns the data of the specified profile.'''
    fpath = _retrieve_config('{}.toml'.format(name))
    try:
        data = _read_config_file(fpath)
    except IOError:
        write_file(fpath, dict())
        return {}
