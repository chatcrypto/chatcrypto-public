# Import things that are needed generically
from asgiref.sync import async_to_sync
import chatcryptor
import sys
from chatcryptor.config import MainConfig, logging

import tracemalloc

tracemalloc.start()

sys.path.append('../src')
# sys.path.insert(0, '../src/chatcryptor')


def test_pick_executor(q):
    from chatcryptor.bot.router.base import RouterPipeLine
    router = RouterPipeLine().setup().set_input(
        input=q).begin().start_extract_tagging().pick_executor()
    print(router._list_picked_executors)


def test_router(q):
    from chatcryptor.bot.router.base import RouterPipeLine
    router = RouterPipeLine().setup(
        enable_memory=True, session_id="aaaasdfasdfasdfasdfasdfa")
    for k in q:
        # print("RESULT", router.run(input=k))
        # print("\n")
        a = router.run(input=k)
        print(a[0].dict())
        # print(router._default_executor.executor.memory.buffer)

    # print(router.run(
    #     input=q))


def test_extraction(q):
    from chatcryptor.bot.extraction.base import EntityExecutor
    a = EntityExecutor().setup().run(input=q)
    print(a.clean())
    pass


def test_default_executor(q):
    from chatcryptor.bot.base.base_executor import DefaultExcecutor
    from chatcryptor.bot.memory.base import create_memory_instance
    memory = create_memory_instance(session_id='aa1231231231231231321231')
    from chatcryptor.bot.prompts.main import HUNMAN_PREFIX
    t = HUNMAN_PREFIX.replace('{input}', q[0] if type(q) is list else q)
    a = DefaultExcecutor().setup(memory=memory)
    # .run(input=t)
    print(a)


def test_run_with_groups(q):
    from chatcryptor.bot.agents.solana_toolkits.base import SolanaExecutor
    from chatcryptor.bot.memory.base import create_memory_instance, create_readonly_memory
    ins = SolanaExecutor().setup(memory=create_readonly_memory(create_memory_instance(
        session_id='aa1231231231231231321231')))
    for k in q:
        print(ins.run(input=q, groups=['token', 'address']))


@async_to_sync
async def test_plugin(domain):
    from plugins import load_plugin, execute_plugin
    plugin = await load_plugin(domain)
    a = execute_plugin(plugin=plugin)
    async for item in a:
        print(item)

# test aptos


def test_tool_aptos(q):
    from chatcryptor.bot.tools.aptos.aptos_onchain_tool import get_type_of_address, search_nft_collection
    print(search_nft_collection(direct=True, keyword='APT'))


def test_chat_aptos(q):
    from chatcryptor.bot.router.base import RouterPipeLine
    router = RouterPipeLine().setup(
        enable_memory=True, session_id="aaaasdfasdfasdfasdfasdfa")
    for k in q:
        # print("RESULT", router.run(input=k))
        # print("\n")
        a = router.run(input=k)
        print(a[0].dict())


if __name__ == "__main__":
    q = ["show me detail of coin on Aptos", 'APT']
    # q = [
    #     # "what is the love?",
    #     # "my address is 3HSYXeGc3LjEPCuzoNDjQN37F1ebsSiR4CqXVqQCdekaa"
    #     # 'show me balance of account on Solana please'
    # ]
    # q= "hi"
    # a = test_router(q)
    test_chat_aptos(q)

    # test_default_executor(q)
