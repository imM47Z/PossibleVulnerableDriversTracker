import os
import sys
import threading
import progressbar
from Classes.Driver import Driver
from internal import Internal

cwd = os.path.dirname(sys.executable) if hasattr(sys, 'frozen') else os.path.dirname(os.path.realpath(sys.argv[0]))
thread = threading.current_thread()
suspectFunctions = ["MmMapIoSpace", "MmUnmapIoSpace", "MmGetPhysicalAddress", "ZwMapViewOfSection", "MmGetSystemRoutineAddress", "MmMapIoSpaceEx"]

def GetDriverInfo(path, file):
    thread = threading.current_thread()
    driver = Driver(path, file)
    if not driver.haveDevice:
        setattr(thread, "driver", False)
        return
    for func in suspectFunctions:
        if not func in driver.content:
            continue
        driver.IncreaseSeverity(1)
    setattr(thread, "driver", driver)
    return


os.system("cls")
os.system("title Possible Vulnerable Driver Tracker")

print("Possible Vulnerable Driver Tracker\n\t\tBy M47Z\n")

searchDir = os.path.abspath(input("Directory To Search: "))

os.system("cls")

with progressbar.ProgressBar(max_value=Internal.CountFilesByExtension(searchDir, ".sys")) as bar:
    print("[+] Searching For All Possible Vulnerable Drivers\n")
    setattr(thread, "progress", 0)
    setattr(thread, "bar", bar)
    driversList = Internal.GetAllDriversInPath(searchDir, GetDriverInfo, thread)

if not os.path.isdir("\\".join((cwd, "result"))):
    os.mkdir("\\".join((cwd, "result")))

for file in os.listdir("\\".join((cwd, "result"))):
    os.remove("\\".join((cwd, "result", file)))

for i in range(1, len(suspectFunctions) + 1):
    filteredDriverList = list(filter(lambda driver: driver.severity == i, driversList))
    if not len(filteredDriverList) > 0:
        continue
    file = open("\\".join((cwd, "result", ".".join((str(i), "txt")))), "w")
    for driver in filteredDriverList:
        file.write("{}\n".format(("" if driver.path[len(driver.path) - 1:] == "\\" else "\\").join((driver.path, driver.name)), ""))
    file.close()

print("\n\nPress Any Key to Exit")
os.system("pause>nul")
