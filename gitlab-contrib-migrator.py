#!/usr/bin/python

import sys
from datetime import datetime


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
    parseArgs(argv)


if __name__ == "__main__":
   main(sys.argv)