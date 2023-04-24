# MisterFPGA Network Shares

Python script to connect a remote server and mounting games folders automatically.

# Usage

+ copy `network_shares.py` in `/media/fat/Scripts` 
+ create a `network_shares.ini` in the same directory (read the [configuration](#configuration) section of the readme)
+ run `network_shares.py`


# Configuration

Configuration is a simple [ini](https://en.wikipedia.org/wiki/INI_file) file with sections.

You can configure both CIFS and NFS, but NFS has an higher priority if you are using bind mounts.

## Settings

```ini
[Settings]
runatstartup = True/False Enable the script to run when misterfpga starts.
```

## CIFS

```ini
[CIFS]
Server    = <ip> or <network name>  *Mandatory Ex: 192.168.1.1
Share     = <shared folder>         *Mandatory Ex: /myshare/mister
Username  = <username>              *Optionnal
Password  = <password>              *Optionnal
Bindmount = True/False              *Optionnal Bind mount each folder in your share to the same folder in games.
Clearafterbindmount = True/False    *Optionnal Remove the default mount point, only when bindmount is used. 
ADDITIONAL_MOUNT_OPTIONS= <additionnal mount parameters> *Optionnal
```

## NFS

```ini
[NFS]
Server      = <ip> or <network name>    *Mandatory Ex: 192.168.1.1
Share       = <shared folder>           *Mandatory Ex: /myshare/mister
Bindmount   = True/False                *Optionnal Bind mount each folder in your share to the same folder in games.
Clearafterbindmount = True/False        *Optionnal Remove the default mount point, only when bindmount is used. 
ADDITIONAL_MOUNT_OPTIONS= <additionnal mount parameters> *Optionnal
```

