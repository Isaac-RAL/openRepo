#!/usr/bin/python
import feedparser
import os
import sys
import errno
import appdirs
import datetime
import time

appname = "rssAlert"
appauthor = "RAL"

# If the data directory doesn't exist, create it
datadir = appdirs.user_data_dir(appname, appauthor)
if (not os.path.isdir(datadir)):
    os.makedirs(datadir)
# Path for saved RSS site feeds
path = os.path.join(datadir, "sites.txt")

text = []
# URLs list is mostly used for checking to make sure we aren't showing the same feed twice (or more.)
urls = []


def showrss():
    # Open sites.txt
    try:
        with open(path, 'r') as f:
            # Get rid of all the newlines while you're reading it in
            global text
            text = [x.strip() for x in f.readlines()]
    except:
        pass
    for line in text:
        line = line.strip()
        # we don't want to process the same URL more than once
        if line in urls:
            continue

        urls.append(line)
        # Feed line found in file to feedparser
        site = feedparser.parse(line)
        holder = site['entries']
        num = min(3, len(holder))
        keyword = ['cisco', 'bravo', 'zulu']
        count = 0
        # find specific keywords in feed before deciding to save or not
        for name in keyword:
            if name in str(holder[:num]).lower():
                # Specify what to do if keyword is found in the feed.
                count += 1
        if count != 0:
            print 'Published on', site['entries'][0]['published']
            # Top three entries from the RSS feed
            for entry in holder[:num]:
                title = entry['title']
                link = entry['link']
                print(title)
                print(link)
        print '\n'
    return

def addNewFeed():
    global text
    # Open the file for appending and just write the new line to it
    new = raw_input("Enter RSS feed to add: ")
    # If you're not subscribed already, subscribe!
    if (new not in text):
        text.append(new)
        with open(path, 'a') as f:
            f.write(new + "\n")
    showRSS()

def menu():
    secs = 0
    while secs != 1:
        p = datetime.datetime.today()
        secs = 3600 - ((p.minute * 60) + p.second)
        print 'Next search at', 25 - p.hour, 'o\'clock\n'
        time.sleep(secs)
    showrss()


menu()
