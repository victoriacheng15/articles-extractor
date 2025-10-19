# Article Extractor

Articles Extractor is a Python application that automatically collects blog articles — including titles, URLs, and published dates — from multiple platforms such as freeCodeCamp, Substack, GitHub Engineering, and Shopify Engineering. The collected data is organized into a Google Sheet, so you can browse, filter, or reference articles from a single place without visiting each site manually.

The tool supports multiple execution methods:

- Manual runs via CLI
- Scheduled runs with GitHub Actions or cron/Docker
- Remote execution via Raspberry Pi

The project demonstrates automation, API integration, and practical workflow improvement for personal use. It's easy to add additional sources or modify the export format based on your needs.

## ✨ Features

- **Multi-source scraping**: Extract articles from freeCodeCamp, GitHub Blog, Shopify Engineering, and Substack
- **Automated scheduling**: Run on a schedule using GitHub Actions, cron, or Docker
- **Google Sheets integration**: Automatically store articles in a Google Sheet
- **Deduplication**: Automatically detects and skips duplicate articles
- **Flexible deployment**: Local, Docker, Raspberry Pi, or cloud-based execution
- **Async processing**: Efficient concurrent web scraping

## 🚀 Quick Start

Please refer to this [Installation Guide](docs/installation.md)

## 📚 Documentation

- [Architecture Guide](docs/architecture.md) - System design, components, and data flow
- [GitHub Actions](docs/github_actions.md) - Workflow automation and scheduling

## 🛠 Tech Stacks

![Python](https://img.shields.io/badge/Python-3.10+-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white)
![Google Sheets API](https://img.shields.io/badge/Google%20Sheets-34A853.svg?style=for-the-badge&logo=Google-Sheets&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED.svg?style=for-the-badge&logo=Docker&logoColor=white)
![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-A22846.svg?style=for-the-badge&logo=Raspberry-Pi&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF.svg?style=for-the-badge&logo=GitHub-Actions&logoColor=white)

## 💡 What I Learned

I discovered how Python generators can streamline workflows that depend on sequential completion. In my original approach, I collected all articles in an array (all_articles) before processing them, which forced the script to wait until every scrape finished before sending anything to Google Sheets. Refactoring to use generators means each article is processed immediately after it's scraped, eliminating the need to store everything upfront. This taught me two key things:

- **Natural Sequencing**: Generators inherently wait for one action (like scraping an article) to complete before yielding the result and moving to the next. This ensured data flowed smoothly into Google Sheets without manual batching.
- **Responsive Execution**: Unlike lists, generators don't always hold all items in memory. While my primary goal wasn't memory optimization, I noticed the script felt more responsive—articles appeared in Sheets incrementally, and interruptions didn't waste prior work.

The change simplified my code by removing temporary storage and made the process feel more deliberate, as if guiding each article step-by-step from source to destination.

## 📖 How This Project Evolved

Learn about the journey of this project: from local-only execution, to Docker containerization, to fully automated GitHub Actions workflows.

[Read the blog post](https://victoriacheng15.vercel.app/blog/from-pi-to-cloud-automation)
