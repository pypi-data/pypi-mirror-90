
from flask import Blueprint
from ..core.Proxy import ProxyManager
from . import common

app = Blueprint('query', __name__)


@app.route('/', methods=['post'])
def query():
    param = common.get_data_from_post()
    px = ProxyManager.get()
    px.query(param['query'])
    return common.df2json(px.get_df_data())
