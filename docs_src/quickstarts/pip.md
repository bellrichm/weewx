# Installation using pip

This is a guide to installing WeeWX using [pip](https://pip.pypa.io). It can be used to
install WeeWX on almost any operating system, including macOS.

## Preparation

- WeeWX V5.x requires Python 3.7 or greater. It cannot be run with Python 2.x.  If you are constrained by this, install WeeWX V4.10, the
  last version to support Python 2.7, Python 3.5, and Python 3.6.

- You must also have a copy of pip. In most cases, your operating system will offer an
  [installation package](https://packaging.python.org/en/latest/guides/installing-using-linux-tools/).
  Otherwise, [see the directions on the pip website](https://pip.pypa.io/en/stable/installation/).

- While you will not need root privileges to install and configure WeeWX,
  you will need them to set up a daemon and, perhaps, to change device permissions.

Depending on your operating system and how complete it is, you may have to install some tools
before beginning. Follow the directions below for your system:

=== "Debian"

    ```shell
    sudo apt update && sudo apt upgrade
    sudo apt -y install gcc
    sudo apt -y install python3-dev
    # This makes the install of pyephem go more smoothly:
    python3 -m pip install wheel
    ```

=== "Redhat"
    ```shell
    sudo yum update
    sudo yum install -y gcc
    sudo yum install -y python3-devel
    # This makes the install of pyephem go more smoothly:
    python3 -m pip install wheel
    ```

=== "openSUSE Leap"

    ```shell
    # Check to see what version of Python you have:
    python3 -V
    # If it is less than Python 3.7, you will have to upgrade to a 
    # later version. The following installs 3.9. Afterwards, you must
    # invoke Python by using "python3.9", NOT "python3"
    sudo zypper install -y python39 python39-devel
    python3.9 -m pip install wheel

    # Finally, you may have to add ~/.local/bin to your path:
    echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.profile
    source ~/.profile
    ```

## Installation steps

Installation is a two-step process:

1. Install the WeeWX application using pip.
2. Provision a new station using the tool `weectl`.


### Step 1: Install the application using pip

Once the preparatory steps are out of the way, you're ready to install WeeWX using pip.

There are many ways to do this (see the wiki document [pip
install strategies](https://github.com/weewx/weewx/wiki/pip-install-strategies)
for a partial list), but the method below is one of the simplest and safest.

!!! Note
    While not strictly necessary, it's a good idea to invoke pip using `python3 -m pip`, rather 
    than simply `pip`. This way you can be sure which version of Python is being used.

```shell
python3 -m pip install weewx --user
```

When finished, the WeeWX executables will have been installed in `~/.local/bin`,
and the libraries in your Python "user" area, generally `~/.local/lib/python3.x/site-packages/`,
where `3.x` is your version of Python.

!!! Note
    You may get a warning to the effect:
          ```
          WARNING: The script wheel is installed in '/home/ubuntu/.local/bin' which is not on PATH.
          Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
          ```
    If you do, log out, then log back in.

### Step 2: Provision a new station

While the first step downloads everything into your local Python source tree, it
does not set up the configuration specific to your station, nor does it set up the
reporting skins. That is the job of the next step, which uses the tool `weectl`. 

This step also does not require root privileges.

```shell
weectl station create
```

The tool will ask you a series of questions, then create a directory `~/weewx-data` in your home
directory with a new configuration file. It will also install skins, documentation, utilitiy files,
and examples in the same directory. After running `weewxd`, the same directory will be used to hold
the database file and any generated HTML pages. It plays a role similar to `/home/weewx` in older
versions of WeeWX but, unlike `/home/weewx`, it does not hold any code.

If you already have a `/home/weewx` and wish to reuse it, see the [Upgrading
guide](../upgrading.htm) and the [*Migrating setup.py installs to Version 5*](v5-upgrade.md).

## Running `weewxd`

### Run directly

After the last step, the main program `weewxd` can be run directly like any
other program:

```shell
weewxd
```

### Run as a daemon

If you wish to run `weewxd` as a daemon, follow the following steps, depending
on your operating system. These steps will require root privileges in order to
install the required daemon file.

=== "Debian"

    !!! Note
        The resulting daemon will be run using your username. If you prefer to use run as `root`,
        you will have to modify the file `/etc/systemd/system/weewx.service`.

    ```shell
    cd ~/weewx-data
    sudo cp util/systemd/weewx.service /etc/systemd/system
    sudo systemctl daemon-reload
    sudo systemctl enable weewx
    sudo systemctl start weewx
    ```
    
=== "Very old Debian"

    !!! Note
        The resulting daemon will be run using your username. If you prefer to use run as `root`,
        you will have to modify the file `/etc/init.d/weewx`.

    ```shell
    # Use the old init.d method if your os is ancient
    cd ~/weewx-data
    sudo cp util/init.d/weewx.debian /etc/init.d/weewx
    sudo chmod +x /etc/init.d/weewx
    sudo update-rc.d weewx defaults 98
    sudo /etc/init.d/weewx start     
    ```

=== "Redhat"

    !!! Note
        The resulting daemon will be run using your username. If you prefer to use run as `root`,
        you will have to modify the file `/etc/systemd/system/weewx.service`.

    ```shell
    # If SELinux is enabled, you will need the following command first:
    chcon -R --reference /bin/ls ~/.local/bin

    # Then proceed as normal:
    cd ~/weewx-data
    sudo cp util/systemd/weewx.service /etc/systemd/system
    sudo systemctl daemon-reload
    sudo systemctl enable weewx
    sudo systemctl start weewx
    ```

=== "openSUSE Leap"

    !!! Note
        The resulting daemon will be run using your username. If you prefer to use run as `root`,
        you will have to modify the file `/etc/systemd/system/weewx.service`.

    ```shell
    cd ~/weewx-data
    sudo cp util/systemd/weewx.service /etc/systemd/system
    sudo systemctl daemon-reload
    sudo systemctl enable weewx
    sudo systemctl start weewx
    ```

=== "macOS"

    ```shell
    cd ~/weewx-data
    sudo cp util/launchd/com.weewx.weewxd.plist /Library/LaunchDaemons
    sudo launchctl load /Library/LaunchDaemons/com.weewx.weewxd.plist
    ```


### Verify

After about 5 minutes (the exact length of time depends on your archive interval), cut and
paste the following into your web browser:

    ~/weewx-data/public_html/index.html

You should see your station information and data.

You may also want to check your system log for any problems.

## Configure

If you chose the simulator as your station type, then at some point you will
probably want to switch to using real hardware. Here's how to reconfigure.

=== "Debian/Redhat/openSUSE"

    ```shell
    sudo systemctl stop
    # Reconfigure to use your hardware:
    weectl station reconfigure
    # Remove the old database:
    rm ~/weewx-data/archive/weewx.sdb
    # Restart:
    sudo systemctl start
    ```

=== "Very old Debian"

    ```shell
    sudo /etc/init.d/weewx stop
    # Reconfigure to use your hardware:
    weectl station reconfigure
    # Remove the old database:
    rm ~/weewx-data/archive/weewx.sdb
    # Restart:
    sudo /etc/init.d/weewx start
    ```

=== "macOS"

    ```shell
    sudo launchctl unload /Library/LaunchDaemons/com.weewx.weewxd.plist
    # Reconfigure to use your hardware:
    weectl station reconfigure
    # Remove the old database:
    rm ~/weewx-data/archive/weewx.sdb
    # Restart:
    sudo launchctl load /Library/LaunchDaemons/com.weewx.weewxd.plist
    ```

## Customize

To enable uploads, such as Weather Underground, or to customize reports, modify
the configuration file `~/weewx-data/weewx.conf`. See the [*User
Guide*](../usersguide) and [*Customization Guide*](../custom) for details.


## Uninstall

Stop, disable, and remove any daemon files:

=== "Debian/Redhat/openSUSE"

    ```shell
    sudo systemctl stop weewx
    sudo systemctl disable weewx
    sudo rm /etc/systemd/system/weewx.service
    ```

=== "Very old Debian"

    ```shell
    sudo /etc/rc.d/init.d/weewx stop
    sudo rm /etc/init.d/weewx
    ```

=== "macOS"

    ```shell
    sudo launchctl unload /Library/LaunchDaemons/com.weewx.weewxd.plist
    sudo rm /Library/LaunchDaemons/com.weewx.weewxd.plist
    ```


Use pip to uninstall the program.

```shell
python3 -m pip uninstall weewx -y
```

You can also use pip to uninstall the dependencies, but first check that they are
not being used by other programs!

```shell
python3 -m pip uninstall pyserial pyusb CT3 Pillow configobj PyMySQL pyephem ephem -y
```

Finally, if desired, delete the data directory:

```shell
rm -r ~/weewx-data
```