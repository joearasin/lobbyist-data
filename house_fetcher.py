#!/usr/bin/env python3

from requests_html import HTMLSession
import sys
import click
import datetime

DOWNLOAD_URL = "http://disclosures.house.gov/ld/LDDownload.aspx"

session = HTMLSession()


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--year",
    help="Year of document to download.",
    type=click.IntRange(2004, datetime.datetime.now().year),
)
@click.option(
    "--document",
    help="Document to download",
    type=click.Choice(
        [
            "Registrations",
            "1stQuarter",
            "2ndQuarter",
            "3rdQuarter",
            "4thQuarter",
            "MidYear",
            "YearEnd",
        ]
    ),
)
@click.option("--file", help="Filename to download")
def download(year, document, file):
    if file is not None:
        formatted_filename = file.replace("_", " ")
    if year is not None and document is not None:
        formatted_filename = "{} {}".format(year, document)
    if formatted_filename is None:
        raise ValueError("Must specify either filename or year and document")

    r = session.get(DOWNLOAD_URL)

    # Get the CSRF Protection Properties
    view_state_generator = r.html.find("#__VIEWSTATEGENERATOR", first=True).attrs[
        "value"
    ]
    view_state = r.html.find("#__VIEWSTATE", first=True).attrs["value"]
    event_validation = r.html.find("#__EVENTVALIDATION", first=True).attrs["value"]

    # Find The File
    files = [
        e.attrs["value"]
        for e in r.html.xpath("//option")
        if formatted_filename in e.attrs["value"]
    ]
    if len(files) == 0:
        raise ValueError("Could not find {}".format(formatted_filename))
    if len(files) > 1:
        raise ValueError("Duplicate documents for {}".format(formatted_filename))

    with session.post(
        DOWNLOAD_URL,
        data={
            "__VIEWSTATEGENERATOR": view_state_generator,
            "__VIEWSTATE": view_state,
            "__EVENTVALIDATION": event_validation,
            "selFilesXML": files[0],
            "btnDownloadXML": "Download",
        },
        stream=True,
    ) as dl:
        for chunk in dl.iter_content(chunk_size=128):
            sys.stdout.buffer.write(chunk)


@cli.command()
def list():
    r = session.get(DOWNLOAD_URL)
    files = [e.attrs["value"] for e in r.html.xpath("//option")]
    for file in files:
        (year, reg, rest) = file.split(" ", maxsplit=2)
        print("{}\t{}".format(year, reg))


if __name__ == "__main__":
    cli()
