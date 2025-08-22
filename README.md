# Article Extractor

Article Extractor is a Python application that automatically scrapes blog articles—such as titles, URLs, and published dates—from platforms like freeCodeCamp, Substack, GitHub Engineering, and Shopify Engineering. The collected data is then organized and stored in a Google Sheet, making it easy to browse, filter, or reference later. This project helps streamline content gathering without needing to visit each site manually.

## Getting Started

Please refer to the [Wiki](https://github.com/victoriacheng15/articles-extractor/wiki)

## Tech Stacks

![Python](https://img.shields.io/badge/Python-3.10+-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white)
![Google Sheets API](https://img.shields.io/badge/Google%20Sheets-34A853.svg?style=for-the-badge&logo=Google-Sheets&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED.svg?style=for-the-badge&logo=Docker&logoColor=white)
![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-A22846.svg?style=for-the-badge&logo=Raspberry-Pi&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF.svg?style=for-the-badge&logo=GitHub-Actions&logoColor=white)

## DevOps with GitHub Actions

The workflow uses commands defined in the [Makefile](./Makefile) for installing dependencies and running scripts.

### Format Workflow

The Format Workflow automatically checks and fixes Python code style using Ruff. It runs when a pull request is made to the main branch or when code is pushed directly to the main branch. It looks at files like `main.py` and anything inside the `utils/` folder.

Steps it does:

- Checks out the code from the pull request.
- Sets up Python 3.10.
- Installs project dependencies (using make init).
- Runs Ruff to format the code (using make format).
- If Ruff changes anything, it automatically commits and pushes the changes back to the pull request.

[Format workflow](.github/workflows/format.yml)

###  Extraction Workflow:

The Extraction Workflow automatically runs every day at 6:00 AM UTC. It scrapes articles and sends the data to the Google Sheet. It installs dependencies, creates a credentials.json file from GitHub secrets, runs the extraction script, and uploads a log file as a GitHub Action artifact. You can also manually trigger the workflow using the "Run workflow" button on GitHub.

Steps it does:

- Checks out the repository code.
- Sets up Python 3.10.
- Installs project dependencies (using make init).
- Creates a credentials.json file from GitHub secrets.
- Verifies that the credentials file exists.
- Runs the article extraction script and saves the logs.
- Cleans up (deletes) the credentials.json file after the script finishes.
- Uploads the log file as a GitHub Action artifact for later review.

[Extraction workflow](.github/workflows/scheduled_extraction.yml)

## Key Features

- Efficient scraping using Python generators to minimize memory usage
- Automated daily scheduling via custom GitHub Actions workflow (06:00 UTC)
- Stores logs and errors as GitHub Action artifacts for transparency and debugging
- Cross-platform — runs on Raspberry Pi, cloud, or local machines
- Extensible architecture for adding new content sources

## What I have learned

I discovered how Python generators can streamline workflows that depend on sequential completion. In my original approach, I collected all articles in an array (all_articles) before processing them, which forced the script to wait until every scrape finished before sending anything to Google Sheets. Refactoring to use generators means each article is processed immediately after it’s scraped, eliminating the need to store everything upfront. This taught me two key things:

- Natural Sequencing: Generators inherently wait for one action (like scraping an article) to complete before yielding the result and moving to the next. This ensured data flowed smoothly into Google Sheets without manual batching.
- Responsive Execution: Unlike lists, generators don’t always hold all items in memory. While my primary goal wasn’t memory optimization, I noticed the script felt more responsive—articles appeared in Sheets incrementally, and interruptions didn’t waste prior work.

The change simplified my code by removing temporary storage and made the process feel more deliberate, as if guiding each article step-by-step from source to destination.
