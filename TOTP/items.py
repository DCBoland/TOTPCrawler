# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class TotpChart(Item):
    date = Field()
    year = Field()
    week = Field()
    tracks = Field()

class TotpTrack(Item):
    trackID = Field()
    title = Field()
    artist = Field()
    img_url = Field()
