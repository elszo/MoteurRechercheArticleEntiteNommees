import scrapy
from scrapy.crawler import CrawlerProcess
from scrapySqlite.scrapySqlite.spiders.scrap_spider import  ScrapingSpider
from scrapy.settings import Settings
from scrapySqlite.scrapySqlite import settings
import sqlite3
import nltk
nltk.data.path.append('C:\\Users\\ACER\\AppData\\Roaming\\nltk_data')
nltk.download('punkt')
from nltk import word_tokenize
from nltk.corpus import stopwords
import spacy
nlp = spacy.load("fr_core_news_sm")
from datetime import datetime
import locale
locale.setlocale(locale.LC_TIME, '')


def triertDict(value):
    return datetime.strptime(value['DatePub'], "%d %B, %Y %H:%M:%S")

def rechercherArticle(texte):
    conn = sqlite3.connect("seneweb.db")
    cur = conn.cursor()
    #doc = nlp(texte)
    articles = []
    token = word_tokenize(texte)
    stp = stopwords.words('french')
    mots = [word for word in token if word not in stp]

    for entity in mots:
        #ent = entity.text.lower()
        ent = entity.lower()
        resultats = cur.execute("""SELECT * FROM articles WHERE entites like ?
                               """,('%'+ent+'%', ))
        for art in resultats.fetchall():
            dt_object = datetime.strptime(art[3], "%Y-%m-%d %H:%M:%S")
            articles.append({"Type": art[0],
                             "Titre": art[1],
                             "Texte": art[2],
                             "DatePub": datetime.strftime(dt_object, "%d %B, %Y %H:%M:%S"),
                            "Source": art[4],
                             "NombreVue": art[5],
                             "Lien": art[9]})

    ListePrincipale = sorted(articles, key=triertDict, reverse=True)
    return ListePrincipale

def scraperArticle():
    lance_scrapy = CrawlerProcess()
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    lance_scrapy = CrawlerProcess(settings=crawler_settings)
    lance_scrapy.crawl(ScrapingSpider)
    lance_scrapy.start()
