

tobashrc() {
    grep -Fxq "$@" /etc/bash.bashrc && echo "$@" >> /etc/bash.bashrc
    $@
}

# setup, load variables
export BOOT_VARS_FILE='/boot/resources/vars.sh'
tobashrc . $BOOT_VARS_FILE

bootvars.add() {
    sed -i -n -e '/^export '"$1"'=/!p' -e '$a'"export $1=$2" "$BOOT_VARS_FILE"
}

bootvars.remove() {
    sed -i '/^export '"$1"'=/d' "$BOOT_VARS_FILE"
}


# print section header
section() {
    echo
    echo '****************************'
    echo ${@}
    echo '****************************'
    echo
}

# copy a file, but make a backup of an existing file
backupcp() {
    if [ -f "$1" ]; then
        [ -f "$2" ] && mv "$2" "${2}.old"
        DIR=$(dirname $(readlink -m "$2"))
        [ ! -z $DIR ] && mkdir -p "$DIR"
        cp "$1" "$2"
    fi
}
# run a file if it exists
mayberun() {
    if [ -f $1 ]; then chmod +x $1; $@;fi
}


STATUSDIR=/boot/.firstboot-status
mkdir -p "$STATUSDIR"
# touch a file to show how far we got
status.update() {
    for i in {000..100}; do
        FNAME="$STATUSDIR/$i-$1"
        if [ -f $FNAME ] || [ -z "$(status.list '*' "$i")" ]; then
            # echo $FNAME
            touch $FNAME
            echo "$FNAME $(date)" >> "$STATUSDIR/times"
            status.upload "$1" "$2"
            break
        fi
    done
}

status.list() {
    name=${2:-*}-${1:-*}
    [ -d "$STATUSDIR" ] && find "$STATUSDIR" -maxdepth 1 ! -path "$STATUSDIR" -name "$name" -print
}

status.clear() {
    [ $(status.list) ] && rm "$STATUSDIR/*" || true
}

status.upload() {
    if [ ! -z "$MONITOR_HOST" ] && [ ! -z "$UUID" ]; then
        URL="http://$MONITOR_HOST/update/$UUID/$1?$2"
        echo "$URL"
        curl "$URL" || echo "calling monitor server failed: $URL"
    fi
}

# get your local IP address (e.g. 192.168.1.54)
localip() {
    _localip wlan0 || _localip eth0
}
_localip() {
    regex="inet ([0-9.]+)" && [[ $(ifconfig ${1:-wlan0}) =~ $regex ]] && echo ${BASH_REMATCH[1]}
}
