# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ScrapysqliteItem(scrapy.Item):
        categorie = scrapy.Field()
        titre = scrapy.Field()
        texte = scrapy.Field()
        datePub = scrapy.Field()
        sourceA = scrapy.Field()
        nombreVue = scrapy.Field()
        nombreAudiance = scrapy.Field()
        commentaire = scrapy.Field()
        entite = scrapy.Field()
        lien = scrapy.Field()
