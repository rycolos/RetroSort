#!/usr/bin/env python3

import os 
import sys
import glob 
import shutil
from datetime import date
import configparser #pip
from paramiko import SSHClient #pip
from scp import SCPClient #pip

transferDate = date.today()

configPath = 'RetroSort.conf'
if not os.path.isfile(configPath): 
	sys.exit("Error: Config file " + configPath + "is missing. Please create it.")

"""
From RetroPie docs: https://retropie.org.uk/docs/
Augment as needed. 
"""
emulatorTarget = {
	"*.cpc": "amstradcpc",
	"*.a26": "atari2600",
	"*.a52": "atari5200",
	"*.a78": "atari7800",
	"*.lnx": "atarilynx",
	"*.gba": "gba",
	"*.gg": "gamegear",
	"*.gb": "gb",
	"*.gbc": "gbc",
	"*.sms": "mastersystem",
	"*.ngp": "ngp",
	"*.ngc": "ngpc",
	"*.z64": "n64",
	"*.n64": "n64",
	"*.v64": "n64",
	"*.nes": "nes",
	"*.fds": "nes",
	"*.pce": "pcengine",
	"*.32x": "sega32x",
	"*.sg": "sg-1000",
	"*.smc": "snes",
	"*.sfc": "snes",
	"*.fig": "snes",
	"*.swc": "snes",
	"*.vec": "vectrex",
	"*.gam": "vectrex",
	"*.szx": "zxspectrum",
	"*.z80": "zxspectrum"
}


"""
Parse RetroSort.conf to get SSH/SCP details and targets. 
Check if key or password auth selected.
Connect to host.
"""
config = configparser.ConfigParser()
config.read(configPath)
host = (config.get("ssh", "host"))
user = (config.get("ssh", "username"))
port = int((config.get("ssh", "port")))
localPath = (config.get("targets", "localdir"))
remotePath = (config.get("targets", "remotedir"))

keyCheck = config.has_option("ssh", "keyfile")
passCheck = config.has_option("ssh", "password")

client = SSHClient()
client.load_system_host_keys()

if keyCheck == True and passCheck == False:
	print("Connecting to " + host)
	print("Authenticating with key...")
	print("\n")
	key = (config.get("ssh", "keyfile"))
	client.connect(host, username=user, key_filename=key, port=port)

elif passCheck == True and keyCheck == False: 
	print("Connecting to " + host)
	print("Authenticating with password...")
	print("\n")
	passwd = (config.get("ssh", "password"))
	client.connect(host, username=user, password=passwd, port=port)

elif passCheck == True and keyCheck == True:
	sys.exit("Cannot authenticate. Key and password both provided. Check RetroSort.conf and try again")

else:
	sys.exit("No authentication provided. Check RetroSort.conf and try again")


"""
Make folder to house completed transfers,
if folder doesn't already exist.
"""
localBackupDir = localPath + str(transferDate) + " " + "transfers"
if not os.path.exists(localBackupDir):
	os.makedirs(localBackupDir)


"""
Parse emulatorTarget into fileExt and system.
If fileExt exists, count + display how many files.
Make emulation system directories (ssh) if don't exist.
Copy files to remote directories via SCP -- will not overwrite in dest.
Move local files into localBackupDir.
"""
sysCount = 0
totalFileCount = 0
for fileExt, system in emulatorTarget.items():
	if glob.glob(localPath + fileExt): #fileExt exists
		print("\n")
		sysCount = sysCount + 1
		
		fileCount = len(glob.glob(localPath + fileExt))
		print("\033[1m" + str(fileCount) + " " + fileExt + " files exist" + "\033[0m")
	
		stdin, stdout, stderr = client.exec_command("mkdir " + remotePath + system)

		for file in glob.glob(localPath + fileExt):
			totalFileCount = totalFileCount + 1
			scp = SCPClient(client.get_transport())
			scp.put(file, remotePath + system)
			print(file + " ...file copied")
			shutil.move(file, localBackupDir)
		
		print("\n")

	else: 
		print("No " + fileExt + " files found.")

scp.close()

print("\n")		
completion = ("Completed transfer of " + str(totalFileCount) + " files for " 
	+ str(sysCount) + " systems to " + remotePath)
print(completion)