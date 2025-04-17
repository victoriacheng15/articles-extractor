# Article Extractor

A Python application that automatically scrapes articles from freeCodeCamp, Substack, and other sources, then organizes them in Google Sheets.

## Getting Started

Please refer to the [Wiki](https://github.com/victoriacheng15/articles-extractor/wiki)

## Tech Stacks

![Python](https://img.shields.io/badge/Python-3.10+-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white)
![Google Sheets API](https://img.shields.io/badge/Google%20Sheets-34A853.svg?style=for-the-badge&logo=Google-Sheets&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED.svg?style=for-the-badge&logo=Docker&logoColor=white)
![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-A22846.svg?style=for-the-badge&logo=Raspberry-Pi&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF.svg?style=for-the-badge&logo=GitHub-Actions&logoColor=white)

## Key Features

- **Efficient scraping** using Python generators to minimize memory usage
- **Automated scheduling** via GitHub Actions (daily runs)
- **Cross-platform** - Runs on Raspberry Pi, cloud, or local machines
- **Extensible architecture** for adding new content sources

## What I have learned

I discovered how Python generators can streamline workflows that depend on sequential completion. In my original approach, I collected all articles in an array (all_articles) before processing them, which forced the script to wait until every scrape finished before sending anything to Google Sheets. By refactoring to use generators, each article is processed immediately after it’s scraped, eliminating the need to store everything upfront. This taught me two key things:

- Natural Sequencing: Generators inherently wait for one action (like scraping an article) to complete before yielding the result and moving to the next. This ensured data flowed smoothly into Google Sheets without manual batching.
- Responsive Execution: Unlike lists, generators don’t hold all items in memory at once. While my primary goal wasn’t memory optimization, I noticed the script felt more responsive—articles appeared in Sheets incrementally, and interruptions didn’t waste prior work.

The change simplified my code by removing temporary storage and made the process feel more deliberate, as if guiding each article step-by-step from source to destination.
