# Subscription configuration
subscriber_feeds = [
        "http://feeds.bbci.co.uk/news/rss.xml",
        "https://feeds.npr.org/1001/rss.xml",
        "https://makezine.com/feed/",
        "https://solar.lowtechmagazine.com/feeds/all.rss.xml",
        "http://original.antiwar.com/feed/",
        ]
subscriber_blocklist = set(["trump","bezos","microsoft"])
subscriber_email = "mr@jasongullickson.com"

# Configuration options for printing directly to a local printer
print_direct = False 
printer_name = "YOUR_CUPS_PRINTER_"

# print-by-email configuration options
email = "pb@2soc.net"
password = "dementia13"
smtp_server = "box.virtualprivatenation.com"
smtp_port = "587"

# weather station config
AMBIENT_ENDPOINT        = "https://api.ambientweather.net/v1",
AMBIENT_APPLICATION_KEY = "db97c03e263a4574976ab5089e086b07fa55f95589a54c35b3143a6c463a959d",
AMBIENT_API_KEY         = "218a1e9de2254acba26cb5b198355dd9b97321508f584f1eaf53d53d4dba9062"
