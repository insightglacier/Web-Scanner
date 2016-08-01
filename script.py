# Launch Locator
# A Python web crawler for new satellite launch information
# By Jeffrey Chan, August 2016

import urllib2

def wordOccurrence(word, page):
    # returns the number of times a word occurs within a page
    print 'running wordOccurrence'
    return 0

print 'Welcome to Launch Locator!'
print 'This program will now begin searching for launch information that might help you!\n'

# Reads in list of URLs fromm ./config/WebsiteList.txt
websiteListFile = open("./config/WebsiteList.txt", "r")
websiteList = websiteListFile.read().split('\n')
websiteListFile.close()

# Reads in list of keywords from ./config/Keywords.txt
keywordFile = open('./config/Keywords.txt', 'r')
keywordList = keywordFile.read().split('\n')
keywordFile.close()

# Make program be able to visit website on the website list
for url in websiteList:
    page = urllib2.urlopen(url).read()
    for word in keywordList:
        wordFrequency = wordOccurrence(keywordList[0], page)
        print 'The word', word, 'appeared', wordFrequency, 'times.'

# Make program count the number of times a keyword appears

# Make program send email about this information