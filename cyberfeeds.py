import feedparser
from datetime import datetime, timedelta
import os
import re

# --- CONFIG ---
FEEDS = [
    "https://feeds.feedburner.com/TheHackersNews",
    "https://www.bleepingcomputer.com/feed/",
    "https://www.securityweek.com/feed"
]
OUTPUT_DIR = "/mnt/e/daily_news"
MAX_ITEMS_PER_FEED = 10  # Limit per feed
KEEP_WEEKS = 1            # Number of weekly files to keep

def banner(msg):
    """Prints a banner-style message for clarity."""
    print("\n" + "="*80)
    print(msg)
    print("="*80)

def get_existing_links():
    """Read all previous weekly files and return a set of stored links."""
    existing_links = set()
    if not os.path.exists(OUTPUT_DIR):
        return existing_links

    for filename in os.listdir(OUTPUT_DIR):
        if re.match(r"cybernews_links_week_\d{4}-\d{2}-\d{2}\.txt", filename):
            file_path = os.path.join(OUTPUT_DIR, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    existing_links.add(line.strip())

    print(f"Found {len(existing_links)} total historical links across previous files.")
    return existing_links

def cleanup_old_files():
    """Keep only the last KEEP_WEEKS files, delete older ones."""
    files = [f for f in os.listdir(OUTPUT_DIR) if re.match(r"cybernews_links_week_\d{4}-\d{2}-\d{2}\.txt", f)]
    if len(files) <= KEEP_WEEKS:
        print(f"No cleanup needed. Total weekly files: {len(files)}")
        return

    # Sort by date in filename (descending)
    files.sort(key=lambda x: datetime.strptime(re.search(r"\d{4}-\d{2}-\d{2}", x).group(), "%Y-%m-%d"), reverse=True)

    # Delete files beyond KEEP_WEEKS
    to_delete = files[KEEP_WEEKS:]
    for old_file in to_delete:
        os.remove(os.path.join(OUTPUT_DIR, old_file))
        print(f"Deleted old file: {old_file}")

    print(f"Cleanup complete. Kept {KEEP_WEEKS} most recent files.")

def fetch_links_last_week():
    banner("Fetching Cybersecurity News Links (Last 7 Days)")
    today = datetime.now().date()
    week_ago = today - timedelta(days=7)
    filename = os.path.join(OUTPUT_DIR, f"cybernews_links_week_{today}.txt")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    existing_links = get_existing_links()
    new_links = []

    for url in FEEDS:
        feed_name = url.split("/")[2]
        print(f"\n--- Processing feed: {feed_name} ---")
        feed = feedparser.parse(url)
        count = 0
        new_from_this_feed = 0

        for entry in feed.entries:
            published_parsed = entry.get("published_parsed") or entry.get("updated_parsed")
            if not published_parsed:
                print("  [!] Skipped: No published/updated date.")
                continue

            entry_date = datetime(*published_parsed[:6]).date()

            # Within last 7 days and not duplicate
            if week_ago <= entry_date <= today:
                link = entry.get("link", "")
                if link and link not in existing_links:
                    new_links.append(link)
                    existing_links.add(link)
                    new_from_this_feed += 1
                    count += 1
                    print(f"  [+] Added: {link}")
                    if count >= MAX_ITEMS_PER_FEED:
                        print(f"  [!] Reached max items per feed ({MAX_ITEMS_PER_FEED}).")
                        break
                else:
                    print(f"  [-] Skipped duplicate: {link}")
            else:
                print(f"  [-] Skipped (old): {entry.get('link', '')}")

        print(f"Feed summary: {new_from_this_feed} new links added from {feed_name}")

    # Only create file if new links found
    if new_links:
        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(new_links))

        banner(f"Created new weekly file: {filename}")
        print(f"Total new links this week: {len(new_links)}")

        # Cleanup after writing new file
        cleanup_old_files()

        return filename
    else:
        banner("No new links found this week! No file created.")
        return None

if __name__ == "__main__":
    file_path = fetch_links_last_week()








































































