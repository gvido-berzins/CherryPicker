from dotenv import load_dotenv

from cherry_picker.server import create_app


def main():
    app = create_app()
    app.run()


if __name__ == "__main__":
    load_dotenv()
    main()
