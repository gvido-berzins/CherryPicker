from dataclasses import dataclass
from typing import Any
from pathlib import Path
import sqlite3

from cherry_picker.models import Codebox

QueryResults = list[tuple[Any]]


@dataclass
class SQLiteClient:
    database_url: str = ""
    connection: sqlite3.Connection = None
    cursor: sqlite3.Cursor = None

    def __post_init__(self):
        if self.database_url:
            self.connect()

    def connect_db(self, db: Path | str):
        self.database_url = str(db)
        self.connect()

    def connect(self):
        self.connection = sqlite3.connect(self.database_url)
        self.cursor = self.connection.cursor()

    def optimize(self):
        self.cursor.execute("PRAGMA synchronous = EXTRA")
        self.cursor.execute("PRAGMA journal_mode = WAL")

    def query(self, query: str) -> QueryResults:
        return [row for row in self.cursor.execute(query)]

    def show_tables(self) -> QueryResults:
        return self.query("SELECT name FROM sqlite_master WHERE type='table';")

    def query_codeboxes(self) -> QueryResults:
        return self.query("SELECT node_id,txt FROM codebox;")

    def query_node(self, node_id: str) -> QueryResults:
        return self.query(f"SELECT name FROM node WHERE node_id='{node_id}';")

    def query_codebox_nodes(self, suffix: str = "") -> QueryResults:
        codeboxes = self.query(
            "SELECT node.node_id, node.name, codebox.txt "
            "FROM codebox INNER JOIN node "
            "ON codebox.node_id = node.node_id " + suffix
        )
        return [Codebox(idx, res[2], res[1]) for idx, res in enumerate(codeboxes)]

    def query_codebox_nodes_by_txt(self, pattern: str) -> QueryResults:
        return self.query_codebox_nodes_by("codebox.txt", pattern)

    def query_codebox_nodes_by_node(self, pattern: str) -> QueryResults:
        return self.query_codebox_nodes_by("node.name", pattern)

    def query_codebox_nodes_by(self, field: str, pattern: str) -> QueryResults:
        suffix = f"WHERE {field} LIKE '{pattern}'"
        return self.query_codebox_nodes(suffix)
