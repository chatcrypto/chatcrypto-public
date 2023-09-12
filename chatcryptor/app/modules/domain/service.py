from chatcryptor.plugins import execute_plugin, load_plugin, load_common_plugin, get_plugin_metadata
from chatcryptor.db.mongodb import MongodbClient
from chatcryptor.plugins.schema import DatabaseLoader, PluginParams
from chatcryptor.models.db_models import DomainConfiguration
import chatcryptor.utils.response as response_module
import chatcryptor.utils as util_module
from pydantic import BaseModel

database_loader = DatabaseLoader(
    main_mongodb=MongodbClient()
)


async def process_by_plugins(domain, plugin_id: str = None, response_json=False):
    """
    Find any information about domain by plugins
    Return data as genarator
    """
    plugin = await load_plugin(domain=domain)
    domain_conf = DomainConfiguration.find_by_domain(domain=domain)
    common_plugin = list(load_common_plugin(list_tags=domain_conf.tags or []))
    default_plugin_params = PluginParams(
        response_module=response_module,
        utils_module=util_module,
        domain_configuratioin=domain_conf
    )

    def process_item(data):
        rs = data
        if isinstance(data, response_module.DataResponse):
            rs = data.dict()
        else:
            rs = response_module.DataResponse(
                data=data,
                chart_type=response_module.REPONSE_CHART_TYPE.TEXT.value,
                description="",
                title=""
            ).dict()
        return rs

    return execute_plugin(
        plugin=common_plugin + [plugin], filter_plugin_id=plugin_id, plugin_params=default_plugin_params, database_loaders=database_loader, response_json=response_json, process_item=process_item)


async def get_plugins_of_domain(domain: str):
    domain_conf = DomainConfiguration.find_by_domain(domain=domain)
    default_plugin_params = PluginParams(
        response_module=response_module,
        utils_module=util_module,
        domain_configuratioin=domain_conf
    )
    return await get_plugin_metadata(domain=domain, plugin_params=default_plugin_params)
