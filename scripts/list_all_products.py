import json

from typesense_client import get_products_collection


def main():
    """
    List all products from the `products` collection without any filters.

    Note: For large datasets you should implement pagination.
    Here we request up to 250 documents in a single page as an example.
    """
    collection = get_products_collection()

    search_parameters = {
        "q": "*",                    # match all
        "query_by": "name,category", # fields used for searching
        "per_page": 250,             # adjust as needed
        "page": 1,
    }

    results = collection.documents.search(search_parameters)

    # Pretty-print the JSON response
    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()


