# Scrapy settings for jarchive project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'jarchive'

SPIDER_MODULES = ['jarchive.spiders']
NEWSPIDER_MODULE = 'jarchive.spiders'

ITEM_PIPELINES = {
    'jarchive.pipelines.JarchivePipeline':100,
    'jarchive.pipelines.JarchiveSQLPipeline':200
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'jarchive (+http://www.example.org)'
