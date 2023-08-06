
import json

version_json = '''
{"date": "2021-01-02T21:29:34.622744", "dirty": false, "error": null, "full-revisionid": "38fa4c5c353afc14d32d43a78052d6db603d4311", "version": "0.26.0"}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

