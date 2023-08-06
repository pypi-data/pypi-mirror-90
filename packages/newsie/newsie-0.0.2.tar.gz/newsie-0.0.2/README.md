# newsie 

How about a daily printed newspaper, govna?


## Description

Paperboy delivers a fresh hard-copy newspaper via your printer every morning based on the news sources you select.  Each article includes a summary and a QR code you can scan with your phone shoud you *want to know more*.


## Status

* Generates a page of news from a list of RSS feeds
* Can print the page directly to CUPS-configured printer
* Emails the page to a configured destination
* Blocks stories based on keywords


## Requirements

You'll need to install a LaTex compiler, something along these lines:

`sudo apt-get install texlive-pictures texlive-science texlive-latex-extra latexmk`

Then install the required Python modules:

`pip install -r requirements.txt` 

## Configuration

### Common

* `subscriber_email`: Email address used to send the paper (PDF) to
* `smtp_server`: Mailserver used to send newspaper PDF
* `smtp_port`: SMTP port number of mailserver
* `email`: Email/username for SMTP server
* `password`: Mailserver password
* `print_direct`: Boolean, enables or disabled CUPS-based printing
* `printer_name`: Name of CUPS printer to use if direct printing is enabled

### News

* `subscriber_feeds`: A list of URL's to RSS feeds to include in the news
* `subscriber_blocklist`: A list of words used to block unwanted stories

### Weather

Weather uses AmbientWeather.net to get weather data from personal weather stations.  Currently this requires having a compatible station and creating an application and api key on ambientweather.net.  In the future other weather sources may be supported.

* `AMBIENT_ENDPOINT`: The URL of the Ambient Weather API
* `AMBIENT_APPLICATION_KEY`: The application key
* `AMBIENT_API_KEY`: The API key
 

## TODO

* ~~Make the feed list dynamic (part of the config)~~
* Add a tool to automate configuration
* Fix encoding/unicode issues (ex:, the `'` in `it's` getting turned into weird characters).
* ~~Blend stories so they don't appear grouped by source~~
* ~~Only include stories from the last 24 hours (or some configured amount)~~
* Grab more of the article if the RSS `summary` is too short
* ~~Figure out why iOS won't parse the QR code links~~
* Create a CLI
* Add forecast to weather
* Make story titles smaller than header

## Notes
