#!/usr/bin/env python

import os
import time

import feedparser
import qrcode

from datetime import datetime, timedelta, timezone

import config
import deliver
import news
import weather
import generate_pdf

def press():
    # Build a list of articles
    articles = news.get_articles()

    article_idx = 0
    selected_articles = []
    # TODO: Select enough articles to fill 2 pages instead of just grabbing a fixed number 
    # TODO: Consider grabbing more of the article if the summary is short.
    for article in articles[-15:]:

        # Generate qr code image files
        article["qr_file"] = os.path.join(os.path.dirname(__file__),  f"img/{article_idx}.jpg")
        qr_link = qrcode.QRCode(
                version = 10,
                box_size = 1,
                border = 4,
                )
        qr_link.add_data(article["link"])
        qr_link.make(fit=False)
        qr_link_img = qr_link.make_image(fill_color="black",back_color="white")
        qr_link_img.save(article["qr_file"], "JPEG")

        selected_articles.append(article)

        article_idx = article_idx + 1

    # TODO: Timestamp files so we can have an archive
    newspaper_pdf = "newspaper.pdf"
    generate_pdf.generate_newspaper_pdf(newspaper_pdf, selected_articles, weather.get_weather())

    # Print it!
    #deliver.to_printer(newspaper_pdf)
    #deliver.to_email(newspaper_pdf)
