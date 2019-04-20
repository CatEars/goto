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


def get_config_home():
    '''Returns the home folder of the configurations.'''
    xdg_home = os.environ.get('XDG_CONFIG_HOME')
    dot_config = os.path.join(os.path.expanduser('~'), '.config')
    dot_goto = os.path.join(os.path.expanduser('~'), '.goto-cd')

    join = os.path.join
    home_path = util.cond(
        (xdg_home, lambda: join(xdg_home, 'goto-cd')),
        (Path(dot_config).exists(), lambda: join(dot_config, 'goto-cd')),
        (True, dot_goto)
    )()

    touch_directory(home_path)
    return home_path


def touch_directory(dirpath):
    '''Makes sure the whole directory path exists.'''
    Path(dirpath).mkdir(exist_ok=True)


def _touch_config_file(fpath):
    '''Makes sure the file exists.'''
    with open(fpath, 'a') as _:
        pass


def _remove_file(name):
    '''Helper for removing file from configuration home.'''
    home = get_config_home()
    fpath = os.path.join(home, '{}.toml'.format(name))
    if os.path.exists(fpath):
        os.remove(fpath)

def _retrieve_config(fname):
    '''Retrieves a config file, if it does not exist, creates it.'''
    touch_directory(get_config_home())
    fpath = os.path.join(get_config_home(), fname)
    _touch_config_file(fpath)
    return fpath


def _read_config_file(fpath):
    '''Reads the content of a file and returns it.'''
    with open(fpath, 'r') as fhandle:
        return toml.load(fhandle)


def write_file(fpath, data):
    '''Writes the data to file.'''
    with open(fpath, 'w') as fhandle:
        toml.dump(data, fhandle)


def _update_settings(data):
    '''Updates the settings with new data.'''
    fname = '_setting.toml'
    home = get_config_home()
    fpath = os.path.join(home, fname)
    write_file(fpath, data)


def _write_default_file():
    '''Writes default data to default.toml'''
    home = get_config_home()
    fpath = os.path.join(home, 'default.toml')
    write_file(fpath, {})


def _get_settings():
    '''Returns the configuration settings.'''
    fname = '_setting.toml'
    home = get_config_home()
    fpath = os.path.join(home, fname)
    if not Path(fpath).exists():
        default_values = {
            'current_profile': 'default',
            'profiles': ['default']
        }
        _update_settings(default_values)
        _write_default_file()
    return _read_config_file(fpath)


def list_profiles():
    '''Returns a list of all available profiles.'''
    data = _get_settings()
    return data.get('profiles', [])


def add_profile(name):
    '''Adds a profile.'''
    data = _get_settings()
    if name in data['profiles']:
        msg = '{} is a profile that already exists'.format(name)
        raise StorageException(msg)
    if name.startswith('_'):
        msg = '{} - you cannot start profiles with "_"'.format(name)
        raise StorageException(msg)

    data['profiles'].append(name)
    _update_settings(data)
    fpath = os.path.join(get_config_home(), '{}.toml'.format(name))
    write_file(fpath, {})


def remove_profile(name):
    '''Removes a profile.'''
    data = _get_settings()
    if name not in data['profiles']:
        msg = '{} - not a profile that exists'.format(name)
        raise StorageException(msg)
    if name == 'default':
        msg = 'you cannot remove the default profile'
        raise StorageException(msg)
    data['profiles'].remove(name)
    _update_settings(data)
    _remove_file(name)

def get_active_profile_name():
    '''Returns the name of the active profile.'''
    data = _get_settings()
    return data.get('current_profile', 'default')


def set_active_profile(name):
    '''Sets the current profile.'''
    data = _get_settings()
    if name not in data['profiles']:
        msg = '{} is not a profile that exists'.format(name)
        raise StorageException(msg)
    data['current_profile'] = name
    _update_settings(data)


def get_default_profile():
    '''Returns the contents of the default profile.'''
    return get_named_profile('default')


def update_default_profile(data):
    '''Updates the default profile.'''
    update_named_profile('default', data)


def update_named_profile(name, data):
    '''Updates the values in a named profile.'''
    config_path = os.path.join(get_config_home(), '{}.toml'.format(name))
    write_file(config_path, data)


def get_named_profile(name, public_file=True):
    '''Returns the data of the specified profile.'''
    if public_file and name.startswith('_'):
        msg = '{} is an invalid name. Cannot start with "_"'.format(name)
        raise StorageException(msg)

    fpath = _retrieve_config('{}.toml'.format(name))
    try:
        data = _read_config_file(fpath)
        return data
    except IOError:
        write_file(fpath, {})
        return {}


def get_active_profile():
    '''Returns the currently active profile.'''
    return get_named_profile(get_active_profile_name())


def update_active_profile(data):
    '''Updates the data of the currently active profile.'''
    update_named_profile(get_active_profile_name(), data)


def set_teleport(name, target):
    '''Sets a (new) teleport path for the currently active profile.'''
    path = Path(os.path.expanduser(target))
    if not path.is_dir():
        raise StorageException('{} is not a directory'.format(target))
    if not name:
        raise StorageException('You must provide a name')
    target = str(path.resolve())
    data = get_active_profile()
    data[name] = target
    update_active_profile(data)


def remove_teleport(name):
    '''Removes a teleport from the currently active profile.'''
    data = get_active_profile()
    if not data.get(name):
        msg = '{} is not a location you can teleport to'.format(name)
        raise StorageException(msg)
    del data[name]
    update_active_profile(data)


def list_teleports():
    '''Lists all different possible teleports.'''
    data = get_active_profile()
    return list(data.keys())


def get_teleport_target(name):
    '''Return a teleport target that matches name or throw an error.'''
    data = get_active_profile()
    if name not in data:
        msg = '{} is not a valid teleport'.format(name)
        raise StorageException(msg)
    return data[name]


def get_matching_teleports(prefix):
    '''Returns all teleports matching the prefix.'''
    teleports = list_teleports()
    return [T + os.sep for T in teleports if T.startswith(prefix)]


def starts_with_teleport(fpath):
    '''Returns true if a path starts with a teleport.'''
    parts = fpath.split(os.sep)
    return parts[0] in list_teleports()


def prefix_can_be_determined(prefix):
    '''Returns true if prefix can complete to a single teleport.'''
    return len(get_matching_teleports(prefix)) == 1


def expand_teleport_path(teleport_path):
    '''Expands the teleport at beginning of a teleport path and normalizes.'''
    if not starts_with_teleport(teleport_path):
        msg = '"{}" does not start with a teleport'.format(teleport_path)
        raise StorageException(msg)
    elements = teleport_path.split(os.sep)

    elements[0] = get_teleport_target(elements[0])
    joined = os.sep.join(elements)
    ends_with_sep = joined.endswith(os.sep)
    if not ends_with_sep and os.path.isdir(joined):
        return '{}{}'.format(joined, os.sep)
    return joined


def is_no_expansion(teleport_path):
    '''Returns true if this is a classic style expansion (no subfolders).'''
    return not os.sep in teleport_path


def is_directory_expansion(teleport_path):
    '''Returns true if the teleport_path expands to a directory.'''
    return os.sep in teleport_path and \
        starts_with_teleport(teleport_path) and \
        os.path.isdir(expand_teleport_path(teleport_path)) and \
        len(list_subprefixes(teleport_path)) <= 1

def is_prefix_expansion(teleport_path):
    '''Returns true if the teleport_path expands to a prefix (non-directory).'''
    return starts_with_teleport(teleport_path) and \
        not is_directory_expansion(teleport_path)


def list_subfolders(teleport_path):
    '''Returns a list of the subfolders for the teleport path.'''
    expanded_path = expand_teleport_path(teleport_path)
    items = os.listdir(expanded_path)
    fullpaths = [os.path.join(expanded_path, x) for x in items]
    return [os.path.basename(x) for x in fullpaths if os.path.isdir(x)]


def list_subprefixes(teleport_path):
    '''Returns a list of prefixes fitting the teleport_path.'''
    basepath, prefix = os.path.split(teleport_path)
    subfolders = list_subfolders(basepath)
    return [x for x in subfolders if x.startswith(prefix)]


def get_directory_expansions(prefix):
    '''Returns valid expansions for the given directory expandable prefix.'''
    subfolders = list_subfolders(prefix)
    return [os.path.join(prefix, x) + os.sep for x in subfolders]


def get_prefix_expansions(prefix):
    '''Returns valid expansions for the given expandable prefix.'''
    subprefixes = list_subprefixes(prefix)
    teleport_no_prefix, _ = os.path.split(prefix)
    return [os.path.join(teleport_no_prefix, x) + os.sep for x in subprefixes]
