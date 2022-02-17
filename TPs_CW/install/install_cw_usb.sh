SCRIPTPATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
sudo cp $SCRIPTPATH/50-newae.rules /etc/udev/rules.d
sudo udevadm control --reload-rules && sudo udevadm trigger
sudo usermod -a -G dialout $USER
