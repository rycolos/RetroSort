# RetroSort
A Python script to sort and transfer local rom files from a local machine to a RetroPie installation using SSH and SCP. 

This was designed to work on a LAN, but should work remotely (be sure to implement SSH security best practices). 

## Caveats
This script only works with roms that use unique extensions linked to the core systems in a stock RetroPie install. This script will not work with .bin, .cue, or other extensions that are used for multiple platforms. This script will not work with RetroPie add ons without modification. The script can be easily expanded by modifying the `emulatorTarget` dict. 

## Requirements
* [RetroPie](https://retropie.org.uk/docs/) installed on a Raspberry Pi with SSH enabled. This has only been tested on RetroPie 4.7 on a Raspberry Pi 3B.
* Python 3 - this script has not been fully tested on Python 2
* [Python pip](https://pip.pypa.io/en/stable/installing/)

## Installation

Using git:
```
cd
git clone https://github.com/rycolos/RetroSort.git
cd RetroSort
```
Using wget:
```
cd
wget https://github.com/rycolos/RetroSort/archive/master.zip
unzip master.zip
cd RetroSort-master
```
Install dependencies:
```
pip install -r requirements.txt
```

## Configuration
Remove `.template` from the `RetroSort.conf.template` config file and update per your local and remote systems.
Host must appear in `known_hosts` in order to connect. If using hostname, host is case sensitive to how it appears in `known_hosts`. 

```
#localdir is directory where roms are stored locally
#remotedir is parent directory on RetroPie where roms are stored remotely (usually /home/pi/RetroPie/roms/)
#use full path, no ~. Targets must end with /

[targets]
localdir = 
remotedir = /home/pi/RetroPie/roms/

#choose either password or key. comment out whatever choice is unused
#keyfile is location of private ssh key. usually in user/.ssh folder. use full path, no ~

[ssh]
host = xxx.xxx.xxx.xxx
port = 22
keyfile = 
username = 
#password = 
```

## Usage
Local roms should be stored in a single directory (like a `/downloads` folder). When the script runs, it will iterate through a dictionary of rom file extensions and the `~/RetroPie/roms/[system]` folder that the extension is associated with. Files will be sorted and transferred to the correct folder on the RetroPie installation, depending on their extension. Local files will be moved to a `[date] transfers` directory for backup and to make it easier to see which files were not transferred (like .cue and .bin files that are not associated with a single system). 

Ensure your RetroSort.conf file has been updated and run the script:
```
python3 RetroSort.conf
```

## Example Output
```
Connecting to 192.168.1.115
Authenticating with key...

No *.cpc files found.
No *.a26 files found.
No *.a52 files found.
No *.a78 files found.

1 *.lnx files exist
/Users/Personal/RetroSort/Testing/test.lnx ...file copied

2 *.gba files exist
/Users/Personal/RetroSort/Testing/test2.gba ...file copied
/Users/Personal/RetroSort/Testing/test.gba ...file copied

4 *.gg files exist
/Users/Personal/RetroSort/Testing/test1.gg ...file copied
/Users/Personal/RetroSort/Testing/test.gg ...file copied
/Users/Personal/RetroSort/Testing/test3.gg ...file copied
/Users/Personal/RetroSort/Testing/test2.gg ...file copied

No *.gb files found.
No *.gbc files found.
No *.sms files found.
No *.ngp files found.

1 *.ngc files exist
/Users/Personal/RetroSort/Testing/biggame.ngc ...file copied

No *.z64 files found.
No *.n64 files found.

1 *.v64 files exist
/Users/Personal/RetroSort/Testing/test.v64 ...file copied

No *.nes files found.
No *.fds files found.
No *.pce files found.
No *.32x files found.
No *.sg files found.
No *.smc files found.
No *.sfc files found.
No *.fig files found.

1 *.swc files exist
/Users/Personal/RetroSort/Testing/test.swc ...file copied

No *.vec files found.
No *.gam files found.
No *.szx files found.
No *.z80 files found.

Completed transfer of 10 files for 6 systems to /home/pi/RetroPie/retro
Local files moved to /Users/Personal/RetroSort/Testing/2020-12-20 transfers
```


