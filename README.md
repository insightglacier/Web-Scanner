# Web Scanner

## Description
A Python web crawler that searches for keywords within specified webpages. This script traverses through a list of websites, crawls through the HTML of the pages in search of keywords, and sends out an email report on what it finds. It also has the ability to visit embedded links within a webpage based on whether the link contains a keyword.

## Dependencies
Web Scanner is built upon Python 2.7. It uses the following libraries/modules:  
- urllib2
- smtplib
- Set
- BeautifulSoup4 (requires installstaion)
