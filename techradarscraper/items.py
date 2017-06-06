from datetime import datetime

from scrapy import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Compose, MapCompose


class Tech(Item):
    name = Field()
    category = Field()
    timeline = Field()


class TimelineCheckpoint(Item):
    date = Field()
    level = Field()
    description = Field()


def load_timeline(loader, timeline_items):
    def load_timeline_item(item):
        return TimelineCheckpointLoader(selector=item).load_item()

    return map(load_timeline_item, timeline_items)


def trim(loader, items):
    return next(map(str.strip, items))


def parse_timeline_dates(loader, dates):
    return map(lambda date_string: datetime.strptime(date_string, '%b %Y'), dates)


def clean(loader, text):
    return text[0].root.text_content()


class TechLoader(ItemLoader):
    default_item_class = Tech

    default_output_processor = TakeFirst()

    timeline_in = load_timeline
    timeline_out = Compose(MapCompose(dict), list)

    def __init__(self, item=None, selector=None, response=None, parent=None, **context):
        super().__init__(item, selector, response, parent, **context)
        self.add_css('name', '#blip-view > div:nth-child(1) > h2::text')
        self.add_css('category', '#blip-view > div:nth-child(1) > a::text')
        self.add_value('timeline', response.css('#blip-view .blip-timeline > .blip-timeline-item'))


class TimelineCheckpointLoader(ItemLoader):
    default_item_class = TimelineCheckpoint

    default_output_processor = TakeFirst()

    date_in = parse_timeline_dates
    level_in = trim
    description_in = clean

    def __init__(self, item=None, selector=None, response=None, parent=None, **context):
        super().__init__(item, selector, response, parent, **context)
        self.add_css('date', '.blip-timeline-item__time::text')
        self.add_css('level', '.blip-timeline-item__ring > span::text')
        self.add_value('description', selector.css('.blip-timeline-item__lead'))
