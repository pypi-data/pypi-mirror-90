# newsie 

How about a daily printed newspaper, govna?


## Description

Newsie delivers a fresh hard-copy newspaper via your printer every morning based on the news sources you select.  Each article includes a summary and a QR code you can scan with your phone shoud you *want to know more*.


## Status

* Generates a page of news from a list of RSS feeds
* Can print the page directly to CUPS-configured printer
* Emails the page to a configured destination
* Blocks stories based on keywords


## Usage

Once installed and configured, the command `new-issue` will email and print a new issue of the paper.

### Requirements

You'll need to install a LaTex compiler, something along these lines:

`sudo apt-get install texlive-pictures texlive-science texlive-latex-extra latexmk`

### Installation

~~`pip install newsie`~~

... or to install from source, clone this repository and then...

`pip install .`

### Configuration

Copy [config_template.ini](./config_template.ini) to `config.ini` and modify the configuration as needed.

*NOTE: Make sure the paths in the configuration file actually exist!"*


## TODO

* ~~Make the feed list dynamic (part of the config)~~
* Add a tool to automate configuration
* Fix encoding/unicode issues (ex:, the `'` in `it's` getting turned into weird characters).
* ~~Blend stories so they don't appear grouped by source~~
* ~~Only include stories from the last 24 hours (or some configured amount)~~
* Grab more of the article if the RSS `summary` is too short
* ~~Figure out why iOS won't parse the QR code links~~
* ~~Create a CLI~~
* Add forecast to weather
* Support other weather providers
* Make story titles smaller than header
* ~~Re-work configuration (module-based is broken now that we're a real package)~~
* ~~Fix path issues that have come-up as a result of packagification~~
* Create qr image directory if it's missing
* Better output (remove debugging code, etc.)
* Fix "first page is blank" problem
* Make number of articles configurable
