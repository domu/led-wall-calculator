# LED Wall Calculator

Applicazione Streamlit per dimensionare un LED wall e consultare una configurazione hardware NovaStar indicativa.

## Avvio in locale

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Test

```powershell
python -m unittest -v test_novastar_catalog.py
```

## Deploy su Streamlit Community Cloud

Collega questo repository GitHub a Streamlit Community Cloud e seleziona `app.py` come file principale.
Le specifiche NovaStar mostrate sono indicative: verificare sempre i dati con il catalogo ufficiale.
