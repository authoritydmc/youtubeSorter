# youtube_dl_fileSorter
Sort the youtube dl playlist on local downloaded directory..

# Usuage:
## sort.py
**1. copy the sort.py and recovery.py to your Playlist Directory**
 
 2. open a **Terminal** and navigate to Playlist Directory(i.e Your current path is playlist directory)

3. run the sort.py 
  
  ``` python sort.py <url_of_playlist>```
    or 
  > ./sort.py
  
 
4. Sort.py will ask two things depending(1 if url is passed via argument)
  whether it should auto rename all the file when the file  is not found and it suggest a best possible match
  
  >Enter y or  Y to Accept this else any key will make you manually decide what to do
 
 ## Recovery.py
  
  this file should be run to recover any changes made by sort.py
  i.e it undo the renaming of file to Original State.
  
  Please note you can run this multiple times untill you get back to the original fileNames.
  

