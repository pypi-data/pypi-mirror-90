from datetime import date

# TODO: Removed unused packages
from pylatex import Package, Document, PageStyle, Head, Foot, MiniPage, LargeText, MediumText, SmallText, LineBreak, Tabu, Section, StandAloneGraphic
from pylatex.utils import bold, NoEscape

def generate_newspaper_pdf(newspaper_pdf, news, weather):

    MAX_ARTICLES = len(news) 
    today = date.today()

    geometry_options = {
        "head": "40pt",
        "margin": "0.5in",
        "bottom": "0.4in",
        "includeheadfoot": True
    }

    doc = Document(geometry_options = geometry_options)

    # For some reason the graphicx package isn't included automatically
    # when StandAloneGraphic, etc. is used, so we do it by hand here
    doc.packages.append(Package("graphicx"))

    first_page = PageStyle("firstpage")

    # Header
    with first_page.create(Head("C")) as center_header:
        with center_header.create(MiniPage(width=NoEscape(r"0.49\textwidth"), pos="c", align="c")) as title_wrapper:
            title_wrapper.append(LargeText(bold("It's Some News!")))
            title_wrapper.append(LineBreak())
            title_wrapper.append(SmallText(bold(today.strftime("%A, %B %d, %Y"))))

    with first_page.create(Head("L")) as left_header:
        with left_header.create(MiniPage(width=NoEscape(r"0.49\textwidth"), pos="c", align="l")) as weather_wrapper:
            weather_wrapper.append(SmallText(bold(f"Temp: {weather['temp']}")))
            weather_wrapper.append(LineBreak())
            weather_wrapper.append(SmallText(bold(f"Humidity: {weather['humidity']}")))

    # TODO: Consider adding something to the right of the header
    doc.preamble.append(first_page)

    # Body 
    with doc.create(Tabu("X[l] X[r]")) as first_page_table:

        # Generate a MiniPage for each article. 
        article_frames = []
        for article in news:
            
            article_frame = MiniPage(width=NoEscape(r"0.45\textwidth"), pos='h')
            # TODO: Figure out how to make the section title smaller
            with article_frame.create(Section(title=article["title"], numbering=False)):
                article_frame.append(article["summary"])
                article_frame.append(LineBreak())
                article_frame.append(StandAloneGraphic(filename=article["qr_file"],image_options="width=65px"))

            article_frames.append(article_frame)

        # Add each article to alternating columns.
        for i in range(0,int(MAX_ARTICLES / 2),2):
            first_page_table.add_row([article_frames[i], article_frames[i+1]])
            first_page_table.add_empty_row()

    # This adds the header to the page for some reason???
    doc.change_document_style("firstpage")

    # TODO: Consider adding a footer

    # TODO: This should be derived from the newspaper_pdf variable
    doc.generate_pdf(newspaper_pdf, clean_tex = False)
