from typesense_client import get_products_collection


def main():
    collection = get_products_collection()

    # Buscar por texto en el campo "name"
    search_parameters = {
        'q': 'zapatos',                # texto a buscar
        'query_by': 'name'             # campos donde buscar
    }

    results = collection.documents.search(search_parameters)
    print(results)


if __name__ == '__main__':
    main()