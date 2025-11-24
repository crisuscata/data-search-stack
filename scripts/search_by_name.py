import json

from typesense_client import get_products_collection


def main():
    collection = get_products_collection()

    # Search by text in the "name" field
    search_parameters = {
        'q': 'Running',           # text to search
        'query_by': 'name'        # fields to search on
    }

    results = collection.documents.search(search_parameters)

    # Pretty-print the JSON response for easier reading in the IDE terminal
    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
