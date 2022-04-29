# CherryPicker

A tool for searching CherryTree sqlite database for code in codeboxes.

Supported CherryTree databases:

- SQLite unencrypted

## Usage

```bash
python -m venv venv
pip install -r requirements.txt
python -m cherry_picker -h
```

## Client (CLI)

TDB.

### Single-run

Run one-off commands and get results

```bash
python -m cherry_picker client node "%snippet%"
python -m cherry_picker client code "%bash -i%"
```

### Iteractive (Not Implemented)

Interact with the client in a command-loop.

## Server (Flask)

For now the flask site only queries the codebox contents.

Run the flask server with the following commands

```bash
# With flask
export FLASK_APP=cherry_picker/server
flask run

# Or an easier way with this
python run.py

# Or run it from the main entrypoint
python -m cherry_picker server
```

This is how the front page looks, the search results appear on keyup events

![Search results](assets/search-results.png)

### Setting up the server as a service

I created this to run as a service on my linux system, I only have setup for systemd,
the unit file is [here](cherry_server.service)

```bash
sudo mv cherry_server.service /etc/systemd/system/
sudo systemctl start cherry_server
sudo systemctl status cherry_server
```

After executing the commands, the service should be visible as running with
the `systemctl status` command
