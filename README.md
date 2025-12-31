# CyberFeeds - Weekly Cybersecurity News Aggregator

CyberFeeds is a lightweight Python script designed to aggregate the latest cybersecurity news from top industry RSS feeds. It fetches, filters, and saves links to recent articles, ensuring you stay up-to-date with the latest threats, vulnerabilities, and security trends without duplicates.

## Features

- **Multi-Source Aggregation:** Fetches news from trusted sources:
  - [The Hacker News](https://thehackernews.com/)
  - [Bleeping Computer](https://www.bleepingcomputer.com/)
  - [Security Week](https://www.securityweek.com/)
- **Smart Filtering:** Only retrieves articles published in the last 7 days.
- **Deduplication:** Checks against previously saved files to prevent duplicate links.
- **Automatic Cleanup:** Automatically manages storage by keeping only the most recent weekly files (configurable).
- **Simple Output:** Generates a clean, plain text file containing a list of URLs for easy reading or integration with other tools.

## Prerequisites

- Python 3.x
- `feedparser` library

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/cyberfeeds.git
    cd cyberfeeds
    ```

2.  **Install dependencies:**
    ```bash
    pip install feedparser
    ```

## Usage

Run the script directly using Python:

```bash
python cyberfeeds.py
```

The script will:
1.  Fetch the latest RSS feeds.
2.  Filter for articles from the last week.
3.  Check for duplicates against existing history.
4.  Save new links to a file named `cybernews_links_week_YYYY-MM-DD.txt`.
5.  Clean up old files if the limit is exceeded.

## Configuration

You can customize the script by modifying the configuration variables at the top of `cyberfeeds.py`:

```python
# --- CONFIG ---
FEEDS = [
    "https://feeds.feedburner.com/TheHackersNews",
    "https://www.bleepingcomputer.com/feed/",
    "https://www.securityweek.com/feed"
]
OUTPUT_DIR = "/mnt/e/daily_news"  # Directory to save output files
MAX_ITEMS_PER_FEED = 10           # Maximum links to fetch per feed
KEEP_WEEKS = 1                    # Number of weekly files to keep before deleting old ones
```

## Output Format

The output is a simple text file (e.g., `cybernews_links_week_2025-11-10.txt`) containing one URL per line:

```text
https://thehackernews.com/2025/11/example-article.html
https://www.bleepingcomputer.com/news/security/example-story/
...
```

## License

This project is open-source and available for personal and educational use.
