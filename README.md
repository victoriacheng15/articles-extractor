# Article Extractor

This application is created to retrieve articles from freeCodeCamp and Substack, and subsequently transfer all pertinent article details to a Google Sheet.

## Tech Stacks

![Python](https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white) ![Google Sheet API](https://img.shields.io/badge/Google%20Sheets-34A853.svg?style=for-the-badge&logo=Google-Sheets&logoColor=white) ![docker](https://img.shields.io/badge/Docker-2496ED.svg?style=for-the-badge&logo=Docker&logoColor=white) ![Raspberry PI](https://img.shields.io/badge/Raspberry%20Pi-A22846.svg?style=for-the-badge&logo=Raspberry-Pi&logoColor=white)

## Getting Started

Please refer to the [Wiki](https://github.com/victoriacheng15/articles-extractor/wiki)

## What I have learned

I employed Python's generator feature for enhanced efficiency. I used this feature to send article information to the Sheets individually. There is no need to store the entire sequence of articles in memory at once. Previously, articles were stored in the array named “all_articles” from various providers. And then I had to loop through the array to send articles to the Sheets.

The generator is a neat way to simplify and streamline the process. This eliminates the need to store the sequence in the memory before sending it to the Sheets