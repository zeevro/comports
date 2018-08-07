import os
import re


DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'usb.ids')
PAT = re.compile(r'^(?:(?P<vendor_id>[\da-f]{4})|\t(?P<product_id>[\da-f]{4}))  (?P<name>.+)$')
_cache = None


def _norm(value, do=True):
    if (not do) or isinstance(value, int):
        return value
    return int(value, 16)


def parse_ids_file(filename=DEFAULT_PATH, normalize=True):
    ret = {}
    vendor_id = None
    with open(filename) as in_f:
        for line in in_f:
            match = re.match(PAT, line)
            if not match:
                continue
            d = match.groupdict()
            if d['vendor_id']:
                vendor_id = _norm(d['vendor_id'], normalize)
                ret[vendor_id] = (d['name'], {})
                continue
            ret[vendor_id][1][_norm(d['product_id'], normalize)] = d['name']
    return ret


def get(vendor_id, product_id=None):
    global _cache
    if not _cache:
        _cache = parse_ids_file()
    vendor = _cache.get(_norm(vendor_id), (None, {}))
    if not product_id:
        return vendor[0]
    return (vendor[0], vendor[1].get(_norm(product_id)))


def main():
    import json
    print(json.dumps(parse_ids_file(normalize=False),
                     separators=(',', ': '),
                     indent=4,
                     sort_keys=True))


if __name__ == '__main__':
    main()
