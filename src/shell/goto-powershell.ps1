
function Goto() {
    if (($args.Count -eq 1) -and (-not ($args[0].StartsWith("-")))) {
        Set-Location $(goto-cd --get $args[0])
    } else {
        goto-cd $args
    }
}

$gotoCompletionScriptBlock = {
    param($wordToComplete, $commandAst, $cursorPosition)
    if ([String]::IsNullOrEmpty($wordToComplete)) {
        $(goto-cd.exe --all-prefix).Split("   ")
    } else {
        $(goto-cd.exe --prefix $wordToComplete).Split("   ") 
    }
}
Register-ArgumentCompleter -CommandName Goto -Native -ScriptBlock $gotoCompletionScriptBlock