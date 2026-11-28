# LED Wall Calculator

Applicazione Streamlit per dimensionare un LED wall e consultare la configurazione delle matrici NovaStar della serie MCTRL.

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
Il catalogo mostrato è limitato ai prodotti MCTRL presenti nella categoria ufficiale NovaStar:
https://www.novastar.tech/product/product.html?catid=2
