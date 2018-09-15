#!/usr/bin/python

import sys, getopt, os
import mm360_face_reader as mm360
#################
# Usage syntax
#################
def usage():
	os.system('clear')
	print("=== WELCOME TO MYMUSIC360 ===\n")
	print('Usage: python mm360_face_reader.py [--help | --load-learn <personGroupId> | --my_music <personGroupId> --root_folder <image_root_folder> --pic <picture>]')
	print('Or')
	print('mm360_face_reader.py [-h | -l <personGroupId> | -m  <personGroupId> | -f <image_root_folder> -p <picture>]')
	print('\nNOTE OF CAUTION::\n')
	print('before running --load-learn, please setup all the folders properly: ')
	print('setup folder <group_pictures>')
	print('subfolders, one fore each person, group_pictures/<sub-folders>')
	print('Lastly, load the training pictures for persons under the appropriate subfolders')
	print('After setup in complete,')
	print('run load-learn first')
	print('usage: python ./mm360_face_reader.py --load-learn')
	print('Now you are all set to enjoy MyMusic, by running, ')
	print('usage: python ./mm360_face_reader.py --my_music')
	print(f"mm360_face_reader assumes default root folder ./group_pictures ")
	print(f"To override the default root_folder use, --root_folder option")
	print(f"To use a static saved pic instead of a realtime pic,")
	print(f"Use the -p <picture> or --pic <picture> option.")

#################
# Main 
#################
def main(argv):
	load_learn = False
	my_music = False
	personGroupId = ''
	root_folder = './group_pictures'
	picToUse = ''
	
	try:
		opts, args = getopt.getopt(argv,"hf:l:m:p:",["help", "root_folder=", "load-learn=", "my_music=", "pic="])
		if(len(opts) == 0):
			usage()
			sys.exit()
	except getopt.GetoptError as e:
		print(f"{e}")
		# usage()
		sys.exit(2)

	for opt, arg in opts:
		if opt in ("-h" , "--help"):
			usage()
			sys.exit()
		elif opt in ("-l", "--load-learn"):
			load_learn = True
			personGroupId = arg
		elif opt in ("-m", "--my_music"):
			my_music = True
			personGroupId = arg
		elif opt in ("-f", "--root_folder"):
			root_folder = arg
		elif opt in ("-p", "--pic"):
			picToUse = arg
		else:
			usage()
			sys.exit()

	print(f"load_learn = {load_learn}")
	print(f"music-begin = {my_music}")
	print(f"personGroupId = {personGroupId}")
	print(f"Root Folder = {root_folder}")
	print(f"Picture = {picToUse}")

	print("--- Starting to Process ---")

	if load_learn:
		print(f"loadGroupImages({root_folder},{personGroupId})")
		mm360.loadGroupImages(root_folder, personGroupId)
	elif my_music:
		print(f"handleMM_User({personGroupId})")
		if (picToUse != ''):
			print(f"Picture = {picToUse}")
			mm360.handleMM_User(personGroupId, picToUse)
		else:
			mm360.handleMM_User(personGroupId)

#################
# Starting Point
#################
if __name__ == "__main__":
	
	main(sys.argv[1:])

	print("COMPLETED!")





