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

echo "Removing teleportation 't'"
goto --remove t

if goto --get t; then
    echo "Removed teleport 't' but it is still here!"
    exit 1
fi

echo "Trying to list all teleports"
goto --list

echo "Changing profile to 'otherprofile'"
goto --profile otherprofile

if goto --get a; then
    echo "Changed to empty profile but got something from --get! not possible!"
    exit 1
fi

echo 'Backing up to /'
cd /

echo "Trying to teleport to 'a' without such a teleport"
goto a

if [ "$(pwd)" == "/tmp/a" ]; then
    echo "Teleported to a, even tough there is no such teleport!"
    exit 1
fi

cd /tmp

echo "Adding aaa, aab, aac and aad and expecting prefix 'aa' to return these"
goto --add aaa:a
goto --add aab:b
goto --add aac:c
goto --add aad:d

if ! goto --prefix aa; then
    echo "Prefix for 'aa' failed"
    exit 1
fi

echo "Getting prefix for aa and testing aaa, aab, aac and aad"
RES="$(goto --prefix aa)"
if [[ $RES != *"aaa"* ]] || [[ $RES != *"aab"* ]] || [[ $RES != *"aac"* ]] || [[ $RES != *"aad"* ]]; then
    echo "Prefix operation did not return everything!"
    exit 1
fi

echo "Getting prefix for aab, should be an exact string"
RES="$(goto --prefix aab)"
if [[ $RES != "aab" ]]; then
    echo "Prefix could not find when a perfectly matching prefix existed"
    exit 1
fi
