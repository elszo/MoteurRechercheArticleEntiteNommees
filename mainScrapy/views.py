from django.shortcuts import render, redirect
#from django.http import HttpResponse
#from django.template import loader
from scrapySqlite.scrapySqlite.main import *
from mainScrapy.forms import *
import unicodedata
from scrapy.crawler import CrawlerProcess
from scrapySqlite.scrapySqlite.spiders.scrap_spider import  ScrapingSpider
from scrapy.settings import Settings
from scrapySqlite.scrapySqlite import settings
import sys
import re
import gpt_2_simple as gpt2


def index(request, message=""):
    #template = loader.get_template("accueil.html")
    form = SearchForm(request.POST or None)
    text_recherche = ""
    result = []
    text_result = ""
    summarized_text = ""
    if form.is_valid():
        text_recherche = unicodedata.normalize('NFD', form.cleaned_data["texte"]).encode('ascii', 'ignore')
        text_recherche = str(text_recherche)[2:-1]
        liste_art = rechercherArticle(text_recherche)
        if len(liste_art) != 0:
            result.append(liste_art[0])
        for el in liste_art:
            res = []
            for r in result:
                res.append(r['Titre'])
            if el['Titre'] not in res:
                result.append(el)
                text_result += el['Texte']

    text_result = re.sub('\(|\)|,|"|«|»|–', '', text_result)
    """sess = gpt2.start_tf_sess()
    sess = gpt2.reset_session(sess)
    gpt2.load_gpt2(sess, run_name='run1')
    texte_resume = gpt2.generate(sess,
                              length=300,
                              temperature=0.8,
                              top_k=50,
                              return_as_list=True,
                              prefix=text_result)"""

    content = {"Titre": "Recherche Article", "form": form, "Resultats": result,
               "text_recherche": text_recherche, "message": message, "text_result": text_result,
               "Texte": "Moteur de recherche d'articles basé sur les entités nommées"}
    return render(request, "accueil.html", content)

def scrapyView(request):
    message = ""
    if "twisted.internet.reactor" not in sys.modules:
        #del sys.modules["twisted.internet.reactor"]
        lance_scrapy = CrawlerProcess()
        crawler_settings = Settings()
        crawler_settings.setmodule(settings)
        lance_scrapy = CrawlerProcess(settings=crawler_settings)
        lance_scrapy.crawl(ScrapingSpider)
        lance_scrapy.start()
        message = "Succès de l'extraction des articles !"
    #form = SearchForm(request.POST or None)
    return index(request, message=message)