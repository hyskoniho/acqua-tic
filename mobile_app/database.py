from typing import Tuple
from pymongo.collection import Collection
from pymongo.mongo_client import MongoClient

import certifi, os
import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']
collection=None

def _build_connection(uri: str = os.getenv("uri", "")) -> Collection:
    global collection
    try:
        if not collection: raise
        else: collection.count_documents({})
    except:
        collection = MongoClient(uri, connect=True, connectTimeoutMS=15000, serverSelectionTimeoutMS=15000, maxConnecting=100, ssl=True, tlsInsecure=True, tlsCAFile=certifi.where())['acqua-tic']['control']
    return collection

def get_collection() -> dict:
    return _build_connection().find_one(filter={'id': 0}, max_time_ms=10000)

def set_value(field: str, value: int | float | bool) -> None:
    _build_connection().update_one({'id': 0}, {'$set': {field: value}})
    
def get_image() -> str:
    return get_collection()['image']

def set_image(image: str) -> None:
    _build_connection().update_one({'id': 0}, {'$set': {'image': image}})

def get_stats() -> Tuple[float, float]:
    data: dict = _build_connection().find_one(filter={'id': 0}, max_time_ms=10000)
    return data['temp'], data['lux']

def set_stats(temp: float = None, lux: float = None) -> None:
    command: dict = {}
    if temp != None: command['temp'] = temp
    if lux != None: command['lux'] = lux
    _build_connection().update_one({'id': 0}, {'$set': command})
    
def get_commands() -> Tuple[bool, bool]:
    data: dict = get_collection()
    return data['heat'], data['lamp']

def set_commands(heat: bool = None, lux: bool = None) -> None:
    command: dict = {}
    if heat != None: command['heat'] = heat
    if lux != None: command['lamp'] = lux
    _build_connection().update_one({'id': 0}, {'$set': command})
    
def set_command(command: str) -> None:
    actual: tuple = get_commands()
    if command == 'heat': set_commands(not actual[0], None)
    elif command == 'lamp': set_commands(None, not actual[1])
    
if __name__ == '__main__':
    print(get_stats())