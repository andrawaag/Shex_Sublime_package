from SPARQLWrapper import SPARQLWrapper, JSON
import pprint
import json
import os

sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
query = """
SELECT ?s ?property ?propertyLabel WHERE {
  ?property wikibase:claim ?s .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
"""
shex_completions= dict()
shex_completions["scope"] = "source.shex"
shex_completions["completions"] = []

file = open("wikidata_completions.sublime-completions", "w")
fn = os.path.join(os.path.dirname(__file__),
                       "../package/wikidata/wikidata_completions.sublime-completions")
file = open(fn, "w")
sparql.setQuery(query)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
for result in results["results"]["bindings"]:
     # { "trigger": "a", "contents": "<a href=\"$1\">$0</a>" },
     #          { "trigger": "abbr", "contents": "<abbr>$0</abbr>" },
     #           { "trigger": "acronym", "contents": "<acronym>$0</acronym>" }
     completion = dict()
     completion["trigger"] = result["propertyLabel"]["value"]
     completion["contents"] = result["s"]["value"].replace("http://www.wikidata.org/prop/", "")
     shex_completions["completions"].append(completion)

pprint.pprint(shex_completions)
file.write(json.dumps(shex_completions))
file.close()