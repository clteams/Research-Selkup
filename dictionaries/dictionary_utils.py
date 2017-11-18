import sqlite3
import json
DATABASE_PATH = './resources/dictionary.sqlite3'

def get_selkup_by_meaning(meaning):
    #TODO: cache connection
    #TODO: use json utils
    selkup_words = []
    with sqlite3.connect(DATABASE_PATH) as conn:
        c = conn.cursor()
        codepoints_meaning = str(meaning.encode("unicode_escape")).strip('b').strip("'").replace('\\\\', '\\')
        t = ('%\"'+ codepoints_meaning + '\"%',)
        c.execute("SELECT d.content, d.title FROM srds_dictionary d WHERE content like ?", t)
        for word in c.fetchall():
            word_json = json.loads(word[0])
            title = word[1]
            selkup_words.append(title)

    return selkup_words

#print(get_selkup_by_meaning('топор'))