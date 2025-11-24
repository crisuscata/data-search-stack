import json
import sys

from typesense_client import get_products_collection


def main(product_id: str | None = None):
    """
    Delete a single product from the `products` collection by its id.

    Usage:
      python delete_product_by_id.py <PRODUCT_ID>
    """
    if product_id is None:
        # Try to read from CLI args
        if len(sys.argv) < 2:
            raise SystemExit("Usage: python delete_product_by_id.py <PRODUCT_ID>")
        product_id = sys.argv[1]

    collection = get_products_collection()

    result = collection.documents[product_id].delete()

    # Pretty-print the JSON response
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()


