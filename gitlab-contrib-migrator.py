#!/usr/bin/python

import sys
from datetime import datetime
from bs4 import BeautifulSoup
import os
from tqdm import tqdm

def createNumOfCommitsOnDate(numOfCommits, date):
    path   = ''
    setter = 'set'

    if os.name != 'nt': # Windows
        path   = '> /dev/null' 
        setter = 'export'

    for i in tqdm(range(numOfCommits)):
        os.system('echo "Commit number {} on {}" >> commit.md'.format((i+1), date.strftime("%m-%d-%Y")))
        os.system('{} GIT_COMMITTER_DATE="{} 12:00:00"'.format(setter, date.strftime("%m-%d-%Y")))
        os.system('{} GIT_AUTHOR_DATE="{} 12:00:00"'.format(setter, date.strftime("%m-%d-%Y")))
        os.system('git add --all {}'.format(path))
        os.system('git commit --date="{} 12:00:00" -m "Commit number {} on {}" {}'.format(date.strftime("%Y-%m-%d"), (i+1), date.strftime("%m-%d-%Y"), path))
    
def parseHTMLAndCreateCommits(htmlContents, startDate):
    fullHtml = BeautifulSoup(htmlContents, 'html.parser')
    dateRects = fullHtml.find_all("rect", {"class": "user-contrib-cell js-tooltip"})
    print("Starting commits!\n")
    for dateRect in tqdm(dateRects):
        contribsAndDate = dateRect["data-original-title"].split("<br />")
        try:
            contribCount = int(contribsAndDate[0].split(" ")[0])
        except ValueError:
            continue;
        date = datetime.strptime(contribsAndDate[1], '%A %b %d, %Y')
        if startDate == -1 or startDate <= date:
            createNumOfCommitsOnDate(contribCount, date)
    print("Created commits for contrib chart! Use 'git push' to push to remote or use 'git log' to check commit log")


def parseArgs(argv):
    if (len(argv) < 2):
        print( "Help - Try running: \n\ngitlab-contrib-migrator.py <htmlFile> <startDate> \n\nhtmlFile = HTML file with GitLab info \nstartDate = start commit date in MM-DD-YYYY format" )
        exit()
    try:
        file = open(argv[1], 'rb')
        htmlContents = file.read()
    except:
        print( "Error when trying to read the HTML file: {}".format(argv[1]) )
        exit()
    if (len(argv) == 3):
        try:
            startDate = datetime.strptime(argv[2], '%m-%d-%Y')
            return (htmlContents, startDate)
        except:
            print( "Error trying to parse start commit date: {} - proceeding without start date".format(argv[2]) )
    return (htmlContents, -1)

def main(argv):
    htmlContents, startDate = parseArgs(argv)
    parseHTMLAndCreateCommits(htmlContents, startDate)


if __name__ == "__main__":
   main(sys.argv)
