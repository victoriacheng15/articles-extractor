# Article Extractor

This application is created to retrieve articles from freeCodeCamp and Substack, and subsequently transfer all pertinent article details to a Google Sheet.

## Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white) ![Google Sheet API](https://img.shields.io/badge/Google%20Sheets-34A853.svg?style=for-the-badge&logo=Google-Sheets&logoColor=white) ![docker](https://img.shields.io/badge/Docker-2496ED.svg?style=for-the-badge&logo=Docker&logoColor=white) ![Raspberry PI](https://img.shields.io/badge/Raspberry%20Pi-A22846.svg?style=for-the-badge&logo=Raspberry-Pi&logoColor=white)

## Getting Started

1. Installation

```bash
git clone git@github.com:victoriacheng15/articles-extractor.git

cd articles-extractor
```

2. Set up Google APIs

Check out the guide from [Python quickstart by Google](https://developers.google.com/sheets/api/quickstart/python)

3. credentials.json

Once you get the Google Sheet API and you will need to get the credentials from Google, rename the json file to `credentials.json` and move the file to root directory. If you are to use different name than `credentials.json`, you would need to update the file name in `config/setup_google_sheet.py` 


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

## Deployment

The application is installed on the Raspberry Pi and set up to run automatically at a specific time daily through a cron schedule. Additionally, I've written a bash script for this purpose.

```bash
#!/bin/bash

cd your_path/articles-extractor # can use pwd to find the path

docker compose up && docker logs extractor > log_articles.txt &&  docker compose down
# or 
docker compose up &&docker compose down
```

You have the flexibility to save the `log_articles.txt` file in a location of your choice. I use this file for monitoring and verifying the proper functioning of the application, but it's entirely optional.

For cron schedule:

```bash
crontab -e
# This will open the cron file where you can set schedule
```

Use [crontab guru](https://crontab.guru/) to find the time that you want to run on.

Let's say you would like to run the app at 9am every day:

```bash
0 9 * * * your_path/the_script_name.sh 

# can use pwd to find where the file is located.
```

Once the schedule is set, `ctrl + o` -> `enter` -> `ctrl + x`!