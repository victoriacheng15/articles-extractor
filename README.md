# Article Scrapper - WIP

This app is designed to extract articles from freeCodeCamp and Substack, then transfer all relevant article information to a Google Sheet.

## Tech Stack

- ![Python](https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white)
- ![Google Sheet API](https://img.shields.io/badge/Google%20Sheets-34A853.svg?style=for-the-badge&logo=Google-Sheets&logoColor=white)
- ![docker](https://img.shields.io/badge/Docker-2496ED.svg?style=for-the-badge&logo=Docker&logoColor=white)

## Getting Started

1. Installation

```bash
git clone git@github.com:victoriacheng15/articles-scrap.git

cd articles-scrap
```

2. Set up Google 

Check out either guide from [Node.js quickstart by Google](https://developers.google.com/sheets/api/quickstart/nodejs) or [Installation and setup by Robocorp](https://robocorp.com/docs/development-guide/google-sheets/interacting-with-google-sheets)

3. credentials.json

Once you get the Google Sheet API and you will need to get the credentials from Google, rename the json file to `credentials.json`


4. Set up `data/providoers.py`

Single url:

```py
provider_name = {
    "class": "the element that contains article Info",
    "urls": # url,
}
```

Mutiply urls:

```py
provider_name = {
    "class": "the element that contains article Info",
    "urls": [
      # all urls
    ],
}
```
5. Run docker container
  
```bash
docker compose up
```