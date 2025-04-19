# Thesis

## Installation steps

- Download Python version 3.11 (Note, chromadb does not work with Python 3.12 or later)
- Create a virtual env (folder .venv). Created using VS Code and selecting Python 3.11

## To run Amazon reviews script ([amazon.py](./amazon.py))

```bash
pip install requests_html lxml_html_clean
```

Run `amazon.py` which should download customers reviews for some mobile devices from amazon.com and save them as JSON in the data folder.


## Install and Run Chromadb

Installing `chromadb`:
```bash
pip install chromadb
```

Running `chromadb` (Port number `8000` and save the database to the `chromadata` folder)

```bash
chroma run --host localhost --port 8000 --path ./chromadata
```

## Install Ollama Package

```bash
pip install chromadb
```

## Save requirements.txt

```bash
pip freeze > requirements.txt
```

This will save the PIP package versions used in a `requirements.txt` file 

To reinstall all packages again run

```bash
python -m venv .venv 
source .venv/bin/activate  # (On Windows, use `.venv\Scripts\activate`)
pip install -r requirements.txt
```


## Sources

- Tutorial Video: [Let's build a RAG system - The Ollama Course](https://www.youtube.com/watch?v=FQTCLOUnIzI)
- Tutorial Video: [How I Scrape Amazon Product Reviews with Python](https://www.youtube.com/watch?v=UD4VzOfhBCQ)
- Code for building RAG system [https://github.com/technovangelist/videoprojects](https://github.com/technovangelist/videoprojects)