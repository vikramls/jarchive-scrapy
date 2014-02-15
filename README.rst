jarchive-scrapy
===============

Scrape j-archive pages using scrapy. 

A quick project to learn scrapy and prepare for Jeopardy! 

Dependencies
------------
Python2.7 since scrapy needs python27 and sqlite3 (from the standard library). Here's what pip freeze looks like:

* Scrapy==0.22.1
* Twisted==13.2.0
* cssselect==0.9.1
* lxml==3.3.0
* pyOpenSSL==0.13.1
* queuelib==1.1.1
* six==1.5.2
* w3lib==1.5
* wsgiref==0.1.2
* zope.interface==4.1.0

Run
---

# Install scrapy using ``pip install scrapy``. 
# Clone this repository
# ``cd`` into the clone and issue ``scrapy crawl jarchive``
# ``jarchive.sqlite`` will be created after the crawler finishes.
