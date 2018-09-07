.DELETE_ON_ERROR:

clean:
	rm -rf output/*

data/files/house/%_XML.zip:
	mkdir -p $(dir $@)
	./house_fetcher.py download --file $(notdir $(basename $@)) > $@


output/house/%_Registrations_Records.csv: data/files/house/%_Registrations_XML.zip
	mkdir -p $(dir $@)
	./house_processor.py registrations $< > $@

output/house/%_Registrations_Lobbyists.csv: data/files/house/%_Registrations_XML.zip
	mkdir -p $(dir $@)
	./house_processor.py lobbyists $< > $@

output/house/%_Registrations_Issues.csv: data/files/house/%_Registrations_XML.zip
	mkdir -p $(dir $@)
	./house_processor.py issues $< > $@

output/house/%_Registrations_AffiliatedOrgs.csv: data/files/house/%_Registrations_XML.zip
	mkdir -p $(dir $@)
	./house_processor.py affiliated_orgs $< > $@

output/house/%_Registrations_ForeignEntities.csv: data/files/house/%_Registrations_XML.zip
	mkdir -p $(dir $@)
	./house_processor.py foreign_entities $< > $@

output/house/%_Reports.csv: data/files/house/%_XML.zip
	mkdir -p $(dir $@)
	./house_processor.py reports $< > $@

output/house/%_Reports_Issues.csv: data/files/house/%_XML.zip
	mkdir -p $(dir $@)
	./house_processor.py reports_issues $< > $@

output/house/%_Reports_Lobbyists.csv: data/files/house/%_XML.zip
	mkdir -p $(dir $@)
	./house_processor.py reports_lobbyists $< > $@
