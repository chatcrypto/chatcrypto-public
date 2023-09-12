
import chatcryptor
from chatcryptor.plugins.decorator import set_plugin, aset_plugin
from chatcryptor.enums.tags import TAGGING
from chatcryptor.utils.defillama import get_defillama_tvl, get_defillama_vol
from chatcryptor.utils.response import DataResponse, REPONSE_CHART_TYPE, BarOrLineChartReponse, PieChartReponse
import math
from chatcryptor.config import MainConfig


@aset_plugin(name="Defi current tvl", description="", tags=[TAGGING.DEFI.value, TAGGING.CEX.value])
async def defillama_current_tvls(*args, **kwargs):
    plugin_params = kwargs.get('plugin_params')
    if not plugin_params.domain_configuratioin or not plugin_params.domain_configuratioin.defillama_id:
        return None
    defillma_id = plugin_params.domain_configuratioin.defillama_id
    defillama_tvl_result = get_defillama_tvl(defillma_id)
    if not defillama_tvl_result:
        return None

    data = []
    label = []
    current_chain_tvls = defillama_tvl_result.get('current_chain_tvls')
    for k in current_chain_tvls:
        label.append(f"TVL on {k} ($)")
        data.append(math.ceil(current_chain_tvls[k]))

    return DataResponse(
        title=f'Current TVL',
        description='',
        chart_type=REPONSE_CHART_TYPE.PIE.value,
        data=[PieChartReponse.render(
            data[len(data)-MainConfig.MAXIMUM_RESULT_OF_PLUGINS.value::],
            label
        )]
    )


@aset_plugin(name="Defi tvls", description="", tags=[TAGGING.DEFI.value, TAGGING.CEX.value])
async def defillama_tvls(*args, **kwargs):
    plugin_params = kwargs.get('plugin_params')
    if not plugin_params.domain_configuratioin or not plugin_params.domain_configuratioin.defillama_id:
        return None
    defillma_id = plugin_params.domain_configuratioin.defillama_id
    defillama_tvl_result = get_defillama_tvl(defillma_id)
    if not defillama_tvl_result:
        return None

    data_lines = []
    chain_tvls = defillama_tvl_result.get('chain_tvls')
    for k in chain_tvls:
        tvls = chain_tvls[k]["tvl"]
        ls = [{'date': k['date'], 'tvl': math.ceil(
            k['totalLiquidityUSD'])} for k in tvls]
        data_lines.append(BarOrLineChartReponse(
            row_data=ls[len(ls)-MainConfig.MAXIMUM_RESULT_OF_PLUGINS.value::],
            x_field='date',
            y_field='tvl',
            x_label="Date",
            y_label="TVL ($)",
            label=f'TVL on {k} ($)'
        ))

    return DataResponse(
        title=f'History TVLs of {plugin_params.domain_configuratioin.domain}',
        description='',
        chart_type=REPONSE_CHART_TYPE.LINE.value,
        data=data_lines
    )


@aset_plugin(name="Cex vols", description="", tags=[TAGGING.CEX.value])
async def defillama_vols(*args, **kwargs):
    plugin_params = kwargs.get('plugin_params')
    if not plugin_params.domain_configuratioin or not plugin_params.domain_configuratioin.defillama_id:
        return None
    defillma_id = plugin_params.domain_configuratioin.defillama_id
    defillama_vol_result = get_defillama_vol(defillma_id)
    if not defillama_vol_result:
        return None

    data_lines = []
    vol_by_chains = defillama_vol_result.get('vol_by_chains')
    chains = defillama_vol_result.get('chains')
    for chain in chains:
        datas = []
        for vol_by_chain in vol_by_chains:
            vol = vol_by_chain[1].get(chain, 0)
            datas.append({
                'date': vol_by_chain[0],
                'vol': math.ceil(vol)
            })

        data_lines.append(BarOrLineChartReponse(
            row_data=datas[len(datas) -
                       MainConfig.MAXIMUM_RESULT_OF_PLUGINS.value::],
            x_field='date',
            y_field='vol',
            label=f'VOL on {chain} ($)',
            x_label="Date",
            y_label="VOL ($)",
        ))

    return DataResponse(
        title=f'Vols of {plugin_params.domain_configuratioin.domain}',
        description='',
        chart_type=REPONSE_CHART_TYPE.GROUPED_BAR.value,
        data=data_lines
    )
