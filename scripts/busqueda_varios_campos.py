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

search_parameters = {
    'q': 'calzado deportivos',
    'query_by': 'name,category'
}

results = client.collections['products'].documents.search(search_parameters)
print(results)