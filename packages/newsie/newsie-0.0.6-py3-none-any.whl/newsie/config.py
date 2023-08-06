# This file provides glue between the module code and the
# configparser module.  The module could work directly with
# configparser instead, but I wanted to make it easier to
# switch configuration providers down the road.

import configparser

# Read config file
cp = configparser.ConfigParser(delimiters=('='))
cp.read("config.ini")

# Assign config file values to variables
subscriber_feeds = cp["news"]["feeds"].split(",")

subscriber_blocklist = set(cp["news"]["block"].split(","))

subscriber_email = cp["email"]["subscriber_email"]

# Configuration options for printing directly to a local printer
print_direct = cp.getboolean("printing","print_direct")
printer_name = cp["printing"]["printer_name"]

# print-by-email configuration options
email = cp["email"]["email"]
password = cp["email"]["password"]
smtp_server = cp["email"]["smtp_server"]
smtp_port = cp.getint("email","smtp_port")

# weather station config
AMBIENT_ENDPOINT        = cp["weather"]["AMBIENT_ENDPOINT"]
AMBIENT_APPLICATION_KEY = cp["weather"]["AMBIENT_APPLICATION_KEY"]
AMBIENT_API_KEY         = cp["weather"]["AMBIENT_API_KEY"]

pdf_output = cp["files"]["pdf_output"]
qr_image_files = cp["files"]["qr_image_files"]
