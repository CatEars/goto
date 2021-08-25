# goto

🔖 🔖 🔖 Bookmarks for the terminal 🔖 🔖 🔖

The tldr usage of `goto`:

1. Bookmark with `goto --add ./my_folder`
2. Use `cd` to go somewhere else, or open a new terminal, or restart your computer
3. Run `goto my_folder` and you're teleported back to `my_folder`

Usage gifs and usage documentation can be found in the
[docs folder](https://github.com/CatEars/goto/blob/master/docs/README.md)

## Key Features

* Like browser bookmarks, but for the commandline!
* Add commonly visited places, like `code/my_project` and teleport to it from anywhere!
* Did you say you want auto-completion with that? Of course there is auto-completion!
* Works with bash, zsh and powershell!
* Got several folders with similar names? Use an alias for the bookmark!

## Unnecessary slogan

Goto - The good way to program

## Installing

#### bash

```sh
cargo install goto-cd
goto-cd --install >> ~/.bashrc
```

#### zsh

```sh
cargo install goto-cd
goto-cd --install >> ~/.zshrc
```

#### powershell

```sh
cargo install goto-cd
goto-cd --install-powershell
```

## Documentation

See the [docs](https://github.com/CatEars/goto/blob/master/docs/README.md) folder.

## Contributing

See [contributing.md](https://github.com/CatEars/goto/blob/master/Contributing.md).

## License

MIT - see [LICENSE](https://github.com/CatEars/goto/blob/master/LICENSE)
