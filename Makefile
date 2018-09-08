.DELETE_ON_ERROR:

.PHONY: all senate_all house_all senate_stacks house_stacks house_registration_stacks

all: senate_all house_all

senate_stacks: output/stacked/senate/Filings.csv output/stacked/senate/Lobbyists.csv  output/stacked/senate/Government_Entities.csv output/stacked/senate/Issues.csv output/stacked/senate/ForeignEntities.csv output/stacked/senate/AffiliatedOrgs.csv

house_stacks: house_registration_stacks house_report_stacks

house_registration_stacks: output/stacked/house/Registrations_AffiliatedOrgs.csv output/stacked/house/Registrations_ForeignEntities.csv output/stacked/house/Registrations_Issues.csv output/stacked/house/Registrations_Lobbyists.csv output/stacked/house/Registrations_Records.csv

house_report_stacks: output/stacked/house/Reports.csv \
	 									 output/stacked/house/Reports_Affiliated_Orgs.csv \
										 output/stacked/house/Reports_ForeignEntities.csv \
										 output/stacked/house/Reports_Issues.csv \
										 output/stacked/house/Reports_Lobbyists.csv \
										 output/stacked/house/Reports_Inactive_ForeignEntities.csv \
										 output/stacked/house/Reports_Inactive_Issues.csv \
										 output/stacked/house/Reports_Inactive_Lobbyists.csv \
										 output/stacked/house/Reports_Inactive_Orgs.csv

output/stacked/house/%.csv:
	mkdir -p $(dir $@)
	./stack.py house output/house/*_$(notdir $@) > $@

output/stacked/senate/%.csv:
	mkdir -p $(dir $@)
	./stack.py senate output/senate/*_$(notdir $@) > $@

senate_all: output/senate/1999_Year output/senate/2000_Year output/senate/2001_Year \
	output/senate/2002_Year output/senate/2003_Year output/senate/2004_Year output/senate/2005_Year \
	output/senate/2006_Year output/senate/2007_Year output/senate/2008_Year output/senate/2009_Year \
	output/senate/2006_Year output/senate/2007_Year output/senate/2008_Year output/senate/2009_Year \
	output/senate/2010_Year output/senate/2011_Year output/senate/2012_Year output/senate/2013_Year \
	output/senate/2014_Year output/senate/2015_Year output/senate/2016_Year output/senate/2017_Year \
	output/senate/2018_1_Filings output/senate/2018_2_Filings output/senate/2018_3_Filings

house_all: output/house/2004_OldYear output/house/2005_OldYear output/house/2006_OldYear output/house/2007_OldYear \
	output/house/2008_Year output/house/2009_Year output/house/2010_Year output/house/2011_Year output/house/2012_Year \
	output/house/2013_Year output/house/2014_Year output/house/2015_Year output/house/2016_Year output/house/2017_Year \
	output/house/2018_Registrations output/house/2018_1stQuarter_Reports output/house/2018_2ndQuarter_Reports output/house/2018_3rdQuarter_Reports

clean:
	rm -rf output/*

data/files/house/%_XML.zip:
	mkdir -p $(dir $@)
	./house_fetcher.py download --file $(notdir $(basename $@)) > $@

data/files/senate/%.zip:
	mkdir -p $(dir $@)
	curl --output $@ --create-dirs -L http://soprweb.senate.gov/downloads/$(notdir $(basename $@)).zip

.PRECIOUS: output/house/%_Registrations_Records.csv
output/house/%_Registrations_Records.csv: data/files/house/%_Registrations_XML.zip
	mkdir -p $(dir $@)
	./house_processor.py registrations $< > $@

.PRECIOUS: output/house/%_Registrations_Lobbyists.csv
output/house/%_Registrations_Lobbyists.csv: data/files/house/%_Registrations_XML.zip
	mkdir -p $(dir $@)
	./house_processor.py lobbyists $< > $@

.PRECIOUS: output/house/%_Registrations_Issues.csv
output/house/%_Registrations_Issues.csv: data/files/house/%_Registrations_XML.zip
	mkdir -p $(dir $@)
	./house_processor.py issues $< > $@

.PRECIOUS: output/house/%_Registrations_AffiliatedOrgs.csv
output/house/%_Registrations_AffiliatedOrgs.csv: data/files/house/%_Registrations_XML.zip
	mkdir -p $(dir $@)
	./house_processor.py affiliated_orgs $< > $@

.PRECIOUS: output/house/%_Registrations_ForeignEntities.csv
output/house/%_Registrations_ForeignEntities.csv: data/files/house/%_Registrations_XML.zip
	mkdir -p $(dir $@)
	./house_processor.py foreign_entities $< > $@

output/house/%_Registrations: output/house/%_Registrations_Records.csv output/house/%_Registrations_Lobbyists.csv \
	output/house/%_Registrations_Issues.csv output/house/%_Registrations_AffiliatedOrgs.csv output/house/%_Registrations_ForeignEntities.csv
	echo "Done"

.PRECIOUS: output/house/%_Reports.csv
output/house/%_Reports.csv: data/files/house/%_XML.zip
	mkdir -p $(dir $@)
	./house_processor.py reports $< > $@

.PRECIOUS: output/house/%_Reports_Issues.csv
output/house/%_Reports_Issues.csv: data/files/house/%_XML.zip
	mkdir -p $(dir $@)
	./house_processor.py report_issues $< > $@

.PRECIOUS: output/house/%_Reports_Lobbyists.csv
output/house/%_Reports_Lobbyists.csv: data/files/house/%_XML.zip
	mkdir -p $(dir $@)
	./house_processor.py report_lobbyists $< > $@

.PRECIOUS: output/house/%_Reports_Inactive_Lobbyists.csv
output/house/%_Reports_Inactive_Lobbyists.csv: data/files/house/%_XML.zip
	mkdir -p $(dir $@)
	./house_processor.py report_inactive_lobbyists $< > $@

.PRECIOUS: output/house/%_Reports_Inactive_Issues.csv
output/house/%_Reports_Inactive_Issues.csv: data/files/house/%_XML.zip
	mkdir -p $(dir $@)
	./house_processor.py report_inactive_issues $< > $@

.PRECIOUS: output/house/%_Reports_Affiliated_Orgs.csv
output/house/%_Reports_Affiliated_Orgs.csv: data/files/house/%_XML.zip
	mkdir -p $(dir $@)
	./house_processor.py report_affiliated_orgs $< > $@

.PRECIOUS: output/house/%_Reports_Inactive_Orgs.csv
output/house/%_Reports_Inactive_Orgs.csv: data/files/house/%_XML.zip
	mkdir -p $(dir $@)
	./house_processor.py report_inactive_orgs $< > $@

.PRECIOUS: output/house/%_Reports_ForeignEntities.csv
output/house/%_Reports_ForeignEntities.csv: data/files/house/%_XML.zip
	mkdir -p $(dir $@)
	./house_processor.py report_foreign_entities $< > $@

.PRECIOUS: output/house/%_Reports_Inactive_ForeignEntities.csv
output/house/%_Reports_Inactive_ForeignEntities.csv: data/files/house/%_XML.zip
	mkdir -p $(dir $@)
	./house_processor.py report_inactive_foreign_entities $< > $@

output/house/%_Reports: output/house/%_Reports.csv output/house/%_Reports_Issues.csv output/house/%_Reports_Lobbyists.csv \
	output/house/%_Reports_Inactive_Lobbyists.csv output/house/%_Reports_Inactive_Issues.csv output/house/%_Reports_Affiliated_Orgs.csv \
	output/house/%_Reports_Inactive_Orgs.csv output/house/%_Reports_ForeignEntities.csv output/house/%_Reports_Inactive_ForeignEntities.csv
	echo "Done"

output/house/%_Year: output/house/%_Registrations output/house/%_1stQuarter_Reports output/house/%_2ndQuarter_Reports output/house/%_3rdQuarter_Reports output/house/%_4thQuarter_Reports
	echo "Done"

output/house/%_OldYear: output/house/%_Registrations output/house/%_MidYear_Reports output/house/%_YearEnd_Reports
	echo "Done"

.PRECIOUS: output/senate/%_Filings.csv
output/senate/%_Filings.csv: data/files/senate/%.zip
	mkdir -p $(dir $@)
	./senate_processor.py filings $< > $@


.PRECIOUS: output/senate/%_Lobbyists.csv
output/senate/%_Lobbyists.csv: data/files/senate/%.zip
	mkdir -p $(dir $@)
	./senate_processor.py lobbyists $< > $@

.PRECIOUS: output/senate/%_Government_Entities.csv
output/senate/%_Government_Entities.csv: data/files/senate/%.zip
	mkdir -p $(dir $@)
	./senate_processor.py government_entities $< > $@

.PRECIOUS: output/senate/%_Issues.csv
output/senate/%_Issues.csv: data/files/senate/%.zip
	mkdir -p $(dir $@)
	./senate_processor.py issues $< > $@

.PRECIOUS: output/senate/%_ForeignEntities.csv
output/senate/%_ForeignEntities.csv: data/files/senate/%.zip
	mkdir -p $(dir $@)
	./senate_processor.py foreign_entities $< > $@

.PRECIOUS: output/senate/%_AffiliatedOrgs.csv
output/senate/%_AffiliatedOrgs.csv: data/files/senate/%.zip
	mkdir -p $(dir $@)
	./senate_processor.py affiliated_orgs $< > $@

output/senate/%_Year: output/senate/%_1_Filings output/senate/%_2_Filings output/senate/%_3_Filings output/senate/%_4_Filings
	echo "Done"

output/senate/%_Filings: output/senate/%_Filings.csv output/senate/%_Lobbyists.csv output/senate/%_Government_Entities.csv \
	output/senate/%_Issues.csv output/senate/%_ForeignEntities.csv output/senate/%_AffiliatedOrgs.csv
	echo "Done"
