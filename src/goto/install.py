'''Installation module for Goto.'''
import os

def append_newline(source_lines):
    '''Add operating system newlines to source lines.'''
    return [
        x + os.linesep for x in source_lines
    ]

def install_general(rcpath_from_home, sourcing_line, source_lines):
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
            fhandle.writelines(source_lines)
        return

    # Else, check if we already have written ourselves in there.
    with open(dotrc, 'r') as fhandle:
        lines = fhandle.readlines()

    if any(sourcing_line in line for line in lines):
        # Already added
        return

    with open(dotrc, 'a') as fhandle:
        fhandle.write(os.linesep)
        fhandle.writelines(source_lines)


def install_unix(rcfile):
    '''Install for unix based system.'''
    python_install_path = os.path.dirname(os.path.abspath(__file__))
    goto = os.path.join(python_install_path, 'shell', 'goto')
    sourcing_line = 'source {}'.format(goto)
    source_lines = [
        '# add `goto` function to shell',
        'if [ -f {} ]; then'.format(goto),
        '  {}'.format(sourcing_line),
        'fi'
    ]
    install_general(rcfile, sourcing_line, append_newline(source_lines))


def install_windows():
    '''Install for windows system.'''
    # This is mainly based on the following SuperUser thread:
    # https://superuser.com/questions/1090141/does-powershell-have-any-sort-of-bashrc-equivalent
    # and
    # https://devblogs.microsoft.com/scripting/understanding-the-six-powershell-profiles/
    python_install_path = os.path.dirname(os.path.abspath(__file__))
    goto = os.path.join(python_install_path, 'shell', 'goto.ps1')
    sourcing_line = '. {}'.format(goto)
    source_lines = [
        '# add `goto` function to shell',
        # '{{' because format-string
        'if (Test-Path {}) {{'.format(goto),
        '  {}'.format(sourcing_line),
        '}'
    ]

    profile = 'Documents\\WindowsPowerShell\\Profile.ps1'
    install_general(profile, sourcing_line, append_newline(source_lines))


def install_bash():
    '''Install for bash.'''
    install_unix('.bashrc')


def install_zsh():
    '''Install for zsh.'''
    install_unix('.zshrc')
