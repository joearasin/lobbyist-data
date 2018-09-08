# lobbyist-data

A set of python scripts and makefiles for downloading and normalizing LD1 and LD2 data from the [House of Representatives](https://lobbyingdisclosure.house.gov) and [US Senate](https://www.senate.gov/legislative/Public_Disclosure/database_download.htm) for loading into a relational database.

## Usage

This project uses [pipenv](https://github.com/pypa/pipenv) to manage python dependencies. Install pipenv, then from this package, run:

```
pipenv install
pipenv shell
```

to have a virtual environment with all dependencies available.

```
make all
```

will then download and format everything (approximately 2GB of data)

## house_fetcher

The House of Representatives download page has some CSRF/CORS protection, so a simple curl request can't be used to download the files. Instead, this navigates to the website and submits the form.

`./house_fetcher.py list` will list available files to download

`./house_fetcher.py download` will download the requested file.

For example `./house_fetcher.py download --file 2018_Registrations` will download the 2018 Registrations file

## house_processor

This reads the LD1 and LD2 forms downloaded, and extracts assorted tables from the specified files.

For working with LD1 Documents, `./house_processor.py registrations <input>` will process the root documents, then any of
`affiliated_orgs`, `foreign_entities`, `issues`, and `lobbyists` will extract the relevant dimensions.

For House LD2 Documents, `./house_processor.py reports <input>` is the root document. `report_issues` and `report_lobbyists` are the rest of the main data. Any updates are available in `report_affiliated_orgs`, `report_foreign_entities`, `report_inactive_foreign_entities`, `report_inactive_issues`,`report_inactive_lobbyists`,`report_inactive_orgs`.

## senate_processor

The Senate packages LD1 and LD2 data together in the same file, by quarter. In addition, the Lobbyists aren't nested inside the issues the way they are in the house records, so it makes for easier processing. `./senate_processor.py filings <input>` will extract the root input, then any of `affiliated_orgs`, `foreign_entities`, `government_entities`, `issues`, and `lobbyists` can be used to extract the relevant information.
