import sys
from pathlib import Path

import typesense

# Ensure we can import the shared Typesense client from the scripts folder
PROJECT_SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(PROJECT_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_SCRIPTS_DIR))

from typesense_client import get_client  # type: ignore


def main() -> None:
    """
    Delete the old 'public_works' collection from Typesense, if it exists.

    This is useful after migrating to the new collection name
    'ido_odop_public_works' aligned with the Oracle schema IDO_ODOP.
    """
    client: typesense.Client = get_client()

    try:
        client.collections["public_works"].delete()
        print("Collection 'public_works' deleted successfully.")
    except Exception as exc:  # noqa: BLE001
        print("Could not delete collection 'public_works':", exc)


if __name__ == "__main__":
    main()


