# Thesis

## Installation steps

- Download Python version 3.11 (Note, chromadb does not work with Python 3.12 or later)
- Create a virtual env (folder .venv). Created using VS Code and selecting Python 3.11

## To run Amazon reviews script ([amazon.py](./amazon.py))

```bash
pip install requests_html lxml_html_clean
```

Run `amazon.py` which should download customers reviews for some mobile devices from amazon.com and save them as JSON in the data folder.

## Install Ollama
 - Download and install Ollama
 - Open a terminal and pull the models used by this project
```bash
ollama pull nomic-embed-text
ollama pull mistral
```

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

## Create a Web UI Application 

- Install `flask` and `flask_cors`. Flask is required to create a web application using Python and flask_cors allows the Vite/React development server to make API calls to the python webserver.
```bash
pip install flask flask_cors
```

- Create a new [React](https://react.dev/) using [vite](https://vite.dev/).
```bash
npx create vite@latest webui -- --template react-ts
cd webui
npm install
```

- Install `sass` and `bootstrap` to have UI
```
npm install sass@^1.76.0 --save-dev
npm install bootstrap
```

- Install `axios` library to make API calls
```
npm install axios
```

- Run [webserver.py](./webserver.py) to run the python webserver

- Run `npm run dev` in the `webui` folder to run the web interface in development mode.

- Run `npm run build` in the `webui` folder to build the client UI.


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

## Components

- [amazon.py](./amazon.py) extracts customer data for some electronic devices from amazon.com website
- [importdocs.py](./importdocs.py) parses the customer review data extracted by [amazon.py](./amazon.py) and stores them in chromadb
- [extract_text.py](./extract_text.py) helper functions used by [importdocs.py](./importdocs.py)
- [search.py](./search.py) uses ollama to answer queries about prodcts. It displays two responses. A response without RAG and another with RAG using the extracted data that was imported by [importdocs.py](./importdocs.py) so as to compare responses.

## Sample Questions/Responses

- [question1.txt](./question1.txt)
- [question2.txt](./question2.txt)

## Sources

- Tutorial Video: [Let's build a RAG system - The Ollama Course](https://www.youtube.com/watch?v=FQTCLOUnIzI)
- Tutorial Video: [How I Scrape Amazon Product Reviews with Python](https://www.youtube.com/watch?v=UD4VzOfhBCQ)
- Code for building RAG system [https://github.com/technovangelist/videoprojects](https://github.com/technovangelist/videoprojects)