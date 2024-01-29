#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#        arquivador.py
#
#        (C) 2011-2024 Alchimista <alchimistawp@gmail.com>
#
#         Distributed under the terms of the GNU GPL license.
#

import pywikibot
from pywikibot import pagegenerators
import re
from datetime import datetime

from dateutil.relativedelta import relativedelta as timediff

datedic = {
    'jan': u"Janeiro",
    'fev': u"Fevereiro",
    'mar': u"Março",
    'abr': u"Abril",
    'mai': u"Maio",
    'jun': u"Junho",
    'jul': u"Julho",
    'ago': u"Agosto",
    'set': u"Setembro",
    'out': u"Outubro",
    'nov': u"Novembro",
    'dez': u"Dezembro",
}


def standardize(string):
    for char in '^$[].|?+*{}()/=:;-':
        if not char in string: continue
        string = string.replace(char, '\\' + char)
    return string


def main():
    original = [u"wikipedia:Esplanada/geral", u"wikipedia:Esplanada/propostas"]
    site = pywikibot.Site()

    now = datetime.utcnow()

    def difftime(self):
        sp = pywikibot.Page(site, self)
        print("--- ", sp.title())


        if sp.exists():
            sp.get()


        elif sp.isRedirectPage():
            sp = sp.getRedirectTarget()



        else:
            # if page doesn't exist, we'll use my up to force
            # the timediff to be more than 14 days.
            return 30
            # return sp

        tempo = sp.editTime()

        if tempo == 0:
            tempo = now

        t = datetime.strptime(str(tempo), "%Y-%m-%dT%H:%M:%SZ")
        diff = timediff(now, t)
        if diff.months >= 1:
            days = 20 + diff.days
        else:
            days = diff.days
        return days

    def removelink(tit, text):
        linksr = (u'{{discussão2|%s|%s|%s}}\n{{:%s}}\n' % (tit[0], tit[1],
                                                           tit[2], tit[3]))
        linksrt = re.compile(standardize(linksr))
        ntext = re.sub(linksrt, u"", text)
        if text == ntext:
            linksr2 = (u'{{discussão2|%s|%s|%s}}\n[[:%s]]\n' % (tit[0], tit[1],
                                                                tit[2], tit[3]))
            linksrt2 = re.compile(standardize(linksr2))
            ntext = re.sub(linksrt2, u"", text)
        pywikibot.showDiff(text, ntext)
        text = ntext
        return text

    for esplanada in original:
        original = pywikibot.Page(site, esplanada)
        try:
            text = original.get()
        except pywikibot.IsRedirectPage:
            original = original.getRedirectTarget()
            try:
                text = original.get()
            except Exception:
                pass

        lr = re.compile(
            u'\{\{discussão2\|(?P<titulo>.*?)\|(?P<data>.*?)\|(?P<esplanada>.*?)\}\}\n(?:\{\{|\[\[)\:(?P<parte2>.*?)(?:\}\}|\]\])',
            re.I | re.M | re.U)
        links = lr.findall(text)
        print(links)
        for tit in links:
            print("tit: ", tit)
            pywikibot.output(tit[3])
            days = difftime(tit[3])
            print("d-", days)
            if days > 14:
                text = removelink(tit, text)

        print(esplanada)
        text = re.sub(r"\n\n\n(\n*)", "\n\n", text)
        pywikibot.showDiff(original.get(), text)
        original.put(text, minor=False,
                     summary=u"[[wp:BOT|BOT]]: A arquivar discussões com mais de 14 dias de inactividade.")


if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()

