# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class JarchiveItem(Item):
    game_title = Field()
    game_number = Field()
    game_url = Field()
    game_id = Field()
    questions = Field()
    
    
    pass
