
import json
import flask
from flask import request, Blueprint
import pandas as pd
from ..core.Proxy import ProxyManager
from . import common

app = Blueprint('loaddata', __name__)


# @app.route('/get_file_args/ext=<ext>', methods=['get'])
# def get_file_args(ext: str):
#     print(ext)
#     print(request.values.get('ext'))
#     return 'done'


@app.route('/file', methods=['post'])
def upload_file():

    file = flask.request.files.get('file')

    ext = flask.request.form['ext']
    filename = flask.request.form['file_name']
    args = json.loads(flask.request.form['args'])

    # todo:根据不同情况做处理
    px = ProxyManager.get()
    px.read_data(file, filename, ext, args)
    return common.df2json(px.get_df_data())
