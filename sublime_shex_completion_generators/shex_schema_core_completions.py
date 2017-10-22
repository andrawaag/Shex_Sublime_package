import requests
import os
import json

def leaf(subschema, completions):
    completion = dict()
    completion["trigger"] = subschema["name"]
    completion["contents"] = subschema["@id"]
    completions["completions"].append(completion)
    print(subschema["name"], subschema["@id"])
    if 'children' in subschema.keys():
        for child in subschema["children"]:
            leaf(child, completions)

fn = os.path.join(os.path.dirname(__file__),
                       "../package/schema/core/core_completions.sublime-completions")
file = open(fn, "w")

shex_completions = dict()
shex_completions["scope"] = "source.shex"
shex_completions["completions"] = []

r = requests.get("http://schema.org/docs/tree.jsonld")
schema = r.json()
leaf(schema, shex_completions)
file.write(json.dumps(shex_completions, indent=4, sort_keys=True))
file.close()


# pprint.pprint(schema)

