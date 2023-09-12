"""
This module used for loading plugins that available for a domain
"""
import chatcryptor.plugins.schema as schema
import logging
from inspect import getmembers, isfunction
import importlib.util
import importlib
import asyncio
from chatcryptor.config import MainConfig
import chatcryptor.utils.response as response_module
from typing import List
import traceback
from chatcryptor.enums.tags import TAGGING

logger = logging.getLogger(__name__)

mapping_tagging_common_plugin = {
    TAGGING.DEFI.value: "plugin_defi",
    TAGGING.TOKEN.value: "plugin_token",
    TAGGING.NFT.value: "plugin_nft",
    TAGGING.CEX.value: "plugin_cex"
}


async def load_plugin(domain: str, plugin_path: str = 'plugins'):
    try:
        spl = domain.split('.')
        plugin_name = f'{spl[-2]}_{spl[-1]}'
        path = f'{plugin_name}'
        logger.info(f"Load plugins: [{f'plugins.{plugin_name}'}]")
        spec = importlib.util.spec_from_file_location(
            path, f"{plugin_path}/{plugin_name}.py")
        mol = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mol)
        return mol
    except BaseException as e:
        logger.info(f"There is no plugin for domain: {domain}")
        logger.debug(e)


def load_common_plugin(list_tags: List[str] = []):
    for tag in list_tags:
        try:
            file = mapping_tagging_common_plugin.get(tag)
            if not file:
                logger.debug(f'common_plugin for tag: [{tag}] does not exist')
                continue
            path = f"chatcryptor/plugins/commons/{file}.py"
            logger.info(
                f"Load common plugin: [{path}] success")
            spec = importlib.util.spec_from_file_location(file, path)
            mol = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mol)
            yield mol
        except BaseException as e:
            logger.debug(e)


async def execute_plugin(plugin, filter_plugin_id: str = None, plugin_params: schema.PluginParams = None, database_loaders: schema.DatabaseLoader = None, process_item=None, **kwargs):

    plugin = plugin if type(plugin) is list else [plugin]

    list_function = []
    for k in plugin:
        for i in getmembers(k, isfunction):
            if hasattr(i[1], '_plugin_metadata'):
                if filter_plugin_id and filter_plugin_id == f"{k.__name__}::{i[0]}":
                    list_function += [(i, k.__name__)]
                    break
                elif not filter_plugin_id:
                    list_function += [(i, k.__name__)]

    for item_meta in list_function:
        item = item_meta[0]
        plugin_metadata = item[1]._plugin_metadata
        parent_plugin_name = item_meta[1]
        plugin_name = f"[{parent_plugin_name}::{plugin_metadata['name']}]"
        func_name = item[0]
        func = item[1]
        plugin_id = f"{parent_plugin_name}::{func_name}"

        is_async = asyncio.iscoroutinefunction(func)

        logger.debug(
            f"Execute function: {'async' if is_async else ''} [{func_name}] on plugin: {plugin_name}")
        try:
            if is_async:
                data = await func(plugin_params=plugin_params, database_loaders=database_loaders, **kwargs)
            else:
                data = func(plugin_params=plugin_params,
                            database_loaders=database_loaders, **kwargs)
            if data is None:
                data = response_module.DataResponse(
                    title=f"",
                    data="No Data",
                    chart_type=response_module.REPONSE_CHART_TYPE.TEXT.value,
                    success=False
                )
        except BaseException as e:
            logger.debug(
                f"Error when execute function: {'async' if is_async else ''} [{func_name}] on plugin: {plugin_name}. Message: {e}")
            logger.debug(traceback.print_exc())
            data = response_module.DataResponse(
                title=f"Error when execute plugin: {plugin_name}. Error: {e}" if MainConfig.LOG_LEVEL.value < 20 else "Error when execute plugin",
                data="",
                chart_type=response_module.REPONSE_CHART_TYPE.TEXT.value,
                success=False

            )
        if hasattr(data, 'plugin_id'):
            data.plugin_id = plugin_id
        # logging plugin and function name if Debug Mode is enabled
        if MainConfig.LOG_LEVEL.value < 20 and isinstance(data, response_module.DataResponse):
            data.debug_plugin_name = plugin_name
            data.debug_plugin_metadata = plugin_metadata

        yield data if not callable(process_item) else process_item(data)


async def get_plugin_metadata(domain: str, plugin_params: schema.PluginParams = None):
    list_plugin = [
        await load_plugin(domain=domain),
    ]
    if plugin_params and plugin_params.domain_configuratioin and plugin_params.domain_configuratioin.tags:
        list_plugin += list(load_common_plugin(
            list_tags=plugin_params.domain_configuratioin.tags or []))
    list_function = []
    for k in list_plugin:
        for i in getmembers(k, isfunction):
            if hasattr(i[1], '_plugin_metadata'):
                metadata = i[1]._plugin_metadata
                metadata['plugin_id'] = f"{k.__name__}::{i[0]}"
                list_function.append(metadata)
    list_function = sorted(
        list_function, key=lambda x: x['priority'], reverse=True)
    return list_function
