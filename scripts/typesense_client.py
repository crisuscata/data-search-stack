import typesense


def get_client():
    """
    Return a reusable Typesense client instance.
    Adjust host, port, protocol and api_key in a single place.
    """
    return typesense.Client({
        'nodes': [{
            'host': 'localhost',
            'port': '8108',
            'protocol': 'http'
        }],
        'api_key': 'xyz123',
        'connection_timeout_seconds': 2
    })


def get_products_collection():
    """
    Helper to directly return the 'products' collection.
    """
    client = get_client()
    return client.collections['products']


def get_public_works_collection():
    """
    Helper to directly return the 'public_works' collection.

    The collection is expected to contain data from the Oracle table
    IDO_ODOP.ODTM_OBRA_PUBLICA.
    """
    client = get_client()
    return client.collections['public_works']


