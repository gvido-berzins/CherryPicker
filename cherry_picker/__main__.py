from cherry_picker import cli, server
from cherry_picker.client import client


def main():
    args = cli.parse_args()
    match args.mode:
        case "server":
            print("Starting server".center(50, "-"))
            server.run()
        case "client":
            print("Starting client".center(50, "-"))
            client.single_run(args)
        case _:
            print("Unrecognized mode")


if __name__ == "__main__":
    main()
