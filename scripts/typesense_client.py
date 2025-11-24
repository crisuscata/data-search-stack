import typesense


def get_client():
    """
    Devuelve una instancia de cliente Typesense reutilizable.
    Ajusta aquí host, puerto, protocolo y api_key en un solo lugar.
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
    Helper para devolver directamente la colección 'products'.
    """
    client = get_client()
    return client.collections['products']


