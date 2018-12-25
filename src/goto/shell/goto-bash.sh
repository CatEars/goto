# This file is meant to be sourced
# Entry point for bash based shells

_GotoHelperFunction() {
    local cur
    COMPREPLY=()
    cur=${COMP_WORDS[COMP_CWORD]}

    if [ $COMP_CWORD -eq 1 ]; then
        # User is trying to jump
        answers="$(_gotohelper --prefix "$cur")"
        COMPREPLY=($answers)
        return
    fi

    if [ $COMP_CWORD -eq 2 ]; then
        command=${COMP_WORDS[1]}
        if [ "$command" = "--remove" ] && [ -n "$cur" ]; then
            # User is trying to remove
            answers="$(_gotohelper --prefix "$cur")"
            COMPREPLY=($answers)
            return
        fi
    fi
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

complete -F _GotoHelperFunction goto
