
import os
import sys
import datetime
import re
import keyboard
import shutil
import cv2
import math
import platform
import subprocess
import config

# globals
fi = config.fi
targetFolder = config.targetFolder
bigPicFolder = config.bigPicFolder
rootFolder = sys.argv[1]
heicProcessed = 0 # number of heic files that has been converted to jpg

# these two varuiables will be sometimes overwritten
# by the 'setBothFilterAndGroupingParamCorrectly' function
# according to the parameters given by users
monthFilter = False
monthlyGrouping = False
    
# fix globals (not expected to be changed after the start of the script
# nor by a user beforehand)
regRootFolder = re.sub('\\' + os.path.sep, '_', rootFolder)
regDate = r'(20\d{2}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))'
thisyear = datetime.date.today().year
lastyear = thisyear - 1
folderRecords = list()
noDateFolders = list()


if (platform.system() == "Windows"):
    imagemagick = "magick"
    clearScreen = "cls"
elif (platform.system() == "Linux"):
    clearScreen = "clear"
    imagemagick = "convert"

#######BANNER#############
Banner = [
' __   ___  ___||__    _______   _____  ___      ______     _______   ___      ___       __      ',
'|/"| /  ")/"  || "|  |   __ "\\ (\\"   \\|"  \\    /    " \\   /"      \\ |"  \\    /"  |     /""\\     ',
'(: |/   /(: ______)  (. |__) :)|.\\\\   \\    |  // ____  \\ |:        | \\   \\  //   |    /    \\    ',
'|    __/  \\/    |    |:  ____/ |: \\.   \\   | /  /    ) :)|_____/   ) /\\\\  \\/.    |   /\' /\\  \\   ',
'(// _  \\  // ___)_   (|  /     |.  \\    \\. |(: (____/ //  //      / |: \\.        |  //  __\'  \\  ',
'|: | \\  \\(:      "| /|__/ \\    |    \\    \\ | \\        /  |:  __   \ |.  \    /:  | /   /  \\\\  \\ ',
'(__|  \\__)\\_______)(_______)    \\___|\\____\\)  \\"_____/   |__|  \\___)|___|\\__/|___|(___/    \\___)'
]
# Displaying the letters
def printKepnormaBanner():
    for row in Banner:
        print(row)

# this function sets 'monthFilter' and 'monthlyGrouping' global variables
# based on the user parameters. 
# it returns 'False' if not both parameters are correctly set
# this return value helps later combined with the number of terminal parameters
# to decide if we have a failure with the user parameters
def setBothFilterAndGroupingParamCorrectly(arg2, arg3):
    global monthFilter
    global monthlyGrouping
    # the next several lines puts two month-like digit into the 'monthFilter' variable
    # or 'False' if the initial input was incorrect
    # e.g.: '-1' -> '01' (- January), '-2' -> '02' (- February), '-13' -> 'False' -> etc 
    if (re.match('^-([1-9]|1[012])$', arg2)):
        monthFilter = re.match('^-([1-9]|1[012])$', arg2).group()[1:].zfill(2)
    elif (re.match('^-([1-9]|1[012])$', arg3)):
        monthFilter = re.match('^-([1-9]|1[012])$', arg3).group()[1:].zfill(2)
    else:
        monthFilter = False

    if (re.match('^--havicsopi$', arg2)):
        monthlyGrouping = True
    elif (re.match('^--havicsopi$', arg3)):
        monthlyGrouping = True
    else:
        monthlyGrouping = False

    if (monthFilter and monthlyGrouping):
        return True
    else:
        return False

def extractTitleAndDate(folderName):
    filteredTitle = filterTitleWithDateRemains(folderName)
    return separateTitleAndDateFromFilteredTitle(filteredTitle)

# this function gets the MONTH out of a date string
def extractMonth(dateStr):
    return dateStr[4:6]

# this function gets the YEAR out of a date string
def extractYear(dateStr):
    return dateStr[:4]

# this function gives us an alternative date for the containing folder 
# when used in aggregate mode (i.e. all dates grouped into one month)
def getAlterDate(year, month):
    if month == "01":
        return year + '0131'
    elif month == "02" and int(year) % 4 == 0:
        return year + '0229'
    elif month == "02":
        return year + '0228'
    elif month == "03":
        return year + '0331'
    elif month == "04":
        return year + '0430'
    elif month == "05":
        return year + '0531'
    elif month == "06":
        return year + '0630'
    elif month == "07":
        return year + '0731'
    elif month == "08":
        return year + '0831'
    elif month == "09":
        return year + '0930'
    elif month == "10":
        return year + '1031'
    elif month == "11":
        return year + '1130'
    elif month == "12":
        return year + '1231'
 
# this function changes the path seperators to a "_" character
# and removes various substrings from 'folderName'
def filterTitleWithDateRemains(folderName):
    retitle = re.sub('\\' + os.path.sep, '_', folderName)
    subreg = '^' + regRootFolder
    retitle = re.sub(subreg , '', retitle, flags=re.IGNORECASE)
    subreg = fi + '_' + str(thisyear) + '_'
    retitle = re.sub(subreg , '', retitle, flags=re.IGNORECASE)
    subreg = fi + '_' + str(thisyear) + "(?!(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"
    retitle = re.sub(subreg , '', retitle, flags=re.IGNORECASE)
    subreg = fi + '_' + str(lastyear) + '_'
    retitle = re.sub(subreg , '', retitle, flags=re.IGNORECASE)
    subreg = fi + '_' + str(lastyear) + "(?!(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))"
    retitle = re.sub(subreg , '', retitle, flags=re.IGNORECASE)
    subreg = fi + '_'
    retitle = re.sub(subreg , '', retitle, flags=re.IGNORECASE)
    return retitle

def separateTitleAndDateFromFilteredTitle(filteredTitle):
    # accepted date format: YYYYMMDD (stored in 'regDate')
    x = re.findall(regDate, filteredTitle)
    dateStr = ''
    if x:
        # we need to get the last occurence and since the regex expression
        # is wrapped in groups we need to address the zeroth item
        # in its list
        dateStr = x[-1][0]
        # yyyymmdd-like substrings will be eliminated
        x = re.search(regDate, filteredTitle)
        while (x):
            filteredTitle = re.sub('_' + x.group() , '', filteredTitle)
            filteredTitle = re.sub(x.group() , '', filteredTitle)
            x = re.search(regDate, filteredTitle)        
    return [filteredTitle, dateStr]

# this function loops through the folder structure that is given to it
# and it saves the important data (in order to construct the standard folder and file structure)
# 'folderRecords' and (if needed) 'noDateFolders' lists are populated
def folderSweeper(folder, startDate):
    global folderRecords
    [title, date] = extractTitleAndDate(folder)
    date = date if date != "" else startDate
    filecounter = 0
    for name in os.scandir(folder):
        if name.is_dir():
            folderSweeper(os.path.join(folder, name.name), date)
        if name.is_file():
            isJpg = re.search(".jpg$", name.name, re.IGNORECASE)
            isJpeg = re.search(".jpeg$", name.name, re.IGNORECASE)
            if date:
                if isJpg or isJpeg:
                    filecounter += 1
                    if {"date": date , "event": title, "folder": folder, "multidates": False, "filecounter":filecounter-1} in folderRecords:
                        i = folderRecords.index({"date": date , "event": title, "folder": folder, "multidates": False, "filecounter":filecounter-1})
                        folderRecords = folderRecords[:i] + [{"date": date , "event": title, "folder": folder, "multidates": False, "filecounter":filecounter}] + folderRecords[i+1:]
                    else:
                        folderRecords.append({"date": date , "event": title, "folder": folder, "multidates": False, "filecounter":filecounter})
            else:
                if isJpg or isJpeg:
                    # initial value (counting the first occurance of such a file)
                    filecounter = 1
                    x = re.search(regDate, name.name)
                    if x:
                        date = x.group()
                        index = indexOfSuchRecordInList({"date": date , "event": title, "folder": folder, "multidates": True}, folderRecords)
                        if not index == -1:
                            filecounter = folderRecords[index]["filecounter"] + 1
                            folderRecords = folderRecords[:index] + [{"date": date , "event": title, "folder": folder, "multidates": True, "filecounter":filecounter}] + folderRecords[index+1:]
                        else:
                            folderRecords.append({"date": date , "event": title, "folder": folder, "multidates": True, "filecounter":filecounter})
                        # 'date' variable needs to be freed up
                        date = ""
                    else:
                        if folder not in noDateFolders:
                            noDateFolders.append(folder)

def folderSweeperHEIC2JPG(folder):
    global heicProcessed
    for name in os.scandir(folder):
        if name.is_dir():
            folderSweeperHEIC2JPG(os.path.join(folder, name.name))
        if name.is_file():
            isHEIC = re.search(".heic$", name.name, re.IGNORECASE)
            if isHEIC:
                subprocess.call(imagemagick + " " + os.path.join(folder, name.name) + " " + os.path.join(folder, name.name)[0:-5] + ".jpg", shell=True)
                heicProcessed += 1
                print("\r {} HEIC fájl átalakítva JPG formátumra.".format(str(heicProcessed)), end='')


def indexOfSuchRecordInList(simpleRecord, actualFolderRecords):
    for record in actualFolderRecords:
        if record["date"] == simpleRecord["date"] and record["event"] == simpleRecord["event"] and record["folder"] == simpleRecord["folder"] and record["multidates"] == simpleRecord["multidates"]:
            return actualFolderRecords.index(record)
    return -1

def checkIfPicturesWithNoDateExist():
    if len(noDateFolders) > 0:
        print('\nA következő mappá(k)ban nem meghatározott dátumú kép található:')
        for folder in noDateFolders:
            print(folder)
        print('Ha szeretnéd ezeket figyelmenkívül hagyva folytatni a folyamatot,')
        print('akkor nyomd meg az "i" vagy az ENTER gombot a billentyűzeten,')
        print('ellenkező esetben megszakad a folyamat.')
        key = keyboard.read_key()
        if key != 'i' and key != 'enter':
            quit()
        else:
            os.system(clearScreen)
            printKepnormaBanner()

def sumFiles2Process():
    sum = 0
    for record in folderRecords:
        sum += record["filecounter"]
    return sum

def checkAndCreateFolder(folder):
    if os.path.isdir(folder) and len(os.listdir(folder)) != 0:
        print('\nA célmappa - "' + folder + '" - nem üres.')
        print('Ha szeretnéd törölni a tartalmát és újra generálni a szabvány szerinti mapparendszert,')
        print('akkor nyomd meg az "i" vagy az ENTER gombot a billentyűzeten,')
        print('ellenkező esetben megszakad a folyamat.')
        key = keyboard.read_key()
        if key != 'i' and key != 'enter':
            quit()
        else:
            os.system(clearScreen)
            printKepnormaBanner()
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(folder, mode=0o777)

def createStandardStructure():
    global folderRecords
    jpgprocessed = 0
    jpgsum = 0
    checkAndCreateFolder(targetFolder)
    if monthFilter:
        filteredRecords = []
        for record in folderRecords:
            if monthFilter == extractMonth(record["date"]):
                filteredRecords.append(record)
        folderRecords = filteredRecords
    jpgsum = sumFiles2Process()
    if len(folderRecords) == 0:
        print("A kiválasztott feltételekkel, a megadott mappában nincs feldolgozható képfájl.")
        quit()
    for record in folderRecords:
        counter = 0
        if monthlyGrouping:
            actualFolder = os.path.join(targetFolder, getAlterDate(extractYear(record["date"]), extractMonth(record["date"])) + '_' + fi)
        else:
            actualFolder = os.path.join(targetFolder, record["date"] + '_' + fi + '_' + record["event"])
        localBigPicFolder = os.path.join(actualFolder, bigPicFolder)
        if not os.path.exists(actualFolder):
            os.mkdir(actualFolder, mode=0o777)
            os.mkdir(localBigPicFolder, mode=0o777)
        elif not monthlyGrouping:
            # if the 'actualFolder' already has been made that means
            # that we probably have already some .jpg files inthere
            # so we need to correct our counter
            counter += offset(localBigPicFolder)
        for file in os.scandir(record["folder"]):
            isJpg = re.search(".jpg$", file.name, re.IGNORECASE)
            isJpeg = re.search(".jpeg$", file.name, re.IGNORECASE)
            dateOK = True if not record["multidates"] else re.search(record["date"], file.name)
            if dateOK and (isJpg or isJpeg):
                counter += 1
                filepath = record["folder"] + os.path.sep + file.name
                shutil.copy2(filepath, localBigPicFolder)
                shutil.move(localBigPicFolder + os.path.sep + file.name, localBigPicFolder + os.path.sep + record["date"] + "_" + fi + "_" + record["event"] + "_" + str(counter).zfill(3) + ".jpg")
    print("¸_______________________________________¸")
    for actualFolder in os.scandir(targetFolder):
        localBigPicFolder = os.path.join(actualFolder, bigPicFolder)
        for pic in os.scandir(localBigPicFolder):
            # printing progress bar
            jpgprocessed += 1
            numberOfHashChar = int(jpgprocessed*20/jpgsum)
            charCountOfPercent = len(str(round(jpgprocessed*100/jpgsum)))
            print("\r|Folyamatban: "+ "#" * numberOfHashChar + " " * (20 - numberOfHashChar) + "|" +"{} %".format(round(jpgprocessed*100/jpgsum)) + " " * (3 - charCountOfPercent) + "|", end='')
            # calling func to create small picture
            makeStandardSmallVersionOfPicture(os.path.join(localBigPicFolder, pic.name), actualFolder)

def offset(actualFolder):
    maxcounter = 0
    for file in os.scandir(actualFolder):
        counter = re.search("(?<=_)\d\d\d", file.name, re.IGNORECASE)
        if counter:
            ctr = int(counter.group())
            maxcounter = ctr if maxcounter < ctr else maxcounter
    return maxcounter
        
def makeSmallVersionOfPicture(picPath, smallPicTargetFolder):
    newPicName = picPath.removesuffix(".jpg").removesuffix(".jpeg") + "_kiskep.jpg"
    # upThreshold and downThreshold resemble file sizes in bytes
    # that are the boundaries of values which would be acceptable as output size
    upThreshold = 750000
    downThreshold = 250000
    # targetPix tries to resemble a pixel number  
    # that gives appr 500 kB file size (it is the middle of the range mentioned above)
    # thinking of 24 bit RGB pictures and the compression of the 'jpg' format
    targetPix = 1500000
    origFileSize = os.path.getsize(picPath)
    img = cv2.imread(picPath, cv2.IMREAD_COLOR)
    if origFileSize > upThreshold:
        # determining height and width
        h, w, c = img.shape 
        # determining ratio
        ratio = int(h * w / targetPix)
        # determining new height and width
        fileSize = origFileSize
        while fileSize > upThreshold or fileSize < downThreshold:
            nh = int(h / math.sqrt(ratio))
            nw = int(w / math.sqrt(ratio))
            # creating new image
            nimg = cv2.resize(img, (nw,nh))
            cv2.imwrite(newPicName, nimg)
            fileSize = os.path.getsize(newPicName)
            if fileSize <= downThreshold:
                #ratio needs to decrease
                targetPix *= 1.2
                ratio = int(h * w / targetPix)
            else:
                #ratio needs to increase
                targetPix *= 0.75
                ratio = int(h * w / targetPix)
    else:
        cv2.imwrite(newPicName, img)
    shutil.move(newPicName, smallPicTargetFolder)
    
def makeStandardSmallVersionOfPicture(picPath, smallPicTargetFolder):
    shorterSide = 1080
    newPicName = picPath.removesuffix(".jpg").removesuffix(".jpeg") + "_kiskep.jpg"
    img = cv2.imread(picPath, cv2.IMREAD_COLOR)
    # determining height and width
    h, w, c = img.shape
    if h > shorterSide and w > shorterSide:
	    if h < w:
	    	ratio = w / h
	    	nh = shorterSide
	    	nw = int(shorterSide * ratio)
	    else:
	    	ratio = h / w
	    	nw = shorterSide
	    	nh = int(shorterSide * ratio)
    else:
    	nw = w
    	nh = h
    
    # creating new image
    nimg = cv2.resize(img, (nw,nh))
    cv2.imwrite(newPicName, nimg)
    shutil.move(newPicName, smallPicTargetFolder)
    
    
    
