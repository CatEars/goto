# Add

### Tags

Basic

### Usage

```bash
$ goto --add path/to/folder
```

or

```bash
$ goto --add my_special_name:path/to/folder
```

### Effect

Will add `folder` as a teleportation target. After adding the folder you should
be able to teleport to it using `$ goto folder` or `$ goto my_special_name`.
Additionally, there should now also be tab completion activated for `folder` or
`my_special_name`.

### Notes

`Add` will only add the target to the current profile, so if you switch profiles
and want to have this teleportation target, then you will need to either switch
back to the same profile or `add` the teleportation target again.
