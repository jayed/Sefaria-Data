# -*- coding: utf-8 -*-

import requests, codecs, json
from bs4 import BeautifulSoup
from sefaria.model import *
import regex as re
from sources.functions import post_link
from data_utilities.util import getGematria, numToHeb

def scrape_wiki():
    url = u"https://he.wikipedia.org/wiki/%D7%9E%D7%A0%D7%99%D7%99%D7%9F_%D7%94%D7%9E%D7%A6%D7%95%D7%95%D7%AA_%D7%A2%D7%9C_%D7%A4%D7%99_%D7%A1%D7%A4%D7%A8_%D7%94%D7%97%D7%99%D7%A0%D7%95%D7%9A"

    page = requests.get(url)
    soup_body = BeautifulSoup(page.text, "lxml")
    tables = soup_body.select(".mw-parser-output > table")

    pairs = []
    links = []

    for table in tables:
        table_tr = table.select("tr")
        for col in table_tr:
            pairs.append((col.contents[1].text.strip(), re.sub(u'</?td>', u'', col.contents[-1].text).strip()))

    for pair in pairs:
        if re.search(u'ספר|מספר', pair[0]):
            continue
        neg_pos = u"Negative Mitzvot" if re.search(u"לאו", pair[1]) else u'Positive Mitzvot'
        rambam = getGematria(re.sub(u'עשה|לאו', u'', pair[1]).strip())
        chinukh = getGematria(pair[0])
        print chinukh, rambam
        chinukh_simanlen = len(Ref(u'Sefer HaChinukh.{}'.format(chinukh)).all_segment_refs())
        print neg_pos
        link = ({"refs": [
            u'Sefer HaChinukh.{}.{}-{}'.format(chinukh, 1, chinukh_simanlen),
            u'Mishneh Torah, {}.{}'.format(neg_pos, rambam)
        ],
            "type": "Sifrei Mitzvot",
            "auto": True,
            "generated_by": "chinukh_rambam_sfm_linker"  # _sfm_linker what is this parametor intended to be?
        })
        print link['refs']
        links.append(link)
        return links

def scrape_daat():
    url = u"http://www.daat.ac.il/daat/mitsvot/tavla.asp"

    page = requests.get(url)
    soup_body = BeautifulSoup(page.text, "lxml")
    rows = soup_body.select("tr td > h2")
    for row in rows:
        print row


if __name__ == "__main__":
    rambam_chinukh_lnks = scrape_wiki()
    # post_link(rambam_chinukh_lnks, VERBOSE=True)
    # scrape_daat()


