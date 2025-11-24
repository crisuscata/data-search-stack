## data-search-stack

Repositorio de ejemplo para levantar un servidor **Typesense** con **Docker** y probar búsquedas desde scripts de **Python**.

---

## Requisitos

- **Sistema operativo**: Windows 10/11 (probado en Windows 11).
- **Docker Desktop** instalado y funcionando.
- **Python**: versión **3.10+** (recomendado **3.11**).
- **IDE**: por ejemplo **Cursor** (basado en VS Code) con el **plugin/extensión de Python** habilitado (el plugin oficial de Microsoft funciona bien).

Opcionalmente puedes usar otro IDE siempre que tengas Python configurado en la terminal.

---

## Estructura del proyecto

- `docker-compose.yml`: define el servicio de **Typesense** en Docker.
- `scripts/`:
  - `typesense_client.py`: cliente compartido para conectarse a Typesense.
  - `insert_products.py`: inserta documentos de ejemplo en la colección `products`.
  - `busqueda_por_nombre.py`: búsqueda de productos por nombre.
  - `busqueda_multicampos.py`: búsqueda usando varios campos (`name`, `category`).
  - `busqueda_rango_precio.py`: búsqueda filtrando por rango de precio.
  - `busqueda_varios_campos.py`: ejemplo alternativo de búsqueda en varios campos.
  - `list_collections.py`: lista las colecciones configuradas en el servidor.
- `typesense-config/`: carpeta reservada para configuración y datos de Typesense.

---

## Levantar Typesense con Docker Compose

1. Asegúrate de tener **Docker Desktop** corriendo.
2. Desde la raíz del proyecto (`data-search-stack`), en una terminal (por ejemplo, la terminal integrada de Cursor), ejecuta:

   ```bash
   docker-compose up -d
   ```

   - Esto levantará un contenedor llamado `typesense-server` usando la imagen `typesense/typesense:27.1`.
   - El servicio quedará escuchando en `http://localhost:8108`.

3. Para detener el contenedor:

   ```bash
   docker-compose down
   ```

> **Nota:** En `docker-compose.yml` se define una API Key de ejemplo (`xyz123clave_admin_secreta`). Asegúrate de que coincida con la `api_key` configurada en los scripts de Python (`typesense_client.py`, etc.).

---

## Entorno de Python en el IDE (Cursor)

1. Abre la carpeta del proyecto (`data-search-stack`) en **Cursor**.
2. Verifica que el plugin/extensión de **Python** esté instalado y habilitado (el oficial de Microsoft es suficiente).
3. Abre una terminal integrada en Cursor (PowerShell o CMD) y crea un entorno virtual (opcional pero recomendado):

   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   ```

4. Instala las dependencias (una vez creado `requirements.txt`):

   ```powershell
   pip install -r requirements.txt
   ```

5. Configura en Cursor que use el intérprete de Python de tu entorno virtual (`.venv`) si lo deseas.

---

## Configuración del cliente Typesense en Python

El archivo `scripts/typesense_client.py` centraliza la configuración del cliente:

- Host: `localhost`
- Puerto: `8108`
- Protocolo: `http`
- `api_key`: **debe coincidir** con la API Key usada por el contenedor en `docker-compose.yml`.

Si cambias la API Key o el puerto en `docker-compose.yml`, actualiza también estos valores en `typesense_client.py`.

---

## Ejecución de scripts

Asegúrate de que:

- El contenedor de Typesense está **levantado** (`docker-compose up -d`).
- Tu entorno de Python tiene instaladas las dependencias.
- Estás situado en la carpeta `scripts` o llamas a los scripts con la ruta correcta.

### 1. Insertar productos de ejemplo

Desde la raíz del proyecto:

```powershell
cd scripts
python insert_products.py
```

Deberías ver una respuesta de importación de documentos indicando el resultado de la operación.

### 2. Listar colecciones

```powershell
cd scripts
python list_collections.py
```

Mostrará las colecciones creadas en Typesense (por ejemplo, `products`).

### 3. Búsqueda por nombre

```powershell
cd scripts
python busqueda_por_nombre.py
```

Realiza una búsqueda por texto en el campo `name` (por ejemplo, `zapatos`).

### 4. Búsqueda en varios campos

- Usando el cliente compartido:

  ```powershell
  cd scripts
  python busqueda_multicampos.py
  ```

- Usando el script alternativo:

  ```powershell
  cd scripts
  python busqueda_varios_campos.py
  ```

Ambos ejemplos realizan búsquedas donde se consulta por `name` y `category`.

### 5. Búsqueda por rango de precio

```powershell
cd scripts
python busqueda_rango_precio.py
```

Realiza una búsqueda (opcionalmente con texto) filtrando por `price` entre un mínimo y un máximo (`filter_by: price:>=50 && price:<=100`).

---

## Notas adicionales

- Si cambias el puerto, host o API Key en `docker-compose.yml`, recuerda **mantenerlos alineados** con los scripts de Python.
- Puedes ejecutar los scripts desde:
  - La **terminal integrada** de Cursor.
  - El botón de **Run**/Debug en el editor (si lo tienes configurado para Python).
- Si tienes errores de conexión, revisa:
  - Que el contenedor `typesense-server` esté corriendo.
  - Que el firewall no bloquee el puerto `8108`.
  - Que la `api_key` sea la misma en Docker y en los scripts.
