# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from TOTP.items import TotpChart, TotpTrack
from scrapy import signals
from scrapy.contrib.exporter import JsonLinesItemExporter

class TotpPipeline(object):

    def __init__(self):
        self.files = {}
        self.ids_seen = set()
        
    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline
    
    def spider_opened(self, spider):
        TrackFile = open('tracks.json', 'w+b')
        self.files['tracks'] = TrackFile
        self.TrackExporter = JsonLinesItemExporter(TrackFile)
        self.TrackExporter.start_exporting()
        
        ChartFile = open('charts.json', 'w+b')
        self.files['charts'] = ChartFile
        self.ChartExporter = JsonLinesItemExporter(ChartFile)
        self.ChartExporter.start_exporting()
        
    def spider_closed(self, spider):
        self.ChartExporter.finish_exporting()
        self.TrackExporter.finish_exporting()
        for file in self.files.values():
            file.close()
    
    def process_item(self, item, spider):
        # TODO: Separate tracks from charts, save to different JSON files.        
        if isinstance(item, TotpChart):
            if item['date'] not in self.ids_seen:
                self.ChartExporter.export_item(item)
                self.ids_seen.add(item['date'])
        elif isinstance(item, TotpTrack):
            if item['trackID'] not in self.ids_seen:
                self.TrackExporter.export_item(item)
                self.ids_seen.add(item['trackID'])
        return item
