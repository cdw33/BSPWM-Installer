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
panel_scripts_dir = "%s/.config/panel" %home
bspwm_scripts_dir = "%s/.config/bspwm/" %home
sxhkd_scripts_dir = "%s/.config/sxhkd/" %home
wallpapers_dir = "%s/wallpapers" %config_dir
bspwmrc_dir = "%s/bspwm/examples/bspwmrc" %tmp_dir
sxhkdrc_dir = "%s/bspwm/examples/sxhkdrc" %tmp_dir
panel_config_dir = "bspwm/examples/panel"
panel_fifo_dir = "/tmp/panel-fifo/"

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
	    return 1
    return 0	

def set_bg(distro):
    with open("%s/bspwmrc" %bspwm_scripts_dir, "a") as bspwmrc_file:
        bspwmrc_file.write("feh --bg-fill %s/wallpapers/%s.jpg &\n" %(config_dir, distro))

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
        
#Make dir for temp files
print "Initializing Temporary Directory...",
mkdir(tmp_dir)
os.chdir(tmp_dir)
print "Done."

install_panel = raw_input("Would you like to install a panel? (y/n) ")
if install_panel != "y":
    end_install()  
    
print("Select panel:\n"
      "1.) LemonBar")
pick_panel = raw_input("> ")

#Download dependencies
print "Downloading Source..."
os.system("git clone %s" %bspwm_git_dir);
os.system("git clone %s" %xtitle_git_dir);
os.system("git clone %s" %sutils_git_dir);
os.system("git clone %s" %lemonbar_git_dir);
print "Download Complete!\n"

print "Building Source...",
os.system("make -C sutils/ && sudo make -C sutils/ install")
os.system("make -C xtitle/ && sudo make -C xtitle/ install")
os.system("make -C bar/ && sudo make -C bar/ install")
print "Done\n"
print "Deploying System...",
mkdir(panel_scripts_dir)
mkdir(panel_fifo_dir)

os.system("cp %s/panel %s/panel" %(panel_config_dir, panel_scripts_dir))
os.system("cp %s/panel_bar %s/panel_bar" %(panel_config_dir, panel_scripts_dir))
os.system("cp %s/panel_colors %s/panel_colors" %(panel_config_dir, panel_scripts_dir))  

#make panel & panel_bar execuatable
os.system("chmod +x %s/panel %s/panel_bar" 
        %(panel_scripts_dir, panel_scripts_dir))

#If we built the older version of bspwm to workaround the xserver bug,
#we need to update the default sxhkdrc to launch 'lemonbar' instead of 'bar'
replace_text("%s/panel" %panel_scripts_dir, " bar ", " lemonbar ")


#Start panel with bspwm
with open("%s/bspwmrc" %bspwm_scripts_dir, "a") as bspwmrc_file:
        bspwmrc_file.write("panel &\n")

#Set Environment Variables
#os.eviron["PATH"] += os.pathsep + panel_scripts_dir
#os.eviron["PANEL_FIFO"] = panel_fifo_path
with open("%s/.profile" %home, "a") as profile_file:
#    if not find_string("%s/.profile" %home,"PANEL_FIFO"):
    profile_file.write("export PATH=$PATH:%s\n"
	               "export PANEL_FIFO=$PANEL_FIFO%s"
                       %(panel_scripts_dir, panel_fifo_dir))

#update envars
os.system("source %s/.profile" %home)
print "Done\n"

print "Panel Sucessfully Installed!"

#TODO - get current term from sxhkdrc
print "The current default terminal is urxvt."
install_panel = raw_input("Would you like to install a different terminal? (y/n) ")
if install_panel != "y":
    end_install()

pick_term = input("Select Terminal for Installation:\n"
                        "1.) xterm\n"
                        "2.) zsh\n"
                        "3.) xfce\n"
                        "4.) rxvt\n"
                        "> ")

#TODO - make this work for other distros
if pick_term == 1:
    os.system("sudo %s xterm" %debian_pm)
elif pick_term ==2:
    os.system("sudo %s zsh" %debian_pm)
elif pick_term == 3:
    os.system("sudo %s xfce" %debian_pm)
elif pick_term == 4:
    os.system("sudo %s rxvt" %debian_pm)
else:    
    end_install()

#Modify sxhkd to use new terminal
#TODO - make func to do this and call above

end_install()
