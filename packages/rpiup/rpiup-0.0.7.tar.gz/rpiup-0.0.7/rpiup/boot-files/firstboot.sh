#!/bin/bash

# expand empty glob to empty string, not original pattern
shopt -s nullglob

UTILS_FILE='/boot/boot-utils.sh'
. $UTILS_FILE
echo ". $UTILS_FILE" >> /etc/bash.bashrc


# if we've already finished, exit.

if [ "$(status.list done)" ]; then
    [ -f /boot/firstboot.sh ] && mv /boot/firstboot.sh /boot/firstboot.sh.done
    exit 0;
fi

########################################
# Setup
########################################

status.update start ip=$(localip)

# make sure the date is right
date -s "$(wget -qSO- --max-redirect=0 google.com 2>&1 | grep Date: | cut -d' ' -f5-8)Z"

status.update pull-correct-time


# run custom setup

if [ -z "$(status.list setup-before)" ]; then
    mayberun /boot/resources/setup-before.sh
    status.update custom-setup-before
fi


# create user

if [ -z "$(status.list new-user)" ]; then
    section "Setting user to $USERNAME:$PASSWORD ..."
    if [ ! -z "$USERNAME" ] && [ ! -d "/home/$USERNAME" ]; then
        adduser --disabled-password --gecos '' $USERNAME
        usermod -aG "$(id -Gn pi | sed -e 's/ /,/g')" $USERNAME
        passwd --lock pi
        echo "Current user: $USER"
    fi

    export HOME="/home/${USERNAME:-pi}"

    if [ ! -z "$PASSWORD" ]; then
        yes "$PASSWORD" | passwd "${USERNAME:-pi}"
        bootvars.remove PASSWORD
    fi

    status.update new-user
fi


# set hostname

if [ -z "$(status.list hostname)" ]; then
    if [ -z "$firstboot_hostname" ]; then
        MAC=$(cat /sys/class/net/eth0/address | sed 's/://g')
        HOSTNAME_PREFIX="${HOSTNAME_PREFIX:-${APP_NAME}node}"
        firstboot_hostname="${HOSTNAME_PREFIX}-${MAC}"
    fi
    section "Setting hostname to $firstboot_hostname ..."

    echo "$firstboot_hostname" > /etc/hostname
    sed -i "s/raspberrypi/$firstboot_hostname/g" /etc/hosts
    hostname "$firstboot_hostname"

    status.update hostname
fi


# set raspi-config defaults (0=yes, 1=no ??idk why)

if [ -z "$(status.list raspi-config)" ]; then
    raspi-config nonint do_boot_wait 1
    raspi-config nonint do_i2c 0
    raspi-config nonint do_boot_splash 0

    # set country - TODO will country/keyboard be the same ???
    COUNTRY=${COUNTRY:-US}
    KEYBOARD=$(echo ${KEYBOARD:-$COUNTRY} | awk '{print tolower($0)}')
    raspi-config nonint do_wifi_country $COUNTRY
    raspi-config nonint do_configure_keyboard $KEYBOARD

    echo "ClientAliveInterval 30" >> /etc/ssh/sshd_config

    status.update raspi-config
fi


if [ -z "$(status.list etc)" ]; then
    # set network interfaces
    backupcp /boot/resources/network_interfaces /etc/network/interfaces
    # set fstab
    backupcp /boot/resources/fstab /etc/fstab

    status.update etc
fi


if [ -z "$(status.list installs)" ]; then
    # install htop wavemon
    section "Installing core packages..."
    apt-get update

    # # set date and timezone
    apt-get install -y jq && \
        timedatectl set-timezone "$(curl -s http://ip-api.com/json/$(curl -s ifconfig.me) | jq -r .timezone 2>&1)"

    apt-get install -y git htop wavemon

    # github
    if [ ! -z "$GIT_USERNAME" ]; then
        git config --global user.name "$GIT_USERNAME"
    fi
    if [ ! -z "$GIT_PASSWORD" ]; then
        git config --global user.password "$GIT_PASSWORD"
        # bootvars.remove GIT_PASSWORD
    fi

    status.update installs
fi


# set splash image
if [ -f /boot/resources/splash.png ]; then
    section "Installing splash image..."
    apt-get install -y fbi
    backupcp /boot/resources/.internal/splashscreen.service /etc/systemd/system/splashscreen.service
    systemctl enable splashscreen
    # systemctl start splashscreen
fi
# backupcp /boot/resources/splash.png /usr/share/plymouth/themes/pix/splash.png


# install python 3 and make it the default
if [ -z "$(status.list install-python)" ]; then
    section "Installing Python 3..."

    apt-get install -y python3 python3-pip
    update-alternatives --install /usr/bin/python python /usr/bin/python3 4
    update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1
    update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 4
    /usr/bin/python3 -m pip install -U pip setuptools

    status.update install-python
fi


# upgrade wifi device
if [ -z "$(status.list wifi-drivers)" ]; then
    section "Installing wifi devices..."

    wget http://downloads.fars-robotics.net/wifi-drivers/install-wifi -O /usr/bin/install-wifi
    chmod +x /usr/bin/install-wifi
    install-wifi -u 8188eu && install-wifi -u 8192eu && install-wifi -u 8812au
    apt-get install -y firmware-ralink

    status.update wifi-drivers
fi


# install docker, docker-compose
if [ -z "$(status.list docker)" ]; then
    section "Installing docker..."

    curl -sSL https://get.docker.com | sh
    [ ! -z $USERNAME ] && usermod -aG docker $USERNAME
    /usr/bin/python3 -m pip install docker-compose
    systemctl restart docker

    status.update docker
fi


# install systemctl services
if [ -z "$(status.list systemctl-services)" ]; then
    section "Installing any systemctl services..."

    CWD=$(pwd)
    for svc_dir in /boot/resources/services/*; do
        cd "$svc_dir"
        if [ -f "./install.sh" ]; then
            ./install.sh
        fi
        # start
        svc_name=$(basename "$svc_dir")
        echo "starting service "$svc_name" and setting to run on boot..."
        systemctl enable "$svc_name"
        systemctl start "$svc_name"
        echo 'done.'
        sleep 1
        systemctl status "$svc_name"
        exit 0
    done
    cd "$CWD"

    status.update systemctl-services
fi


# install docker containers
if [ -z "$(status.list docker-compose)" ]; then
    section "Installing any docker containers..."

    CWD=$(pwd)
    for svc_dir in /boot/resources/docker/*; do
        touchlap "docker-$(basename "$svc_dir")"
        cd "$svc_dir"
        docker-compose up -d
    done
    cd "$CWD"

    status.update docker-compose
fi


# run custom setup
if [ -z "$(status.list custom-setup)" ]; then
    mayberun /boot/resources/setup.sh
    status.update custom-setup
fi

section "Done! Enjoy!! Don't be evil. **Do** topple capitalism. :D"
status.update "done"

# sleep 5
# reboot
