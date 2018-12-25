# This file is meant to be sourced
# Entry point for zsh based shells

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

function _GotoHelperFunction() {
    local context state state_descr line
    typeset -A opt_args

    _arguments -C \
               "-h[Show help information]" \
               "--help[Show help information]" \
               "--add[Add a teleport]" \
               "--remove[Remove a teleport]" \
               "--install[Install for either bash or zsh]" \
               "--profile[Change to a different profile]" \
               "--profiles[List all profiles]" \
               "--rmprofile[Remove a profile]" \
               "*::arg:->string"

    A=$line
    if [[ ! $A == -* ]]; then
        target=($(_gotohelper --prefix "$A"))
        _describe -t target 'teleports' target
    fi
}

compdef _GotoHelperFunction goto
