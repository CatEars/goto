'''Installation module for Goto.'''
import os

def install_unix(rcfile):
    '''Install for unix based system.'''
    homefolder = os.path.expanduser('~')
    if not os.path.exists(homefolder):
        return
    dotrc = os.path.join(homefolder, rcfile)
    python_install_path = os.path.dirname(os.path.abspath(__file__))
    goto = os.path.join(python_install_path, 'shell', 'goto')
    source_line = 'source {}'.format(goto)

    def add_source_line(fhandle):
        '''Adds the actual sourcing to the file handle.'''
        fhandle.write('# add `goto` function to shell\n')
        fhandle.write('if [ -f {} ]; then\n'.format(goto))
        fhandle.write('  {}\n'.format(source_line))
        fhandle.write('else\n')
        fhandle.write('  echo "Could not source {}"\n'.format(goto))
        fhandle.write('fi\n')

    if not os.path.exists(dotrc):
        with open(dotrc, 'w') as fhandle:
            add_source_line(fhandle)
        return
    with open(dotrc, 'r') as fhandle:
        lines = fhandle.readlines()

    if any(source_line in line for line in lines):
        # Already added
        return

    with open(dotrc, 'a') as fhandle:
        fhandle.write('\n')
        add_source_line(fhandle)


def install_bash():
    '''Install for bash.'''
    install_unix('.bashrc')


def install_zsh():
    '''Install for zsh.'''
    install_unix('.zshrc')
