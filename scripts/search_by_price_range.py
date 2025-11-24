import json

from typesense_client import get_products_collection


def main():
    collection = get_products_collection()

    search_parameters = {
        'q': 'tenis',                 # can be empty: '' if you only filter
        'query_by': 'name',
        'filter_by': 'price:>=50 && price:<=100'
    }

    results = collection.documents.search(search_parameters)

    # Pretty-print the JSON response
    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()

