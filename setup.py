'''Setup file for goto.'''
import os
import sys
import setuptools
from setuptools.command.install import install

def get_description():
    '''Returns the description of the README.'''
    with open('README.md', 'r') as fhandle:
        description = fhandle.read()
    return description

class PostInstallCommand(install):
    '''Post Install step for Goto installation.

    Adds a sourcing of `shell/goto` in the users .bashrc and .zshrc

    '''

    def run(self):
        homefolder = os.path.expanduser('~')
        if not os.path.exists(homefolder):
            return
        bashrc = os.path.join(homefolder, '.bashrc')
        zshrc = os.path.join(homefolder, '.zshrc')
        python_install_path = sys.prefix
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

        def add_sourcing(fpath):
            '''Adds a `source ...goto...` statement to file.'''

            if not os.path.exists(fpath):
                with open(fpath, 'w') as fhandle:
                    add_source_line(fhandle)
                return
            with open(fpath, 'r') as fhandle:
                lines = fhandle.readlines()

            if any(source_line in line for line in lines):
                # Already added
                return

            with open(fpath, 'a') as fhandle:
                fhandle.write('\n')
                add_source_line(fhandle)

        add_sourcing(bashrc)
        add_sourcing(zshrc)
        install.run(self)


setuptools.setup(
    name="goto-cd",
    version="0.0.1",
    author="Henke Adolfsson",
    author_email="catears13@gmail.com",
    description="Teleport to anywhere on your computer",
    long_description=get_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/catears/goto",
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'goto-helper = goto.cli:main'
        ]
    },
    data_files=[
        ('shell', ['shell/goto', 'shell/goto-bash.sh', 'shell/goto-zsh.sh'])
    ],
    cmdclass={
        'install': PostInstallCommand
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3",
        "Topic :: System :: Shells"
    ]
)
