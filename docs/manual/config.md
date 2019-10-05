# CONFIG

### Tags

Basic

### Usage

```bash
$ goto --config set attribute value
$ goto --config get attribute -1
$ goto --config remove attribute -1
```

### Effect

1. Will set and store `attribute`/`value` in `_setting.toml` 
2. Will get the `attribute` (if it exists) from `_setting.toml`
3. Will remove the `attribute` (if it exists) from `_setting.toml`

### Notes

`get` and `remove` need -1 as the module click doesn't allow variable length arguements
