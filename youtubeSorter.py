#!/usr/bin/env python
import os
from pathlib import Path
from difflib import SequenceMatcher
import datetime
import argparse
import sys
import time
import youtube_dl
# how to get the playlist
# youtube-dl -e --skip-download --flat-playlist  https://www.youtube.com/playlist?list=PLhixgUqwRTjxglIswKp9mpkfPNfHkzyeN>list.txt
# some replacement youtube_dl does
# :" -> " -"
# "/"-> "_"
# "?"->""
#BETA VERSION
# INITIALISATION
RECOVERY_DIRECTORY=".recovery"

RATIO_LIST=[]
RATIO_THREASHOLD=0.6  #below this do not suggest file

def main(youtube_file_list,original_file_list,shouldEnforceRename):
	_file_count=-1
	backup_file=getbackupfile()
	ISLOG_SUCCESSFUL=False
	sizeFormatter=str(len(str(len(youtube_file_list))))
	print(f"Size formatter ->{sizeFormatter}")
	print("RECOVERY MADE AT  "+datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")+" @authoritydmc")
	backup_file.write("RECOVERY MADE AT  "+datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")+ "IST (+5:30)\n\n")
	print("Should EnforceRename-> ","True" if shouldEnforceRename else "False")
	print("Renaming ....")
	for files in youtube_file_list:
		_file_count+=1
		fileName=files.replace("\n","")
		fileName=fileName.replace(":"," -")
		fileName=fileName.replace("/","_")
		fileName=fileName.replace("?","")
		if len(fileName)<=0:
			continue
		high_ratio_fileName=""
		high_ratio=0
		print(f"\nCurrent file=>{fileName}<=\n")
		for original_fileName in original_file_list:
			ratio=SequenceMatcher(a=fileName,b=original_fileName).ratio()
			if ratio>high_ratio:
				high_ratio=ratio
				high_ratio_fileName=original_fileName
			if fileName in original_fileName:
				
				print(f"\n___MATCH___ at {original_fileName}\n")
				if str(_file_count) in original_fileName.split()[0]:
					print("File Already Renamed. Continuing") 
					break
				final_name=f"%0{sizeFormatter}d "%(_file_count)+original_fileName
				print("\nSuggestedName-> ",final_name)

				if Path(final_name).is_file():
					print(f"{final_name} already exist ")
					break
				else:
					print(f"Renaming {original_fileName}-> {final_name}")
					try:
						ISLOG_SUCCESSFUL=True
						os.rename(original_fileName,final_name)
						backup_file.write(f" [ {original_fileName} / {final_name} ]")
						backup_file.write("\n")

					except :
						print("Failed to rename ,Maybe File does not Exist",original_fileName)
				break
				# input("matched press any key")
			else:
				pass


			
		else:# couldnot find a exact match using in keyword
		#that's why now we will use SequenceMatcher ratio to Suggest FileName
			print("-"*50)
			print("\nCouldn't find a exact match ")
			ext=original_fileName.split(".")[-1]
			suggestName=f"%0{sizeFormatter}d "%(_file_count)+fileName+"."+ext
			print(f"\n\nSuggested Filename:\t\n\t{suggestName} \nFOR (original file): \n\t {high_ratio_fileName}")
			#only if the maximum suggested filename ratio is greater than Threshold than only replace
			if high_ratio>=RATIO_THREASHOLD:
				if not shouldEnforceRename:
					ch=input("press Enter to Accept or N or n to Reject Current Selection ")		
					if ch.lower()=="n":
						continue		
				try:
						ISLOG_SUCCESSFUL=True
						os.rename(high_ratio_fileName,suggestName)
						backup_file.write(f" [ {high_ratio_fileName} / {suggestName} ]")
						backup_file.write("\n")
				except:
						print("Failed to rename maybe File Does not Exist. ",high_ratio_fileName)
			else:
				print(f"\nThe Highest Match Ratios is {high_ratio} is not Above {RATIO_THREASHOLD} to Trigger Renaming")

			print("-"*50)
		RATIO_LIST.append(high_ratio)

		print("="*80)

				


	
	backup_file.close()
	if ISLOG_SUCCESSFUL:
		print("\aDone.....")
	else:
		print("no File Renamed hence no backup made ")
		os.remove(backup_file.name)



def getbackupfile():
	if not os.path.isdir("./"+RECOVERY_DIRECTORY):
		print("Directory DoesNot Exist..Making one")
		os.makedirs("./"+RECOVERY_DIRECTORY)
	else:
		print("Making Recovery exist...")
	try:
		recovery_file_name=RECOVERY_DIRECTORY+"/"+"rec"
		for i in range(10000):
			if Path(recovery_file_name+str(i)).is_file():
				continue
			else:
				recovery_file_name=recovery_file_name+str(i)
				break
		else:
			print("MAX RECOVERY LIMIT REACHED ") #todo implement logic to remove this limitation
		f=open(recovery_file_name,"w")
		print("Setup of recovery complete at ",recovery_file_name)

		return f
	except :
		print("An exception occured while Setting up for Recovery log..")
		input("Press any key to Continue without Recovery option\n ctrl+c to exit the progran")


if __name__=="__main__":
	file_list_from_youtube=[]
	url=""
	shouldEnforceRename=False
	argumentList=sys.argv
	print("-"*80)
	print("\t\tyoutubeSorter v2.0 by authoritydmc")
	print("-"*80)
	print("\n\n\nCurrent Director:",os.getcwd())
	print()
	if not Path(".youtube_playlist").is_file():
		if len(argumentList)<2:
			print("Please Enter the Youtube Playlist url")
			url=input() 
		else:
			url=argumentList[1]
	else:
		print("-->A Playlist Already Exist.Getting Data from it")
		with open(".youtube_playlist","r") as fl:
			for line in fl:
				file_list_from_youtube.append(line.replace("\n",""))

	print("\n\nDo you want to Enforce file naming (All the files will be auto renamed to highest possible match)\nEnter y or Y to autorename else any key to manualy rename:--->",end=" ")
	ch= input()
	if ch.lower()=="y":
		shouldEnforceRename=True
	if len(file_list_from_youtube)<=0:
		print("Downloading the list ....will take some time")
		#get ydl object 
		ydl =youtube_dl.YoutubeDL({'extract_flat' : True})

		with ydl:
			#extract the info
			result = ydl.extract_info(url,False)
			# #in the entries of result we have all the required item
			if result['_type'] !="playlist":
				print("Given link is not of a Playlist...")
			else:
				print("Valid Link of a playlist")
			#loop through each entry
			print("Total -video ",len(result['entries']))
			for video in result['entries']:
				#add the title to playlist
				file_list_from_youtube.append(video['title'])
				

		

		print("Playlist Downloaded...")
#save downloaded list into the file now ,,,
		with open(".youtube_playlist","w")as f:
			for l in file_list_from_youtube:
				f.write(l)
				f.write("\n")

	#will contain current path's filelist 
	flist = []
	for p in Path('.').iterdir():
		if p.is_file():
			print(p)
			flist.append(str(p))


	main(file_list_from_youtube,flist,shouldEnforceRename)
	for i in range(5):
		print(f"Exiting in {5-i} seconds",end="\r")
		time.sleep(1)
		
