from cherry_picker import cli


def main():
    args = cli.parse_args()
    match args.mode:
        case "server":
            print("Starting server")
        case "client":
            print("Starting client")
        case _:
            print("Unrecognized mode")


if __name__ == "__main__":
    main()
