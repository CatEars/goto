# goto

![build](https://travis-ci.org/CatEars/goto.svg?branch=master)
[![PyPI version](https://badge.fury.io/py/goto-cd.svg)](https://badge.fury.io/py/goto-cd)
![coverage](https://github.com/CatEars/goto/blob/master/badges/coverage.svg)
![Tested With Docker, pytest and Tox](https://img.shields.io/badge/tested%20with-docker%20|%20pytest%20|%20tox-blue.svg)
[![CodeFactor](https://www.codefactor.io/repository/github/catears/goto/badge)](https://www.codefactor.io/repository/github/catears/goto)
[![saythanks](https://img.shields.io/badge/say-thanks-ffa500.svg?style=for-the-badge)](https://saythanks.io/to/CatEars)

🚀 🚀 🚀 A command line tool for teleporting around your computer! 🚀 🚀 🚀

The (very) tldr usage of `goto`:

![Usage Picture](https://github.com/CatEars/goto/blob/master/docs/tldrusage.png)

Gifs and usage documentation can be found in the
[docs folder](https://github.com/CatEars/goto/blob/master/docs/README.md)

## Key Features

* Like browser bookmarks, but for the commandline!
* Add commonly visited places, like `code/my_project` and teleport to it from anywhere!
* Did you say you want auto-completion with that? Of course there is auto-completion!
* Works with both zsh and bash!
* What if you want to call `my_project` "secret_project" instead? Goto's got you covered!
* Do you want different auto completion at different times? We got profiles for that!
* Works great as a complement to `j`!

## Unnecessary slogan

Goto - The good way to program

## Installing

#### bash

```sh
pip install --user goto-cd
_gotohelper --install bash
source ~/.bashrc
```

#### zsh

```sh
pip install --user goto-cd
_gotohelper --install zsh
source ~/.zshrc
```

#### Help I get "Command not found!"

There is a slight chance you get the error message `_gotohelper: command not
found` when installing. This probably means that goto was installed correctly,
but your `PATH` variable needs to include where `_gotohelper` is located. With
newer versions of pip `_gotohelper` tends to be installed in `~/.local/bin` and
so you would add `export PATH=$PATH:~/.local/bin` to the end of your `.bashrc`
in bash and `.zshrc` in zsh.

## Documentation

See the [docs](https://github.com/CatEars/goto/blob/master/docs/README.md) folder.

## Contributing

See [contributing.md](https://github.com/CatEars/goto/blob/master/Contributing.md).

## License

MIT - see [LICENSE](https://github.com/CatEars/goto/blob/master/LICENSE)
