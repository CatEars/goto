# This file is meant to be sourced
# Entry point for zsh based shells

function _GotoHelperFunction() {

}

function goto() {
    GT=_gotohelper
    A=$1
    B=$2
    if [[ ! $A == -* ]] && [ -n "$A" ]; then
        # We are dealing with a goto that wants to go somewhere
        # The first argument is non-null and does not start with a dash!
        target=$($GT --get $A)
        if [ $? -ne 0 ]; then
            echo "$target"
        elif [ -d $target ]; then
            cd $target
        else
            echo "'$target' seems to not be a directory..."
        fi
    else
        # We are dealing with a command + argument
        $GT $A $B
    fi
}

compdef _GotoHelperFunction goto
