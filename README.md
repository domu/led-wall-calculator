# LED Wall Calculator

Applicazione Streamlit per dimensionare un LED wall e consultare la configurazione delle matrici NovaStar della serie MCTRL.

## Avvio in locale

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Test

```powershell
python -m unittest -v
```

## Versione applicazione

La versione corrente è definita in `app_version.py` e mostrata nella barra laterale.
Aggiorna `APP_VERSION` seguendo Semantic Versioning quando pubblichi una nuova release.

## Deploy su Streamlit Community Cloud

Collega questo repository GitHub a Streamlit Community Cloud e seleziona `app.py` come file principale.
Il catalogo mostrato è limitato ai prodotti MCTRL presenti nella categoria ufficiale NovaStar:
https://www.novastar.tech/product/product.html?catid=2

## Archivio pannelli

I profili dei pannelli sono conservati in `panel_archive.json` e includono nome, produttore,
progetto, dimensioni, pixel pitch e assorbimento massimo per pannello in Watt. L'app permette
di aggiungere profili e scaricare l'archivio aggiornato. Su Streamlit Community Cloud, sostituire
il file nel repository e pubblicare la modifica per conservarla tra i deploy.
