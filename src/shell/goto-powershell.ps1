function Goto() {
    if (($args.Count -eq 1) -and (-not ($args[0].StartsWith("-")))) {
        Set-Location $(goto-cd --get $args[0])
    } else {
        goto-cd $args
    }
}