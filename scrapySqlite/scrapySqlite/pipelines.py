import sqlite3

class ScrapysqlitePipeline:
        # Connection SQLITE
        def __init__(self):
            self.conn = sqlite3.connect("seneweb.db")
            self.cur = self.conn.cursor()
            self.create_table()

        def create_table(self):
            self.cur.execute("""create table if not exists articles(
            categorie text, titre text, texte text, datePub date, sourceA text,
            nombreVue int, nombreAudiance text, commentaires text, entites text, lien text)""")

        def process_item(self, item, spider):
            self.cur.execute("""INSERT OR IGNORE INTO articles VALUES (?,?,?,?,?,?,?,?,?,?)""",
                             (''.join(item['categorie'][0]), ' '.join(item['titre'][0]),
                              ' '.join(item['texte'][0]), item['datePub'][0],
                              ' '.join(item['sourceA'][0]), ' '.join(item['nombreVue'][0]),
                              ' '.join(item['nombreAudiance'][0]),
                              ' '.join(item['commentaire'][0]),
                              ';'.join(map(str, item['entite'])), item['lien']))

            self.conn.commit()
            return item
