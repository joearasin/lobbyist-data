.DELETE_ON_ERROR:

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

output/senate/%_Filings: output/senate/%_Filings.csv output/senate/%_Lobbyists.csv output/senate/%_Government_Entities.csv \
	output/senate/%_Issues.csv output/senate/%_ForeignEntities.csv output/senate/%_AffiliatedOrgs.csv
	echo "Done"
