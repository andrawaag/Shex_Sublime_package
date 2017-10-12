from SPARQLWrapper import SPARQLWrapper, JSON
import pprint
import json
import os
import sys

sparql = SPARQLWrapper("http://www.ebi.ac.uk/rdf/services/atlas/sparql")

main_query = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX dbpedia2: <http://dbpedia.org/property/>
PREFIX dbpedia: <http://dbpedia.org/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT DISTINCT  ?allOlsOntologiesGraph
WHERE {
<http://rdf.ebi.ac.uk/dataset/ols> dcterms:hasPart  ?allOlsOntologiesGraph  .
}
"""
sparql.setQuery(main_query)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
for result in results["results"]["bindings"]:
     print(result["allOlsOntologiesGraph"]["value"])
     shex_completions = dict()
     shex_completions["scope"] = "source.shex"
     shex_completions["completions"] = []
     fn = os.path.join(os.path.dirname(__file__),
                       "../package/obo/" + result["allOlsOntologiesGraph"]["value"].replace("http://rdf.ebi.ac.uk/dataset/",
                                                                            "") + "_completions.sublime-completions")
     file = open(fn, "w")
     query = ("     PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n"
              "     PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n"
              "     PREFIX owl: <http://www.w3.org/2002/07/owl#>\n"
              "     PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\n"
              "     PREFIX dc: <http://purl.org/dc/elements/1.1/>\n"
              "     PREFIX dcterms: <http://purl.org/dc/terms/>\n"
              "     PREFIX dbpedia2: <http://dbpedia.org/property/>\n"
              "     PREFIX dbpedia: <http://dbpedia.org/>\n"
              "     PREFIX foaf: <http://xmlns.com/foaf/0.1/>\n"
              "     PREFIX skos: <http://www.w3.org/2004/02/skos/core#>\n"
              "\n"
              "     PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n"
              "     SELECT ?class ?label\n"
              "     FROM <http://rdf.ebi.ac.uk/dataset/"+result["allOlsOntologiesGraph"]["value"].replace("http://rdf.ebi.ac.uk/dataset/", "")+">"
              "     WHERE {"
              "          ?class rdfs:label ?label .}")

     sparql.setQuery(query)
     sparql.setReturnFormat(JSON)
     results = sparql.query().convert()
     for result in results["results"]["bindings"]:
          completion = dict()
          completion["trigger"] = result["label"]["value"]
          completion["contents"] = result["class"]["value"].replace("http://purl.obolibrary.org/obo/", "obo:")
          shex_completions["completions"].append(completion)

     pprint.pprint(shex_completions)
     file.write(json.dumps(shex_completions))
     file.close()