import sys
from argparse import ArgumentParser, _SubParsersAction


def parse_args():
    parser = ArgumentParser()
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit("\nNot enough args!")

    subparsers = parser.add_subparsers(dest="mode")
    parse_client_args(subparsers)
    parse_server_args(subparsers)
    return parser.parse_args()


def parse_client_args(subparsers: _SubParsersAction):
    client = subparsers.add_parser("client")
    client.add_argument(
        "-i", "--interactive", action="store_true", help="Enter a command loop"
    )
    client.add_argument(
        "target", default="code", choices=["code", "node"], help="What to search by"
    )
    client.add_argument("pattern", help="SQL pattern to search for the target")


def parse_server_args(subparsers: _SubParsersAction):
    server = subparsers.add_parser("server")
    server.add_argument("--host", type=str, default="127.0.0.1", help="Server host IP")
    server.add_argument("--port", type=int, default=9001, help="Server port")
