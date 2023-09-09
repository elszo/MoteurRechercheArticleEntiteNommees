import spacy
nlp = spacy.load("fr_core_news_sm")
from datetime import datetime
import re
import locale
locale.setlocale(locale.LC_TIME, '')


def find_base_url(lien):
    base_url = re.findall(re.compile('www\..*\..{3}'), lien)
    base_url = ''.join(base_url)
    return base_url

def scrape_seneweb(item, response):
    tous_article = response.css('div.posts_block_content')

    for article in tous_article:
        art_lien = str(response)
        if find_base_url(art_lien[4:-1]) == "www.seneweb.com":
            art_categorie = article.css('span.post_header_categ::text').extract()
            # art_categorie = response.xpath("//span[@class='post_header_categ']/text()").extract()
            art_titre = article.css('h1::text').extract()
            #art_titre = response.xpath("//h1/text()").extract()
            art_texte = article.css('font::text').extract()
            art_date = article.css('span[style="padding-left:0px;margin-left:0px"]::text').extract()
            art_source = article.css('span.meta_source a::text').extract()
            art_nombreVue = article.css('span[style="padding-right:0px;margin-right:0px"] span[style="color:#3973ac"]::text').extract()
            art_nombreAudiance = article.css('span[style="padding-right:0px;margin-right:0px;color:red"]::text').extract()
            art_commentaire = response.css('.comment_item_content span::text').extract()

            datePub = ''.join(map(str, art_date[0]))
            datePub = re.sub('à', '', datePub)
            datePub = re.sub('\s{2,}', ' ', datePub)[:-1]

            item['categorie'] = art_categorie,
            item['titre'] = art_titre,
            item['texte'] = art_texte,
            item['datePub'] = datetime.strptime(datePub, "%d %B, %Y %H:%M:%S"),
            item['sourceA'] = art_source,
            item['nombreVue'] = art_nombreVue,
            item['nombreAudiance'] = art_nombreAudiance,
            item['commentaire'] = art_commentaire,
            item['lien'] = art_lien[4:-1]

            string_titre = ''.join(item['titre'][0])
            string_texte = ''.join(item['texte'][0])
            string_categorie = ''.join(item['categorie'][0])

            doc = nlp(string_titre+' '+string_texte)
            #unicodedata.normalize('NFD', entity.text.lower()).encode('ascii', 'ignore')
            entite = [entity.text for entity in doc.ents]
            #entite = [str(ent) for ent in entite]
            #entite = [ent[2:-1] for ent in entite]
            entite.append(string_categorie.lower())
            item['entite'] = set(entite)

def scrape_senenews(item, response):
    tous_article = response.css('div.single_page')

    for article in tous_article:
        art_lien = str(response)
        if find_base_url(art_lien[4:-1]) == "www.senenews.com":
            art_categorie = article.css('nav.rank-math-breadcrumb p a::text').extract()
            # art_categorie = response.xpath("//span[@class='post_header_categ']/text()").extract()
            art_titre = article.css('h1.entry-title::text').extract()
            #art_titre = response.xpath("//h1/text()").extract()
            art_texte = article.css('div.content-single-full p::text').extract()
            art_date = article.css('span.date::text').extract()
            art_source = article.css('a.aSingle::text').extract()
            art_nombreVue = article.css('div.jssocials-share-count-box span.jssocials-share-count::text').extract()
            art_nombreAudiance = article.css('div.comments-area div.comments-title::text').extract()
            art_commentaire = article.css('div.lstcom p::text').extract()

            datePub = ''.join(art_date[0])
            datePub = re.sub('à', '', datePub)
            datePub = re.sub('\s{2,}', ' ', datePub)

            item['categorie'] = art_categorie[-1],
            item['titre'] = art_titre,
            item['texte'] = art_texte,
            item['datePub'] = datetime.strptime(datePub, "%d/%m/%Y %H:%M"),
            item['sourceA'] = art_source,
            item['nombreVue'] = art_nombreVue,
            item['nombreAudiance'] = art_nombreAudiance,
            item['commentaire'] = art_commentaire,
            item['lien'] = art_lien[4:-1]

            string_titre = ''.join(item['titre'][0])
            string_texte = ''.join(item['texte'][0])
            string_categorie = ''.join(item['categorie'][0])

            doc = nlp(string_titre+' '+string_texte)
            #unicodedata.normalize('NFD', entity.text.lower()).encode('ascii', 'ignore')
            entite = [entity.text for entity in doc.ents]
            #entite = [str(ent) for ent in entite]
            #entite = [ent[2:-1] for ent in entite]
            entite.append(string_categorie.lower())
            item['entite'] = set(entite)


def scrape_dakarbuzz(item, response):
    tous_article = response.css('div.header-style-header-1')

    for article in tous_article:
        art_lien = str(response)
        if find_base_url(art_lien[4:-1]) == "www.dakarbuzz.net":
            art_categorie = article.css('a.penci-cat-32::text').extract()
            # art_categorie = response.xpath("//span[@class='post_header_categ']/text()").extract()
            art_titre = article.css('h1.post-title::text').extract()
            #art_titre = response.xpath("//h1/text()").extract()
            art_texte = article.css('div.entry-content p::text').extract()
            art_date = article.css('time.entry-date::text').extract()
            art_source = article.css('a.author-url::text').extract()
            art_nombreVue = article.css('span[style="padding-right:0px;margin-right:0px"] span[style="color:#3973ac"]::text').extract()
            art_nombreAudiance = article.css('span.single-comment-o::text').extract()
            art_commentaire = response.css('.comment_item_content span::text').extract()


            datePub = ''.join(map(str, art_date[0]))
            datePub = re.sub('\s{2,}', ' ', datePub)

            item['categorie'] = art_categorie,
            item['titre'] = art_titre,
            item['texte'] = art_texte,
            item['datePub'] = datetime.strptime(datePub, "%d %B %Y"),
            item['sourceA'] = art_source,
            item['nombreVue'] = art_nombreVue,
            item['nombreAudiance'] = art_nombreAudiance,
            item['commentaire'] = art_commentaire,
            item['lien'] = art_lien[4:-1]

            string_titre = ''.join(item['titre'][0])
            string_texte = ''.join(item['texte'][0])
            string_categorie = ''.join(item['categorie'][0])

            doc = nlp(string_titre+' '+string_texte)
            #unicodedata.normalize('NFD', entity.text.lower()).encode('ascii', 'ignore')
            entite = [entity.text for entity in doc.ents]
            #entite = [str(ent) for ent in entite]
            #entite = [ent[2:-1] for ent in entite]
            entite.append(string_categorie.lower())
            item['entite'] = set(entite)


def scrape_afrikmag(item, response):
    tous_article = response.css('div.main-content')

    for article in tous_article:
        art_lien = str(response)
        if find_base_url(art_lien[4:-1]) == "www.afrikmag.com":
            art_categorie = article.css('a.post-cat::text').extract()
            # art_categorie = response.xpath("//span[@class='post_header_categ']/text()").extract()
            art_titre = article.css('h1.entry-title::text').extract()
            #art_titre = response.xpath("//h1/text()").extract()
            art_texte = article.css('div.entry-content p::text').extract()
            art_date = article.css('span.date::text').extract()
            art_source = article.css('a.author-name::text').extract()
            art_nombreVue = article.css('span.meta-views::text').extract()
            art_nombreAudiance = article.css('span.meta-comment::text').extract()
            art_commentaire = article.css('div.comment-content p::text').extract()

            datePub = ''.join(art_date[0])
            datePub = re.sub('à', '', datePub)
            datePub = re.sub('\s{2,}', ' ', datePub)

            item['categorie'] = art_categorie[-1],
            item['titre'] = art_titre,
            item['texte'] = art_texte,
            item['datePub'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            item['sourceA'] = art_source[-1],
            item['nombreVue'] = art_nombreVue[-1],
            item['nombreAudiance'] = art_nombreAudiance[0][-1],
            item['commentaire'] = art_commentaire,
            item['lien'] = art_lien[4:-1]

            string_titre = ''.join(item['titre'][0])
            string_texte = ''.join(item['texte'][0])
            string_categorie = ''.join(item['categorie'][0])

            doc = nlp(string_titre+' '+string_texte)
            #unicodedata.normalize('NFD', entity.text.lower()).encode('ascii', 'ignore')
            entite = [entity.text for entity in doc.ents]
            #entite = [str(ent) for ent in entite]
            #entite = [ent[2:-1] for ent in entite]
            entite.append(string_categorie.lower())
            item['entite'] = set(entite)


def scrape_dakarmatin(item, response):
    tous_article = response.css('div.jeg_inner_content')

    for article in tous_article:
        art_lien = str(response)
        if find_base_url(art_lien[4:-1]) == "www.dakarmatin.com":
            art_categorie = article.css('span.breadcrumb_last_link a::text').extract()
            # art_categorie = response.xpath("//span[@class='post_header_categ']/text()").extract()
            art_titre = article.css('h1.jeg_post_title::text').extract()
            #art_titre = response.xpath("//h1/text()").extract()
            art_texte = article.css('p.has-medium-font-size::text').extract()
            art_date = article.css('div.jeg_meta_date a::text').extract()
            art_source = article.css('div.jeg_meta_author a::text').extract()
            art_nombreVue = article.css('div.jeg_views_count div.counts::text').extract()
            art_nombreAudiance = article.css('div.jeg_meta_comment a::text').extract()
            art_commentaire = article.css('div.comment-content p::text').extract()

            datePub = ''.join(art_date[0])
            datePub = re.sub('-', '', datePub)
            datePub = re.sub('\s{2,}', ' ', datePub)

            item['categorie'] = art_categorie[-1],
            item['titre'] = art_titre,
            item['texte'] = art_texte,
            item['datePub'] = datetime.strptime(datePub, "%d %B %Y %H:%M"),
            item['sourceA'] = art_source,
            item['nombreVue'] = art_nombreVue,
            item['nombreAudiance'] = art_nombreAudiance,
            item['commentaire'] = art_commentaire,
            item['lien'] = art_lien[4:-1]

            string_titre = ''.join(item['titre'][0])
            string_texte = ''.join(item['texte'][0])
            string_categorie = ''.join(item['categorie'][0])

            doc = nlp(string_titre+' '+string_texte)
            #unicodedata.normalize('NFD', entity.text.lower()).encode('ascii', 'ignore')
            entite = [entity.text for entity in doc.ents]
            #entite = [str(ent) for ent in entite]
            #entite = [ent[2:-1] for ent in entite]
            entite.append(string_categorie.lower())
            item['entite'] = set(entite)