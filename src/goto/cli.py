'''Command Line Interface for working with Goto.
'''
import os
import click
from . import util
from . import storage
from . import install as install_self

def do_add(name, target):
    '''Sets a teleport for the active profile.'''
    storage.set_teleport(name, target)


def do_get(name):
    '''Returns the target for `name`.'''
    if storage.is_no_expansion(name):
        return storage.get_teleport_target(name)
    return storage.expand_teleport_path(name)

def do_prefix(prefix):
    '''Returns all the matching teleports for the prefix.'''
    if storage.is_no_expansion(prefix):
        return storage.get_matching_teleports(prefix)
    if storage.is_directory_expansion(prefix):
        return storage.get_directory_expansions(prefix)
    if storage.is_prefix_expansion(prefix):
        return storage.get_prefix_expansions(prefix)
    return []


def do_remove(name):
    '''Removes the teleport from the current profile.'''
    storage.remove_teleport(name)


def do_list():
    '''Returns a list of all different teleports and their destinations.'''
    teleports = storage.list_teleports()
    targets = [storage.get_teleport_target(tele) for tele in teleports]
    return list(zip(teleports, targets))


def do_rmprofile(profile):
    '''Removes the profile.

    If the profile is the active profile, changes to the default profile.

    '''
    if profile == storage.get_active_profile_name():
        storage.set_active_profile('default')
    storage.remove_profile(profile)


def do_profile(profile):
    '''Sets the current profile to `profile`. Throws on error.'''
    if profile not in storage.list_profiles():
        storage.add_profile(profile)
    storage.set_active_profile(profile)

def do_profiles():
    '''Returns a tuple of (currently active profile, all profiles)'''
    profiles = storage.list_profiles()
    chosen_profile = storage.get_active_profile_name()
    return chosen_profile, profiles

def do_set_config(attr, value):
    '''Sets config of attr to value'''
    storage.set_config(attr, value)

def do_get_config(attr):
    '''Returns the configuration of attr'''
    return storage.get_config(attr)

def do_rm_config(attr):
    '''Removes attr from config file'''
    storage.remove_config(attr)

def handle_add(add):
    '''Handler for adding a target.'''
    if ':' in add:
        _, target = add.split(':')
    else:
        target = add

    target = os.path.expanduser(target)
    if not os.path.isdir(target):
        util.error('Could not find "{}".'.format(target))
        util.error('Is it really a directory?')
        return

    target = os.path.abspath(target)
    if ':' in add:
        name, _ = add.split(':')
    else:
        name = os.path.basename(target)

    do_add(name, target)
    util.pretty('Added "', nl=False)
    util.detail('{}'.format(name), nl=False)
    util.pretty('" which points to "', nl=False)
    util.detail('{}'.format(target), nl=False)
    util.pretty('"')


def handle_remove(remove):
    '''Handler for removing a target.'''
    do_remove(remove)
    util.pretty('Removed teleport "', nl=False)
    util.detail(remove, nl=False)
    util.pretty('"')


def handle_list():
    '''Handler for listing a target.'''
    listing = do_list()
    # default=0 is not possible in py2 so we default to the list [0]
    # Can we please just move on to python3 now. It's not funny anymore.
    biggest_tele_length = max([len(x[0]) for x in listing] or [0])
    length = biggest_tele_length
    for tele, target in listing:
        util.pretty('{}'.format(tele.ljust(length)), nl=False)
        util.boring(' => ', nl=False)
        util.pretty(target)


def handle_get(get):
    '''Handler for getting teleport target.'''
    target = do_get(get)
    util.text_response(target)


def handle_prefix(prefix):
    '''Handler for printing prefixes matching "prefix".'''
    prefixes = do_prefix(prefix)
    if prefixes:
        util.text_response(' '.join(prefixes))


def handle_rmprofile(rmprofile):
    '''Handler for removing a profile.'''
    pre_profile = storage.get_active_profile_name()
    do_rmprofile(rmprofile)
    post_profile = storage.get_active_profile_name()
    util.pretty('Removed profile: ', nl=False)
    util.detail(rmprofile)
    if pre_profile != post_profile:
        util.pretty('Changed to profile: ', nl=False)
        util.detail(post_profile)


def handle_profile(profile):
    '''Handler for changing profile.'''
    do_profile(profile)
    util.pretty('Changed to profile: ', nl=False)
    util.detail(profile)

def handle_profiles():
    '''Handler for listing profiles.'''
    chosen_profile, profiles = do_profiles()
    for profile in profiles:
        if chosen_profile == profile:
            util.detail('> {}'.format(chosen_profile))
        else:
            util.pretty(profile)


def handle_install(install):
    '''Installs for different shells.'''
    if install == 'bash':
        install_self.install_bash()
        util.pretty('goto is now installed when using bash.')
        util.pretty('to activate it make sure to RESTART your' +
                    'shell, like in the good old days')
    elif install == 'zsh':
        install_self.install_zsh()
        util.pretty('goto is now installed when using zsh')
        util.pretty('to activate it make sure to RESTART your' +
                    'shell, like in the good old days')

def handle_config(config, configuration):
    '''Handler for configuration of settings'''
    if config == 'set':
        do_set_config(configuration[0], configuration[1])
        util.detail('{}'.format(configuration[0]), nl=False)
        util.detail(' {}'.format(config), nl=False)
        util.pretty(' to "', nl=False)
        util.detail('{}'.format(configuration[1]), nl=False)
        util.pretty('"')
    elif config == 'get':
        value = do_get_config(configuration[0])
        util.detail('{}\n'.format(value), nl=False)
    elif config == 'remove':
        do_rm_config(configuration[0])
        util.detail('{}'.format(configuration[0]), nl=False)
        util.pretty(' removed from config\n', nl=False)

def print_help():
    '''Prints help text and exists with non-zero exit code.'''
    with click.Context(main) as ctx:
        click.echo(main.get_help(ctx))
    exit(1)


HELP = {
    'add': 'Add a teleport ([name:]path/to/directory)',
    'get': 'Print a teleport target',
    'prefix': 'List all targets that have X as prefix',
    'remove': 'Remove a teleport',
    'list': 'List all teleports',
    'rmprofile': 'Remove a profile',
    'profile': 'Switch to a (possibly non-existant) profile',
    'profiles': 'List all profiles',
    'install': 'Install goto for the given shell, "bash" or "zsh"',
    'config': 'Configure behaviour get/set/remove'
}

BASH_ZSH = click.Choice(['bash', 'zsh'])

@click.command()
@click.argument('configuration', nargs=-1)
@click.option('--add', '-a', default='', help=HELP['add'])
@click.option('--get', '-g', default='', help=HELP['get'])
@click.option('--prefix', default=None, help=HELP['prefix'])
@click.option('--remove', '-r', default='', help=HELP['remove'])
@click.option('--list', '-l', is_flag=True, default=False, help=HELP['list'])
@click.option('--rmprofile', '-m', default='', help=HELP['rmprofile'])
@click.option('--profile', '-p', default=None, help=HELP['profile'])
@click.option('--profiles', is_flag=True, default=False, help=HELP['profiles'])
@click.option('--install', required=False, type=BASH_ZSH, help=HELP['install'])
@click.option('--config', default='', help=HELP['config'])
def main(configuration, **kwargs):
    '''CLI for teleporting to anywhere on your computer!'''
    try:
        has_prefix = kwargs['prefix'] is not None
        has_profile = kwargs['profile'] is not None
        has_rm = kwargs['rmprofile']
        util.cond(
            (kwargs['add'], lambda: handle_add(kwargs['add'])),
            (kwargs['get'], lambda: handle_get(kwargs['get'])),
            (has_prefix, lambda: handle_prefix(kwargs['prefix'])),
            (kwargs['remove'], lambda: handle_remove(kwargs['remove'])),
            (kwargs['list'], handle_list),
            (has_rm, lambda: handle_rmprofile(kwargs['rmprofile'])),
            (has_profile, lambda: handle_profile(kwargs['profile'])),
            (kwargs['profiles'], handle_profiles),
            (kwargs['install'], lambda: handle_install(kwargs['install'])),
            (kwargs['config'], lambda: handle_config(kwargs['config'],
                                                    configuration)),
            (True, print_help)
        )()
    except storage.StorageException as exception:
        util.error(str(exception))
        exit(1)
