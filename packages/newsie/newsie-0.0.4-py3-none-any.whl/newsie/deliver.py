import os
import smtplib
import glob 

import cups

from email.message import EmailMessage

import newsie.config as config

def to_email(newspaper_pdf):
    # Send via email
    message = EmailMessage()
    message["Subject"] = "Extree! Extree!"
    message["From"] = config.email
    message["To"] = config.subscriber_email
    message.set_content("Latest edition attached!")
    
    message.add_attachment(open(f"{newspaper_pdf}.pdf",mode="rb").read(), maintype="application/pdf", subtype="pdf")

    smtp = smtplib.SMTP(f"{config.smtp_server}:{config.smtp_port}")
    smtp.ehlo()
    smtp.starttls()
    smtp.login(config.email, config.password)
    smtp.send_message(message)
    smtp.quit()

def to_printer(newspaper_pdf):
    # Print directly to the printer with CUPS
    if config.print_direct:
        pdf_file = newspaper_pdf 
        with open(pdf_file, "wb") as pf:
            pf.write(newspaper_pdf)

        conn = cups.Connection()
        conn.printFile(config.printer_name, pdf_file, " ", {"sides":"two-sided-long-edge", "fit-to-page":"1"}) 

    # TODO: Should this happen somewhere more global?
    # Clean-up temp files
    for f in glob.glob("./img/*"):
        os.remove(f)
