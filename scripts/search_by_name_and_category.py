import json

from typesense_client import get_products_collection


def main():
    collection = get_products_collection()

    search_parameters = {
        'q': 'calzado deportivos',
        'query_by': 'name,category'
    }

    results = collection.documents.search(search_parameters)

    # Pretty-print the JSON response
    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()

