import setuptools

with open('README.md', 'r') as f:
    description = f.read();

setuptools.setup(
    name="goto-cd",
    version="0.0.1",
    author="Henke Adolfsson",
    author_email="catears13@gmail.com",
    description="Teleport to anywhere on your computer",
    long_description=description,
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
