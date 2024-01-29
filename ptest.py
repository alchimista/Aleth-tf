#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       ptest.py
#       
#       (C) 2011 - 2024 Alchimista <alchimista@toolserver.org>
# 		
#		Distributed under the terms of the GNU GPL license.
#  
"""
This bot is still in an experimental fase, do not use it.
The bot script will go throw local sandbox pages, if the page content is diferent than
<!--não apague esta linha-->{{página de testes}}<!--não apague esta linha-->\n<!--Escreva abaixo da linha! -------------------------------- -->'
it will substitute it for that code.

To do:
* Add feature so that it only cleans the page after X minutes (need a nasty wrapper)
* Clean up the messy code (provably some day)
* Fix timer outputs

"""

import pywikibot
from pywikibot import pagegenerators
from datetime import datetime
from dateutil.relativedelta import relativedelta as timediff

site = pywikibot.Site('pt', 'wikipedia')

now = datetime.utcnow()
pywikibot.output("Horas: %s (UTC)" % now)

# Lista de páginas de testes a limpar
n = ['1','2','3','4']
ns = ['Ajuda', 'Ajuda discussão']
# Texto a constar na página de testes limpa
txtmain = u'<!--não apague esta linha-->{{página de testes}}<!--não apague esta linha-->\n<!--Escreva abaixo da linha! -------------------------------- -->'
txtdisc = u'<!-- POR FAVOR, NÃO APAGUE ESTA LINHA -->{{Página de testes/disc}}<!-- não apagar -->\n\n----'

def main():
	def diffminutes(self):
		tempo = sp.editTime()
		pywikibot.output("Edição feita em: %s" % tempo)
		t = datetime.strptime(str(tempo), "%Y-%m-%dT%H:%M:%SZ")
		diff = timediff(now, t)
		pywikibot.output(u"Alterada à %i d %i h %i' %i''" % (diff.days, diff.hours, diff.minutes, diff.seconds))
		if diff.minutes >= 10:
			minutos = diff.minutes
			pywikibot.output("Ultima alteração à %s minutos" % minutos)
			return minutos
		elif diff.days != 0:
			minutos = 100
			dias = diff.days 
			pywikibot.output("Ultima alteração à %s dias" % dias)
			return minutos
		elif diff.hours != 0:
			minutos = 100
			horas = diff.hours # well, no need for big inventions
			pywikibot.output("Ultima alteração à %s horas" % horas)
			return minutos

	for k in n:
		num = k
		site = pywikibot.Site('pt','wikipedia')
		for nspace in ns:
			if nspace == "Ajuda":
				txt = txtmain
				sp=pywikibot.Page(site,u"Ajuda:Página de testes/"+num)
			elif nspace == "Ajuda discussão":
				txt = txtdisc
				sp=pywikibot.Page(site,u"Ajuda discussão:Página de testes/"+num)
			texto = sp.get(get_redirect=True)

			if texto != txt:
				pywikibot.output(u"\n\n\03{lightyellow}Página alterada: \n %s \03{default}" % (texto) )
				if diffminutes(sp) >= 10:
					sp.put(txt,comment = u'[[wp:bot|Bot]]: A limpar página de testes')
			else:
				pywikibot.output(u'Página sem alterações')
				tmp = diffminutes(sp)
				pywikibot.output(u"%s " % tmp)
if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()

