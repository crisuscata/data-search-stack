import json
from pathlib import Path

from typesense_client import get_products_collection


DATA_FILE = Path(__file__).with_name("products.json")


def main():
    """
    Load product records from a local JSON file and upsert them into Typesense.

    Expected JSON format in products.json:
    [
      {
        "id": "p001",
        "name": "Running Shoes",
        "category": "shoes",
        "price": 79.99
      },
      ...
    ]
    """
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Data file not found: {DATA_FILE}")

    with DATA_FILE.open(encoding="utf-8") as f:
        products = json.load(f)

    if not isinstance(products, list):
        raise ValueError("products.json must contain a JSON array of product objects")

    collection = get_products_collection()

    # Insert or update multiple documents
    response = collection.documents.import_(
        products,
        {"action": "upsert"},
    )

    print("Import result:", response)


if __name__ == "__main__":
    main()


