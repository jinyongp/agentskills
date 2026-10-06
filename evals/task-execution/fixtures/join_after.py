def join(ids, catalog):
    first = {}
    for row in catalog:
        first.setdefault(row['id'], row['label'])
    return [(key, first.get(key)) for key in ids]
