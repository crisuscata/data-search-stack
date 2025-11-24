from typesense_client import get_products_collection


def main():
    collection = get_products_collection()

    search_parameters = {
        'q': 'calzado deportivos',
        'query_by': 'name,category'
    }

    results = collection.documents.search(search_parameters)
    print(results)


if __name__ == '__main__':
    main()



