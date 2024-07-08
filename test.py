import os
import sys
import kepnormalib as klib

# this file should be called with an argument however it is for the 'picstardlib' which is tested here. 
# the value of it is not important. it will be overwritten.
 
def test_filterTitleWithDateRemains():
    # The regRootFolder which normally comes from the command line is overwritten here...
    # The "_" character gets inthere in the 'picstardlib' too, but this step is also omitted here... 
    print("test_filterTitleWithDateRemains() ->")
    klib.regRootFolder = "._folder_" 
    print("CASE 1:")
    input1 = ".\\folder\\Eg_2024_subfolder\\subsub_20240211"
    wantedout1 = "subfolder_subsub_20240211"
    result = (klib.filterTitleWithDateRemains(input1) == wantedout1)
    if result == True:
        print("OK")
    else:
        print("NOK")
    print("CASE 2:")
    input2 = ".\\folder\\Eg_2024_subfolder\\subsub"
    wantedout2 = "subfolder_subsub"
    result = (klib.filterTitleWithDateRemains(input2) == wantedout2)
    if result == True:
        print("OK")
    else:
        print("NOK")

def test_separateTitleAndDateFromFilteredTitle():
    print("test_separateTitleAndDateFromFilteredTitle() ->")
    print("CASE 1:")
    input1 = "subsub_20240211"
    wantedout1 = ["subsub","20240211"]
    result = (klib.separateTitleAndDateFromFilteredTitle(input1) == wantedout1)
    if result == True:
        print("OK")
    else:
        print("NOK")
    input2 = "subsub20240211"
    wantedout2 = ["subsub","20240211"]
    print("CASE 2:")
    result = (klib.separateTitleAndDateFromFilteredTitle(input2) == wantedout2)
    if result == True:
        print("OK")
    else:
        print("NOK")
    input3 = "test_2024_szivbol_jovo_20240202_Eg_20240211_Szocakcio"
    wantedout3 = ["test_2024_szivbol_jovo_Eg_Szocakcio","20240211"]
    print("CASE 3:")
    result = (klib.separateTitleAndDateFromFilteredTitle(input3) == wantedout3)
    if result == True:
        print("OK")
    else:
        print("NOK")
    input4 = "szivbol_jovo_Szocakcio"
    wantedout4 = ["szivbol_jovo_Szocakcio",""]
    print("CASE 4:")
    result = (klib.separateTitleAndDateFromFilteredTitle(input4) == wantedout4)
    if result == True:
        print("OK")
    else:
        print("NOK")

def test_extractTitleAndDate():
    # The regRootFolder which normally comes from the command line is overwritten here...
    # The "_" character gets inthere in the 'picstardlib' too, but this step is also omitted here... 
    print("test_extractTitleAndDate() ->")
    klib.regRootFolder = "._folder_" 
    print("CASE 1:")
    input1 = ".\\folder\\Eg_2024_subfolder\\subsub_20240211"
    wantedout1 = ["subfolder_subsub", "20240211"]
    result = (klib.extractTitleAndDate(input1) == wantedout1)
    if result == True:
        print("OK")
    else:
        print("NOK")
    input2 = ".\\folder\\Eg_2024_subfolder\\subsub"
    wantedout2 = ["subfolder_subsub", ""]
    print("CASE 2:")
    result = (klib.extractTitleAndDate(input2) == wantedout2)
    if result == True:
        print("OK")
    else:
        print("NOK")
    input3 = "test_2024_szivbol_jovo_20240202_Eg_20240211_Szocakcio"
    wantedout3 = ["test_2024_szivbol_jovo_Szocakcio","20240211"]
    print("CASE 3:")
    result = (klib.extractTitleAndDate(input3) == wantedout3)
    if result == True:
        print("OK")
    else:
        print("NOK")

def test_createStandardStructure():
    print("test_createStandardStructure() ->")
    klib.folderRecords = [{'date': '20240110', 'event': 'sakk', 'folder': 'test' + os.sep + '2024_sakk', "multidates": True, "filecounter":1},
                          {'date': '20240208', 'event': 'sakk', 'folder': 'test' + os.sep + '2024_sakk', "multidates": True, "filecounter":2},
                          {'date': '20240210', 'event': 'szocakcio', 'folder': 'test' + os.sep + '2024_szivbol' + os.sep + 'jovo_20240202' + os.sep + 'Eg_20240211_Szocakcio', "multidates": False, "filecounter":4}]
    klib.createStandardStructure()
    print()
    print("CASE 1:")
    print(" - Target folder created - ")
    result = (os.path.isdir(klib.targetFolder ))
    if result == True:
        print("OK")
    else:
        print("NOK")
    print("CASE 2:")
    print(" - Resulting folder has been named correctly - ")
    result = (os.path.isdir(os.path.join(klib.targetFolder, klib.folderRecords[0]['date'] + '_' + klib.fi + '_' + klib.folderRecords[0]["event"])))
    if result == True:
        print("OK")
    else:
        print("NOK")
    print("CASE 3:")
    print(" - if 'monthFilter' variable is set to a valid value (here:'01') -> the function eliminates all other dates before creating the result - ")
    klib.monthFilter = '01'
    klib.createStandardStructure()


def test_folderSweeper():
    print("test_folderSweeper() ->")
    testFolder1 = "test" + os.sep + "2024_sakk"
    testFolder2 = "test" + os.sep + "2024_szivbol"
    testFolder3 = "test" + os.sep + "2024_kamu"

    testFolderRecords1 = [{'date': '20240110', 'event': 'test_2024_sakk', 'folder': 'test' + os.sep + '2024_sakk', 'multidates': True, 'filecounter': 1}, {'date': '20240208', 'event': 'test_2024_sakk', 'folder': 'test' + os.sep + '2024_sakk', 'multidates': True, 'filecounter': 2}]
    testNoDateFolders1 = ['test' + os.sep + '2024_sakk']
    testFolderRecords2 = [{'date': '20240211', 'event': 'test_2024_szivbol_jovo_Szocakcio', 'folder': 'test' + os.sep + '2024_szivbol' + os.sep + 'jovo_20240202' + os.sep + 'Eg_20240211_Szocakcio', 'multidates': False, 'filecounter': 4}]
    testNoDateFolders2 = []
    klib.folderRecords.clear()
    klib.noDateFolders.clear()
    klib.folderSweeper(testFolder1, "")
    print("CASE 1:")
    print("folderRecords: \n", klib.folderRecords)
    if (klib.folderRecords == testFolderRecords1):
        print("OK")
    else:
        print("NOK")
    print("noDateFolders: \n", klib.noDateFolders)
    if (klib.noDateFolders == testNoDateFolders1):
        print("OK")
    else:
        print("NOK")

    klib.folderRecords.clear()
    klib.noDateFolders.clear()
    klib.folderSweeper(testFolder2, "")
    print("CASE 2:")
    print("folderRecords: \n", klib.folderRecords)
    if (klib.folderRecords == testFolderRecords2):
        print("OK")
    else:
        print("NOK")
    print("noDateFolders: \n", klib.noDateFolders)
    if (klib.noDateFolders == testNoDateFolders2):
        print("OK")
    else:
        print("NOK")
    klib.folderRecords.clear()
    klib.noDateFolders.clear()
    klib.folderSweeper(testFolder3, "")
    print("CASE 3:")
    print("folderRecords: \n", klib.folderRecords)
    if (klib.folderRecords == []):
        print("OK")
    else:
        print("NOK")
    print("noDateFolders: \n", klib.noDateFolders)
    if (klib.noDateFolders == []):
        print("OK")
    else:
        print("NOK")

def test_checkIfPicturesWithNoDateExist():
    print("test_checkIfPicturesWithNoDateExist() ->")
    klib.noDateFolders = ["test" + os.sep + "2024_sakk",
    "test" + os.sep + "2024_szivbol",
    "test" + os.sep + "2024_kamu"] 
    klib.checkIfPicturesWithNoDateExist()
    klib.noDateFolders.clear()

def test_sumFiles2Process():
    print("test_sumFiles2Process() ->")
    klib.folderRecords= [{'date': '20240110', 'event': 'test_2024_sakk', 'folder': 'test' + os.sep + '2024_sakk', 'multidates': True, 'filecounter': 1}, {'date': '20240208', 'event': 'test_2024_sakk', 'folder': 'test' + os.sep + '2024_sakk', 'multidates': True, 'filecounter': 2}]
    print("sum of files: ", klib.sumFiles2Process())
    if klib.sumFiles2Process() == 3:
        print("OK")
    else:
        print("NOK")
    klib.folderRecords.clear()

def test_offset():
    print(klib.offset("EG_Kesz\\20230518_EG\\nagy_kepek"))
# calling test functions:

def test_folderSweeperHEIC2JPG():
    klib.folderSweeperHEIC2JPG("test" + os.sep + "2024_iphone")
    
#test_filterTitleWithDateRemains()
#test_separateTitleAndDateFromFilteredTitle()
#test_extractTitleAndDate()
#test_createStandardStructure()
#test_folderSweeper()
#test_checkIfPicturesWithNoDateExist()
#test_sumFiles2Process()
#test_offset()
test_folderSweeperHEIC2JPG()
