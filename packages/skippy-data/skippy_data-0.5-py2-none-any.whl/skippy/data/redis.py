import json
import logging
import os
from typing import List

import redis


def client():
    redis_host = os.environ.get('redis_host', None)
    logging.info('Redis host (%s)' % redis_host)
    rds = redis.Redis(decode_responses=True, host=redis_host)
    return rds


def get_dl_bandwidth(from_to: str, tar_to: str) -> float:
    bandwidth_json = client().hget(name='bandwidth_graph', key='bandwidth_graph')
    bandwidth = json.loads(bandwidth_json)
    return bandwidth[from_to][tar_to]


def get_storage_nodes(urn: str) -> List[str]:
    nodes_item_json = client().hget(name='nodes_item', key='nodes_item')
    nodes_item = json.loads(nodes_item_json)
    return nodes_item.get(urn)


def get_storage_bucket(bucket: str) -> List[str]:
    buckets_json = client().hget(name='buckets', key='buckets')
    nodes_item = json.loads(buckets_json)
    return nodes_item.get(bucket)


def get_files_size(path: str):
    items_size_json = client().hget(name='items_size', key='items_size')
    items_size = json.loads(items_size_json)
    return items_size.get(path)
