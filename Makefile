.DELETE_ON_ERROR:

clean:
	rm -rf output/*

data/files/house/%_XML.zip:
	mkdir -p $(dir $@)
	./house_fetcher.py download --file $(notdir $(basename $@)) > $@

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
