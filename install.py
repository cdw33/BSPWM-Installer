##################################################
#                                                #
#            BSPWM Installation Script           #
#                                                #
#               Chris Wilson - 2015              #
#                                                #
##################################################

import os
#import shutil
import sys #used for sys.exit() in debugging
import subprocess

##File Directories
bspwm_git_dir = "https://github.com/baskerville/bspwm"
sxhkd_git_dir = "https://github.com/baskerville/sxhkd"
xtitle_git_dir = "https://github.com/baskerville/xtitle"
sutils_git_dir = "https://github.com/baskerville/sutils"
lemonbar_git_dir = "https://github.com/LemonBoy/bar"

config_dir = "~/.config"
panel_scripts_dir = "~/.config/panel/"
bspwm_scripts_dir = "~/.config/bspwm/"
sxhkd_scripts_dir = "~/.config/sxhkd/"

bspwmrc_dir = "bspwm/examples/bspwmrc"
sxhkdrc_dir = "bspwm/examples/sxhkdrc"
panel_config_dir = "bspwm/examples/panel/"
panel_fifo_dir = "/tmp/panel-fifo/"

tmp_dir = "/tmp/bspwm_installer/"

arch_pm = "sudo pacman -S"
debian_pm = "sudo apt-get install"


def mkdir(d):
    if not os.path.exists(d):
        os.makedirs(d)

print "\nBSPWM Installer v0.1"
print "Chris Wilson - 2015\n"

#Download any necessary dependencies
print "Downloading Dependencies..."
##add -qq for quiet install (except errors)
os.system("sudo apt-get install gcc git make libasound2 xcb libxcb-util0-dev"
     	  " libxcb-ewmh-dev libxcb-randr0-dev libxcb-icccm4-dev"
	      " libxcb-keysyms1-dev libxcb-xinerama0-dev")
print "Download Complete\n"
        
sys.exit()        

#make directory for temp files
print "Initializing Temporary Directory..."
mkdir(tmp_dir)
os.chdir(tmp_dir)

#get source files via git
print "Downloading Source..."
os.system("git clone %s" %bspwm_git_dir);
# There is a bug with the current bspwm build that causes 
# an Xserver connection error when using Make. The current
# workaround is by checking out and older version
os.system("cd bspwm && git checkout b0e8dd3 && cd ..")
os.system("git clone %s" %sxhkd_git_dir);
#git Panel Source Files
#os.system("git clone %s" %xtitle_git_dir);
#os.system("git clone %s" %sutils_git_dir);
#os.system("git clone %s" %lemonbar_git_dir);
print "Download Complete\n"

#Use make to build source
print "Building Source..."
os.system("make -C bspwm/ && sudo make -C bspwm/ install")
os.system("make -C sxhkd/ && sudo make -C sxhkd/ install")
#Build Panel Source
#os.system("make -C xtitle/ && sudo make -C sutils/ install")
#os.system("make -C bspwm/ && sudo make -C bspwm/ install")
#os.system("make -C bar/ && sudo make -C bar/ install")
print "Build Complete\n"

#Deploy Files to System
print "Deploying System..."
#~/.config/panel/panel,panel_bar, panel_colors
#~/.config/bspwm/bspwm
#~/.config/sxhkd/sxhkdrc
#edit $PATH to include panel location
#add PANEL_FIFO=/tmp/panel_fifo to /etc/profile(?)
mkdir(config_dir)
mkdir(bspwm_scripts_dir)
mkdir(sxhkd_scripts_dir)
#mkdir(panel_scripts_dir)
#mpdir(panel_fifo_dir)

#shutil.copy(bspwmrc_dir, bspwm_scripts_dir)
os.system("cp %s %s" %(bspwmrc_dir, bspwm_scripts_dir))
os.system("cp %s %s" %(sxhkdrc_dir, sxhkd_scripts_dir))
#os.system("cp %s/panel %s/panel" %(panel_config_dir, panel_scripts_dir))
#os.system("cp %s/panel_bar %s/panel_bar" %(panel_config_dir, panel_scripts_dir))
#os.system("cp %s/panel_color %s/panel_color" %(panel_config_dir, panel_scripts_dir))    
print "System Deployment Complete\n"

#Cleanup Files
#os.rmdir("tmp") //file not empty (shutil.rmtree?)
print "Cleaning Up..."
os.system("rm -rf %s" %tmp_dir)
print "Cleanup Complete.\n"

print "BSPWM is now installed!"
