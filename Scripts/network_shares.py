#!/usr/bin/env python3

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Copyright 2023 Wilfried "willoucom" JEANNIARD

# You can download the latest version of this script from:
# https://github.com/willoucom/MisterFPGA_Network_Shares


import configparser
import os
import shutil
import subprocess
import time

# Loop for server availability
def waitforserver(server, timeout=10):
    if timeout <= 0:
        print("Timeout")
        return False
    try:
        subprocess.check_output(["ping", "-4", "-c", "1", server])
        return True
    except subprocess.CalledProcessError:
        print("Ping KO (Retries:"+str(timeout)+")")
        time.sleep(1)
        return waitforserver(server, timeout-1)

# Mount directory using CIFS
def cifs_mount(settings):
    print("CIFS mount")
    dest = "/media/network"
    checkdirectory(dest)
    source = "//"+settings["server"]+""+settings["share"]
    options = ""
    if "username" in settings and "password" in settings:
        options = "-o username=" + \
            settings["username"] + ",password=" + settings["password"]
    if "ADDITIONAL_MOUNT_OPTIONS" in settings and settings["ADDITIONAL_MOUNT_OPTIONS"] != "":
        options += options + "" + settings["ADDITIONAL_MOUNT_OPTIONS"]
    timeout = 10
    if "Timeout" in settings and settings["Timeout"] != "":
        timeout = settings["Timeout"]
    # Wait for server
    if waitforserver(settings["server"], timeout):
        # mount
        cmd = "/usr/bin/busybox mount -t cifs " + source + " " + dest + " " + options
        os.system(cmd)

# Mount directory using NFS(v3)
def nfs_mount(settings):
    print("NFS mount")
    dest = "/media/network"
    checkdirectory(dest)
    source = ""+settings["server"]+":"+settings["share"]
    options = "-o nolock"
    if "ADDITIONAL_MOUNT_OPTIONS" in settings and settings["ADDITIONAL_MOUNT_OPTIONS"] != "":
        options = options+""+settings["ADDITIONAL_MOUNT_OPTIONS"]
    timeout = 10
    if "Timeout" in settings and settings["Timeout"] != "":
        timeout = settings["Timeout"]
    # Wait for server
    if waitforserver(settings["server"], timeout):
        # mount
        cmd = "/usr/bin/busybox mount -t nfs " + source + " " + dest + " " + options
        os.system(cmd)

# Check if directory exists and unmount
def checkdirectory(dir):
    # Check if dest exists
    if not os.path.isdir(dir):
        print(dir+" not found, creating")
        os.makedirs(dir, exist_ok=True)
    # umount
    umount(dir)

# Unmount
def umount(dir):
    if (os.path.ismount(dir)):
        # umount
        cmd = "/usr/bin/busybox umount " + dir
        os.system(cmd)

# Add current script to user-startup.sh
def writeuserscript():
    print("Run script at Mister startup")
    # check for userscript file
    if not os.path.isfile("/media/fat/linux/user-startup.sh"):
        print("/media/fat/linux/user-startup.sh not found, creating")
        open("/media/fat/linux/user-startup.sh", mode='a').close()
    # Add to user-startup if not already present
    needle = "[[ -e " + __file__ + " ]] && " + __file__ + "\n"
    with open("/media/fat/linux/user-startup.sh", "r+") as file:
        for line in file:
            if needle in line:
                break
        else:  # not found, we are at the eof
            file.writelines(["# User Network Shares\n", needle, "#\n"])

# Main
def main():
    # Move to script directory
    os.chdir(os.path.dirname(__file__))
    # Init config
    config = configparser.ConfigParser()
    if os.path.isfile('network_shares.ini'):  # Check config file is present
        # Read config
        config.read('network_shares.ini')
    else:
        exit("config file network_shares.ini not found")

    if "CIFS" in config:  # Mount CIFS
        cifs_mount(config["CIFS"])

    if "NFS" in config:  # Mount NFS
        nfs_mount(config["NFS"])

    if "Settings" in config:
        if "runatstartup" in config["Settings"] and config["Settings"]["runatstartup"] == "True":
            writeuserscript()


# Run script
main()
