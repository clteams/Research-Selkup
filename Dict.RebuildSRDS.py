#!/usr/bin/python3
import sqlite3
import json
import re

srds_dictionary = sqlite3.connect('./databases/14-10-2017-build/dictionary.sqlite3')
dict_agent = srds_dictionary.cursor()

new_dictionary = sqlite3.connect('./new_dictionary.sqlite3')
new_dict_agent = new_dictionary.cursor()

index = 4610

srds = dict_agent.execute('select title, content from srds_dictionary').fetchall()
rx_ob_capital = r'[СШЧI]+'
dialect_codes = (
    ('ел', 'EL'),
    ('кет', 'KET'),
    ('вас', 'VAS'),
    ('тур', 'TUR'),
    ('тым', 'TYM')
)
prop_abbrs_source = {
    "апелл.": "gram[appell]",
    "бран. сл.": "sem[offensive]",
    "вас.": "dialect[VAS]",
    "ввод. сл.": "sem[parenthesis]",
    "вин. п.": "gram[case][acc]",
    "в.-обск.": "dialect[UpperOB]",
    "вр.": "gram[tense]",
    "возвр.": "gram[reflex]",
    "возвр. местм.": "gram[reflex][pronoun]",
    "возвр.-личн.": "gram[reflex/pers]",
    "вспом. гл": ("gram[aux][verb]", "pos[verb]"),
    "гидр.": "sem[hydronym]",
    "гл.": "pos[verb]",
    "гл.-дееприч. словосоч.": "gram[phrase][verb/transgressive]",
    "гл.-имен. словосоч.": "gram[phrase][rhema/onyma]",
    "гл.-наречн. словосоч.": "gram[phrase][verb/adverb]",
    "д.": "sem[toponym][village]",
    "дв. ч.": "gram[number][dual]",
    "дееприч.": "pos[transgressive]",
    "ед. ч.": "gram[number][sing]",
    "ел.": "dialect[EL]",
    "звукоподр.": "sem[onomatopoetic]",
    "ид.": "sem[idiom]",
    "имен. сказ.": "gram[onyma+onyma]",
    "имп.": "gram[tense][imperf]",
    "императ.": "gram[mood][imperative]",
    "имя действ.": "sem[name.of.action]",
    "исх. п.": "gram[case][abl]",
    "кет.": "dialect[KET]",
    "кетск.": "language[KET]",
    "колич. числ.": "pos[numeral][cardinal]",
    "коми-зыр.": "language[KOMI/ZYR]",
    "л.": "gram[person]",
    "личн. местм.": "gram[pronoun][pers]",
    "лишит.": "gram[case][abess]",
    "мед.": "sem[thesaurus.cat][medicine]",
    "межд.": "pos[interjection]",
    "местм.": ("pos[pronoun]", "gram[pronoun.related]"),
    "м. -вр. п.": "gram[case][local.temporal]",
    "миф.": "sem[thesaurus.cat][myth]",
    "мн. ч.": "gram[number][plur]",
    "мод сл.": "gram[modal]",
    "мод. част.": "pos[modal/part]",
    "нареч.": "pos[adverb]",
    "нареч. необл.": ("pos[adverb]", "sem[does.not.have]"),
    "нареч. неполн. степ. кач.": ("pos[adverb]", "sem[quantity.level.imperfection]"),
    "наст. вр.": "gram[tense][present]",
    "необл.": "sem[does.not.have]",
    "неопр. местм.": "pos[pronoun][indef]",
    "неопр. местм. нареч.": ("pos[adverb][indef]", "gram[pronoun.related]"),
    "неопр. нареч.": "pos[adverb][indef]",
    "неопр. числ.": "pos[numeral][indef]",
    "непер.": "gram[intrans]",
    "неполн. кач.": "sem[quantity.imperfection]",
    "н.п.": "sem[toponym][place]",
    "НС": "gram[aspect][imperfective]",
    "одуш.": "sem[anim]",
    "ойк.": "sem[oikonym]",
    "ор.-совм.": "gram[case][conjunctive]",
    "отгл.": "gram[verb.related]",
    "относит. местм.": "pos[pronoun][relative]",
    "отн. местм.": "pos[pronoun][relative]",
    "отр.": "sem[negative]",
    "отриц. гл.": ("sem[negative]", "pos[verb]"),
    "отриц. част.": ("sem[negative]", "pos[particle]"),
    "отым.": "gram[onyma.related]",
    "отым. прил. обл.": ("pos[adjective]", "gram[onyma.related]", "sem[does.have]"),
    "п.": "sem[toponym][village]",
    "пас.": "gram[mood][passive]",
    "пер.": "gram[transitive]",
    "побуд. част.": ("pos[particle]", "sem[imperative]"),
    "пог.": "sem[thesaurus.cat][proverb]",
    "подч., подчинит. союз": "pos[conjunction][subordinative]",
    "порядк. числ.": "pos[numeral][ordinal]",
    "посл.": "pos[postpositive]",
    "послов.": "sem[thesaurus.cat][proverb]",
    "преверб. гл.": ("pos[verb]", "gram[preverb]"),
    "предл.": "gram[sentence]",
    "приблиз.": "sem[approx]",
    "прил.": "pos[adjective]",
    "прил. необл.": ("pos[adjective]", "sem[does.not.have]"),
    "прил. обл.": ("pos[adjective]", "sem[does.have]"),
    "прил. облад.": ("pos[adjective]", "sem[does.have]"),
    "прил. ф.": ("pos[adjective]", "sem[predicative]"),
    "предик. ф.": ("pos[adjective]", "sem[predicative]"),
    "прит. местм.": "pos[pronoun][possessive]",
    "прич.": "pos[participle]",
    "произв.": "sem[derivative]",
    "прош. вр.": "gram[tense][perfect]",
    "против.": "sem[adversative]",
    "противит.": "sem[adversative]",
    "р.": "sem[hydronym][river]",
    "разд. посл.": ("pos[postpositive]", "sem[division]"),
    "разд. числ.": ("pos[numeral]", "sem[division]"),
    "русск.": "language[RUS]",
    "С": "gram[aspect][perfective]",
    "сакр.": "sem[thesaurus.cat][sacral]",
    "ск.": "sem[thesaurus.cat][fable]",
    "слож. посл.": ("pos[postpositive]", "gram[phrase]"),
    "слож. сл.": "gram[phrase]",
    "собир.": "sem[collective]",
    "соед. союз": "gram[copulative]",
    "сост.": "gram[state]",
    "сост. наим.": "gram[phrase]",
    "сочинит. союз": "pos[conjunction][coordinate]",
    "союз": "pos[conjunction]",
    "спр.": "gram[conjugation]",
    "сравн. констр.": ("gram[phrase]", "sem[comparative]"),
    "сравн. посл.": ("pos[postpositive]", "sem[comparative]"),
    "сравн. союз": ("pos[conjunction]", "sem[comparative]"),
    "ср.-обск.": "dialect[MiddleOB]",
    "субст.": ("gram[substantivation]", "gram[noun.related]"),
    "сущ.": "pos[noun]",
    "таб.": "sem[taboo]",
    "тюрк.": "language[TURK]",
    "указ. местм.": "pos[pronoun][demonstrative]",
    "уменьш.": "sem[diminutive]",
    "уничиж.": "sem[pejorative]",
    "уст. словосоч.": "gram[phrase]",
    "уступ. част.": ("pos[particle]", "sem[concessive]"),
    "финит.": "gram[finit]",
    "фольк.": "sem[thesaurus.cat][folk]",
    "хант.": "language[KHANT]",
    "част.": "pos[particle]",
    "числ.": "pos[numeral]",
    "чулым.": "language[CHUL]",
    "этн.": "sem[ethnonym]",
    "ю.": "sem[thesaurus.cat][yurt]"
}

prop_abbrs = dict()
for key in prop_abbrs_source:
    new_key = key.replace('.', r'\.*')
    new_key = r'^[\s\t]*' + re.sub(r'\s+', r'\s+', new_key) + r'[\s\t]*$'
    prop_abbrs[new_key] = prop_abbrs_source[key]

for row in srds:
    object = json.loads(row[1])
    values = []
    for lexic_group in object['lexic']:
        values += lexic_group['meaning']
    see = []
    if 'see' in object:
        see = object['see']
    titles = []
    for i, title in enumerate(object['title']):
        title_object = dict()
        title_object['dialects'] = []
        title_object['query'] = title['query']
        for dialect_group in title['dialects']:
            if 'об' in dialect_group and not re.search(rx_ob_capital, dialect_group):
                title_object['dialects'].append('OB.COMMON')
            elif 'об' in dialect_group:
                for dlc in re.findall(rx_ob_capital, dialect_group):
                    if dlc == 'С':
                        title_object['dialects'].append("OB.SU")
                    elif dlc == 'Ч':
                        title_object['dialects'].append("OB.CU")
                    elif "OB.SO" not in title_object['dialects']:
                        if dlc == 'Ш':
                            title_object['dialects'].append("OB.SO")
                        elif 'I' in dlc:
                            title_object['dialects'].append("OB.SO")
            else:
                for script, code in dialect_codes:
                    if script in dialect_group:
                        title_object['dialects'].append(code)
        def_props = []
        indef_props = []
        if 'props' in title:
            for prop in title['props']:
                for abbr in prop_abbrs:
                    prop_tag = prop_abbrs[abbr]
                    if re.search(abbr, prop):
                        if type(prop_tag) == str and prop_tag not in def_props:
                            def_props.append(prop_tag)
                        else:
                            for tag in prop_tag:
                                if tag not in def_props:
                                    def_props.append(tag)
                                else:
                                    indef_props.append(prop)

        new_dict_agent.execute(
            'insert into dictionary values (?, ?, ?, ?)',
            (index, 'dict.title', str(i), title_object['query']))
        new_dict_agent.execute(
            'insert into dictionary values (?, ?, ?, ?)',
            (index, 'dict.source', '@', 'srds'))
        new_dict_agent.execute(
            'insert into dictionary values (?, ?, ?, ?)',
            (index, 'dict.status', '@', 'proper'))
        for j, value in enumerate(values):
            new_dict_agent.execute(
                'insert into dictionary values (?, ?, ?, ?)',
                (index, 'dict.value', str(j), value))
        for j, dialect in enumerate(title_object['dialects']):
            new_dict_agent.execute(
                'insert into dictionary values (?, ?, ?, ?)',
                (index, 'dict.dialect', str(j), dialect))
        for j, prop in enumerate(def_props):
            new_dict_agent.execute(
                'insert into dictionary values (?, ?, ?, ?)',
                (index, 'dict.props.def', str(j), prop))
        for j, prop in enumerate(indef_props):
            new_dict_agent.execute(
                'insert into dictionary values (?, ?, ?, ?)',
                (index, 'dict.props.indef', str(j), prop))
        for j, see_link in enumerate(see):
            new_dict_agent.execute(
                'insert into dictionary values (?, ?, ?, ?)',
                (index, 'dict.see', str(j), 'srds'))

        index += 1
        print(index)


new_dictionary.commit()
new_dictionary.close()

srds_dictionary.commit()
srds_dictionary.close()