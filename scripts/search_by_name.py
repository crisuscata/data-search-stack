from typesense_client import get_products_collection


def main():
    collection = get_products_collection()

    # Search by text in the "name" field
    search_parameters = {
        'q': 'zapatos',           # text to search
        'query_by': 'name'        # fields to search on
    }

    results = collection.documents.search(search_parameters)
    print(results)


if __name__ == '__main__':
    main()


