# youtube_dl_fileSorter
Sort the youtube dl playlist on local downloaded directory..

# Usage:
## sort.py
### **1. copy the youtubeSorter.py and youtubeSorter_Recovery.py to your /usr/local/bin Directory**
 **make it Executable**
 
 >sudo chmod +x youtubeSorter.py youtubeSorter_Recovery.py
 own the file ..
 >sudo chown <username>  youtubeSorter.py
 >sudo chown <username> youtubeSorter_Recovery.py
 
 
### 2. open a **Terminal** and navigate to Playlist Directory(i.e Your current path is playlist directory)

### 3. run the youtubeSorter.py 
  
  ``` youtubeSorter.py <url of playlist> ```
    or 
  > python youtubeSorter.py
  
 
### 4. YoutubeSorter.py
  will ask two things ```url``` and ```shouldEnforceRename``` (1 if url is passed via argument).
  whether it should auto rename all the file when the file  is not found and it suggest a best possible match
  
  >Enter y or  Y to Accept this else any key will make you manually decide what to do
 
 ## youtubeSorter_Recovery.py
  
  this file should be run to recover any changes made by sort.py
  i.e it undo the renaming of file to Original State.
  
  Please note you can run this multiple times untill you get back to the original fileNames.
  
##### note

Run using python3
