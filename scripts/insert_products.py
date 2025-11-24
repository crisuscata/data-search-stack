from typesense_client import get_products_collection

# Productos a insertar
products = [
    {
        "id": "p001",
        "name": "Zapatos deportivos",
        "category": "calzado",
        "price": 79.99
    },
    {
        "id": "p002",
        "name": "Tenis Puma Running",
        "category": "calzado",
        "price": 60.50
    },
    {
        "id": "p003",
        "name": "Sandalias Nike",
        "category": "calzado",
        "price": 45.90
    },
    {
        "id": "p004",
        "name": "Botas Timberland",
        "category": "botas",
        "price": 120.00
    },
    {
        "id": "p005",
        "name": "Zapatillas new star",
        "category": "calzado",
        "price": 500.00
    }
]


def main():
    collection = get_products_collection()

    # Insertar varios documentos
    response = collection.documents.import_(
        products,
        {'action': 'upsert'}
    )

    print("Resultado:", response)


if __name__ == '__main__':
    main()
