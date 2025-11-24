import json

import typesense

client = typesense.Client({
    'nodes': [{
        'host': 'localhost',
        'port': '8108',
        'protocol': 'http'
    }],
    'api_key': 'xyz123',
    'connection_timeout_seconds': 2
})

collections = client.collections.retrieve()

# Pretty-print the JSON response
print(json.dumps(collections, indent=2, ensure_ascii=False))

