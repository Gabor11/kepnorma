import os
import sys

# these statements and commands ensure that a folder is given to the script
if len(sys.argv) < 2:
    print("Nem adtad meg a letöltött képeket tartalmazó mappát. Kilépek.")
    quit()

if not os.path.isdir(sys.argv[1]):
    print("A megadott hivatkozás nem egy mappára mutat.\nA letöltött képeket tartalmazó mappát kérem megadni.")
    quit()

if len(sys.argv) > 4:
    print("Túl sok paramétert adtál meg. Kilépek.")
    quit()

# this library contains the necessary functions and global variables e.g. "rootFolder"
import kepnormalib as klib

# taking care of arguments if there are 3 or 4 of them
# and setting 'arg2' and 'arg3' 
# -> order in the command line is irrelevant
# the script decides based on the content 
# which parameter they are about
arg2 = "empty"
arg3 = "empty"
if len(sys.argv) == 3:
    arg2 = sys.argv[2]

klib.setBothFilterAndGroupingParamCorrectly(arg2, arg3)

if len(sys.argv) == 4:
    arg2 = sys.argv[2]
    arg3 = sys.argv[3]
    if (not klib.setBothFilterAndGroupingParamCorrectly(arg2, arg3)):
        print("Nem megfelelő paramétereket adtál meg. Kilépek.")
        quit()

# printing banner
klib.printKepnormaBanner()
# converting HEIC to JPG
klib.folderSweeperHEIC2JPG(klib.rootFolder)
# collecting info regarding event names and dates
klib.folderSweeper(klib.rootFolder, "")
klib.checkIfPicturesWithNoDateExist()
# creating standard folder structure with resized pictures
klib.createStandardStructure()


