def join(ids, catalog):
    return [(key, next((row['label'] for row in catalog if row['id'] == key), None))
            for key in ids]
