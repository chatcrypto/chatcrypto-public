
from chatcryptor.plugins.decorator import set_plugin, aset_plugin
from chatcryptor.utils.response import DataResponse, REPONSE_CHART_TYPE, BarOrLineChartReponse, TableResponse


@aset_plugin(name="test", description="", tags=[], priority=99)
async def test(*args, **kwargs):
    
    data = TableResponse.render(
        header={
            'name': 'Test'
        },
        data=[{
            'name': 'tester',
            
        } ]

    return DataResponse(
        title='Test data for raydium',
        description='',
        chart_type=REPONSE_CHART_TYPE.TABLE.value,
        data=data
    )
