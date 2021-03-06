from flask import Blueprint, render_template, request

from cherry_picker import utils
from cherry_picker.config import CherryConfig, cherry_config
from cherry_picker.database import SQLiteClient
from cherry_picker.models import Codebox
from cherry_picker.server.styler import pigmentize

home = Blueprint("home", __name__)


@home.post("/query")
@cherry_config()
def query(cfg: CherryConfig):
    search_string = request.json.get("search", "")
    results: list[Codebox] = []

    if not search_string:
        return render_template("results.html", results=results)

    dbs = utils.find_databases(cfg.database.paths, cfg.database.patterns)
    client = SQLiteClient()

    for db in dbs:
        client.connect_db(db)
        boxes = client.query_codebox_nodes_by_txt(search_string)
        for box in boxes:
            box.txt = pigmentize(box.txt)
        results.extend(boxes)

    return render_template("results.html", results=results)


@home.route("/")
def index():
    return render_template("index.html", title="CherryPicker")
