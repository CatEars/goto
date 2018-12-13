import os
import tempfile
import shutil
import decorator

@decorator.decorator
def custom_home(func, *args, **kwargs):
    '''Use a custom home for most operations.'''
    try:
        os.environ['XDG_CONFIG_HOME'] = tempfile.mkdtemp(prefix='gotocd')
        func(*args, **kwargs)
    finally:
        shutil.rmtree(os.environ['XDG_CONFIG_HOME'])


def home_path(fpath):
    '''Returns a path relative to 'Home'.'''
    home = os.environ['XDG_CONFIG_HOME']
    return os.path.join(home, fpath)
