'''Setup file for goto.'''
import setuptools

def get_description():
    '''Returns the description of the README.'''
    with open('README.md', 'r') as fhandle:
        description = fhandle.read()
    return description

setuptools.setup(
    name="goto-cd",
    version="1.0.1",
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
            '_gotohelper = goto.cli:main'
        ]
    },
    package_data={
        'goto': ['shell/*']
    },
    install_requires=[
        'toml', 'click', 'pathlib2'
    ],
    python_requires='>=2.7.6,!=3.0.*,!=3.1.*,!=3.2.*',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "Topic :: System :: Shells"
    ]
)
