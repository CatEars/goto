# Install

### Tags

Basic, Run Once

### Usage

```bash
$ _gotohelper --install bash
```

or 

```zsh
$ _gotohelper --install zsh
```

### Effect

Will install goto either under `bash` or under `zsh`. This command uses
`_gotohelper` in order to bootstrap `goto` into your shell. It should only be
necessary to run once and should be the first command you run.

### Notes

If you want to install goto under both `bash` and `zsh` then you just run both
of the commands. They use the same "backend" and only differ in that one targets
your `.bashrc` and the other targets your `.zshrc`. If it helps you can think of
it like two different `git` user interfaces (porcelains). Both use the same
underlying data to work properly.
