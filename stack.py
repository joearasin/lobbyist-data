#!/usr/bin/env python3

import click
import pandas as pd
from pathlib import Path
import sys


def read_senate_file(filename):
    (year, quarter, contents) = Path(filename).stem.split("_", maxsplit=2)
    df = pd.read_csv(filename)
    df.insert(0, "file_year", year)
    df.insert(1, "file_quarter", quarter)
    return df


def read_house(filename):
    (year, reporting_window, contents) = Path(filename).stem.split("_", maxsplit=2)
    df = pd.read_csv(filename, dtype=object)
    df.insert(0, "file_year", year)
    if reporting_window != "Registrations":
        df.insert(1, "file_reporting_window", reporting_window)
    return df


@click.group()
def cli():
    pass


@cli.command()
@click.argument("files", nargs=-1, type=click.Path())
def house(files):
    frames = [read_house(file) for file in files]
    stack = pd.concat(frames)
    stack.to_csv(sys.stdout, index=False)


@cli.command()
@click.argument("files", nargs=-1, type=click.Path())
def senate(files):
    frames = [read_senate_file(file) for file in files]
    stack = pd.concat(frames)
    stack.to_csv(sys.stdout, index=False)


if __name__ == "__main__":
    cli()
