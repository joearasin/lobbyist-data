#!/usr/bin/env python3

import click
import tablib
from lxml import objectify, etree
from os import path
import os
from pathlib import Path
from collections import namedtuple
import sys
import zipfile


FILING_INFO_FIELDS = [
    "id",
    "year",
    "received",
    "amount",
    "type",
    "period",
    "registrant_id",
    "registrant_name",
    "registrant_general_description",
    "registrant_address",
    "registrant_country",
    "registrant_ppb_country",
    "client_id",
    "client_name",
    "client_general_description",
    "client_self_filer",
    "client_contact_fullname",
    "client_is_state_or_local_gov",
    "client_country",
    "client_ppb_country",
    "client_state",
    "client_ppb_state",
]

FilingInfo = namedtuple("Filing", FILING_INFO_FIELDS)

LOBBYIST_FIELDS = [
    "name",
    "covered_gov_position_indicator",
    "official_position",
    "activity_information",
]
Lobbyist = namedtuple("Lobbyist", LOBBYIST_FIELDS)

ISSUE_FIELDS = ["code", "specific_issue"]
Issue = namedtuple("Issue", ISSUE_FIELDS)

FOREIGN_ENTITY_FIELDS = [
    "name",
    "country",
    "ppb_country",
    "contribution",
    "ownership_percentage",
    "status",
]
ForeignEntity = namedtuple("ForeignEntity", FOREIGN_ENTITY_FIELDS)

AFFILIATED_ORG_FIELDS = ["name", "country", "ppb_country"]
AffiliatedOrg = namedtuple("AffiliatedOrg", AFFILIATED_ORG_FIELDS)


class Filing:
    def __init__(self, obj):
        self.obj = obj
        self.id = obj.get("ID")

    def info(self):
        obj = self.obj
        return FilingInfo(
            self.obj.get("ID"),
            self.obj.get("Year"),
            self.obj.get("Received"),
            self.obj.get("Amount"),
            self.obj.get("Type"),
            self.obj.get("Period"),
            self.obj.Registrant.get("RegistrantID"),
            self.obj.Registrant.get("RegistrantName"),
            self.obj.Registrant.get("GeneralDescription"),
            self.obj.Registrant.get("Address"),
            self.obj.Registrant.get("RegistrantCountry"),
            self.obj.Registrant.get("RegistrantPPBCountry"),
            self.obj.Registrant.get("ClientID"),
            self.obj.Registrant.get("ClientName"),
            self.obj.Registrant.get("GeneralDescription"),
            self.obj.Registrant.get("SelfFiler"),
            self.obj.Registrant.get("ContactFullname"),
            self.obj.Registrant.get("IsStateOrLocalGov"),
            self.obj.Registrant.get("ClientCountry"),
            self.obj.Registrant.get("ClientPPBCountry"),
            self.obj.Registrant.get("ClientState"),
            self.obj.Registrant.get("ClientPPBState"),
        )

    def lobbyists(self):
        if hasattr(self.obj, "Lobbyists"):
            return [
                Lobbyist(
                    lobbyist.get("LobbyistName"),
                    lobbyist.get("LobbyistCoveredGovPositionIndicator"),
                    lobbyist.get("OfficialPosition"),
                    lobbyist.get("ActivityInformation"),
                )
                for lobbyist in self.obj.Lobbyists.Lobbyist
            ]
        return []

    def government_entities(self):
        if hasattr(self.obj, "GovernmentEntities"):
            return [
                entity.get("GovEntityName")
                for entity in self.obj.GovernmentEntities.GovernmentEntity
            ]
        return []

    def issues(self):
        if hasattr(self.obj, "Issues"):
            return [
                Issue(issue.get("Code"), issue.get("SpecificIssue"))
                for issue in self.obj.Issues.Issue
            ]
        return []

    def foreign_entities(self):
        if hasattr(self.obj, "ForeignEntities"):
            return [
                ForeignEntity(
                    entity.get("ForeignEntityName"),
                    entity.get("ForeignEntityCountry"),
                    entity.get("ForeignEntityPPBcountry"),
                    entity.get("ForeignEntityContribution").strip(),
                    entity.get("ForeignEntityOwnershipPercentage"),
                    entity.get("ForeignEntityStatus"),
                )
                for entity in self.obj.ForeignEntities.Entity
            ]
        return []

    def affiliated_orgs(self):
        if hasattr(self.obj, "AffiliatedOrgs"):
            return [
                AffiliatedOrg(
                    org.get("AffiliatedOrgName"),
                    org.get("AffiliatedOrgCountry"),
                    org.get("AffiliatedOrgPPBCcountry"),
                )
                for org in self.obj.AffiliatedOrgs.Org
            ]
        return []


class SenateFile:
    def __init__(self, contents):
        try:
            if path.isfile(contents):
                obj = objectify.parse(contents).getroot()
            else:
                obj = objectify.fromstring(contents)
        except:
            obj = objectify.fromstring(contents)
        self.obj = obj

    def filings(self):
        return [Filing(filing) for filing in self.obj.Filing]


def read_files(files):
    for file in files:
        if path.isdir(file):
            for f in os.listdir(file):
                yield Path(f).stem, path.join(file, f)
        elif zipfile.is_zipfile(file):
            zfile = zipfile.ZipFile(file, "r")
            for name in zfile.namelist():
                yield Path(name).stem, zfile.read(name)
        else:
            yield Path(file).stem, file


def read_filings(files):
    for (file_id, contents) in read_files(files):
        try:
            file = SenateFile(contents)
            for filing in file.filings():
                yield filing
        except ValueError as err:
            print("Could not read {}. Error: {}".format(file_id, err), file=sys.stderr)


@click.group()
def cli():
    pass


@cli.command()
@click.argument("files", nargs=-1, type=click.Path())
def filings(files):
    COLUMNS = FILING_INFO_FIELDS
    data = tablib.Dataset(headers=COLUMNS)
    for filing in read_filings(files):
        data.append(list(filing.info()))
    sys.stdout.buffer.write(data.export("csv").encode())


@cli.command()
@click.argument("files", nargs=-1, type=click.Path())
def lobbyists(files):
    COLUMNS = ["filing_id"] + LOBBYIST_FIELDS
    data = tablib.Dataset(headers=COLUMNS)
    for filing in read_filings(files):
        for lobbyist in filing.lobbyists():
            data.append([filing.id] + list(lobbyist))
    sys.stdout.buffer.write(data.export("csv").encode())


@cli.command()
@click.argument("files", nargs=-1, type=click.Path())
def government_entities(files):
    COLUMNS = ["filing_id", "entity_name"]
    data = tablib.Dataset(headers=COLUMNS)
    for filing in read_filings(files):
        for entity in filing.government_entities():
            data.append([filing.id, entity])
    sys.stdout.buffer.write(data.export("csv").encode())


@cli.command()
@click.argument("files", nargs=-1, type=click.Path())
def issues(files):
    COLUMNS = ["filing_id"] + ISSUE_FIELDS
    data = tablib.Dataset(headers=COLUMNS)
    for filing in read_filings(files):
        for issue in filing.issues():
            data.append([filing.id] + list(issue))
    sys.stdout.buffer.write(data.export("csv").encode())


@cli.command()
@click.argument("files", nargs=-1, type=click.Path())
def foreign_entities(files):
    COLUMNS = ["filing_id"] + FOREIGN_ENTITY_FIELDS
    data = tablib.Dataset(headers=COLUMNS)
    for filing in read_filings(files):
        for entity in filing.foreign_entities():
            data.append([filing.id] + list(entity))
    sys.stdout.buffer.write(data.export("csv").encode())


@cli.command()
@click.argument("files", nargs=-1, type=click.Path())
def affiliated_orgs(files):
    COLUMNS = ["filing_id"] + AFFILIATED_ORG_FIELDS
    data = tablib.Dataset(headers=COLUMNS)
    for filing in read_filings(files):
        for org in filing.affiliated_orgs():
            data.append([filing.id] + list(org))
    sys.stdout.buffer.write(data.export("csv").encode())


if __name__ == "__main__":
    cli()
