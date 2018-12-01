export LC_ALL=C.UTF-8
export LANG=C.UTF-8

EXEC=$(which _gotohelper)
if [ -z "$EXEC" ]; then
    echo "Shell test failed. _gotohelper not installed!"
    exit 1
fi


_gotohelper --install $SHELL
export PS1="fake interactivity. otherwise we get kicked out of .bashrc"
source $RCFILE

cd /tmp
# Make a/b/c/d, deep levels and top levels a, b, c and d
mkdir -p a/b/c/d b c d

goto --add ./a

if [ -z "$(goto --get a)" ]; then
    echo "Simple test failed, could not get 'goto --get a'"
    exit 1
fi

cd /
goto a
if [ "$(pwd)" != "/tmp/a" ]; then
    echo "Could not teleport using goto"
    exit 1
fi

goto --add t:b/c/d
if ! goto --get t; then
    echo "Cannot use different name for teleports"
    exit 1
fi
goto --remove t

# Try listing
goto --list

goto --profile otherprofile

if goto --get a; then
    echo "Changed to empty profile but got something from --get! not possible!"
    exit 1
fi

cd /

goto a

if [ "$(pwd)" == "/tmp/a" ]; then
    echo "Teleported to a, even tough there is no such teleport!"
    exit 1
fi


