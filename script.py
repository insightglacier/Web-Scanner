# Launch Locator
# A Python web crawler for new satellite launch information
# By Jeffrey Chan, August 2016

import urllib2
import smtplib
from bs4 import BeautifulSoup
from sets import Set

def htmlCrawler(word, html):
    # returns the number of times given word appears in given html
    # case sensitive
    counter = htmlIndex = wordIndex = 0
    while htmlIndex < len(html):
        if (wordIndex < len(word) and htmlIndex < len(html) and html[htmlIndex] == word[wordIndex]):
            wordIndex += 1
            if wordIndex == len(word):
                counter += 1
                wordIndex = 0
        else:
            wordIndex = 0
        htmlIndex += 1
    return counter

print 'Welcome to Launch Locator!'

reportSwitch = raw_input('Would you like a full report on my search results? (y/n)\n')
if reportSwitch == 'y':
    reportSwitch = True
elif reportSwitch == 'n':
    reportSwitch = False
else:
    print 'Invalid input. By default, I will send out a full report'
    reportSwitch = True

print 'This program will now begin searching for launch information that might help you!\n'

# Reads URLs from ./config/WebsiteList.txt and stores in websiteList
websiteListFile = open("./config/WebsiteList.txt", "r")
websiteList = websiteListFile.read().split('\n')
websiteListFile.close()

# Reads keywords from ./config/Keywords.txt and stores in keywordList
keywordFile = open('./config/Keywords.txt', 'r')
keywordList = keywordFile.read().split('\n')
keywordFile.close()

urlSet = Set([]) # create an empty set to hold other links

# Pull HTML from listed websites and look for keywords
for url in websiteList:
    page = urllib2.urlopen(url).read().lower() # stores lowercase page HTML into variable
    soup = BeautifulSoup(page, 'html.parser') # pass html into BeautifulSoup constructor
    for link in soup.find_all('a'):         # find external links and add them to urlSet
        urlSet.add(link.get('href'))
    print 'Looking for keywords within', url
    for keyword in keywordList:
        wordAppearance = htmlCrawler(keyword.lower(), page)
        print 'The word', keyword, 'appeared', wordAppearance, 'times.'
    print '\n'

# Pull HTML from external websites and look for keywords
for url in urlSet:
    page = urllib2.urlopen(url).read().lower()
    print 'Looking for keywords within', url
    for keyword in keywordList:
        wordAppearance = htmlCrawler(keyword.lower(), page)
        print 'The word', keyword, 'appeared', wordAppearance, 'times.'
    print '\n'

# Make program send email about this information
# server = smtplib.SMTP('smtp.gmail.com', 587)
# server.starttls()
# server.login("YOUR EMAIL ADDRESS", "YOUR PASSWORD")
#
# msg = "YOUR MESSAGE!"
# server.sendmail("YOUR EMAIL ADDRESS", "EMAIL ADDRESS TO SEND TO", msg)
# server.quit()