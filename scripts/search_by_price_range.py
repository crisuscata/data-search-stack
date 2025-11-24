from typesense_client import get_products_collection


def main():
    collection = get_products_collection()

    search_parameters = {
        'q': 'tenis',                 # can be empty: '' if you only filter
        'query_by': 'name',
        'filter_by': 'price:>=50 && price:<=100'
    }

    results = collection.documents.search(search_parameters)
    print(results)


if __name__ == '__main__':
    main()


