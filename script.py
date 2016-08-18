# Launch Locator
# A Python web crawler for new satellite launch information
# By Jeffrey Chan, August 2016

import urllib2
import smtplib
from bs4 import BeautifulSoup
from sets import Set

# Search Function
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

# Start of Program
print 'Welcome to Launch Locator!'

# Logic to determine what type of report to send
fullReport = raw_input('Would you like a full report on my search results? (y/n)\n')
if fullReport == 'y':
    fullReport = True
elif fullReport == 'n':
    print 'Got it. I will send a statistics summary instead.'
    fullReport = False
else:
    print 'Invalid input. By default, I will send out a stats summary'
    fullReport = False

print 'I will now begin searching for launch information that might help you.\n'

# Reads URLs from ./config/WebsiteList.txt and stores in websiteList (stack)
websiteListFile = open("./config/WebsiteList.txt", "r")
websiteList = websiteListFile.read().split('\n')
websiteListFile.close()

# Reads keywords from ./config/Keywords.txt and stores in keywordList
keywordFile = open('./config/Keywords.txt', 'r')
keywordList = keywordFile.read().split('\n')
keywordFile.close()

# set will help with identifying unique and unvisited links
urlSet = Set(websiteList)

# Headers for report
msg = "Launch Locator"
if fullReport:
    msg += ' Full Report \n\n'
else:
    msg += ' Statistics Summary \n\n'


# Pop urls off stack and passes them into search function
while len(websiteList) > 0:
    currentLink = websiteList.pop()
    page = urllib2.urlopen(currentLink).read().lower()   # stores lowercase HTML into page
    soup = BeautifulSoup(page, 'html.parser')  # pass html into BeautifulSoup constructor

    # Searches for keywords first
    if fullReport:
        print 'Observing:', currentLink
        msg += 'Link: ' + currentLink + '\n'
        for tag in soup.find_all(["p", "h1", "h2", "h3", "a"]): # finds listed tags
            text = tag.string # get just the text from the HTML tags
            if (text is None) or not all(ord(c) < 128 for c in text): # can't handle non ascii chars
                continue
            textHits = 0
            for keyword in keywordList:
                textHits += htmlCrawler(keyword, text)
            if textHits > 0:
                msg += '\"' + text + '\"\n'
        msg += '\n'
        print '\n'

    else:
        print 'Observing:', currentLink
        msg += 'Link: ' + currentLink + '\n'
        for keyword in keywordList:
            wordAppearance = htmlCrawler(keyword.lower(), page)
            print 'The word', keyword, 'appeared', wordAppearance, 'times.'
            msg += 'The word ' + keyword + ' appeared ' + str(wordAppearance) + ' times.' + '\n'
        msg += '\n'
        print '\n'

    # Processes embedded links second
    for link in soup.find_all('a'):
        embeddedURL = link.get('href')
        linkHits = 0
        for keyword in keywordList:
            linkHits += htmlCrawler(keyword, str(embeddedURL))
        # if unvisited, unique, valid (contains 'http'), and contains a keyword, push onto websiteList stack
        if (not embeddedURL in urlSet) and htmlCrawler('http', str(embeddedURL)) == 1 and linkHits > 0:
            urlSet.add(embeddedURL)
            websiteList.append(embeddedURL)

# Logic for Email System
print 'Invoking report system'

# Sender/Receiver Information
senderAddress = raw_input('What is your Gmail address?\n')
senderPassword = raw_input('What is your Gmail password?\n')
receiverEmail = raw_input('Who would you like to send the report to?\n')

print '\nAttempting to login to the gmail server with your credentials\n'
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(senderAddress, senderPassword)

print 'The message that will be sent is:\n'
print msg
server.sendmail(senderAddress, receiverEmail, msg)
server.quit()