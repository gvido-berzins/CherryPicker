from pathlib import Path
from typing import Any
import time

from cherry_picker.database import SQLiteClient

MODULE_DIR = Path(__file__).parent
CWD = Path().resolve()
DB_EXTENSIONS = ["ctb", "db"]
VERBOSE = 0

search_paths = set(
    [
        MODULE_DIR,
        CWD,
        # From config
    ]
)


def find_databases(paths: list[Path]) -> list[Path]:
    dbs = []
    for path in paths:
        dbs.extend(find_sqlite_db(path))
    return dbs


def find_sqlite_db(path: Path) -> list[Path]:
    return [file for ext in DB_EXTENSIONS for file in path.glob(f"*.{ext}")]


def pl(list_: list[Any]) -> None:
    [print(el) for el in list_]


def main():
    dbs = find_databases(search_paths)
    client = SQLiteClient()
    for db in dbs:
        print("SEARCHING".center(75, "-"))
        print(f"Path: {db.name}")
        client.connect_db(db)
        client.optimize()
        print("RESULTS".center(75, "-"))
        # pl(client.query_codebox_nodes())
        boxes = client.query_codebox_nodes_by_txt("%sudo -l%")
        pl(boxes)
        print()
        while True:
            if idx := input("Inspect> ").strip():
                box = boxes[int(idx)]
                print()
                print("NAME>", box.node_name)
                print("." * 75)
                print(box.txt)
                print("." * 75)
                break

        # pl(client.query_codebox_nodes_by_node("%Penetration%"))


if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"\nTook: {time.time() - start_time}s")
