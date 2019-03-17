# zyxel-poe-manager
A convenience script to manage the state of the PoE ports of a Zyxel GS1900 series switch.

## Motivation

This was written because my Zyxel GS1900-10HP switch managed to get me angry enough with the abhorrent web interface and inability to do anything useful via SNMP or the CLI.
The only thing it does is log into the web management and do the same you would do by clicking approx. 10 times.


## Dependencies

This program was written for python3. You are welcome to rewrite it for python2 and make a PR.

The only dependency is `requests`. You can install it using pip:
```bash
python3 -m pip install requests
```
Furthermore the script was tested on firmware version `V2.40(AAZI.1)_20180705` of my `GS1900-10HP` model rev `A1`. There are absolutely no guarantees that it will work with your system.


## Usage
```
usage: poe-manager.py [-h] --host HOST --user USER --password PWD --port PORT
                      --state {0,1}

Manage PoE ports for a Zyxel GS1900-10HP switch.

optional arguments:
  -h, --help            show this help message and exit
  --host HOST, -H HOST  The hostname of the switch.
  --user USER, -U USER  An administrative user.
  --password PWD, -P PWD
                        Password of the admin user.
  --port PORT, -p PORT  The port number.
  --state {0,1}, -s {0,1}
                        Turn the port on (1) or off (0).
```

## Examples

### Turn on PoE port 3

```bash
python3 poe-manager.py --host '10.10.10.2' --user admin --password hunter2 --port 3 --state 1
```

### Turn off PoE port 3

```bash
python3 poe-manager.py --host '10.10.10.2' --user admin --password hunter2 --port 3 --state 0
```

### Bash convenience function

This is how I primarily use this script. Insert the following in your `.bashrc`:
```bash
function poemanager() { /path/to/poe-manager.py -H '10.10.10.2' -U admin -P hunter2 -p $1 -s $2; }
```
This would make the above examples look like the following:
```bash
poemanager 3 1   # turn on port 3
poemanager 3 0   # turn off port 3
```

Yes, you are saving the password in your `.bashrc`, but if someone can read arbitrary files in your system you're in much more trouble.


## Contribution

If you manage to extend the feature set of this script, I'd really appreciate a PR.


## Licensing

This program is licensed under the GPL 2.0 license. For more information, please refer to `LICENSE`.
