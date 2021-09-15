#!/usr/bin/python

import sys
from datetime import datetime
from bs4 import BeautifulSoup
import os
from tqdm import tqdm

def createNumOfCommitsOnDate(numOfCommits, date):
    for i in tqdm(range(numOfCommits)):
        os.system('echo "Commit number {} on {}" >> commit.md'.format((i+1), date.strftime("%m-%d-%Y")))
        os.system('export GIT_COMMITTER_DATE="{} 12:00:00"'.format(date.strftime("%m-%d-%Y")))
        os.system('export GIT_AUTHOR_DATE="{} 12:00:00"'.format(date.strftime("%m-%d-%Y")))
        os.system('git add --all > /dev/null')
        os.system('git commit --date="{} 12:00:00" -m "Commit number {} on {}" > /dev/null'.format( date.strftime("%Y-%m-%d"), (i+1), date.strftime("%m-%d-%Y")))


def parseHTMLAndCreateCommits(htmlContents, startDate):
    fullHtml = BeautifulSoup(htmlContents, 'html.parser')
    dateRects = fullHtml.find_all("rect", {"class": "user-contrib-cell has-tooltip"})
    print("Starting commits!\n")
    for dateRect in tqdm(dateRects):
        contribsAndDate = dateRect["title"].split("<br />")
        try:
            contribCount = int(contribsAndDate[0].split(" ")[0])
        except ValueError:
            continue
        try:
            dateFormat = contribsAndDate[1].split(">")[1].split("</")[0]
        except Exception:
            exit( "Error parsing date from HTML (possibly a new GitLab update breaking the script)" )
        date = datetime.strptime(dateFormat, '%A %b %d, %Y')
        if startDate == -1 or startDate <= date:
            createNumOfCommitsOnDate(contribCount, date)
    print( "Created commits for contrib chart! Use 'git push' to push to remote or use 'git log' to check commit log" )


def parseArgs(argv):
    if len(argv) < 2:
        exit( "Help - Try running: \n\ngitlab-contrib-migrator.py <htmlFile> <startDate> \n\nhtmlFile = HTML file with GitLab info \nstartDate = start commit date in MM-DD-YYYY format" )
    try:
        file = open(argv[1], 'rb')
        htmlContents = file.read()
    except:
        exit( "Error when trying to read the HTML file: {}".format(argv[1]) )
    if len(argv) == 3:
        try:
            startDate = datetime.strptime(argv[2], '%m-%d-%Y')
            return (htmlContents, startDate)
        except:
            print( "Error trying to parse start commit date: {} - proceeding without start date".format(argv[2]), file=sys.stderr )
    return (htmlContents, -1)

def main(argv):
    htmlContents, startDate = parseArgs(argv)
    parseHTMLAndCreateCommits(htmlContents, startDate)


if __name__ == "__main__":
   main(sys.argv)
