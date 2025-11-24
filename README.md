## data-search-stack

Example repository to spin up a **Typesense** server with **Docker** and run search examples from **Python** scripts.

---

## Requirements

- **Operating system**: Windows 10/11 (tested on Windows 11).
- **Docker Desktop** installed and running.
- **Python**: version **3.10+** (recommended **3.11**).
- **IDE**: for example **Cursor** (VS Code–based) with the **Python extension** enabled (the official Microsoft extension `ms-python.python` works well).

You can use any other IDE as long as Python is correctly configured in the terminal.

---

## Project structure

- `docker-compose.yml`: defines the **Typesense** service running in Docker.
- `scripts/`:
  - `typesense_client.py`: shared client helper to connect to Typesense.
  - `seed_products.py`: inserts sample documents into the `products` collection.
  - `search_by_name.py`: search products by the `name` field.
  - `search_by_name_and_category.py`: search using multiple fields (`name`, `category`) via the shared client.
  - `search_by_price_range.py`: search filtering by price range.
  - `search_by_name_and_category_alt.py`: alternative multi-field search using a direct Typesense client instance.
  - `list_typesense_collections.py`: lists the collections configured on the Typesense server.
- `typesense-config/`: reserved folder for Typesense configuration and data.

---

## Running Typesense with Docker Compose

1. Make sure **Docker Desktop** is running.
2. From the project root (`data-search-stack`), in a terminal (for example, Cursor’s integrated terminal), run:

   ```bash
   docker-compose up -d
   ```

   - This will start a container called `typesense-server` using the image `typesense/typesense:27.1`.
   - The service will be available at `http://localhost:8108`.

3. To stop the container:

   ```bash
   docker-compose down
   ```

> **Note:** In `docker-compose.yml` an example API key is defined (`xyz123clave_admin_secreta`). Make sure it matches the `api_key` configured in the Python scripts (`typesense_client.py`, etc.).

---

## Python environment in the IDE (Cursor)

1. Open the project folder (`data-search-stack`) in **Cursor**.
2. Ensure the **Python** extension is installed and enabled (the official Microsoft extension is recommended).
3. Open an integrated terminal in Cursor (PowerShell or CMD) and create a virtual environment (optional but recommended):

   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   ```

4. Install the dependencies (once `requirements.txt` exists):

   ```powershell
   pip install -r requirements.txt
   ```

5. Optionally configure Cursor to use the Python interpreter from your virtual environment (`.venv`).  

---

## Typesense client configuration in Python

The file `scripts/typesense_client.py` centralizes the Typesense client configuration:

- Host: `localhost`
- Port: `8108`
- Protocol: `http`
- `api_key`: **must match** the API key used by the container in `docker-compose.yml`.

If you change the API key or port in `docker-compose.yml`, update these values accordingly in `typesense_client.py`.

---

## Running the example scripts

Before running any script, make sure that:

- The Typesense container is **running** (`docker-compose up -d`).
- Your Python environment has the dependencies installed.
- You are either inside the `scripts` folder or calling the scripts with the correct path.

### 1. Seed sample products

From the project root:

```powershell
cd scripts
python seed_products.py
```

You should see an import response indicating the result of the operation.

### 2. List collections

```powershell
cd scripts
python list_typesense_collections.py
```

This will print the collections created in Typesense (for example, `products`).

### 3. Search by name

```powershell
cd scripts
python search_by_name.py
```

Performs a text search on the `name` field (for example, `zapatos`).  

### 4. Search by name and category (multi-field)

- Using the shared client helper:

  ```powershell
  cd scripts
  python search_by_name_and_category.py
  ```

- Using the alternative script (direct Typesense client):

  ```powershell
  cd scripts
  python search_by_name_and_category_alt.py
  ```

Both examples run a search that queries across `name` and `category`.

### 5. Search by price range

```powershell
cd scripts
python search_by_price_range.py
```

Performs a search (optionally with text) filtering `price` between a minimum and maximum (`filter_by: price:>=50 && price:<=100`).  

---

## Additional notes

- If you change the port, host, or API key in `docker-compose.yml`, remember to **keep them aligned** with the Python scripts.
- You can run the scripts from:
  - Cursor’s **integrated terminal**.
  - The **Run/Debug** button in the editor (if configured for Python).
- If you encounter connection errors, check that:
  - The `typesense-server` container is running.
  - The firewall is not blocking port `8108`.
  - The `api_key` is the same in Docker and in the scripts.
