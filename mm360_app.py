#!/usr/bin/python

import sys, getopt, os
import mm360_face_reader as mm360
#sys.path.append('./Code')
import Spotify_Query as sq
import webbrowser
import platform

#################
# Usage syntax
#################
def usage():
	os.system('clear')
	print("=== WELCOME TO MYMUSIC360 ===\n")
	print('Usage: python mm360_app.py [--help | --load-learn <personGroupId> | --my_music <personGroupId> --root_folder <image_root_folder> --pic <picture>]')
	print('Or')
	print('mm360_app.py [-h | -l <personGroupId> | -m  <personGroupId> | -f <image_root_folder> -p <picture>]')
	print('\nNOTE OF CAUTION::\n')
	print('before running --load-learn, please setup all the folders properly: ')
	print('setup folder <group_pictures>')
	print('subfolders, one fore each person, group_pictures/<sub-folders>')
	print('Lastly, load the training pictures for persons under the appropriate subfolders')
	print('After setup in complete,')
	print('run load-learn first')
	print('usage: python ./mm360_app.py --load-learn')
	print('Now you are all set to enjoy MyMusic, by running, ')
	print('usage: python ./mm360_app.py --my_music')
	print(f"mm360_app assumes default root folder ./group_pictures ")
	print(f"To override the default root_folder use, --root_folder option")
	print(f"To use a static saved pic instead of a realtime pic,")
	print(f"Use the -p <picture> or --pic <picture> option.")

#################
# Main 
#################
def main(argv):
    os_name = platform.platform()
    if(os_name.split('-')[0] == 'Windows'):
        print(f"Running in Windows")
        chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
    elif(os_name.split('-')[0] == 'Darwin'): # os == Mac
        print(f"Running in Mac")
        chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
    else: #(os == Linux)
        print(f"Running in Linux")
        # chrome_path = '/usr/bin/google-chrome %s'
    
    print(f"Chrome Path = {chrome_path}")
    
    load_learn = False
    my_music = False
    personGroupId = ''
    root_folder = './group_pictures'
    picToUse = ''
    new_face_for = ''
    user_data = {}

    try:
        opts, args = getopt.getopt(argv,"hf:l:m:p:n:",["help", "root_folder=", "load-learn=", "my_music=", "pic=", "new_face_for="])
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
        elif opt in ("-n", "--new_face_for"):
            val = arg.split(':')
            if(len(val) != 2):
                print(f"new_face_for, arguments not set correctly = {len(val)}")
                sys.exit()
            personGroupId = val[0]
            new_face_for = val[1]
        else:
            usage()
            sys.exit()

    print(f"load_learn = {load_learn}")
    print(f"music-begin = {my_music}")
    print(f"personGroupId = {personGroupId}")
    print(f"Root Folder = {root_folder}")
    print(f"Picture = {picToUse}")
    print(f"new_face_for = {new_face_for}")

    print("--- Starting to Process ---")

    if load_learn:
        print(f"loadGroupImages({root_folder},{personGroupId})")
        mm360.loadGroupImages(root_folder, personGroupId)
    elif my_music:
        print(f"handleMM_User({personGroupId})")
        if (picToUse != ''):
            print(f"Picture = {picToUse}")
            user_data = mm360.handleMM_User(personGroupId, picToUse)
            print(f" USER_DATA = {user_data}, calling sq.get_song_for_mood()")
            song_url = sq.get_song_for_mood(user_data['userCurrentMood'],None)
            print(f"Playing song {song_url['Song URI']}")
            webbrowser.get(chrome_path).open(song_url['Song URI'])
        else:
            user_data = mm360.handleMM_User(personGroupId)
            print(f" USER_DATA = {user_data}, calling sq.get_song_for_mood()")
            song_url = sq.get_song_for_mood(user_data['userCurrentMood'],None)
            print(f"Playing song {song_url['Song URI']}")
            webbrowser.get(chrome_path).open(song_url['Song URI'])
    elif new_face_for != '':
        print(f"Loading new picture = [{picToUse}], for [{new_face_for}] in group [{personGroupId}]")
        user_data = mm360.addFaceToExistingPerson(picToUse, personGroupId, new_face_for)
        print(f" USER_DATA = {user_data}, calling sq.get_song_for_mood()")
        song_url = sq.get_song_for_mood(user_data['userCurrentMood'],None)
        print(f"Playing song {song_url['Song URI']}")
        webbrowser.get(chrome_path).open(song_url['Song URI'])

    
#################
# Starting Point
#################
if __name__ == "__main__":
	
	main(sys.argv[1:])

	print("COMPLETED!")





