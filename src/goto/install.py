'''Installation module for Goto.'''
import os


def install_general(rcpath_from_home, source_line, add_source_lines):
    '''Install working for both windows and unix systems.'''
    homefolder = os.path.expanduser('~')
    if not os.path.exists(homefolder):
        return
    dotrc = os.path.join(homefolder, rcpath_from_home)
    profile_directory = os.path.dirname(dotrc)
    if not os.path.exists(profile_directory):
        os.makedirs(profile_directory)

    # If it doesn't exist, just write it.
    if not os.path.exists(dotrc):
        with open(dotrc, 'w') as fhandle:
            add_source_lines(fhandle)
        return

    # Else, check if we already have written ourselves in there.
    with open(dotrc, 'r') as fhandle:
        lines = fhandle.readlines()

    if any(source_line in line for line in lines):
        # Already added
        return

    with open(dotrc, 'a') as fhandle:
        fhandle.write('\n')
        add_source_lines(fhandle)


def install_unix(rcfile):
    '''Install for unix based system.'''
    python_install_path = os.path.dirname(os.path.abspath(__file__))
    goto = os.path.join(python_install_path, 'shell', 'goto')
    source_line = 'source {}'.format(goto)
    def add_source_lines(fhandle):
        '''Adds the actual sourcing to the file handle.'''
        fhandle.write('# add `goto` function to shell' + os.sep)
        fhandle.write('if [ -f {} ]; then'.format(goto) + os.sep)
        fhandle.write('  {}'.format(source_line) + os.sep)
        fhandle.write('fi' + os.sep)
    install_general(rcfile, source_line, add_source_lines)


def install_windows():
    '''Install for windows system.'''
    # This is mainly based on the following SuperUser thread:
    # https://superuser.com/questions/1090141/does-powershell-have-any-sort-of-bashrc-equivalent
    # and
    # https://devblogs.microsoft.com/scripting/understanding-the-six-powershell-profiles/
    python_install_path = os.path.dirname(os.path.abspath(__file__))
    goto = os.path.join(python_install_path, 'shell', 'goto.ps1')
    source_line = '. {}'.format(goto)
    def add_source_lines(fhandle):
        '''Adds the actual sourcing of the function implementation in goto.'''
        fhandle.write('# add `goto` function to shell' + os.sep)
        # '{{' because format-string
        fhandle.write('if (Test-Path {}) {{'.format(goto) + os.sep)
        fhandle.write('  {}'.format(source_line) + os.sep)
        fhandle.write('}' + os.sep)

    profile = 'Documents\\WindowsPowerShell\\Profile.ps1'
    install_general(profile, source_line, add_source_lines)


def install_bash():
    '''Install for bash.'''
    install_unix('.bashrc')


def install_zsh():
    '''Install for zsh.'''
    install_unix('.zshrc')
