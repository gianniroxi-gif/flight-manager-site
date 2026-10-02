# flight-manager.it

Sito di FlightManager. GitHub Pages, dominio su register.it, `www` fa 301
sull'apex.

## Non cancellare

**`google2f4e7498c241fbb1.html`** — e' il file con cui Google Search Console
verifica che il sito e' tuo. Non contiene niente di utile da leggere e sembra
spazzatura: se sparisce, Google toglie la verifica e si perde l'accesso ai dati
di ricerca finche' non si rifa' tutto.

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
