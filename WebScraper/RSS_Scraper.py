import json
import requests
import xmltodict

class rss_scraper:

    def __init__(self,url_list:list,post_url:str='http://127.0.0.1:3000/articles'):
        self.url_list = url_list
        self.post_url = post_url

    def get_articles(self):
        # Pour chacun des liens présents ci-dessus
        for link in self.url_list:
            print(link)

            # On y accède
            r = requests.get(link)

            # Transforme son contenu en dictionnaire
            r_dict = xmltodict.parse(r.text)

            # Puis en JSON
            r_json = json.dumps(r_dict)
            articles_json = json.loads(r_json)

            # Comme chaque article est sous un 'item', on les prend tous
            articles = articles_json['rss']['channel']['item']

            # Pour chacun de ces "items" (/articles)
            for i in range(0, len(articles)):
                # On ajoute le champ 'feed_id'
                # Son feed_id sera le lien d'où il vient
                articles[i]['feed_id'] = link

                # Et à l'adresse voulu (app Flask) on envoie le JSON récolté dans la requête pour mise en base de donnée de l'article.
                x = requests.post(self.post_url, json=articles[i])





