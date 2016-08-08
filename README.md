# Launch-Locator

## Description
A Python web crawler that searches for information on new commercial satellite launches. This program traverses through a list of websites, crawls through the HTML of the page in search of keywords, and sends out a notification when it finds any useful information on new satellite launches, new launch vehicles/busses, new launch dates, etc.

## Dependencies
Launch Locator is built upon Python 2.7. It uses the following libraries/modules:  
    - urllib2
    - smtplib
    - BeautifulSoup4 (requires installstaion if you don't already have it)