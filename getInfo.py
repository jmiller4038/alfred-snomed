 # encoding: utf-8

import requests
import sys

from workflow import ICON_WARNING, Workflow

EDITION = "us-edition"
VERSION = "20180301"
ENDPOINT = "https://prod-browser-exten.ihtsdotools.org/api/snomed/{0}/v{1}/concepts/{{0}}".format(EDITION, VERSION)

def get_term_result(term):
	r = requests.get(ENDPOINT.format(term))
	result = r.json()
	return result

def main(wf):
	term = wf.args[0]
	result = wf.cached_data(term, lambda: get_term_result(term), max_age=3600)
	if result:
		wf.add_item(
			title = result["defaultTerm"], 
			subtitle = result["conceptId"],
			arg = "{0} - {1}".format(result["conceptId"], result["defaultTerm"]),
			valid = True
		)
	else:
		wf.add_item(title = "No terms found", subtitle = "Try another term", icon = ICON_WARNING)	
	wf.send_feedback()

if __name__ == u"__main__":
	wf = Workflow()
	sys.exit(wf.run(main))
