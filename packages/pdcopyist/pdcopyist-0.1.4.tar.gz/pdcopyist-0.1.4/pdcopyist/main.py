
from .src.controllers import (
    cusFuns_controller, query_controller, table_controller,
    command_controller, groupby_controller, loaddata_controller)
from flask import Flask
import flask
from flask import request
import traceback
import sys


from .src.cusFuns.core.FunsPool import auto_register


import webbrowser
import os

import pathlib
base_path = pathlib.Path(__file__).parent
auto_register(base_path, 'src/cusFuns')


app = Flask(__name__,
            template_folder='./web/templates',
            static_folder='./web/static')


app.register_blueprint(cusFuns_controller.app, url_prefix='/api/cus_fun')
app.register_blueprint(query_controller.app, url_prefix='/api/query')
app.register_blueprint(table_controller.app, url_prefix='/api/table')

app.register_blueprint(command_controller.app, url_prefix='/api/cmd')
app.register_blueprint(groupby_controller.app, url_prefix='/api/groupby')
app.register_blueprint(loaddata_controller.app, url_prefix='/api/data_source')


@app.errorhandler(Exception)
def error_handler(ex):
    exc_type, exc_value, exc_traceback_obj = sys.exc_info()
    return {
        'type':
        'error',
        'code':
        traceback.format_exception(exc_type,
                                   exc_value,
                                   exc_traceback_obj,
                                   limit=2),
        'message':
        repr(ex)
    }


@app.route('/')
def index():
    return flask.render_template('index.html')


def run():

    port = 5551

    # The reloader has not yet run - open the browser
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        webbrowser.open_new(f'http://localhost:{port}/')

    # Otherwise, continue as normal
    app.run(host="localhost", port=port)


def find_arg(args, flag, return_value=True):
    try:
        idx = args.index(flag)

        if return_value:
            return True, args[idx+1]
        return idx >= 0, None
    except ValueError:
        pass

    return False, None


def copy_bat():
    import pathlib
    import shutil
    src_path = pathlib.Path(__file__).parent / 'startup_win.bat'
    shutil.copyfile(src_path, 'startup_win.bat')


def main():
    args = sys.argv

    # has, dir = find_arg(args, '-dir')
    # if has:
    #     os.chdir(dir)

    has, _ = find_arg(args, '-c', return_value=False)
    if has:
        copy_bat()
        return

    run()


if __name__ == '__main__':
    main()
