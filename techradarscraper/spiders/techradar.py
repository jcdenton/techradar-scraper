import scrapy
import scrapy.spiders

from techradarscraper.items import TechLoader


class TechRadarSpider(scrapy.spiders.Spider):
    name = 'techradar'
    start_urls = ['https://www.thoughtworks.com/radar/a-z']

    def parse(self, response):
        links = response.css('.a-z-links > ul > li.blip.hit > a')
        for link in links:
            title = link.css('::text').extract_first()
            href = link.css('::attr(href)').extract_first()
            url = response.urljoin(href)
            yield scrapy.Request(url, self.parse_tech)

    def parse_tech(self, response):
        return TechLoader(response=response).load_item()


if __name__ == '__main__':
    from scrapy.utils.project import get_project_settings
    settings = get_project_settings()
    settings.setdict({
        'LOG_LEVEL': 'INFO',
        'OUTPUT_FILENAME': '../../out/techradar.json',
        'ITEM_PIPELINES': {
            'techradarscraper.pipelines.JsonWriterPipeline': 300,
        },
    })

    from scrapy.crawler import CrawlerProcess
    process = CrawlerProcess(settings)
    process.crawl(TechRadarSpider)
    process.start()
