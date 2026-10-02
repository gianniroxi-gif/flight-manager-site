# flight-manager.it

Sito di FlightManager. GitHub Pages, dominio su register.it, `www` fa 301
sull'apex.

## Google Search Console

Il sito e' verificato come **proprieta' Dominio**, con un record **TXT sul DNS
di register.it**:

    "google-site-verification=p5y_RguOyfUXdKlBng1SAvPgUU3ovd_vBH50IQPB3y8"

**Quel record non si tocca.** Se sparisce da register.it, Google toglie la
verifica e si perde l'accesso ai dati di ricerca. Sta accanto al TXT dell'SPF
(`v=spf1 include:spf.webapps.net ~all`), che a sua volta non si tocca: e' quello
delle email.

Il 2 ottobre 2026 si e' provato prima col metodo a **file HTML**
(`google2f4e7498c241fbb1.html`, ancora in questa cartella). Non ha mai
funzionato: il file rispondeva 200 con il contenuto esatto, anche allo user
agent di Google, senza redirect — e Search Console continuava a dire «impossibile
trovare il file». Il DNS ha funzionato al primo colpo. Se un giorno servisse
rifare la verifica, partire da li' e non perdere tempo col file.

Quel file puo' restare o sparire, non verifica piu' niente.

## Non cancellare

**`CNAME`** — tiene il dominio. Senza, il sito torna su
`gianniroxi-gif.github.io`.

## La pagina inglese si genera, non si scrive

`en/index.html` non si tocca a mano: lo riscrive `genera-en.py` partendo
dall'italiano.

    python3 genera-en.py

I due testi stanno negli attributi `data-it` e `data-en` di `index.html`. Il
selettore di lingua li scambia per chi guarda, ma Google legge l'HTML servito:
senza una pagina inglese vera, per lui la versione inglese non esiste. Dopo
ogni modifica all'italiano, rigenerare e committare tutti e due.

## Cosa c'e' dentro

    index.html        italiano
    en/index.html     inglese, generato
    styles.css        condiviso
    app.js            selettore di lingua, data di oggi, animazioni
    sitemap.xml       dichiara le due lingue a Google
    robots.txt
    privacy.html      richiesti da Apple, linkati dal footer
    terms.html
    screens/          schermate dell'app, anche nel formato di App Store Connect
    app/              pagina che rimanda allo store
