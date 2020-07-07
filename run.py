import os
from superdad.web import app


def main():
    app.run(
        host=os.environ["FLASK_RUN_HOST"],
        port=os.environ["FLASK_RUN_PORT"],
        debug=os.environ["FLASK_DEBUG"],
        use_reloader=False
    )


if __name__ == '__main__':
    main()
