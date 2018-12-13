import os.path
import tempfile
import shutil
import functools

def custom_home(func):
    '''Use a custom home for most operations.'''

    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        try:
            os.environ['XDG_CONFIG_HOME'] = tempfile.mkdtemp(prefix='gotocd')
            func(*args, **kwargs)
        finally:
            shutil.rmtree(os.environ['XDG_CONFIG_HOME'])
    return wrapped

def home_path(fpath):
    '''Returns a path relative to 'Home'.'''
    home = os.environ['XDG_CONFIG_HOME']
    return os.path.join(home, fpath)
