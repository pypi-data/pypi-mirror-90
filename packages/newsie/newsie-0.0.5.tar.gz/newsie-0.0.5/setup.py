import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="newsie",
    version="0.0.5",
    description="How about a daily printed newspaper, govna!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/jjg/newsie",
    author="Jason J. Gullickson",
    author_email="mr@jasongullickson.com",
    license="GPL3",
    packages=setuptools.find_packages(),
    install_requires=[
        "ambient-api",
        "cups",
        "feedparser",
        "image",
        "PyLaTeX",
        "qrcode",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "new-issue=newsie.issue:press"
        ],
    }
)
