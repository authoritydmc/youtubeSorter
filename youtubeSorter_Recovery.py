#!/usr/bin/env python
import os
from pathlib import Path

 
RECOVERY_DIRECTORY=".recovery"

def recovery():
    ISRECOVERY_DONE=False
    ISVALID_FILE=False
    if not os.path.isdir("./"+RECOVERY_DIRECTORY):
        print("Exiting")
    else:
        print("starting recovery")
        recovery_file_name=RECOVERY_DIRECTORY+"/"+"rec"
        temp=RECOVERY_DIRECTORY+"/"+"rec"
        for i in range(10000):
            if Path(temp+str(i)).is_file():
                recovery_file_name=temp+str(i)
            else:
                break
        try:
            with open(recovery_file_name,"r") as filee:
                for line in filee:
                    files=line[2:-2].strip()
                    if "[" in line:
                        ISVALID_FILE=True
                        splt=files.split("/")
                        after_name=splt[-1].strip()
                        before_name=splt[0].strip()
                        try:
                            os.rename(after_name,before_name) #renaming to old name
                            ISRECOVERY_DONE=True
                        
                        except:
                            print(f"couldn't rename {after_name} to {before_name}")
                            input("press any key to continue")
        except :
            print("Error .NO recovery File Exist")
            exit()
    if ISRECOVERY_DONE or not ISVALID_FILE:
        if ISRECOVERY_DONE:
            print("Recovery Done")
        print("Removing backup file")
        os.system(f"rm {recovery_file_name}")
    else:
        print("Failed To do Recovery")

if __name__=="__main__":
    print("YoutubeSorter_Recovery v1.0 by authoritydmc")
    recovery()