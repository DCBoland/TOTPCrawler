# Scrapy settings for TOTP project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'TOTP'

SPIDER_MODULES = ['TOTP.spiders']
NEWSPIDER_MODULE = 'TOTP.spiders'
ITEM_PIPELINES = {
    'TOTP.pipelines.TotpPipeline': 100,
}

RETRY_ENABLED = False

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'TOTP (+http://www.yourdomain.com)'
