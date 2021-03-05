import aiohttp


async def get(url, headers=None, params=None, cookies=None, timeout=10):
    # async request get
    client_timeout = aiohttp.ClientTimeout(total=timeout * 3, connect=timeout)
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        async with session.get(url, headers=headers, params=params, cookies=cookies, verify_ssl=False,
                               timeout=client_timeout) as response:
            return await response.read()
