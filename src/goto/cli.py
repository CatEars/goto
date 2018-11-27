'''Command Line Interface for working with Goto.
'''
import click
import os
from . import util
from . import storage


def do_add(name, target):
    '''Sets a teleport for the active profile.'''
    storage.set_teleport(name, target)


def do_get(name):
    '''Returns the target for `name`'''
    return storage.get_teleport_target(name)


def do_prefix(prefix):
    '''Returns all the matching teleports for the prefix.'''
    return storage.get_matching_teleports(prefix)


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


@click.command()
@click.option('--add', '-a', default='', help='Add a teleport ([name:]path/to/directory)')
@click.option('--get', '-g', default='', help='Get a teleport')
@click.option('--prefix', default='', help='List all paths that are prefix of X')
@click.option('--remove', '-r', default='', help='Remove a teleport')
@click.option('--list', '-l', is_flag=True, default=False, help='List all teleports')
@click.option('--rmprofile', '-m', default='', help='Remove a profile')
@click.option('--profile', '-p', default='', help='Switch to a different profile')
@click.option('--profiles', is_flag=True, default=False, help='List all profiles')
def main(add, get, prefix, remove, rmprofile, list, profile, profiles):
    '''Helper for jumping to anywhere on your computer!'''

    def handle_add():
        '''Handler for adding a target'''
        if ':' in add:
            _, target = add.split(':')
        else:
            target = add

        if not os.path.isdir(target):
            util.error('Could not find "{}". Is it really a directory?'.format(target))
            return

        if ':' in add:
            name, _ = add.split(':')
        else:
            name = os.path.basename(target)

        target = os.path.abspath(target)
        do_add(name, target)
        util.pretty('Added "', nl=False)
        util.detail('{}'.format(name), nl=False)
        util.pretty('" which points to "', nl=False)
        util.detail('{}'.format(target), nl=False)
        util.pretty('"')

    def handle_get():
        target = do_get(get)
        util.text_response(target)

    def handle_prefix():
        prefixes = do_prefix(prefix)
        if prefixes:
            util.text_response(' '.join(prefixes))

    def handle_remove():
        do_remove(remove)

    def handle_list():
        listing = do_list()
        biggest_tele_length = max((len(x[0]) for x in listing), default=0)
        L = biggest_tele_length
        for tele, target in listing:
            util.pretty('{}'.format(tele.ljust(L)), nl=False)
            util.boring(' => ', nl=False)
            util.pretty(target)

    def handle_rmprofile():
        pre_profile = storage.get_active_profile_name()
        do_rmprofile(rmprofile)
        post_profile = storage.get_active_profile_name()
        util.pretty('Removed profile: ', nl=False)
        util.detail(rmprofile)
        if pre_profile != post_profile:
            util.pretty('Changed to profile: ', nl=False)
            util.detail(post_profile)


    def handle_profile():
        do_profile(profile)

    def handle_profiles():
        chosen_profile, profiles = do_profiles()
        for profile in profiles:
            if chosen_profile == profile:
                util.detail('> {}'.format(chosen_profile))
            else:
                util.pretty(profile)

    try:
        util.cond(
            (add, handle_add),
            (get, handle_get),
            (prefix, handle_prefix),
            (remove, handle_remove),
            (list, handle_list),
            (rmprofile, handle_rmprofile),
            (profile, handle_profile),
            (profiles, handle_profiles)
        )()
    except storage.StorageException as exception:
        util.error(str(exception))
