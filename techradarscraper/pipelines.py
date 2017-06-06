from datetime import datetime
from pathlib import Path

from scrapy.exporters import JsonItemExporter


class JsonWriterPipeline:
    @staticmethod
    def datetime_handler(d):
        if isinstance(d, datetime):
            return d.isoformat()
        return d

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get('OUTPUT_FILENAME'))

    def __init__(self, filename):
        self._filename = filename
        self._filepath = Path(filename)


    def open_spider(self, spider):
        Path(self._filepath.parent).mkdir(exist_ok=True)
        self._file = self._filepath.open('wb')
        self._exporter = JsonItemExporter(self._file, indent=2)
        self._exporter.start_exporting()

    def process_item(self, item, spider):
        self._exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self._exporter.finish_exporting()
        self._file.close()
