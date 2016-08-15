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

# Logic to determine what type of report to send
reportSwitch = raw_input('Would you like a full report on my search results? (y/n)\n')
if reportSwitch == 'y':
    reportSwitch = True
elif reportSwitch == 'n':
    reportSwitch = False
else:
    print 'Invalid input. By default, I will send out a full report'
    reportSwitch = True

print 'I will now begin searching for launch information that might help you.\n'

# Reads URLs from ./config/WebsiteList.txt and stores in websiteList
websiteListFile = open("./config/WebsiteList.txt", "r")
websiteList = websiteListFile.read().split('\n')
websiteListFile.close()

print 'Website list initially looks like: ', websiteList

# Reads keywords from ./config/Keywords.txt and stores in keywordList
keywordFile = open('./config/Keywords.txt', 'r')
keywordList = keywordFile.read().split('\n')
keywordFile.close()

urlSet = Set(websiteList) # create a set from the list original list of websites
print 'urlSet initially looks like: ', urlSet

msg = "YOUR MESSAGE!" # string for email message

# Pop url's and pass them into search module
while len(websiteList) > 0:                                   # while there's still links to search
    currentLink = websiteList.pop()                           # pop a link into a variable
    print 'After popping, websiteList now looks like: ', websiteList
    print 'LOOKING AT ', currentLink
    page = urllib2.urlopen(currentLink).read().lower()        # stores lowercase HTML into variable
    soup = BeautifulSoup(page, 'html.parser')                 # pass html into BeautifulSoup constructor
    for link in soup.find_all('a'):                           # find external links and add them to urlSet
        embeddedURL = link.get('href')
        print embeddedURL
        print embeddedURL in urlSet
        if not embeddedURL in urlSet:
            print 'Adding ', embeddedURL, ' to urlSet'
            urlSet.add(embeddedURL)
            print 'After adding, urlSet now looks like: ', urlSet
            websiteList.append(embeddedURL)
    print 'Looking for keywords within', currentLink
    for keyword in keywordList:
        wordAppearance = htmlCrawler(keyword.lower(), page)
        print 'The word', keyword, 'appeared', wordAppearance, 'times.'
    print '\n'

# Make program send email about this information
print 'Invoking report system'

if reportSwitch:                                                    # reportSwitch received earlier
    # logic for sending a report within an email
    senderAddress = raw_input('What is your Gmail address?\n')
    senderPassword = raw_input('What is your Gmail password?\n')
    receiverEmail = raw_input('Who would you like to send the report to?\n')

    print 'Attempting to login to the gmail server with your credentials'
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(senderAddress, senderPassword)

    print 'The message that will be sent is:'
    print msg
    server.sendmail(senderAddress, receiverEmail, msg)
    server.quit()
else:
    print 'Have a nice day.'