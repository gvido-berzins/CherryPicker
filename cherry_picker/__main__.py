from cherry_picker import cli
from cherry_picker.client import client


def main():
    args = cli.parse_args()
    match args.mode:
        case "server":
            print("Starting server")
        case "client":
            print("Starting client")
            client.single_run(args)
        case _:
            print("Unrecognized mode")


if __name__ == "__main__":
    main()
