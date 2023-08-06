
from ..helper.utils import json_converter
import flask
from flask import request, Blueprint
import pandas as pd
from ..core.Proxy import ProxyManager
from . import common

app = Blueprint('command', __name__)


@app.route('/remove', methods=['post'])
def remove_cmd():
    param = common.get_data_from_post()
    id = param['id']

    px = ProxyManager.get()
    px.remove_cmd(id)
    return common.df2json(px.get_df_data())


@app.route('/')
def get_cmds():
    cmds = ProxyManager.get().get_cmds()
    res = flask.json.dumps(cmds, default=json_converter)
    return res


@app.route('/code')
def get_py_code():
    ret = ProxyManager.get().to_code()
    return ret
