import feedparser

from datetime import datetime, timedelta, timezone

import newsie.config as config

def get_articles():
    # Build a list of articles
    articles = []

    for feed_url in config.subscriber_feeds:

        # Load RSS feed
        feed = feedparser.parse(feed_url)

        for article in feed.entries:
            yesterday = datetime.now(timezone.utc) - timedelta(days=1)

            # Different feeds specify the TZ with different formats.  This is an attempt
            # to handle that; it's awkward but will do until we find something better
            try:
                article.published_parsed = datetime.strptime(article["published"], "%a, %d %b %Y %H:%M:%S %z")
            except ValueError:
                # Thanks to a bug in strptime (https://bugs.python.org/issue22377), we have to force the TZ on these
                article.published_parsed= datetime.strptime(article["published"], "%a, %d %b %Y %H:%M:%S %Z").replace(tzinfo=timezone.utc)

            if article.published_parsed > yesterday:

                # Filter out articles containing keywords the user doesn't want to see
                title_set = set(article["title"].lower().split())
                if config.subscriber_blocklist.intersection(title_set):
                    print(f"blocked: {config.subscriber_blocklist.intersection(title_set)} {article['title']}")
                else:
                    print(f"added: {article['title']}")
                    articles.append(article)

    # Sort articles by (parsed) publication date
    articles.sort(key=lambda x: x.published_parsed, reverse=False)

    return articles
