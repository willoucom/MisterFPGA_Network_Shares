# MisterFPGA Network Shares

Python script to connect a remote server and mounting games folders automatically.

## Installation

Add the following to the bottom of `downloader.ini`:

```ini
[willoucom/MisterFPGA_Network_Shares]
db_url = https://raw.githubusercontent.com/willoucom/MisterFPGA_Network_Shares/db/db.json.zip
```

# Usage

+ create a `network_shares.ini` in the same directory (read the [configuration](#configuration) section of the readme)
+ run `network_shares.py`


# Configuration

Configuration is a simple [ini](https://en.wikipedia.org/wiki/INI_file) file with sections.

You can configure both CIFS and NFS, but NFS has an higher priority for symlinks.

## Settings

```ini
[Settings]
runatstartup = True/False Enable the script to run when misterfpga starts.
symlinks = True/False Link each folder in your share to the same folder in games.
```

## CIFS

```ini
[CIFS]
Server    = <ip> or <network name>  *Mandatory Ex: 192.168.1.1
Share     = <shared folder>         *Mandatory Ex: /myshare/mister
Username  = <username>              *Optionnal
Password  = <password>              *Optionnal
ADDITIONAL_MOUNT_OPTIONS= <additionnal mount parameters> *Optionnal
```

## NFS

```ini
[NFS]
Server      = <ip> or <network name>    *Mandatory Ex: 192.168.1.1
Share       = <shared folder>           *Mandatory Ex: /myshare/mister
ADDITIONAL_MOUNT_OPTIONS= <additionnal mount parameters> *Optionnal
```

