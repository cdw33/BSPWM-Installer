##################################################
#                                                #
#            BSPWM Installation Script           #
#                                                #
#               Chris Wilson - 2015              #
#                                                #
##################################################

import os
import sys #used for sys.exit() in debugging

bspwm_git_dir = "https://github.com/baskerville/bspwm"
sxhkd_git_dir = "https://github.com/baskerville/sxhkd"
xtitle_git_dir = "https://github.com/baskerville/xtitle"
sutils_git_dir = "https://github.com/baskerville/sutils"
lemonbar_git_dir = "https://github.com/LemonBoy/bar"

panel_scripts_dir = "~/.config/panel"
bspwm_scripts_dir = "~/.config/bspwm"
sxkhd_scripts_dir = "~/.config/sxkhd"

tmp_dir = "/tmp/bspwm_installer"

def mkdir(d):
    if not os.path.exists(d):
        os.makedirs(d)

print "\nBSPWM Installer v0.1"
print "Chris Wilson - 2015\n"

#Check necessary parameters are met
#check for git && make && gcc (build-essential(?))


#make directory for temp files
mkdir(tmp_dir)
os.chdir(tmp_dir)

#get source files via git
print "Downloading Source..."
os.system("git clone %s" %bspwm_git_dir);
#this is a bug with the current bspwm build that causes 
#an xserver connection error on Make. This is fixed by 
#checking out a previous version
os.system("cd bspwm && git checkout b0e8dd3 && cd ..")
os.system("git clone %s" %sxhkd_git_dir);
os.system("git clone %s" %xtitle_git_dir);
os.system("git clone %s" %sutils_git_dir);
os.system("git clone %s" %lemonbar_git_dir);
print "Download Complete\n"

#Download any necessary dependencies
print "Downloading Dependencies..."
##add -qq for quiet install
os.system("sudo apt-get install libasound2 xcb libxcb-util0-dev"
     	  " libxcb-ewmh-dev libxcb-randr0-dev libxcb-icccm4-dev"
	      " libxcb-keysyms1-dev libxcb-xinerama0-dev")
print "Download Complete\n"

#Use make to build source
print "Building Source..."
os.system("make -C bspwm/ && sudo make -C bspwm/ install")
os.system("make -C sxhkd/ && sudo make -C sxhkd/ install")
os.system("make -C xtitle/ && sudo make -C sutils/ install")
os.system("make -C bspwm/ && sudo make -C bspwm/ install")
os.system("make -C bar/ && sudo make -C bar/ install")
print "Build Complete\n"

#move files to thier final location &
#edit necessary files accoringly
print "Deploying System..."
#~/.config/panel/panel,panel_bar, panel_colors
#~/.config/bspwm/bspwm
#~/.config/sxhkd/sxhkdrc

#edit $PATH to include panel location
#add PANEL_FIFO=/tmp/panel_fifo to /etc/profile(?)
print "System Deploymen Complete\n"


#cleanup my mess
#os.rmdir("tmp") //file not empty (shutil.rmtree?)
print "Cleaning Up..."
os.system("rm -rf %s" %tmp_dir)
print "Cleanup Complete.\n"
print "BSPWM is now installed!"
