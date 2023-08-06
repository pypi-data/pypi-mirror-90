
from flask import Blueprint
from ..core.Proxy import ProxyManager
from . import common

app = Blueprint('groupby', __name__)


@app.route('/', methods=['post'])
def groupby():
    param = common.get_data_from_post()
    keys = param['_keys']
    aggs = param['_aggs']

    aggs = {d['filed']: d['methods'] for d in aggs}

    px = ProxyManager.get()
    px.groupby(keys, aggs)

    return common.df2json(px.get_df_data())
