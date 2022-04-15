from cherry_picker import utils
from cherry_picker.config import CherryConfig, cherry_config
from cherry_picker.database import SQLiteClient
from cherry_picker.models import ClientArgs, Codebox


@cherry_config()
def single_run(cfg: CherryConfig, args: ClientArgs) -> None:
    print("Single run client".center(75, "-"))
    print(cfg)
    dbs = utils.find_databases(cfg.database.paths, cfg.database.patterns)
    client = SQLiteClient()

    match args.target:
        case "code":
            query_func = client.query_codebox_nodes_by_txt
        case "node":
            query_func = client.query_codebox_nodes_by_node
        case _:
            query_func = None

    for db in dbs:
        print("SEARCHING".center(75, "-"))
        print(f"Path: {db.name}")
        client.connect_db(db)
        # client.optimize()
        print("RESULTS".center(75, "-"))
        boxes = query_func(args.pattern)

        while True and boxes:
            utils.pl(boxes)
            print()
            try:
                inspect_boxes(boxes)
            except KeyboardInterrupt:
                print("\n\nBreaking out...")
            except IndexError:
                print("\n\nOut of range...")
                continue
            break


def inspect_boxes(boxes: list[Codebox]):
    if idx := input("Inspect> ").strip():
        box = boxes[int(idx)]
        print()
        print("NAME>", box.node_name)
        print("." * 75)
        print(box.txt)
        print("." * 75)
