import os
import tempfile
import shutil

def custom_home(f):
    def wrapped(*args, **kwargs):
        try:
            os.environ['XDG_CONFIG_HOME'] = tempfile.mkdtemp(prefix='gotocd')
            f(*args, **kwargs)
        finally:
            shutil.rmtree(os.environ['XDG_CONFIG_HOME'])
    return wrapped
