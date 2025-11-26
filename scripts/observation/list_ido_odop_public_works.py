import json
import sys
from pathlib import Path

# Ensure we can import the shared Typesense client from the scripts folder
PROJECT_SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(PROJECT_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_SCRIPTS_DIR))

from typesense_client import get_ido_odop_public_works_collection


LOG_FILE = Path(__file__).with_name("list_ido_odop_public_works.log")


def main() -> None:
    """
    List all documents stored in the 'public_works' collection in Typesense
    and write the JSON output to a log file in this folder.
    """
    collection = get_ido_odop_public_works_collection()

    search_parameters = {
        "q": "*",  # match all
        "query_by": "name,ubigeo,status",
        "per_page": 250,
        "page": 1,
    }

    results = collection.documents.search(search_parameters)

    pretty = json.dumps(results, indent=2, ensure_ascii=False)

    # Print to console
    print(pretty)

    # Also write to a log file in the same folder
    LOG_FILE.write_text(pretty, encoding="utf-8")
    print(f"\nLog written to: {LOG_FILE}")


if __name__ == "__main__":
    main()



