'''Command Line Interface for working with Goto.
'''
import click
from . import util

@click.command()
@click.option('--add', '-a', default='', help='Add a teleport ([name:]path/to/directory)')
@click.option('--get', '-g', default='', help='Get a teleport')
@click.option('--prefix', default='', help='List all paths that are prefix of X')
@click.option('--remove', '-r', default='', help='Remove a teleport')
@click.option('--list', '-l', is_flag=True, default=False, help='List all teleports')
@click.option('--profile', '-p', default='', help='Switch to a different profile')
@click.option('--profiles', is_flag=True, default=False, help='List all profiles')
def main(add, get, prefix, remove, list, profile, profiles, version):
    '''Helper for jumping to anywhere on your computer!'''

    def handle_add():
        util.pretty('add')

    def handle_get():
        util.pretty('get')

    def handle_prefix():
        util.pretty('prefix')

    def handle_remove():
        util.pretty('remove')

    def handle_list():
        util.pretty('list')

    def handle_profile():
        util.pretty('profile')

    def handle_profiles():
        util.pretty('profiles')

    def handle_version():
        util.pretty('version')

    util.cond(
        (version, handle_version),
        (add, handle_add),
        (get, handle_get),
        (prefix, handle_prefix),
        (remove, handle_remove),
        (list, handle_list),
        (profile, handle_profile),
        (profiles, handle_profiles)
    )()
