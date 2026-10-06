"""A supported strict consumer and a proposed additive response change."""
import json


def provider(*, proposed=False):
    result = {'id': 'item-1', 'state': 'ready'}
    if proposed:
        result['label'] = 'Item one'
    return json.dumps(result)


def consumer(payload):
    value = json.loads(payload)
    if set(value) != {'id', 'state'}:
        raise ValueError('unsupported response fields')
    if value['state'] not in {'ready', 'pending'}:
        raise ValueError('unsupported state')
    return value['id'], value['state']
