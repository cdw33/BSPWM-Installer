import os

xinitrc = "/home/chris/Development/.xinitrc"
xinitrc_str = "sxhkd &\nexec bspwm"


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


write_string_to_file(xinitrc, xinitrc_str)
