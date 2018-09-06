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

AFFILIATED_ORG_COLUMNS = ['name', 'address', 'city', 'state', 'zip', 'country', 'prin_org_city', 'prin_org_state', 'prin_org_country']
AffiliatedOrg = namedtuple('AffiliatedOrg', AFFILIATED_ORG_COLUMNS)

FOREIGN_ENTITY_COLUMNS = ['name', 'address', 'city', 'state', 'country', 'prin_city', 'prin_state', 'prin_country', 'contribution', 'ownership_percentage']
ForeignEntity = namedtuple('ForeignEntity', FOREIGN_ENTITY_COLUMNS)

def clean(field):
    return str(field).strip()

class HouseRegistrationsFile():
    def __init__(self, contents):
        if path.isfile(contents):
            obj = objectify.parse(contents).getroot()
        else:
            obj = objectify.fromstring(contents)
        if("LOBBYINGDISCLOSURE1" in obj.tag):
            # Match on substring b/c some documents have a namespace
            self.obj = obj
        else:
            raise ValueError("Document is not an LOBBYINGDISCLOSURE1. It is a {}".format(obj.tag))

    def lobbyists(self):
        lobbyists = self.obj.lobbyists
        return [ Lobbyist(clean(lobbyist.lobbyistFirstName),
            clean(lobbyist.lobbyistLastName),
            clean(lobbyist.lobbyistSuffix),
            clean(lobbyist.coveredPosition),
            clean(lobbyist.lobbyistNew) == 'Y') for lobbyist in lobbyists.lobbyist if clean(lobbyist.lobbyistFirstName) or clean(lobbyist.lobbyistLastName)
        ]

    def registration(self):
        get_column = lambda c: clean(self.obj[c]) if hasattr(self.obj, c) else None
        return Registration(
            get_column('regType'),
            get_column('organizationName'),
            get_column('prefix'), get_column('firstName'),get_column('lastName'), get_column('address1'), get_column('address2'),
            get_column('city'),get_column('state'),get_column('zip'),get_column('zipext'),get_column('country'),get_column('principal_city'),get_column('principal_state'), get_column('principal_zip'), get_column('principal_zipext'), get_column('principal_country'), get_column('contactIntlPhone'), get_column('registrantGeneralDescription'), get_column('selfSelect'), get_column('clientName'), get_column('clientAddress'), get_column('clientCity'), get_column('clientState'), get_column('clientZip'), get_column('clientZipExt'), get_column('clientCountry'), get_column('prinClientCity'), get_column('prinClientState'), get_column('prinClientZip'), get_column('prinClientZipExt'), get_column('prinClientCountry'), get_column('clientGeneralDescription'), get_column('senateID'), get_column('houseID'), get_column('specific_issues'), get_column('affiliatedUrl'), get_column('reportYear'), get_column('reportType'), get_column('effectiveDate'), get_column('printedName'), get_column('signedDate')
        )

    def issues(self):
        alis = self.obj.alis
        if(hasattr(alis, 'ali_Code')):
            return [ clean(ali_code) for ali_code in alis.ali_Code if clean(ali_code)]
        return []

    def affiliated_orgs(self):
        affiliated_orgs = self.obj.affiliatedOrgs
        return [ AffiliatedOrg(
                    clean(org.affiliatedOrgName),
                    clean(org.affiliatedOrgAddress),
                    clean(org.affiliatedOrgCity),
                    clean(org.affiliatedOrgState),
                    clean(org.affiliatedOrgZip),
                    clean(org.affiliatedOrgCountry),
                    clean(org.affiliatedPrinOrgCity),
                    clean(org.affiliatedPrinOrgState),
                    clean(org.affiliatedPrinOrgCountry)) for org in affiliated_orgs.affiliatedOrg if clean(org.affiliatedOrgName)
        ]

    def foreign_entities(self):
        foreign_entities = self.obj.foreignEntities
        return [ ForeignEntity(
                    clean(entity.name),
                    clean(entity.address),
                    clean(entity.city),
                    clean(entity.state),
                    clean(entity.country),
                    clean(entity.prinCity),
                    clean(entity.prinState),
                    clean(entity.prinCountry),
                    clean(entity.contribution),
                    clean(entity.ownership_Percentage)) for entity in foreign_entities.foreignEntity if clean(entity.name)
        ]

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

def read_registrations(files):
    for (file_id, contents) in read_files(files):
        try:
            reg_file = HouseRegistrationsFile(contents)
            yield file_id, reg_file
        except ValueError as err:
            print("Could not read {}. Error: {}".format(file_id, err), file=sys.stderr)

@cli.command()
@click.argument('files', nargs=-1, type=click.Path())
def registrations(files):
    COLUMNS = ['id'] + REGISTRATION_COLUMNS
    data = tablib.Dataset(headers=COLUMNS)
    data = tablib.Dataset(headers=COLUMNS)
    for (file_id, registration) in read_registrations(files):
        data.append([file_id] + list(registration.registration()))
    sys.stdout.buffer.write(data.export('csv').encode())


@cli.command()
@click.argument('files', nargs=-1, type=click.Path())
def lobbyists(files):
    COLUMNS = ['registration_id'] + LOBBYIST_COLUMNS
    data = tablib.Dataset(headers=COLUMNS)
    for (file_id, registration) in read_registrations(files):
        for lobbyist in registration.lobbyists():
            data.append([file_id] + list(lobbyist))
    sys.stdout.buffer.write(data.export('csv').encode())

@cli.command()
@click.argument('files', nargs=-1, type=click.Path())
def issues(files):
    COLUMNS = ['registration_id', 'ali_code']
    data = tablib.Dataset(headers=COLUMNS)
    for (file_id, registration) in read_registrations(files):
        for issue in registration.issues():
            data.append([file_id, issue])
    sys.stdout.buffer.write(data.export('csv').encode())

@cli.command()
@click.argument('files', nargs=-1, type=click.Path())
def affiliated_orgs(files):
    COLUMNS = ['registration_id'] + AFFILIATED_ORG_COLUMNS
    data = tablib.Dataset(headers=COLUMNS)
    for (file_id, registration) in read_registrations(files):
        for org in registration.affiliated_orgs():
            data.append([file_id] + list(org))
    sys.stdout.buffer.write(data.export('csv').encode())


@cli.command()
@click.argument('files', nargs=-1, type=click.Path())
def foreign_entities(files):
    COLUMNS = ['registration_id'] + FOREIGN_ENTITY_COLUMNS
    data = tablib.Dataset(headers=COLUMNS)
    for (file_id, registration) in read_registrations(files):
        for entity in registration.foreign_entities():
            data.append([file_id] + list(entity))
    sys.stdout.buffer.write(data.export('csv').encode())



if __name__ == '__main__':
    cli()
