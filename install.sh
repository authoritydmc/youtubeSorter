#!/bin/bash
echo "0. installing ...youtube-dl (neccessary)"
sudo apt install youtube-dl
sudo chmod 755 youtubeSorter*
clear
echo "Installation of Youtube Sorter Starting..."
echo "1.Removing any Existing youtubeSorter module first"
sudo rm /usr/local/bin/youtubeSorter*
echo "2.Installing current Module"
sudo cp youtubeSorter* /usr/local/bin
echo "3.Installation Done"

echo "4.you can now access using youtubeSorter.py from anywhere"

echo "Done ..Setup finished "