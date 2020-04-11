#!/bin/bash
echo "installing ...youtube-dl (neccessary)"
sudo apt install youtube-dl
sudo chmod 755 youtubeSorter*
echo "Removing any Existing youtubeSorter module first"
sudo rm /usr/local/bin/youtubeSorter*
echo "Installing current Module"
sudo cp youtubeSorter* /usr/local/bin
echo "installation Done"

echo "you can now access using youtubeSorter.py from anywhere"

