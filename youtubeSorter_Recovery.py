#!/usr/bin/env python3
import os
from pathlib import Path

 
RECOVERY_DIRECTORY=".recovery"

def recovery():

    rec_file=None #recovery file object will used with open function
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
            rec_file=open(recovery_file_name,"r") 
            for line in rec_file:
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
            print("Error no recovery File Exist")
            exit()
    if ISRECOVERY_DONE or not ISVALID_FILE:
        if ISRECOVERY_DONE:
            print("Recovery Done")
        print("Removing backup file")
        os.remove(rec_file.name)
    else:
        print("Failed To do Recovery")
    
    #close the recovery file now
    rec_file.close()

if __name__=="__main__":
    print("-"*80)
    print("\t\tyoutubeSorter_Recovery v2.0 by authoritydmc")
    print("-"*80)

    recovery()