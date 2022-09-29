import aiohttp

async def get_code(ip: str = "127.0.0.1") -> str:
    """Obtain the ISO 3166-1 alpha-2 country code based on an IP address
    
    Args:
        ip (str): The IP address to resolve
    
    Returns:
        str -- The two-character country code associated with the IP address"""
    async with aiohttp.ClientSession() as cs:
        if ip == "127.0.0.1":
            async with cs.get("https://api.ipify.org") as pub_ip:
                ip = await pub_ip.text()
        async with cs.get(f"https://ipinfo.io/{ip.strip()}/country") as rq:
            code = await rq.text()
    return code.strip()