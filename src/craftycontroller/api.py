# src/audio/craftycontroller/api.py
# The api functions


# Imports
from os import getenv
from typing import AsyncIterator

import aiohttp


# Definitions
class ApiException(Exception): ...


async def get_server_ids() -> list[int]:
    """Get all of the server ids"""
    
    # Get all ids
    async with aiohttp.ClientSession(headers={"Authorization": f"Bearer {getenv('CRAFTYCONTROLLER_API_TOKEN')}"}) as session:
        async with session.get(f"https://{getenv('CRAFTYCONTROLLER_URL')}/api/v2/roles/{getenv('CRAFTYCONTROLLER_ROLE_ID')}/servers?ids=true") as response:
            if response.status == 200:
                json = await response.json()
                return json["data"]
            else:
                raise ApiException(f"Error getting server ids: {response.status}")


async def get_server_names() -> list[str]:
    """Get all of the server names"""
    
    # Out list
    out: list[str] = []
    
    # Get the name for every id
    for id_ in await get_server_ids():
        async with aiohttp.ClientSession(headers={"Authorization": f"Bearer {getenv('CRAFTYCONTROLLER_API_TOKEN')}"}) as session:
            async with session.get(f"https://{getenv('CRAFTYCONTROLLER_URL')}/api/v2/servers/{id_}/public") as response:
                if response.status == 200:
                    json = await response.json()
                    out.append(json["data"]["server_name"])
                else:
                    raise ApiException(f"Error getting server names: {response.status}")
    
    # Return the list
    return out


async def get_name_map() -> dict[str, int]:
    """Get a map of names to ids"""
    
    return dict(zip(await get_server_names(), await get_server_ids()))


async def start_server(id_: int) -> None:
    """Start a server"""
    
    # Start the server
    async with aiohttp.ClientSession(headers={"Authorization": f"Bearer {getenv('CRAFTYCONTROLLER_API_TOKEN')}"}) as session:
        async with session.post(f"https://{getenv('CRAFTYCONTROLLER_URL')}/api/v2/servers/{id_}/action/start_server") as response:
            if response.status == 200:
                return
            else:
                raise ApiException(f"Error starting server: {response.status}")
