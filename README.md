# goto

![build](https://travis-ci.org/CatEars/goto.svg?branch=master)
[![PyPI version](https://badge.fury.io/py/goto-cd.svg)](https://badge.fury.io/py/goto-cd)
![coverage](https://github.com/CatEars/goto/blob/master/badges/coverage.svg)

A command line tool for teleporting around your computer!

![Usage Gif](https://github.com/CatEars/goto/blob/master/docs/simple-usage.gif)

## Key Features

* Add commonly visited places, like `code/my_project` and teleport to it from anywhere!
* Did you say you want auto-completion with that? Of course there is auto-completion!
* Works with both zsh and bash!
* What if you want to call `my_project` "secret_project" instead? This is entirely possible!
* Do you want different auto completion at different times? We got profiles for that!

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
