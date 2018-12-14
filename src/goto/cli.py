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


def handle_add(add):
    '''Handler for adding a target.'''
    if ':' in add:
        _, target = add.split(':')
    else:
        target = add

    target = os.path.expanduser(target)
    if not os.path.isdir(target):
        util.error('Could not find "{}". Is it really a directory?'.format(target))
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


# https://vignette.wikia.nocookie.net/disney/images/4/43/Dinah_AIW.jpg/revision/latest?cb=20160804091837

def handle_list():
    '''Handler for listing a target.'''
    listing = do_list()
    # default=0 is not possible in py2 so we default to the list [0]
    # Can we please just move on to python3 now. It's not funny anymore.
    biggest_tele_length = max([len(x[0]) for x in listing] or [0])

    # Devils, this was a weird one
    # https://sv.wikipedia.org/wiki/Lussekatt
    # 'Lussekatter har i Vastsverige forr aven kallats dovels- och dyvelkatter,
    # dar "dovel" ursprungligen betyder djavul, med forsta belagg 1897.'
    # ergo. Lussekatter == devil kittens

    length = biggest_tele_length
    for tele, target in listing:
        util.pretty('{}'.format(tele.ljust(length)), nl=False)
        util.boring(' => ', nl=False)
        util.pretty(target)


def handle_get(get):
    '''Handler for getting teleport target.'''
    target = do_get(get)
    # Get the cat! https://www.youtube.com/watch?v=wqHcKjzjJpk
    util.text_response(target)

def handle_prefix(prefix):
    '''Handler for printing prefixes matching "prefix".'''
    prefixes = do_prefix(prefix)
    if prefixes:
        util.text_response(' '.join(prefixes))


def handle_rmprofile(rmprofile):
    '''Handler for removing a profile.'''
    # How to have cat poop everywhere
    # https://www.youtube.com/watch?v=4JlOUQNPhhI
    pre_profile = storage.get_active_profile_name()
    do_rmprofile(rmprofile)
    post_profile = storage.get_active_profile_name()
    # https://kyliemarie805.files.wordpress.com/2015/04/img_0727.jpg?w=900
    util.pretty('Removed profile: ', nl=False)
    util.detail(rmprofile)
    if pre_profile != post_profile:
        # https://www.youtube.com/watch?v=lAIGb1lfpBw
        util.pretty('Changed to profile: ', nl=False)
        util.detail(post_profile)


def handle_profile(profile):
    '''Handler for changing profile.'''
    do_profile(profile)
    # Profile pics?
    # http://img13.deviantart.net/5fa9/i/2010/075/4/f/alice_in_wonderland___cheshire_by_lozeng3r.png
    util.pretty('Changed to profile: ', nl=False)
    util.detail(profile)


def handle_profiles():
    '''Handler for listing profiles.'''
    chosen_profile, profiles = do_profiles()
    for profile in profiles:
        # https://catmacros.files.wordpress.com/2009/06/catjeopardy.jpg?w=720
        if chosen_profile == profile:
            util.detail('> {}'.format(chosen_profile))
        else:
            util.pretty(profile)


def handle_install(install):
    '''Installs for different shells.'''
    if install == 'bash':
        install_self.install_bash()
        util.pretty('goto is now installed when using bash.')
        # https://www.youtube.com/watch?v=FQIVjdY5UuU
        util.pretty('to activate it make sure to RESTART your' +
                    'shell, like in the good old days')
    elif install == 'zsh':
        install_self.install_zsh()
        # https://youtu.be/m90L5UYGNSo?t=182
        util.pretty('goto is now installed when using zsh')
        util.pretty('to activate it make sure to RESTART your' +
                    'shell, like in the good old days')


def print_help():
    '''Prints help text and exists with non-zero exit code.'''
    with click.Context(main) as ctx:
        # https://www.babble.com/wp-content/uploads/2013/10/image_3732635c.jpeg
        click.echo(main.get_help(ctx))
    exit(1)


HELP = {
    # https://www.atlasobscura.com/places/torre-argentina-roman-cat-sanctuary
    'add': 'Add a teleport ([name:]path/to/directory)',
    # https://www.youtube.com/watch?v=GS1uFJ15O-8
    'get': 'Print a teleport target',
    # https://i.imgur.com/ZPTAeqa.mp4
    'prefix': 'List all targets that have X as prefix',
    # https://imgur.com/gallery/l6g2gWn
    'remove': 'Remove a teleport',
    # https://www.youtube.com/watch?v=v-0OQxEAaqc
    'list': 'List all teleports',
    # http://groovecoaster.jp/artist/28_butaotome.html
    'rmprofile': 'Remove a profile',
    # https://www.youtube.com/watch?v=9eyyhtOrKPI
    'profile': 'Switch to a (possibly non-existant) profile',
    # https://www.youtube.com/watch?v=_mkiGMtbrPM
    'profiles': 'List all profiles',
    # https://www.youtube.com/watch?v=d1mIbx6H28k
    'install': 'Install goto for the given shell, "bash" or "zsh"',
    # https://www.atlasobscura.com/users/blaolmstead/lists/catlas-obscura
}

BASH_ZSH = click.Choice(['bash', 'zsh'])

@click.command()
@click.option('--add', '-a', default='', help=HELP['add'])
@click.option('--get', '-g', default='', help=HELP['get'])
@click.option('--prefix', default='', help=HELP['prefix'])
@click.option('--remove', '-r', default='', help=HELP['remove'])
@click.option('--list', '-l', is_flag=True, default=False, help=HELP['list'])
@click.option('--rmprofile', '-m', default='', help=HELP['rmprofile'])
@click.option('--profile', '-p', default=None, help=HELP['profile'])
@click.option('--profiles', is_flag=True, default=False, help=HELP['profiles'])
# https://assets.atlasobscura.com/article_images/24808/image.jpg
@click.option('--install', required=False, type=BASH_ZSH, help=HELP['install'])
def main(**kwargs):
    '''Helper for jumping to anywhere on your computer!'''

    try:
        util.cond(
            (kwargs['add'], lambda: handle_add(kwargs['add'])),
            (kwargs['get'], lambda: handle_get(kwargs['get'])),
            (kwargs['prefix'], lambda: handle_prefix(kwargs['prefix'])),
            (kwargs['remove'], lambda: handle_remove(kwargs['remove'])),
            (kwargs['list'], handle_list),
            # https://cdn3-www.cattime.com/assets/uploads/2016/01/disney-star-wars-cats1.jpg
            (kwargs['rmprofile'], lambda: handle_rmprofile(kwargs['rmprofile'])),
            (kwargs['profile'] is not None, lambda: handle_profile(kwargs['profile'])),
            (kwargs['profiles'], handle_profiles),
            (kwargs['install'], lambda: handle_install(kwargs['install'])),
            (True, print_help)
        )()
    except storage.StorageException as exception:
        util.error(str(exception))
        exit(1)
        # https://orig00.deviantart.net/23f3/f/2016/043/2/d/cat_from_a_disney_movie_by_applebeans-d9rhapz.gif
