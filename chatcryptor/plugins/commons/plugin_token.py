
from chatcryptor.plugins.decorator import set_plugin, aset_plugin
from chatcryptor.utils.coingecko import get_token_price
from chatcryptor.enums.tags import TAGGING
from chatcryptor.utils.response import DataResponse, REPONSE_CHART_TYPE, BarOrLineChartReponse


@aset_plugin(name="Token Price", description="", tags=[TAGGING.TOKEN.value, TAGGING.PRICE.value])
async def coingecko_token_price(*args, **kwargs):
    plugin_params = kwargs.get('plugin_params')
    if not plugin_params.domain_configuratioin or not plugin_params.domain_configuratioin.coingecko_id:
        return None
    coingecko_id = plugin_params.domain_configuratioin.coingecko_id
    list_price_7d = get_token_price(
        coingecko_id)
    if not list_price_7d:
        return None

    return DataResponse(
        title=f'Price of token {plugin_params.domain_configuratioin.token_symbol}',
        description='',
        chart_type=REPONSE_CHART_TYPE.LINE.value,
        data=[BarOrLineChartReponse(
            row_data=[{'date': k[0], 'price': k[1]} for k in list_price_7d],
            x_field='date',
            y_field='price',
            x_label="Date",
            y_label="Price ($)",
            label='Token Price'
        )]
    )
