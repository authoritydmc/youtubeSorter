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
RATIO_THREASHOLD=0.6  #below this do not suggest file

def main(youtube_file_list,original_file_list,shouldEnforceRename):
	_file_count=-1
	backup_file=getbackupfile()
	ISLOG_SUCCESSFUL=False
	sizeFormatter=str(len(str(len(youtube_file_list))))
	print(f"Size formatter ->{sizeFormatter}")
	print("RECOVERY MADE AT  "+datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")+ "IST (+5:30)")
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
						print("Failed to rename ",original_fileName)
				break
				# input("matched press any key")
			else:
				pass


			
		else:# for end
			print("-"*50)
			print("\nCouldn't find a exact match ")
			ext=original_fileName.split(".")[-1]
			suggestName=f"%0{sizeFormatter}d "%(_file_count)+fileName+"."+ext
			print(f"\n\nSuggested Filename:\t\n\t{suggestName} \nFOR (original file)__: \n\t {high_ratio_fileName}")
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
						print("Failed to rename ",high_ratio_fileName)
			else:
				print(f"\nThe Highest Match Ratios is {high_ratio} is not Above {RATIO_THREASHOLD} to Trigger Renaming")

			print("-"*50)
		RATIO_LIST.append(high_ratio)

		print("="*100)

				


	
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
	if not Path(".youtube_playlist").is_file():
		if len(argumentList)<2:
			print("Please Enter the Youtube Playlist url")
			url=input() #"https://www.youtube.com/playlist?list=PLhixgUqwRTjxglIswKp9mpkfPNfHkzyeN"
		else:
			url=argumentList[1]
	else:
		print("A Playlist Already Exist.Getting Data from it")
		with open(".youtube_playlist","r") as fl:
			for line in fl:
				file_list_from_youtube.append(line.replace("\n",""))

	print("\n\nDo you want to Enforce file naming i.e All the files will be auto renamed to highest possible match\ny or Y to autorename else any key to manualy rename")
	ch= input()
	if ch.lower()=="y":
		shouldEnforceRename=True
	if len(file_list_from_youtube)<=0:
		print("Downloading the list ....will take some time")
		stream=os.popen(f"youtube-dl -e --skip-download --flat-playlist {url}")
		output=stream.read().split("\n")
		file_list_from_youtube=[x for x in output]
		print("Playlist Downloaded...")
		with open(".youtube_playlist","w")as f:
			for l in file_list_from_youtube:
				f.write(l)
				f.write("\n")
	stream=os.popen("ls")
	output=stream.read().split("\n")
	current_file_list=[x for x in output]
	# print(current_file_list)
	main(file_list_from_youtube,current_file_list,shouldEnforceRename)