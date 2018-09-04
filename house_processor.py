#!/usr/bin/env python3

import click
import tablib
from lxml import objectify
from os import path
import os
from pathlib import Path
from collections import namedtuple
import sys
import zipfile

@click.group()
def cli():
    pass

LOBBYIST_COLUMNS = ['first_name','last_name','suffix','covered_position','new']
Lobbyist = namedtuple('Lobbyist', LOBBYIST_COLUMNS)

REGISTRATION_COLUMNS = ['reg_type', 'organization_name', 'prefix', 'first_name', 'last_name', 'address1', 'address2', 'city', 'state', 'zip', 'zipext', 'country', 'principal_city', 'principal_state', 'principal_zip', 'principal_zipext', 'principal_country', 'contact_intl_phone', 'registrant_general_description', 'self_select', 'client_name', 'client_address', 'client_city', 'client_state', 'client_zip', 'client_zipext', 'client_country', 'prin_client_city', 'prin_client_state',     'prin_client_zip', 'prin_client_zipext', 'prin_client_country', 'client_general_description', 'senate_ID', 'house_ID', 'specific_issues', 'affiliated_url', 'report_year', 'report_yype', 'effective_date', 'printed_name', 'signed_date']
Registration = namedtuple('Registration', REGISTRATION_COLUMNS)

class HouseRegistrationsFile():
    def __init__(self, contents):
                if path.isfile(contents):
                    self.obj = objectify.parse(contents).getroot()
                else:
                    self.obj = objectify.fromstring(contents)

    def lobbyists(self):
        lobbyists = self.obj.lobbyists
        return [ Lobbyist(str(lobbyist.lobbyistFirstName).strip(),
            str(lobbyist.lobbyistLastName).strip(),
            str(lobbyist.lobbyistSuffix).strip(),
            str(lobbyist.coveredPosition).strip(),
            str(lobbyist.lobbyistNew).strip() == 'Y') for lobbyist in lobbyists.lobbyist if str(lobbyist.lobbyistFirstName).strip() or str(lobbyist.lobbyistLastName).strip()
        ]

    def registration(self):
        get_column = lambda c: str(self.obj[c]).strip() if hasattr(self.obj, c) else None
        return Registration(
            get_column('regType'),
            get_column('organizationName'),
            get_column('prefix'), get_column('firstName'),get_column('lastName'), get_column('address1'), get_column('address2'),
            get_column('city'),get_column('state'),get_column('zip'),get_column('zipext'),get_column('country'),get_column('principal_city'),get_column('principal_state'), get_column('principal_zip'), get_column('principal_zipext'), get_column('principal_country'), get_column('contactIntlPhone'), get_column('registrantGeneralDescription'), get_column('selfSelect'), get_column('clientName'), get_column('clientAddress'), get_column('clientCity'), get_column('clientState'), get_column('clientZip'), get_column('clientZipExt'), get_column('clientCountry'), get_column('prinClientCity'), get_column('prinClientState'), get_column('prinClientZip'), get_column('prinClientZipExt'), get_column('prinClientCountry'), get_column('clientGeneralDescription'), get_column('senateID'), get_column('houseID'), get_column('specific_issues'), get_column('affiliatedUrl'), get_column('reportYear'), get_column('reportType'), get_column('effectiveDate'), get_column('printedName'), get_column('signedDate')
        )


def read_files(files):
        for file in files:
            if path.isdir(file):
                for f in os.listdir(file):
                    yield Path(f).stem, path.join(file,f)
            elif zipfile.is_zipfile(file):
                zfile = zipfile.ZipFile(file, 'r')
                for name in zfile.namelist():
                    yield Path(name).stem, zfile.read(name)
            else:
                yield Path(file).stem, file

@cli.command()
@click.argument('files', nargs=-1, type=click.Path())
def registrations(files):
    COLUMNS = ['id'] + REGISTRATION_COLUMNS
    data = tablib.Dataset(headers=COLUMNS)
    data = tablib.Dataset(headers=COLUMNS)
    for (file_id, contents) in read_files(files):
        reg_file = HouseRegistrationsFile(contents)
        data.append([file_id] + list(reg_file.registration()))
    sys.stdout.buffer.write(data.export('csv').encode())


@cli.command()
@click.argument('files', nargs=-1, type=click.Path())
def lobbyists(files):
    COLUMNS = ['registration_id'] + LOBBYIST_COLUMNS
    data = tablib.Dataset(headers=COLUMNS)
    for (file_id, contents) in read_files(files):
        reg_file = HouseRegistrationsFile(contents)
        for lobbyist in reg_file.lobbyists():
            data.append([file_id] + list(lobbyist))
    sys.stdout.buffer.write(data.export('csv').encode())

if __name__ == '__main__':
    cli()
