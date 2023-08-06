
import flask
from flask import request, Blueprint
import pandas as pd
from ..core.Proxy import ProxyManager
from . import common

app = Blueprint('table', __name__)


@app.route('/filters', methods=['post'])
def table_filters():
    param = common.get_data_from_post()

    px = ProxyManager.get()
    px.query(param['query'])
    return common.df2json(px.get_df_data())


@app.route('/handle', methods=['post'])
def table_handle():

    # todo:重构
    def _to_df_cols(df: pd.DataFrame, col: str):
        # 如果是多层索引，使用eval转成元组
        if isinstance(df.columns, pd.MultiIndex):
            return eval(col)

        return col

    param = common.get_data_from_post()

    filters = param['filters']
    sort = param['sort']

    filters = ((f['field'], f['values']) for f in filters)

    px = ProxyManager.get()
    px.filter(filters)

    df_ret = px.get_df_data()

    if sort:
        order = True if sort['order'] == 'asc' else False
        df_ret = df_ret.sort_values(_to_df_cols(
            df_ret, sort['field']), ascending=order)

    return common.df2json(df_ret)
