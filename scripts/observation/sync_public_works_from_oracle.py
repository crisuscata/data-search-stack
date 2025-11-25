import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List

import oracledb

# Make sure we can import the shared Typesense client when running this file directly.
PROJECT_SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(PROJECT_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_SCRIPTS_DIR))

from typesense_client import get_client, get_public_works_collection


# -----------------------------
# Oracle connection helpers
# -----------------------------

def get_oracle_connection() -> oracledb.Connection:
    """
    Create an Oracle connection using environment variables.

    Required environment variables:
      - ORACLE_USER
      - ORACLE_PASSWORD
      - ORACLE_DSN   (for example: host:port/service_name)
    """
    user = os.environ.get("ORACLE_USER")
    password = os.environ.get("ORACLE_PASSWORD")
    dsn = os.environ.get("ORACLE_DSN")

    if not user or not password or not dsn:
        raise RuntimeError(
            "ORACLE_USER, ORACLE_PASSWORD and ORACLE_DSN environment variables must be set"
        )

    # Thin mode by default (no Oracle Client required)
    return oracledb.connect(user=user, password=password, dsn=dsn)


# -----------------------------
# Typesense schema & helpers
# -----------------------------

PUBLIC_WORKS_COLLECTION_NAME = "public_works"


def ensure_public_works_collection() -> None:
    """
    Ensure the 'public_works' collection exists in Typesense with an appropriate schema.
    If it already exists, this function does nothing.
    """
    client = get_client()

    try:
        client.collections[PUBLIC_WORKS_COLLECTION_NAME].retrieve()
        return
    except Exception:
        # Collection does not exist (or another error) -> try to create it.
        schema = {
            "name": PUBLIC_WORKS_COLLECTION_NAME,
            "fields": [
                {"name": "id", "type": "string"},
                {"name": "name", "type": "string"},
                {"name": "snip_code", "type": "string", "facet": True},
                {"name": "cui_code", "type": "string", "facet": True},
                {"name": "infobras_id", "type": "string", "facet": True},
                {"name": "ubigeo", "type": "string", "facet": True, "optional": True},
                {"name": "execution_year", "type": "int32", "optional": True},
                {"name": "state_id", "type": "int32", "optional": True},
                {"name": "status", "type": "string", "facet": True, "optional": True},
                {"name": "lat", "type": "float", "optional": True},
                {"name": "lng", "type": "float", "optional": True},
                {"name": "start_date", "type": "string", "optional": True},
                {"name": "end_date", "type": "string", "optional": True},
                {"name": "entity_id", "type": "int32", "optional": True},
                {"name": "amount_viable", "type": "float", "optional": True},
                {"name": "amount_approved", "type": "float", "optional": True},
                {"name": "source_amount", "type": "string", "optional": True},
                {"name": "source_cui", "type": "string", "optional": True},
                {"name": "source_name", "type": "string", "optional": True},
                {"name": "execution_mode_id", "type": "int32", "optional": True},
                {"name": "investment_phase_id", "type": "int32", "optional": True},
                {"name": "resident_id", "type": "int32", "optional": True},
                {"name": "supervisor_id", "type": "int32", "optional": True},
                {"name": "contractor_id", "type": "int32", "optional": True},
            ],
            # Use execution year as default sorting field
            "default_sorting_field": "execution_year",
        }
        client.collections.create(schema)


def oracle_row_to_document(row: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map a row from IDO_ODOP.ODTM_OBRA_PUBLICA to a Typesense document.

    Expected Oracle columns (based on the SELECT you tested):
      ID_OBRA_PUBLICA, CO_SNIP, CO_CUI, ID_INFOBRAS, NO_INVERSION,
      CO_UBIGEO, NU_ANIO_EJECUCION, ID_ESTADO_OBRA, TI_SITUACION_OBRA,
      ME_LATITUD, ME_LONGITUD, FE_INICIO_EJECUCION, FE_FIN_EJECUCION,
      ID_ENTIDAD, MO_VIABLE, MO_APROBADO,
      TI_FUENTE_MONTO, TI_FUENTE_CUI, TI_FUENTE_NOMBRE,
      ID_MODALIDAD_EJECUCION, ID_FASE_INVERSION,
      ID_RESIDENTE, ID_SUPERVISOR, ID_CONTRATISTA
    """

    def to_int(value: Any) -> int | None:
        return int(value) if value is not None else None

    def to_float(value: Any) -> float | None:
        return float(value) if value is not None else None

    def to_iso_date(value: Any) -> str | None:
        # oracledb returns datetime/date objects; convert to ISO string if present
        if value is None:
            return None
        try:
            return value.isoformat()
        except AttributeError:
            return str(value)

    name = row.get("NO_INVERSION") or ""
    ubigeo = row.get("CO_UBIGEO") or ""
    execution_year = to_int(row.get("NU_ANIO_EJECUCION")) or 0

    return {
        "id": str(row["ID_OBRA_PUBLICA"]),
        "name": name,
        "snip_code": row.get("CO_SNIP"),
        "cui_code": row.get("CO_CUI"),
        "infobras_id": row.get("ID_INFOBRAS"),
        "ubigeo": ubigeo,
        "execution_year": execution_year,
        "state_id": to_int(row.get("ID_ESTADO_OBRA")),
        "status": row.get("TI_SITUACION_OBRA"),
        "lat": to_float(row.get("ME_LATITUD")),
        "lng": to_float(row.get("ME_LONGITUD")),
        "start_date": to_iso_date(row.get("FE_INICIO_EJECUCION")),
        "end_date": to_iso_date(row.get("FE_FIN_EJECUCION")),
        "entity_id": to_int(row.get("ID_ENTIDAD")),
        "amount_viable": to_float(row.get("MO_VIABLE")),
        "amount_approved": to_float(row.get("MO_APROBADO")),
        "source_amount": row.get("TI_FUENTE_MONTO"),
        "source_cui": row.get("TI_FUENTE_CUI"),
        "source_name": row.get("TI_FUENTE_NOMBRE"),
        "execution_mode_id": to_int(row.get("ID_MODALIDAD_EJECUCION")),
        "investment_phase_id": to_int(row.get("ID_FASE_INVERSION")),
        "resident_id": to_int(row.get("ID_RESIDENTE")),
        "supervisor_id": to_int(row.get("ID_SUPERVISOR")),
        "contractor_id": to_int(row.get("ID_CONTRATISTA")),
    }


def fetch_public_works_rows(conn: oracledb.Connection) -> Iterable[Dict[str, Any]]:
    """
    Fetch all rows from IDO_ODOP.ODTM_OBRA_PUBLICA and yield them as dicts.
    """
    sql = """
        SELECT
          ID_OBRA_PUBLICA,
          CO_SNIP,
          CO_CUI,
          ID_INFOBRAS,
          NO_INVERSION,
          CO_UBIGEO,
          NU_ANIO_EJECUCION,
          ID_ESTADO_OBRA,
          TI_SITUACION_OBRA,
          ME_LATITUD,
          ME_LONGITUD,
          FE_INICIO_EJECUCION,
          FE_FIN_EJECUCION,
          ID_ENTIDAD,
          MO_VIABLE,
          MO_APROBADO,
          TI_FUENTE_MONTO,
          TI_FUENTE_CUI,
          TI_FUENTE_NOMBRE,
          ID_MODALIDAD_EJECUCION,
          ID_FASE_INVERSION,
          ID_RESIDENTE,
          ID_SUPERVISOR,
          ID_CONTRATISTA
        FROM IDO_ODOP.ODTM_OBRA_PUBLICA
    """
    with conn.cursor() as cursor:
        cursor.execute(sql)
        columns = [col[0] for col in cursor.description]
        for row in cursor:
            yield dict(zip(columns, row))


def chunked(iterable: Iterable[Dict[str, Any]], size: int) -> Iterable[List[Dict[str, Any]]]:
    """
    Yield lists of at most `size` elements from an iterable.
    """
    batch: List[Dict[str, Any]] = []
    for item in iterable:
        batch.append(item)
        if len(batch) >= size:
            yield batch
            batch = []
    if batch:
        yield batch


def main() -> None:
    """
    Sync all rows from Oracle table IDO_ODOP.ODTM_OBRA_PUBLICA into a
    Typesense collection called 'public_works'.

    Usage:
      - Set ORACLE_USER, ORACLE_PASSWORD, ORACLE_DSN in your environment.
      - Run: python -m observation.sync_public_works_from_oracle
    """
    ensure_public_works_collection()
    collection = get_public_works_collection()

    conn = get_oracle_connection()
    try:
        total_rows = 0
        total_imported = 0

        for batch_rows in chunked(fetch_public_works_rows(conn), size=250):
            docs = [oracle_row_to_document(row) for row in batch_rows]

            # Upsert all docs in a single call
            import_result = collection.documents.import_(
                docs,
                {"action": "upsert"},
            )

            total_rows += len(batch_rows)
            total_imported += len(docs)

            print("Batch imported:")
            print(json.dumps(import_result, indent=2, ensure_ascii=False))

        print(f"Done. Fetched {total_rows} rows from Oracle and upserted {total_imported} documents into Typesense.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()


