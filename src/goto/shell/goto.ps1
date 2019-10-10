function goto($A, $B, $C, $D) {
	if ($A.StartsWith("-") -or [string]::IsNullOrEmpty($A)) {
		_gotohelper $A $B $C $D
	} else {
		$target=$(_gotohelper --get $A)
		if (!$?) {
			# Last operation failed
			echo "$target"
		} elseif (Test-Path $target) {
			cd $target
		} else {
			echo "'$target' seems to not be a directory..."
		}
	}
}