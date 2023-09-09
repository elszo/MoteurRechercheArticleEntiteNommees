#from scrapy import Request, Spider
import scrapy
from scrapySqlite.scrapySqlite.items import ScrapysqliteItem
import spacy
nlp = spacy.load("fr_core_news_sm")
import locale
locale.setlocale(locale.LC_TIME, '')
from .functions_scrape_sites import *

class ScrapingSpider(scrapy.Spider):
    # Nom du spider
    name = "scrapingSqlite"
    art_url = []
    # URL de la page à scraper
    start_urls = [
        'https://www.seneweb.com/',
        'https://www.senenews.com/',
        'https://www.dakarbuzz.net/',
        'https://www.afrikmag.com/',
        'https://www.dakarmatin.com/'
    ]

    def __init__(self):
        self.links = []

    # Extraction de l'ensemble des liens
    BASE_URL = 'https://www.seneweb.com'

    def parse(self, response):
        #self.links.append(response.url)
        for elt in response.css('a.module_main_post_title').xpath('@href').extract():
            self.links.append(elt)
        for elt in response.css('a.secondUneFloat').xpath('@href').extract():
            self.links.append(elt)
        for elt in response.css('a.penci-image-holder').xpath('@href').extract():
            self.links.append(elt)
        for elt in response.css('h2.post-title a').xpath('@href').extract():
            self.links.append(elt)
        for elt in response.css('h3.jeg_post_title a').xpath('@href').extract():
            self.links.append(elt)


        for link in self.links:
            site = re.findall(re.compile('https'), link)
            site = ''.join(site)
            if site == "":
                self.absolute_url = self.BASE_URL + link
            else:
                self.absolute_url = link
            self.art_url = []
            self.art_url.append(self.absolute_url)
            #print(absolute_url)

            yield scrapy.Request(self.absolute_url, callback=self.parse_dir_contents)

    # Extraction de contenus des pages

    def parse_dir_contents(self, response):
        item = ScrapysqliteItem()
        scrape_seneweb(item, response)
        scrape_senenews(item, response)
        scrape_dakarbuzz(item, response)
        scrape_afrikmag(item, response)
        scrape_dakarmatin(item, response)

        yield item
