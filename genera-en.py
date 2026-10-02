# -*- coding: utf-8 -*-
"""Genera en/index.html dall'italiano.

La pagina tiene i due testi negli attributi data-it e data-en e li scambia in
JavaScript. Per una persona va bene; per Google no: il motore legge l'HTML
servito, vede solo l'italiano, e la versione inglese per lui non esiste.
Questo script la fa esistere come pagina vera, con un URL suo.

    python3 genera-en.py        (dalla cartella del sito)

Si rigenera ogni volta che index.html cambia. Non si modifica en/index.html a
mano: la prossima esecuzione lo sovrascrive.
"""
import html, os, re
from html.parser import HTMLParser

VUOTI = {'meta','link','br','img','input','hr','source','area','base','col','embed','track','wbr'}

class Traduci(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.out, self.salta, self.tag, self.prof = [], False, None, 0
        self.tradotti = 0

    def handle_starttag(self, tag, attrs):
        raw = self.get_starttag_text()
        if self.salta:
            if tag == self.tag and tag not in VUOTI: self.prof += 1
            return
        d = dict(attrs)
        if 'data-it' in d and 'data-en' in d and tag not in VUOTI:
            self.out.append(raw)
            self.out.append(html.unescape(d['data-en']))
            self.salta, self.tag, self.prof = True, tag, 1
            self.tradotti += 1
        else:
            self.out.append(raw)

    def handle_startendtag(self, tag, attrs):
        if not self.salta: self.out.append(self.get_starttag_text())

    def handle_endtag(self, tag):
        if self.salta:
            if tag == self.tag:
                self.prof -= 1
                if self.prof == 0:
                    self.salta = False
                    self.out.append(f'</{tag}>')
            return
        if tag not in VUOTI: self.out.append(f'</{tag}>')

    def handle_data(self, d):
        if not self.salta: self.out.append(d)
    def handle_entityref(self, n):
        if not self.salta: self.out.append(f'&{n};')
    def handle_charref(self, n):
        if not self.salta: self.out.append(f'&#{n};')
    def handle_comment(self, d):   self.out.append(f'<!--{d}-->')
    def handle_decl(self, d):      self.out.append(f'<!{d}>')

src = open('index.html', encoding='utf-8').read()
p = Traduci(); p.feed(src); p.close()
out = ''.join(p.out)

SOST = [
 ('<html lang="it">', '<html lang="en">'),
 ('<title>Flightmanager — Logbook EASA FCL.050, limiti FTL e busta paga</title>',
  '<title>Flightmanager — EASA FCL.050 logbook, FTL limits and payslip</title>'),
 ('content="Flightmanager è il logbook EASA FCL.050 per piloti: importa i voli, calcola limiti FTL e validità, ed elabora la stima della busta paga Malta Air."',
  'content="Flightmanager is the EASA FCL.050 logbook for airline pilots: import your flights, track FTL limits and recency, and estimate your Malta Air payslip."'),
 ('content="Flightmanager — Logbook EASA FCL.050 per piloti"',
  'content="Flightmanager — EASA FCL.050 logbook for pilots"'),
 ('content="Sai già se sei pronto al volo: logbook EASA, limiti FTL, validità e stima busta paga in un\'unica app."',
  'content="Know if you are ready to fly: EASA logbook, FTL limits, recency and payslip estimate in one app."'),
 ('<meta property="og:url" content="https://flight-manager.it/" />',
  '<meta property="og:url" content="https://flight-manager.it/en/" />'),
 ('<link rel="canonical" href="https://flight-manager.it/" />',
  '<link rel="canonical" href="https://flight-manager.it/en/" />'),
 ('"description": "Libretto di volo EASA FCL.050 per piloti di linea: ore, decolli, atterraggi, validità FCL.060 e limiti di volo ORO.FTL.210 calcolati dai voli volati, con export PDF. Per i piloti Malta Air e Ryanair Spain anche la stima della busta paga.",',
  '"description": "EASA FCL.050 flight logbook for airline pilots: hours, take-offs, landings, FCL.060 recency and ORO.FTL.210 flight time limits worked out from the flights you actually flew, with PDF export. For Malta Air and Ryanair Spain pilots, a payslip estimate too.",'),
 ('"operatingSystem": "iOS 15.1 o successivo",', '"operatingSystem": "iOS 15.1 or later",'),
 ('"url": "https://flight-manager.it/",', '"url": "https://flight-manager.it/en/",'),
 ('"jobTitle": "Pilota di linea"', '"jobTitle": "Airline pilot"'),
 ('"name": "Mensile", "price": "6.99"', '"name": "Monthly", "price": "6.99"'),
 ('"name": "Annuale", "price": "44.99"', '"name": "Annual", "price": "44.99"'),
]
for a, b in SOST:
    assert out.count(a) == 1, f'non trovato o ambiguo: {a[:60]}'
    out = out.replace(a, b)

os.makedirs('en', exist_ok=True)
open('en/index.html', 'w', encoding='utf-8').write(out)
print(f'en/index.html — {len(out)} byte, {p.tradotti} nodi tradotti')
