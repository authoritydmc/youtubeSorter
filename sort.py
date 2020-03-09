#!/usr/bin/env python
import os
from pathlib import Path
from difflib import SequenceMatcher
import datetime
import argparse
import sys
# how to get the playlist
# youtube-dl -e --skip-download --flat-playlist  https://www.youtube.com/playlist?list=PLhixgUqwRTjxglIswKp9mpkfPNfHkzyeN>list.txt
# some replacement youtube_dl does
# :" -> " -"
# "/"-> "_"
# "?"->""
# 
# INITIALISATION
RECOVERY_DIRECTORY=".recovery"

RATIO_LIST=[]
RATIO_THREASHOLD=0.3  #below this do not suggest file

def main(youtube_file_list,original_file_list,shouldEnforceRename):
	_file_count=-1
	backup_file=getbackupfile()
	ISLOG_SUCCESSFUL=False
	sizeFormatter=str(len(str(len(youtube_file_list))))
	print(f"Size formatter ->{sizeFormatter}")
	print("RECOVERY MADE AT  "+datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")+ "IST (+5:30)")
	backup_file.write("RECOVERY MADE AT  "+datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")+ "IST (+5:30)\n\n")
	# print(original_list)
	print("Should EnforceRename-> ","True" if shouldEnforceRename else "False")
	print("Renaming ....")
	for files in youtube_file_list:
		_file_count+=1
		# for l in files:
		fileName=files.replace("\n","")
		fileName=fileName.replace(":"," -")
		fileName=fileName.replace("/","_")
		fileName=fileName.replace("?","")

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
				final_name=f"%0{sizeFormatter}d "%(_file_count)+original_fileName
				print("\nSuggestedName-> ",final_name)
				
				if Path(final_name).is_file():
					print(f"{final_name} already exist ")
				else:
					print(f"Renaming {original_fileName}-> {final_name}")
					try:
						ISLOG_SUCCESSFUL=True
						os.rename(original_fileName,final_name)
						backup_file.write(f" [ {original_fileName} / {final_name} ]")
						backup_file.write("\n")

					except :
						print("Failed to rename ",original_fileName)
				break
				# input("matched press any key")
			else:
				pass

			
		else:# for end
			print("-"*50)
			print("Couldn't find a exact match ")
			if high_ratio>=RATIO_THREASHOLD:
				ext=original_fileName.split(".")[-1]
				suggestName=f"%0{sizeFormatter}d "%(_file_count)+fileName+"."+ext
				print(f"\n\nSuggested Filename:\t\n\t{suggestName} \nFOR (original file)__: \n\t {high_ratio_fileName}")
				print("-"*50)
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
						print("Failed to rename ",high_ratio_fileName)
			
				
				
				
	# print("-"*50)	
	# print(f"\nHighest Matched =>{high_ratio_fileName}<=\nRatio= {high_ratio}\n")	
	# print("-"*50)
	RATIO_LIST.append(high_ratio)

	print("="*80)

	
	backup_file.close()
	if ISLOG_SUCCESSFUL:
		print("\aDone.....")
	else:
		print("no File Renamed hence no backup made ")
		os.remove(backup_file.name)
	# print(RATIO_LIST)
	# print("minimum highest ratio==",min(RATIO_LIST))
	

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

	if len(argumentList)<2:
		print("Please Enter the Youtube Playlist url")
		url="https://www.youtube.com/playlist?list=PLhixgUqwRTjxglIswKp9mpkfPNfHkzyeN"
	if len (argumentList)< 3:
		print("Do you want to Enforce file naming i.e All the files will be auto renamed to highest possible match\ny or Y to autorename else any key to manualy rename")
		ch= "y"#input()
		if ch.lower()=="y":
			shouldEnforceRename=True
	if len(url)>0:
		print("Downloading the list ....will take some time")
		stream=os.popen(f"youtube-dl -e --skip-download --flat-playlist {url}")
		output=stream.read().split("\n")
		file_list_from_youtube=[x for x in output]
		print("Playlist Downloaded...")
	# print(file_list_from_youtube)
	stream=os.popen("ls")
	output=stream.read().split("\n")
	current_file_list=[x for x in output]
	# print(current_file_list)
	main(file_list_from_youtube,current_file_list,shouldEnforceRename)