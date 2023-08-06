

from flask import Flask


import webbrowser
import os

from .core.proxy import ProxyManager

app = Flask(__name__)


@app.route('/')
def index():
    pm = ProxyManager()
    return 'done'


def run():

    port = 5551

    # The reloader has not yet run - open the browser
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        webbrowser.open_new(f'http://localhost:{port}/')

    # Otherwise, continue as normal
    app.run(host="localhost", port=port)


if __name__ == '__main__':
    run()
