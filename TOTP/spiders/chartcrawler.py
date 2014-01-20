from scrapy.spider import Spider
from scrapy.selector import Selector
from TOTP.items import TotpChart, TotpTrack
from scrapy.http import Request, Response
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc

class ChartCrawler(Spider):
    name = "TOTP"
    allowed_domains = ["officialcharts.com"]
    start_urls = ["http://www.officialcharts.com/archive/music/"]
    
    def parse(self, response):        
        sel = Selector(response)
        
        # Construct per-year URLs from the dropdown box
        base = urljoin_rfc(get_base_url(response),sel.css('#yearSelectSingles::attr(action)').extract()[0])
        years = sel.css('.year option::attr(value)').extract()
        
        # Crawl each yearly URL for the weekly charts
        for year in years:
            URL = urljoin_rfc(base,year)
            yield Request(URL, self.parseYear, meta={'year':year})
            
    def parseYear(self, response):
        base = get_base_url(response)
        
        sel = Selector(response)
        weeks = sel.css('.entry')
        for week in weeks:
            weekNumber = week.css('.week::text').extract()[0]
            date = week.css('.date::text').extract()[0]
            URL = urljoin_rfc(base,week.css('.links a::attr(href)').extract()[0])
            yield Request(URL,self.parseChart,meta=dict(response.meta,week=weekNumber,date=date))
        
    def parseChart(self, response):        
        chart = TotpChart()
        chart['week'] = response.meta['week']
        chart['date'] = response.meta['date']
        chart['year'] = response.meta['year']
        
        chart['tracks'] = []
        
        sel = Selector(response)
        tracks = sel.css('.entry')
        for track in tracks:
            trackItem = TotpTrack()
            
            # Don't use these just now, assume tracks returned in order
            # TODO: check this assumption
            position = track.css('.currentposition::text').extract()[0]
            prev_position = track.css('.lastposition::text').extract()[0]
            
            infobox = track.css('.infoHolder')
            trackItem['title'] = infobox.xpath('h3/text()').extract()[0]
            trackItem['artist'] = infobox.xpath('h4/text()').extract()[0]
            trackItem['img_url'] = infobox.css('.coverimage::attr(src)').extract()[0]
            trackItem['trackID'] = hash((trackItem['artist'],trackItem['title']))
            
            chart['tracks'].append(trackItem['trackID'])
            
            yield trackItem
            
        yield chart         