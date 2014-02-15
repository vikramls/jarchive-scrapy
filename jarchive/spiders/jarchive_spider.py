import re

from scrapy.spider import Spider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector

from jarchive.items import JarchiveItem

ANSWER_PREFIX = 'correct_response&quot;&gt;'
ANSWER_SUFFIX = '&lt;/em&gt;'
FJ_ANSWER_PREFIX = '\&quot;correct_response\&quot;&gt;'
FJ_ANSWER_SUFFIX = '&lt;/em&gt;'

class Question(object):
    __slots__ = ('id', 'text', 'ans', 'value', 'url_id', 'type', 'cat',  'round')
    pass

def process_div(div, cats, jround):
    fields = div.extract().split('"')
    f1 = fields[1]
    f3 = fields[3]
    q_id = f1[f1.find("toggle('")+len("toggle('"):f1.find(',')][:-1]
    q_text = f3[f3.find("_stuck', ") + len("_stuck',"):][2:-2]
    q_ans = f1[f1.find(ANSWER_PREFIX)+len(ANSWER_PREFIX):f1.find(ANSWER_SUFFIX)]
    q_value = ''
    q_url_id = ''
    q_type = ''
    q_cat = ''

    f13 = fields[13]
    f14 = fields[14]
    f17 = fields[17]
    q_value = f14[f14.find('>$')+len('>$'):f14.find('<')]
    q_url_id = f17.split('=')[1]
    if 'double' in f13:
        q_type = 'double'

    q_cat = cats[int(q_id.split('_')[2])-1]
    return (q_id, q_text, q_ans, q_value, q_url_id, q_type, q_cat, jround)

def process_div_j(div, j_cats):
    jround = 'jeopardy'
    return process_div(div, j_cats, jround)

def process_div_dj(div, dj_cats):
    jround = 'double_jeopardy'
    return process_div(div, dj_cats, jround)

def process_div_fj(div):
    q_cat = div.xpath('.//table//tr//td[@class="category_name"]/text()').extract()[0]
    tmp = div.xpath('@onmouseout').extract()[0]
    q_id = 'FJ'
    q_text = tmp[tmp.find('_stuck\', \'') + len('_stuck\', \''):tmp.find('\')')]
    tmp2 = div.xpath('@onmouseover').extract()[0]
    q_ans = tmp2[tmp2.find(FJ_ANSWER_PREFIX) + len(FJ_ANSWER_PREFIX):tmp2.find(FJ_ANSWER_SUFFIX)]
    q_value = ''
    q_url_id = ''
    q_type = ''
    return q_id, q_text, q_ans, q_value, q_url_id, q_type, q_cat, 'final_jeopardy'


class JarchiveSpider(CrawlSpider):
    name = "jarchive"
    allowed_domains = ["www.j-archive.com",]
    #start_urls = ["http://www.j-archive.com/showgame.php?game_id=4420"]
    start_urls = ['http://www.j-archive.com/']
    rules = (
        Rule(SgmlLinkExtractor(allow=('showseason\.php'))),
        Rule(SgmlLinkExtractor(allow=('showgame\.php', )), callback='parse_game'),
    )

    def parse_game(self, response):
        questions = []
        sel = Selector(response)
        j_divs = sel.xpath('//div[@id="jeopardy_round"]//div')
        j_cats = sel.xpath('//div[@id="jeopardy_round"]//table[@class="round"]//tr//td[@class="category"]//table//tr//td[@class="category_name"]/text()').extract()
        dj_divs = sel.xpath('//div[@id= "double_jeopardy_round"]//div')
        dj_cats = sel.xpath('//div[@id="double_jeopardy_round"]//table[@class="round"]//tr//td[@class="category"]//table//tr//td[@class="category_name"]/text()').extract()
        fj_divs = sel.xpath('//div[@id= "final_jeopardy_round"]//div')
        item = JarchiveItem()
        item['game_title'] = sel.xpath('//div[contains(@id, "game_title")]/h1/text()').extract()
        item['game_number'] = item['game_title'][0].split()[1][1:]
        item['game_url'] = response.url
        item['game_id'] = item['game_url'].split('=')[1]

        for div in j_divs:
            question = process_div_j(div, j_cats)
            questions.append(question)
            
        for div in dj_divs:
            question = process_div_dj(div, dj_cats)
            questions.append(question)

        for div in fj_divs:
            question = process_div_fj(div)
            questions.append(question)

        item['questions'] = questions
        return item
