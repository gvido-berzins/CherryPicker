from argparse import ArgumentParser
from re import sub
import sys


def parse_args():
    parser = ArgumentParser()
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit("\nNot enough args!")

    subparsers = parser.add_subparsers(dest="mode")
    parse_client_args(subparsers)
    parse_server_args(subparsers)
    return parser.parse_args()


def parse_client_args(subparsers):
    client = subparsers.add_parser("client")


def parse_server_args(subparsers):
    server = subparsers.add_parser("server")
