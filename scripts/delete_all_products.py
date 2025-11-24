import json

from typesense_client import get_products_collection


def main():
    """
    Delete all documents in the `products` collection.

    WARNING: This removes every product currently indexed.
    """
    collection = get_products_collection()

    # `filter_by: *` isn't valid; instead we use a condition that matches everything.
    # In Typesense 0.25.x, an always-true filter like `id:!=0` is commonly used.
    result = collection.documents.delete({"filter_by": "id:!=0"})

    # Pretty-print the JSON response
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()


