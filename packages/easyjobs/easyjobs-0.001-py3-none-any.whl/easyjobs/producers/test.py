import asyncio
from easyrpc.proxy import EasyRpcProxy

async def setup():
    manager_proxy = await EasyRpcProxy.create(
        '0.0.0.0',
        '8220',
        '/ws/jobs',
        server_secret='abcd1234',
        namespace='DEFAULT',
        debug=True
    )
    await asyncio.sleep(2)
    print(manager_proxy.proxy_funcs)
    funcs = await manager_proxy.get_all_registered_functions()
    print(funcs)

    result = await manager_proxy['worker_a'](1, 2, 3)
    print('result is ', result)


asyncio.run(setup())