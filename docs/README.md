# Documentation

`goto $NAME`

![PNG Normal Usage](https://github.com/CatEars/goto/raw/master/docs/tldrusage.png)

To see usage in the form of GIFs, look in the [tldr folder](https://github.com/CatEars/goto/blob/master/docs/tldr/README.md)

To see usage for each command in a `man` style manual, look in the [manual folder](https://github.com/CatEars/goto/tree/master/docs/manual)

## F.A.Q

#### `goto` is too long to type. I just want to type `abc` instead. How to?

The easiest way to accomplish this is to modify your `.zshrc` or `.bashrc` and add something like this:

```bash
function abc() {
   goto $@
}
```

This would work for bash atleast, but you could probably find what works for zsh
[here](https://unix.stackexchange.com/questions/337800/on-the-relative-merits-of-and).

Of course you probably want to have tab completion as well. The above won't give
you that. For bash you would add the following:

```
complete -F _GotoHelperFunction abc
```

For zsh you would add the following:

```
compdef _GotoHelperFunction abc
```

IMPORTANT NOTE: The above will have to be placed after `goto` is `source`d.
Otherwise the `_GotoHelperFunction` will not be defined yet.
