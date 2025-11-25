import os


def main() -> None:
    """
    Print the current Oracle environment variables used by
    sync_public_works_from_oracle.py.
    """
    user = os.environ.get("ORACLE_USER")
    password = os.environ.get("ORACLE_PASSWORD")
    dsn = os.environ.get("ORACLE_DSN")

    print("ORACLE_USER    =", repr(user))
    print("ORACLE_PASSWORD=", repr(password))
    print("ORACLE_DSN     =", repr(dsn))

    if not user or not password or not dsn:
        print("\nOne or more variables are NOT set. Make sure to define:")
        print("  ORACLE_USER, ORACLE_PASSWORD, ORACLE_DSN")


if __name__ == "__main__":
    main()


