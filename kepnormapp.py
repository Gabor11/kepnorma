import tkinter
import platform
import subprocess

sourceFolder = "letoltott"

root = tkinter.Tk()
root.title("KépnormApp")
frameCommon = tkinter.Frame(root, padx=30, pady=30)
frameCommon.pack(side=tkinter.TOP)
frameGrouping = tkinter.LabelFrame(frameCommon, text="csoportosítás",width=200, height=100)
frameGrouping.pack(side=tkinter.TOP)
frameGrouping.pack_propagate(False)
frameFilter = tkinter.LabelFrame(frameCommon, text="hónapszűrő",width=200, height=100)
frameFilter.pack()
frameFilter.pack_propagate(False)
frameButton = tkinter.Frame(frameCommon)
frameButton.pack(side=tkinter.BOTTOM)

if (platform.system() == "Windows"):
    initialCommand = "start cmd /K py"
elif (platform.system() == "Linux"):
    initialCommand = "sudo python3"

def work():
    monthValue = month.get()
    if(monthValue == "" or monthValue == "mind"):
        decideMonthlyGroupingAndExecuteWithFilterValue("")
    elif(monthValue =="január"):
        decideMonthlyGroupingAndExecuteWithFilterValue("-1")
    elif(monthValue == "február"):
        decideMonthlyGroupingAndExecuteWithFilterValue("-2")
    elif(monthValue == "március"):
        decideMonthlyGroupingAndExecuteWithFilterValue("-3")
    elif(monthValue == "április"):
        decideMonthlyGroupingAndExecuteWithFilterValue("-4")
    elif(monthValue == "május"):
        decideMonthlyGroupingAndExecuteWithFilterValue("-5")
    elif(monthValue == "június"):
        decideMonthlyGroupingAndExecuteWithFilterValue("-6")
    elif(monthValue == "július"):
        decideMonthlyGroupingAndExecuteWithFilterValue("-7")
    elif(monthValue == "augusztus"):
        decideMonthlyGroupingAndExecuteWithFilterValue("-8")
    elif(monthValue == "szeptember"):
        decideMonthlyGroupingAndExecuteWithFilterValue("-9")
    elif(monthValue == "október"):
        decideMonthlyGroupingAndExecuteWithFilterValue("-10")
    elif(monthValue == "november"):
        decideMonthlyGroupingAndExecuteWithFilterValue("-11")
    elif(monthValue == "december"):
        decideMonthlyGroupingAndExecuteWithFilterValue("-12")

def decideMonthlyGroupingAndExecuteWithFilterValue(filterValue):
    commandStr = initialCommand + " kepnorma.py " + sourceFolder
    if(r.get() == 2):
        subprocess.call(commandStr + " " + filterValue, shell=True)
    else:
        subprocess.call(commandStr + " " + "--havicsopi" + " " + filterValue, shell=True)

r= tkinter.IntVar()
r.set(2)
v= tkinter.IntVar()

radioButtonMonth = tkinter.Radiobutton(frameGrouping, text="hónap szerint", variable=r, value=1)
#radioButtonMonth.grid(row=0,column=0)
radioButtonMonth.pack(padx=40,pady=5)
radioButtonEvent = tkinter.Radiobutton(frameGrouping, text="esemény szerint", variable=r, value=2)
#radioButtonMonth.grid(row=1,column=0)
radioButtonEvent.pack(padx=40)

# Dropdown menu options 
options = [ 
    "mind",
    "január", 
    "február", 
    "március", 
    "április", 
    "május", 
    "június", 
    "július",
    "augusztus",
    "szeptember",
    "október",
    "november",
    "december"
] 
month = tkinter.StringVar() 
month.set("mind")
# Create Dropdown menu
drop = tkinter.OptionMenu(frameFilter , month , *options ) 
drop.pack(pady=20) 

button = tkinter.Button( frameButton , text = "Indítsd!" , command = work ).pack(side=tkinter.BOTTOM, pady=30) 

tkinter.mainloop()

