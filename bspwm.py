##################################################
#                                                #
#            BSPWM Installation Script           #
#                                                #
#               Chris Wilson - 2015              #
#                                                #
##################################################

import os
import sys
import platform
import fileinput

#Source URLs
bspwm_git_dir = "https://github.com/baskerville/bspwm"
sxhkd_git_dir = "https://github.com/baskerville/sxhkd"
xtitle_git_dir = "https://github.com/baskerville/xtitle"
sutils_git_dir = "https://github.com/baskerville/sutils"
lemonbar_git_dir = "https://github.com/LemonBoy/bar"

#Directories
installer_dir = sys.path[0]

from os.path import expanduser
home = expanduser("~")

tmp_dir = "/tmp/bspwm_installer/"

config_dir = "%s/.config" %home
bspwm_scripts_dir = "%s/.config/bspwm/" %home
sxhkd_scripts_dir = "%s/.config/sxhkd/" %home
wallpapers_dir = "%s/wallpapers" %config_dir
bspwmrc_dir = "bspwm/examples/bspwmrc"
sxhkdrc_dir = "bspwm/examples/sxhkdrc"
xinitrc_dir = "%s/.xinitrc" %home

#Strings
xinitrc_exec_bspwm = "sxhkd &\nexec bspwm"

#Package Managers
arch_pm = "pacman -S"
debian_pm = "apt-get install"

#Makes directory (d) if it does not exist
def mkdir(d):
    if not os.path.exists(d):
        os.makedirs(d)

def end_install():
    print "Installation Complete."
    cleanup()
    print "Exiting..."
    sys.exit()

def cleanup():
    #Cleanup Files
    print "Cleaning Up...",  
    os.system("rm -rf %s" %tmp_dir)
    print "Done"

def replace_text(file,search_text,replace_text):
    for line in fileinput.FileInput(file, inplace=1):
        if search_text in line:
            line = line.replace(search_text,replace_text)
            sys.stdout.write(line)

def find_string(file, search_str):
    for line in fileinput.FileInput(file, inplace=1):
    	if search_str in line:
		fileinput.close()
        	return 1
    fileinput.close()
    return 0    

def set_bg(distro):
    with open("%s/bspwmrc" %bspwm_scripts_dir, "a") as bspwmrc_file:
        bspwmrc_file.write("\nfeh --bg-fill %s/wallpapers/%s.jpg &\n" %(config_dir, distro))

def write_string_to_file(file_loc, write_str):
	string_exists = 0
	search_str = write_str.split('\n') #split up multi line strings to ease searching
	if os.path.isfile('%s' %file_loc):
		with open('%s' %file_loc, 'r') as xinitrc:
			#make sure the given string does not already exist in the file
			for line in xinitrc:		
				if "%s" %search_str[0] in line:
					string_exists = 1
	#append string to file
	with open('%s' %file_loc, 'a') as xinitrc:
		if not string_exists:
			xinitrc.write("\n%s\n" %write_str)

print ("\nBSPWM Installer v0.1 \n"
       "Chris Wilson - 2015  \n")

#Attempt to detect distro
distro = platform.dist()
#distro = platform.linux_distribution()
#distro = os.system("uname -v")

#NOTE - This is untested
if distro == ("Debian", "*", "*"):
    distro = "debian"
elif distro == ("Arch", "*", "*"):
    distro = "arch"
elif distro == ("Ubuntu", "*", "*"):
    distro = "ubuntu"
else:
    print "OS Autodetect Failed!"
    pick_distro = input("Please Select Distribution\n"
                        "1.) Debian\n"
                        "2.) Arch\n"
                        "3.) Ubuntu\n"
                        "4.) Other\n"
                        "> ")
    if pick_distro == 1:
        distro = "debian"
    elif pick_distro == 2:
        distro = "arch"
    elif pick_distro == 3:
        distro = "ubuntu"
    else:
        distro = "linux"

#Download dependencies
print "Downloading Dependencies..."
if pick_distro == 1: #'-qq' quiet
    os.system("sudo %s gcc git make libasound2 libasound2-dev xcb libxcb-util0-dev "
              "libxcb-ewmh-dev libxcb-randr0-dev libxcb-icccm4-dev "
              "libxcb-keysyms1-dev libxcb-xinerama0-dev xorg "
              "suckless-tools rxvt-unicode feh" %debian_pm)
elif pick_distro == 2:
    os.system("sudo %s libxcb xcb-util xcb-util-keysyms "
              "xcb-util-wm" %arch_pm)
print "Download Complete!\n"
        
#Make dir for temp files
print "Initializing Temporary Directory...",
mkdir(tmp_dir)
os.chdir(tmp_dir)
print "Done."

#Get source files via git
print "Downloading Source..."
os.system("git clone %s" %bspwm_git_dir);

# There is a bug with the current bspwm build that throws
# an Xserver connection error on some distros when using 
# Make. This workaround checks out an older version.
os.system("cd bspwm && git checkout b0e8dd3 && cd ..")

os.system("git clone %s" %sxhkd_git_dir);
print "Download Complete!\n"

#Build Source
print "Building Source..."
os.system("make -C bspwm/ && sudo make -C bspwm/ install")
os.system("make -C sxhkd/ && sudo make -C sxhkd/ install")
print "Build Complete!\n"

#Deploy Files to System
print "Deploying System...",

#make dirs for config files
mkdir(config_dir)
mkdir(bspwm_scripts_dir)
mkdir(sxhkd_scripts_dir)

#copy in bspwm configs
#shutil.copy(bspwmrc_dir, bspwm_scripts_dir)
os.system("cp %s %s" %(bspwmrc_dir, bspwm_scripts_dir))
os.system("cp %s %s" %(sxhkdrc_dir, sxhkd_scripts_dir))

#make bspwmrc executable
os.system("chmod +x %s" %bspwmrc_dir)

#write exec script to ~/.xinitrc 
write_string_to_file(xinitrc_dir, xinitrc_exec_bspwm)
  
sys.exit()
print "Done\n"

#Set Background
print "Setting Background...",
mkdir("%s/wallpapers" %config_dir)
#TODO - change this to only copy distro WP
os.system("cp %s/wallpapers/* %s" %(installer_dir, wallpapers_dir))

set_bg(distro)
print "Done\n"

print "BSPWM Installed Successfully!\n"

end_install()
