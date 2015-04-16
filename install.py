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

#Source URLs
bspwm_git_dir = "https://github.com/baskerville/bspwm"
sxhkd_git_dir = "https://github.com/baskerville/sxhkd"
xtitle_git_dir = "https://github.com/baskerville/xtitle"
sutils_git_dir = "https://github.com/baskerville/sutils"
lemonbar_git_dir = "https://github.com/LemonBoy/bar"

#Directories
config_dir = "~/.config"
panel_scripts_dir = "~/.config/panel/"
bspwm_scripts_dir = "~/.config/bspwm/"
sxhkd_scripts_dir = "~/.config/sxhkd/"
bspwmrc_dir = "bspwm/examples/bspwmrc"
sxhkdrc_dir = "bspwm/examples/sxhkdrc"
panel_config_dir = "bspwm/examples/panel/"
panel_fifo = "/tmp/panel-fifo/"
tmp_dir = "/tmp/bspwm_installer/"

#Package Managers
arch_pm = "pacman -S"
debian_pm = "apt-get install"

#Makes file (d) if it does not exist
def mkdir(d):
    if not os.path.exists(d):
        os.makedirs(d)

print (" BSPWM Installer v0.1 \n"
       " Chris Wilson - 2015  \n")

pico_distro = input("Select Distribution\n"
                    "1.) Debian\n"
                    "2.) Arch)"

pick_panel = input("Select panel:\n"
                   "1.) None\n"
                   "2.) LemonBar")




#Download dependencies
print "Downloading Dependencies..."
if pick_distro == 1: #'-qq' quiet
    os.system("sudo %s gcc git make libasound2 xcb libxcb-util0-dev "
         	  "libxcb-ewmh-dev libxcb-randr0-dev libxcb-icccm4-dev "
	          "libxcb-keysyms1-dev libxcb-xinerama0-dev" debian_pm)
else if pick_distro == 2:
    os.system("sudo %s libxcb xcb-util xcb-util-keysyms "
              "xcb-util-wm" arch_pm)
print "Download Complete!\n"
        
sys.exit()        

#Make dir for temp files
print "Initializing Temporary Directory..."
mkdir(tmp_dir)
os.chdir(tmp_dir)

#Get source files via git
print "Downloading Source..."
os.system("git clone %s" %bspwm_git_dir);

# There is a bug with the current bspwm build that throws
# an Xserver connection error on some distros when using 
# Make. This workaround checkouts and older version.
os.system("cd bspwm && git checkout b0e8dd3 && cd ..")

os.system("git clone %s" %sxhkd_git_dir);
#git Panel Source Files
#os.system("git clone %s" %xtitle_git_dir);
#os.system("git clone %s" %sutils_git_dir);
#os.system("git clone %s" %lemonbar_git_dir);
print "Download Complete!\n"

#Build Source
print "Building Source..."
os.system("make -C bspwm/ && sudo make -C bspwm/ install")
os.system("make -C sxhkd/ && sudo make -C sxhkd/ install")

#Build Panel Source
#os.system("make -C sutils/ && sudo make -C sutils/ install")
#os.system("make -C xtitle/ && sudo make -C xtitle/ install")
#os.system("make -C bar/ && sudo make -C bar/ install")
print "Build Complete!\n"

#Deploy Files to System
print "Deploying System..."

#make dirs for config files
mkdir(config_dir)
mkdir(bspwm_scripts_dir)
mkdir(sxhkd_scripts_dir)
#mkdir(panel_scripts_dir)
#mpdir(panel_fifo_dir)

#copy in bspwm configs
#shutil.copy(bspwmrc_dir, bspwm_scripts_dir)
os.system("cp %s %s" %(bspwmrc_dir, bspwm_scripts_dir))
os.system("cp %s %s" %(sxhkdrc_dir, sxhkd_scripts_dir))

#copy in panel configs
#os.system("cp %s/panel %s/panel" %(panel_config_dir, panel_scripts_dir))
#os.system("cp %s/panel_bar %s/panel_bar" %(panel_config_dir, panel_scripts_dir))
#os.system("cp %s/panel_color %s/panel_color" %(panel_config_dir, panel_scripts_dir))    

#make bspwmrc executable
os.system("chmod +x %s" bspwmrc_dir)

#make panel & panel_bar execuatable
#os.system("chmod +x %s/panel %s/panel_bar")

# Bar changed its name to lemonbar. This does not yet show 
# in the default panel config and needs to be changed


#Set Environment Variables
#os.eviron["PATH"] += os.pathsep + panel_scripts_dir
#os.eviron["PANEL_FIFO"] = panel_fifo_path

#make/update file .xinitrc
with file.open(name, '~/.initrc') as init_file
    initfile.write("sxhkd\n & exec bspwm")
print "System Deployment Complete!\n"

#Cleanup Files
print "Cleaning Up..."
os.system("rm -rf %s" %tmp_dir)
print "Cleanup Complete.\n"

print "BSPWM is now installed!"
