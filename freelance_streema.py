import requests
from bs4 import BeautifulSoup
import shutil
import logging
import time
import re
import os

station_names = []
bitrate = []
urls = []
genres = []
pls = []
query = input("Search URL (streema): ")


def downloadEntirePage():
    threadse = []
    resp = requests.get(query) 
    soup = BeautifulSoup(resp.content, 'html.parser')

    x = soup.find("div",class_="items-list")
    b = x.find_all("div",{"title" : True})
    for b in b:
        d = b['title'][5:] # title of station
        station_names.append(d)

        d = b['data-url'] # streaming URL
        pls.append("http://streema.com/" + d)

        gnrs = []
        for p in b.find_all("p",class_="genre"):
            for i in p.find_all("span"):
                gnrs.append(i.get_text().strip()) # genres
        genres.append(gnrs)


        
downloadEntirePage()
name = input("Program has completed. File name:")

PATH = './' + name + ".txt"
while os.path.isfile(PATH) and os.access(PATH, os.R_OK):
	print("Invalid filename. File already exists.")
	name = input("File name:")
	PATH = './' + name + ".txt"

f = open(name + ".txt", "a",encoding="utf-8")

downloadEntirePage()

for i in range(len(station_names)):
    print("Name: ", station_names[i])
    print("Streaming URL: ", pls[i])
    print("Genres: ", end="")
    for item in genres[i]:
        print("%s " % item, end="")
    print("\n-----------------------------------------------------------------\n")

    f.write("Name: " + station_names[i] + "\n")
    f.write("Streaming URL: " + pls[i] + "\n")
    f.write("Genres: ")
    for item in genres[i]:
        f.write("%s " % item)
    f.write("\n\n-----------------------------------------------------------------\n\n")

f.write("\nEnd of Search\n\n\n")

f.close()

wait = input("\nDone! Hit Enter to close the program.")