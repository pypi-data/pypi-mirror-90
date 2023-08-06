
import flask
from flask import request, Blueprint
from ..core.Proxy import ProxyManager
from ..helper.utils import json_converter
from . import common

app = Blueprint('cus_fun', __name__)


@app.route('/', methods=['post'])
def cus_fun():
    param = common.get_data_from_post()
    data = param['data']

    px = ProxyManager.get()

    px.run_cus_fun(data)

    return common.df2json(px.get_df_data())


@app.route('/desc')
def get_cus_funcs_desc():
    # auto_register(base_path , 'src/cusFuns')
    ret = ProxyManager.get().get_cus_funcs_desc()
    ret = flask.json.dumps(ret, default=json_converter)
    return ret


@app.route('/model', methods=['get'])
def get_cus_funcs_ui_model():

    uid = str(request.args.get('uid'))

    ret = ProxyManager.get().get_ui_model(uid)
    ret = flask.json.dumps(ret, default=json_converter)
    return ret


@app.route('/input', methods=['post'])
def get_cus_funcs_input():
    param = common.get_data_from_post()
    data = param['data']

    px = ProxyManager.get()

    px.input_cus_funcs(data)
    return common.df2json(px.get_df_data())
